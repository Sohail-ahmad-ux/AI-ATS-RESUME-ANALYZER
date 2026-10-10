# utils/pdf_report.py

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

import os
import re


# ============================================================
# COLORS
# ============================================================

NAVY = colors.HexColor("#0F172A")
BLUE = colors.HexColor("#2563EB")
LIGHT_BLUE = colors.HexColor("#EFF6FF")

GREEN = colors.HexColor("#16A34A")
LIGHT_GREEN = colors.HexColor("#F0FDF4")

RED = colors.HexColor("#DC2626")
LIGHT_RED = colors.HexColor("#FEF2F2")

ORANGE = colors.HexColor("#EA580C")
LIGHT_ORANGE = colors.HexColor("#FFF7ED")

GRAY_50 = colors.HexColor("#F8FAFC")
GRAY_100 = colors.HexColor("#F1F5F9")
GRAY_200 = colors.HexColor("#E2E8F0")
GRAY_400 = colors.HexColor("#94A3B8")
GRAY_500 = colors.HexColor("#64748B")
GRAY_700 = colors.HexColor("#334155")
GRAY_900 = colors.HexColor("#0F172A")

WHITE = colors.white


# ============================================================
# FONT REGISTRATION
# ============================================================

def register_fonts():
    """
    Register a modern Unicode font if available.
    Falls back to Helvetica if no custom font exists.
    """

    font_paths = [
        "static/fonts/DejaVuSans.ttf",
        "static/fonts/Inter-Regular.ttf",
        "static/fonts/Roboto-Regular.ttf",
    ]

    bold_paths = [
        "static/fonts/DejaVuSans-Bold.ttf",
        "static/fonts/Inter-Bold.ttf",
        "static/fonts/Roboto-Bold.ttf",
    ]

    regular_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    for path in font_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(
                    TTFont("ATSRegular", path)
                )
                regular_font = "ATSRegular"
                break
            except Exception:
                pass

    for path in bold_paths:
        if os.path.exists(path):
            try:
                pdfmetrics.registerFont(
                    TTFont("ATSBold", path)
                )
                bold_font = "ATSBold"
                break
            except Exception:
                pass

    return regular_font, bold_font


# ============================================================
# SAFE TEXT
# ============================================================

def safe_text(value, default="N/A"):
    """
    Convert arbitrary values into readable text.
    """

    if value is None:
        return default

    if isinstance(value, list):
        return ", ".join(str(x) for x in value)

    if isinstance(value, dict):
        return ", ".join(
            f"{k}: {v}"
            for k, v in value.items()
        )

    text = str(value).strip()

    if not text:
        return default

    return text


def clean_html(text):
    """
    Escape text so it can safely be used inside
    ReportLab Paragraph.
    """

    if text is None:
        return ""

    text = str(text)

    return (
        text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


# ============================================================
# SCORE HELPERS
# ============================================================

def format_score(value):

    try:
        score = float(value)
        return f"{score:.1f}%"

    except Exception:
        return "0%"


def score_color(score):

    try:
        score = float(score)

    except Exception:
        score = 0

    if score >= 80:
        return GREEN

    if score >= 60:
        return ORANGE

    return RED


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_feedback(text):
    """
    Convert AI-generated Markdown-like feedback into
    separate lines that can be formatted properly.
    """

    if not text:
        return []

    text = str(text)

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Normalize bullet symbols
    text = text.replace("•", "\n• ")
    text = text.replace("●", "\n• ")
    text = text.replace("▪", "\n• ")
    text = text.replace("◦", "\n• ")

    # Convert markdown headings
    text = text.replace("###", "\n")

    # Put numbered sections on new lines
    text = re.sub(
        r"\s+(\d+\.)\s+",
        r"\n\1 ",
        text,
    )

    # Remove markdown bold
    text = text.replace("**", "")

    # Remove markdown italic
    text = text.replace("__", "")

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        lines.append(line)

    return lines


# ============================================================
# SECTION TITLE
# ============================================================

def make_section_title(title, styles):

    return Paragraph(
        clean_html(title),
        styles["SectionTitle"],
    )


# ============================================================
# SCORE CARD
# ============================================================

def score_card(score, recommendation, styles):

    color = score_color(score)

    score_text = Paragraph(
        f'<font color="{color.hexval()}">'
        f"<b>{format_score(score)}</b>"
        f"</font>",
        styles["ScoreValue"],
    )

    recommendation_text = Paragraph(
        f"<b>{clean_html(recommendation)}</b>",
        styles["Recommendation"],
    )

    data = [
        [
            Paragraph(
                "OVERALL ATS SCORE",
                styles["SmallLabel"],
            ),
            score_text,
            recommendation_text,
        ]
    ]

    table = Table(
        data,
        colWidths=[
            55 * mm,
            45 * mm,
            75 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_BLUE,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    1,
                    BLUE,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    14,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    14,
                ),
            ]
        )
    )

    return table


# ============================================================
# CANDIDATE INFORMATION
# ============================================================

def candidate_information(result, styles):

    candidate = safe_text(
        result.get("candidate_name"),
        "Unknown",
    )

    education = safe_text(
        result.get("resume_education"),
        "Not provided",
    )

    experience = safe_text(
        result.get("resume_experience"),
        "Not provided",
    )

    recommendation = safe_text(
        result.get("recommendation"),
        "Not provided",
    )

    data = [
        [
            Paragraph(
                "<b>Candidate</b>",
                styles["TableHeader"],
            ),
            Paragraph(
                clean_html(candidate),
                styles["TableCell"],
            ),
        ],
        [
            Paragraph(
                "<b>Education</b>",
                styles["TableHeader"],
            ),
            Paragraph(
                clean_html(education),
                styles["TableCell"],
            ),
        ],
        [
            Paragraph(
                "<b>Experience</b>",
                styles["TableHeader"],
            ),
            Paragraph(
                clean_html(experience),
                styles["TableCell"],
            ),
        ],
        [
            Paragraph(
                "<b>Recommendation</b>",
                styles["TableHeader"],
            ),
            Paragraph(
                clean_html(recommendation),
                styles["TableCell"],
            ),
        ],
    ]

    table = Table(
        data,
        colWidths=[
            45 * mm,
            130 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, -1),
                    GRAY_100,
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, -1),
                    WHITE,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GRAY_200,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    return table


# ============================================================
# SCORE BREAKDOWN
# ============================================================

def score_breakdown(result, styles):

    categories = [
        (
            "Skills",
            result.get("skill_score", 0),
        ),
        (
            "Experience",
            result.get("experience_score", 0),
        ),
        (
            "Education",
            result.get("education_score", 0),
        ),
        (
            "Keywords",
            result.get("keyword_score", 0),
        ),
        (
            "Resume Quality",
            result.get("resume_quality_score", 0),
        ),
    ]

    data = [
        [
            Paragraph(
                "Category",
                styles["TableHeaderWhite"],
            ),
            Paragraph(
                "Score",
                styles["TableHeaderWhite"],
            ),
        ]
    ]

    for category, score in categories:

        color = score_color(score)

        score_paragraph = Paragraph(
            f'<font color="{color.hexval()}">'
            f"<b>{format_score(score)}</b>"
            f"</font>",
            styles["TableCell"],
        )

        data.append(
            [
                Paragraph(
                    clean_html(category),
                    styles["TableCell"],
                ),
                score_paragraph,
            ]
        )

    table = Table(
        data,
        colWidths=[
            120 * mm,
            55 * mm,
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, 0),
                    NAVY,
                ),
                (
                    "TEXTCOLOR",
                    (0, 0),
                    (-1, 0),
                    WHITE,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GRAY_200,
                ),
                (
                    "BACKGROUND",
                    (0, 1),
                    (-1, -1),
                    WHITE,
                ),
                (
                    "ALIGN",
                    (1, 1),
                    (1, -1),
                    "RIGHT",
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "MIDDLE",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    9,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    return table


# ============================================================
# SKILL / LIST SECTION
# ============================================================

def skill_section(
    title,
    items,
    styles,
    background,
    text_color,
):

    if not items:

        return Paragraph(
            "None identified.",
            styles["TableCell"],
        )

    rows = []

    for item in items:

        item_text = clean_html(item)

        rows.append(
            [
                Paragraph(
                    f'<font color="{text_color.hexval()}">'
                    f"<b>• {item_text}</b>"
                    f"</font>",
                    styles["TableCell"],
                )
            ]
        )

    table = Table(
        rows,
        colWidths=[
            80 * mm
        ],
    )

    table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    background,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    background,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    10,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    6,
                ),
            ]
        )
    )

    return table


# ============================================================
# FEEDBACK SECTION
# ============================================================

def feedback_section(feedback, styles):

    elements = []

    lines = normalize_feedback(feedback)

    if not lines:

        return [
            Paragraph(
                "No AI feedback available.",
                styles["TableCell"],
            )
        ]

    for line in lines:

        # ----------------------------------------------------
        # Numbered section
        # ----------------------------------------------------

        numbered = re.match(
            r"^(\d+)\.\s*(.*)",
            line,
        )

        if numbered:

            number = numbered.group(1)
            text = numbered.group(2).strip()

            elements.append(
                Paragraph(
                    f'<font color="{BLUE.hexval()}">'
                    f"<b>{number}. "
                    f"{clean_html(text)}</b>"
                    f"</font>",
                    styles["FeedbackHeading"],
                )
            )

            continue

        # ----------------------------------------------------
        # Bullet
        # ----------------------------------------------------

        if line.startswith("•"):

            bullet_text = line[1:].strip()

            elements.append(
                Paragraph(
                    f"• {clean_html(bullet_text)}",
                    styles["CustomBullet"],
                )
            )

            continue

        # ----------------------------------------------------
        # Dash bullet
        # ----------------------------------------------------

        if line.startswith("-"):

            bullet_text = line[1:].strip()

            elements.append(
                Paragraph(
                    f"• {clean_html(bullet_text)}",
                    styles["CustomBullet"],
                )
            )

            continue

        # ----------------------------------------------------
        # Normal paragraph
        # ----------------------------------------------------

        elements.append(
            Paragraph(
                clean_html(line),
                styles["FeedbackText"],
            )
        )

    return elements


# ============================================================
# INTERVIEW QUESTIONS
# ============================================================

def interview_section(questions, styles):

    elements = []

    if not questions:

        elements.append(
            Paragraph(
                "No interview questions available.",
                styles["TableCell"],
            )
        )

        return elements

    # ========================================================
    # DICTIONARY
    # ========================================================

    if isinstance(questions, dict):

        for category, items in questions.items():

            elements.append(
                Paragraph(
                    clean_html(category),
                    styles["FeedbackHeading"],
                )
            )

            if isinstance(items, list):

                for index, item in enumerate(
                    items,
                    1,
                ):

                    if isinstance(item, dict):

                        question = item.get(
                            "question",
                            item.get(
                                "Question",
                                "",
                            ),
                        )

                        answer = item.get(
                            "ideal_answer",
                            item.get(
                                "answer",
                                item.get(
                                    "Ideal Answer",
                                    "",
                                ),
                            ),
                        )

                        if question:

                            elements.append(
                                Paragraph(
                                    f"<b>{index}. "
                                    f"{clean_html(question)}</b>",
                                    styles["Question"],
                                )
                            )

                        if answer:

                            elements.append(
                                Paragraph(
                                    f"<b>Ideal Answer:</b> "
                                    f"{clean_html(answer)}",
                                    styles["Answer"],
                                )
                            )

                    else:

                        elements.append(
                            Paragraph(
                                f"<b>{index}. "
                                f"{clean_html(item)}</b>",
                                styles["Question"],
                            )
                        )

                    elements.append(
                        Spacer(1, 5)
                    )

            elements.append(
                Spacer(1, 8)
            )

        return elements

    # ========================================================
    # LIST
    # ========================================================

    if isinstance(questions, list):

        for index, item in enumerate(
            questions,
            1,
        ):

            if isinstance(item, dict):

                question = item.get(
                    "question",
                    item.get(
                        "Question",
                        "",
                    ),
                )

                answer = item.get(
                    "ideal_answer",
                    item.get(
                        "answer",
                        item.get(
                            "Ideal Answer",
                            "",
                        ),
                    ),
                )

                if question:

                    elements.append(
                        Paragraph(
                            f"<b>{index}. "
                            f"{clean_html(question)}</b>",
                            styles["Question"],
                        )
                    )

                if answer:

                    elements.append(
                        Paragraph(
                            f"<b>Ideal Answer:</b> "
                            f"{clean_html(answer)}",
                            styles["Answer"],
                        )
                    )

            else:

                elements.append(
                    Paragraph(
                        f"<b>{index}. "
                        f"{clean_html(item)}</b>",
                        styles["Question"],
                    )
                )

            elements.append(
                Spacer(1, 5)
            )

        return elements

    # ========================================================
    # STRING
    # ========================================================

    text = str(questions)

    for line in normalize_feedback(text):

        if line.startswith("•"):

            elements.append(
                Paragraph(
                    f"• {clean_html(line[1:].strip())}",
                    styles["CustomBullet"],
                )
            )

        elif line.startswith("-"):

            elements.append(
                Paragraph(
                    f"• {clean_html(line[1:].strip())}",
                    styles["CustomBullet"],
                )
            )

        else:

            elements.append(
                Paragraph(
                    clean_html(line),
                    styles["Answer"],
                )
            )

    return elements


# ============================================================
# HEADER / FOOTER
# ============================================================

def draw_header_footer(
    canvas,
    doc,
    regular_font,
    bold_font,
):

    canvas.saveState()

    width, height = A4

    # --------------------------------------------------------
    # Header line
    # --------------------------------------------------------

    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(2)

    canvas.line(
        18 * mm,
        height - 14 * mm,
        width - 18 * mm,
        height - 14 * mm,
    )

    # --------------------------------------------------------
    # Footer line
    # --------------------------------------------------------

    canvas.setStrokeColor(GRAY_200)
    canvas.setLineWidth(0.5)

    canvas.line(
        18 * mm,
        15 * mm,
        width - 18 * mm,
        15 * mm,
    )

    # --------------------------------------------------------
    # Footer text
    # --------------------------------------------------------

    canvas.setFont(
        regular_font,
        7.5,
    )

    canvas.setFillColor(GRAY_500)

    canvas.drawString(
        18 * mm,
        9 * mm,
        "AI ATS Resume Analyzer",
    )

    canvas.drawRightString(
        width - 18 * mm,
        9 * mm,
        f"Page {doc.page}",
    )

    canvas.restoreState()


# ============================================================
# MAIN REPORT
# ============================================================

def generate_report(result, filename):

    regular_font, bold_font = register_fonts()

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=22 * mm,
        bottomMargin=22 * mm,
        title="AI ATS Resume Report",
        author="AI ATS Resume Analyzer",
    )

    styles = getSampleStyleSheet()

    # ========================================================
    # CUSTOM STYLES
    # ========================================================

    styles.add(
        ParagraphStyle(
            name="ReportTitle",
            fontName=bold_font,
            fontSize=23,
            leading=28,
            textColor=NAVY,
            alignment=TA_CENTER,
            spaceAfter=6,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ReportSubtitle",
            fontName=regular_font,
            fontSize=10,
            leading=14,
            textColor=GRAY_500,
            alignment=TA_CENTER,
            spaceAfter=20,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SectionTitle",
            fontName=bold_font,
            fontSize=14,
            leading=18,
            textColor=NAVY,
            spaceBefore=8,
            spaceAfter=9,
        )
    )

    styles.add(
        ParagraphStyle(
            name="SmallLabel",
            fontName=bold_font,
            fontSize=8,
            leading=10,
            textColor=GRAY_500,
        )
    )

    styles.add(
        ParagraphStyle(
            name="ScoreValue",
            fontName=bold_font,
            fontSize=25,
            leading=28,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Recommendation",
            fontName=bold_font,
            fontSize=11,
            leading=14,
            textColor=NAVY,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeader",
            fontName=bold_font,
            fontSize=9,
            leading=12,
            textColor=NAVY,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableHeaderWhite",
            fontName=bold_font,
            fontSize=9,
            leading=12,
            textColor=WHITE,
        )
    )

    styles.add(
        ParagraphStyle(
            name="TableCell",
            fontName=regular_font,
            fontSize=9,
            leading=13,
            textColor=GRAY_700,
        )
    )

    styles.add(
        ParagraphStyle(
            name="FeedbackHeading",
            fontName=bold_font,
            fontSize=10.5,
            leading=14,
            textColor=BLUE,
            spaceBefore=7,
            spaceAfter=5,
        )
    )

    styles.add(
        ParagraphStyle(
            name="FeedbackText",
            fontName=regular_font,
            fontSize=9,
            leading=14,
            textColor=GRAY_700,
            spaceAfter=6,
        )
    )

    # IMPORTANT:
    # Do NOT name this style "Bullet".
    # ReportLab already has a built-in style with that name.
    styles.add(
        ParagraphStyle(
            name="CustomBullet",
            fontName=regular_font,
            fontSize=9,
            leading=14,
            leftIndent=12,
            firstLineIndent=-7,
            textColor=GRAY_700,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Question",
            fontName=bold_font,
            fontSize=9.5,
            leading=14,
            textColor=NAVY,
            spaceBefore=5,
            spaceAfter=4,
        )
    )

    styles.add(
        ParagraphStyle(
            name="Answer",
            fontName=regular_font,
            fontSize=8.8,
            leading=13,
            textColor=GRAY_700,
            leftIndent=8,
            spaceAfter=6,
        )
    )

    # ========================================================
    # STORY
    # ========================================================

    story = []

    overall_score = result.get(
        "overall_score",
        0,
    )

    recommendation = safe_text(
        result.get("recommendation"),
        "Not available",
    )

    candidate_name = safe_text(
        result.get("candidate_name"),
        "Unknown",
    )

    # ========================================================
    # REPORT HEADER
    # ========================================================

    story.append(
        Spacer(1, 5)
    )

    story.append(
        Paragraph(
            "AI ATS RESUME ANALYZER",
            styles["ReportTitle"],
        )
    )

    story.append(
        Paragraph(
            "Applicant Tracking System — Candidate Evaluation Report",
            styles["ReportSubtitle"],
        )
    )

    # ========================================================
    # CANDIDATE INFORMATION
    # ========================================================

    story.append(
        make_section_title(
            "Candidate Information",
            styles,
        )
    )

    story.append(
        candidate_information(
            result,
            styles,
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # ATS SCORE
    # ========================================================

    story.append(
        make_section_title(
            "ATS Score",
            styles,
        )
    )

    story.append(
        score_card(
            overall_score,
            recommendation,
            styles,
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # SCORE BREAKDOWN
    # ========================================================

    story.append(
        make_section_title(
            "Score Breakdown",
            styles,
        )
    )

    story.append(
        score_breakdown(
            result,
            styles,
        )
    )

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # SKILLS ANALYSIS
    # ========================================================

    matched_skills = result.get(
        "matched_skills",
        [],
    )

    missing_skills = result.get(
        "missing_skills",
        [],
    )

    story.append(
        make_section_title(
            "Skills Analysis",
            styles,
        )
    )

    matched_content = skill_section(
        "Matched",
        matched_skills,
        styles,
        LIGHT_GREEN,
        GREEN,
    )

    missing_content = skill_section(
        "Missing",
        missing_skills,
        styles,
        LIGHT_RED,
        RED,
    )

    skills_table = Table(
        [
            [
                Paragraph(
                    "<b>Matched Skills</b>",
                    styles["TableHeader"],
                ),
                Paragraph(
                    "<b>Missing Skills</b>",
                    styles["TableHeader"],
                ),
            ],
            [
                matched_content,
                missing_content,
            ],
        ],
        colWidths=[
            87 * mm,
            87 * mm,
        ],
    )

    skills_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    LIGHT_GREEN,
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    LIGHT_RED,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GRAY_200,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(
        skills_table
    )

    story.append(
        Spacer(1, 12)
    )

    # ========================================================
    # CANDIDATE EVALUATION
    # ========================================================

    strengths = result.get(
        "strengths",
        [],
    )

    weaknesses = result.get(
        "weaknesses",
        [],
    )

    story.append(
        make_section_title(
            "Candidate Evaluation",
            styles,
        )
    )

    strengths_content = skill_section(
        "Strengths",
        strengths,
        styles,
        LIGHT_GREEN,
        GREEN,
    )

    weaknesses_content = skill_section(
        "Weaknesses",
        weaknesses,
        styles,
        LIGHT_ORANGE,
        ORANGE,
    )

    evaluation_table = Table(
        [
            [
                Paragraph(
                    "<b>Strengths</b>",
                    styles["TableHeader"],
                ),
                Paragraph(
                    "<b>Areas for Improvement</b>",
                    styles["TableHeader"],
                ),
            ],
            [
                strengths_content,
                weaknesses_content,
            ],
        ],
        colWidths=[
            87 * mm,
            87 * mm,
        ],
    )

    evaluation_table.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (0, 0),
                    LIGHT_GREEN,
                ),
                (
                    "BACKGROUND",
                    (1, 0),
                    (1, 0),
                    LIGHT_ORANGE,
                ),
                (
                    "GRID",
                    (0, 0),
                    (-1, -1),
                    0.5,
                    GRAY_200,
                ),
                (
                    "VALIGN",
                    (0, 0),
                    (-1, -1),
                    "TOP",
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    8,
                ),
            ]
        )
    )

    story.append(
        evaluation_table
    )

    # ========================================================
    # AI RESUME FEEDBACK
    # ========================================================

    story.append(
        PageBreak()
    )

    story.append(
        make_section_title(
            "AI Resume Feedback",
            styles,
        )
    )

    feedback = result.get(
        "feedback",
        "",
    )

    feedback_elements = feedback_section(
        feedback,
        styles,
    )

    # IMPORTANT:
    # Add feedback elements directly to the story.
    #
    # DO NOT put the entire feedback list inside
    # a single Table cell.
    #
    # This allows ReportLab to split the feedback
    # naturally across multiple pages.
    for element in feedback_elements:

        story.append(
            element
        )

    def interview_section(questions, styles):

    elements = []

    if not questions:
        elements.append(
            Paragraph(
                "No interview questions available.",
                styles["TableCell"],
            )
        )
        return elements

    # ========================================================
    # HELPER: ADD QUESTION
    # ========================================================

    def add_question(question, number=None):

        if not question:
            return

        question = str(question).strip()

        if number is not None:
            question_text = f"<b>{number}. {clean_html(question)}</b>"
        else:
            question_text = f"<b>{clean_html(question)}</b>"

        elements.append(
            Paragraph(
                question_text,
                styles["Question"],
            )
        )

    # ========================================================
    # HELPER: ADD ANSWER
    # ========================================================

    def add_answer(answer):

        if not answer:
            return

        answer = str(answer).strip()

        elements.append(
            Paragraph(
                f"<b>What the interviewer is evaluating:</b> "
                f"{clean_html(answer)}",
                styles["Answer"],
            )
        )

    # ========================================================
    # DICTIONARY
    # ========================================================

    if isinstance(questions, dict):

        for category, items in questions.items():

            # Category heading
            elements.append(
                Paragraph(
                    clean_html(category),
                    styles["FeedbackHeading"],
                )
            )

            if isinstance(items, list):

                for index, item in enumerate(items, 1):

                    if isinstance(item, dict):

                        question = (
                            item.get("question")
                            or item.get("Question")
                            or item.get("text")
                            or item.get("Text")
                        )

                        evaluation = (
                            item.get("what_the_interviewer_is_evaluating")
                            or item.get("evaluation")
                            or item.get("ideal_answer")
                            or item.get("answer")
                            or item.get("Ideal Answer")
                        )

                        add_question(question, index)

                        if evaluation:
                            add_answer(evaluation)

                    else:

                        add_question(item, index)

            else:

                add_question(items)

            elements.append(
                Spacer(1, 8)
            )

        return elements

    # ========================================================
    # LIST
    # ========================================================

    if isinstance(questions, list):

        for index, item in enumerate(questions, 1):

            if isinstance(item, dict):

                question = (
                    item.get("question")
                    or item.get("Question")
                    or item.get("text")
                    or item.get("Text")
                )

                evaluation = (
                    item.get("what_the_interviewer_is_evaluating")
                    or item.get("evaluation")
                    or item.get("ideal_answer")
                    or item.get("answer")
                    or item.get("Ideal Answer")
                )

                add_question(question, index)

                if evaluation:
                    add_answer(evaluation)

            else:

                add_question(item, index)

            elements.append(
                Spacer(1, 5)
            )

        return elements

    # ========================================================
    # STRING / MARKDOWN
    # ========================================================

    text = str(questions)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove markdown code fences
    text = text.replace("```markdown", "")
    text = text.replace("```text", "")
    text = text.replace("```", "")

    # Normalize bullets
    text = text.replace("•", "\n•")
    text = text.replace("●", "\n•")
    text = text.replace("▪", "\n•")

    # Normalize markdown headings
    text = re.sub(
        r"#{1,6}\s*",
        "",
        text,
    )

    # ========================================================
    # PROCESS LINES
    # ========================================================

    question_number = 0
    current_question = None
    current_evaluation = []

    def flush_question():

        nonlocal current_question
        nonlocal current_evaluation

        if current_question:

            question_number_local = flush_question.counter + 1
            flush_question.counter = question_number_local

            add_question(
                current_question,
                question_number_local,
            )

            if current_evaluation:

                add_answer(
                    " ".join(current_evaluation)
                )

            elements.append(
                Spacer(1, 6)
            )

        current_question = None
        current_evaluation = []

    flush_question.counter = 0

    lines = text.splitlines()

    for raw_line in lines:

        line = raw_line.strip()

        if not line:
            continue

        # ----------------------------------------------------
        # CATEGORY HEADINGS
        # ----------------------------------------------------

        category_match = re.match(
            r"^(Technical Questions|Job-Specific Questions|"
            r"Missing-Skill Questions|Project Questions)"
            r"\s*:?\s*$",
            line,
            re.IGNORECASE,
        )

        if category_match:

            flush_question()

            elements.append(
                Paragraph(
                    clean_html(
                        category_match.group(1)
                    ),
                    styles["FeedbackHeading"],
                )
            )

            continue

        # ----------------------------------------------------
        # GENERIC HEADINGS
        # ----------------------------------------------------

        if (
            line.endswith(":")
            and not re.match(r"^\d+\.", line)
            and len(line) < 80
        ):

            flush_question()

            elements.append(
                Paragraph(
                    clean_html(
                        line.rstrip(":")
                    ),
                    styles["FeedbackHeading"],
                )
            )

            continue

        # ----------------------------------------------------
        # NUMBERED QUESTION
        # ----------------------------------------------------

        numbered_match = re.match(
            r"^\s*(\d+)[\.\)]\s+(.+)",
            line,
        )

        if numbered_match:

            flush_question()

            current_question = numbered_match.group(2).strip()

            continue

        # ----------------------------------------------------
        # BULLET QUESTION
        # ----------------------------------------------------

        bullet_match = re.match(
            r"^[•\-]\s+(.+)",
            line,
        )

        if bullet_match:

            content = bullet_match.group(1).strip()

            # Detect evaluation/answer text
            if re.match(
                r"^(what the interviewer is evaluating|"
                r"ideal answer|answer|evaluation)\s*:",
                content,
                re.IGNORECASE,
            ):

                evaluation = re.sub(
                    r"^(what the interviewer is evaluating|"
                    r"ideal answer|answer|evaluation)\s*:\s*",
                    "",
                    content,
                    flags=re.IGNORECASE,
                )

                current_evaluation.append(
                    evaluation
                )

            else:

                flush_question()

                current_question = content

            continue

        # ----------------------------------------------------
        # EVALUATION / ANSWER
        # ----------------------------------------------------

        evaluation_match = re.match(
            r"^(What the interviewer is evaluating|"
            r"Ideal Answer|Answer|Evaluation)\s*:\s*(.*)",
            line,
            re.IGNORECASE,
        )

        if evaluation_match:

            evaluation = evaluation_match.group(2).strip()

            if evaluation:
                current_evaluation.append(
                    evaluation
                )

            continue

        # ----------------------------------------------------
        # CONTINUATION TEXT
        # ----------------------------------------------------

        if current_question:

            current_evaluation.append(line)

        else:

            # Standalone text
            elements.append(
                Paragraph(
                    clean_html(line),
                    styles["Answer"],
                )
            )

    # ========================================================
    # FLUSH LAST QUESTION
    # ========================================================

    flush_question()

    if not elements:

        elements.append(
            Paragraph(
                "No interview questions available.",
                styles["TableCell"],
            )
        )

    return elements

    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    story.append(
        Spacer(1, 15)
    )

    story.append(
        make_section_title(
            "Report Summary",
            styles,
        )
    )

    summary_text = (
        f"The candidate "
        f"<b>{clean_html(candidate_name)}</b> "
        f"received an ATS score of "
        f"<b>{format_score(overall_score)}</b> "
        f"with a recommendation of "
        f"<b>{clean_html(recommendation)}</b>."
    )

    summary_card = Table(
        [
            [
                Paragraph(
                    summary_text,
                    styles["FeedbackText"],
                )
            ]
        ],
        colWidths=[
            175 * mm
        ],
    )

    summary_card.setStyle(
        TableStyle(
            [
                (
                    "BACKGROUND",
                    (0, 0),
                    (-1, -1),
                    LIGHT_BLUE,
                ),
                (
                    "BOX",
                    (0, 0),
                    (-1, -1),
                    0.7,
                    BLUE,
                ),
                (
                    "LEFTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "RIGHTPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "TOPPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
                (
                    "BOTTOMPADDING",
                    (0, 0),
                    (-1, -1),
                    12,
                ),
            ]
        )
    )

    story.append(
        summary_card
    )

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(
        story,
        onFirstPage=lambda canvas, doc:
            draw_header_footer(
                canvas,
                doc,
                regular_font,
                bold_font,
            ),
        onLaterPages=lambda canvas, doc:
            draw_header_footer(
                canvas,
                doc,
                regular_font,
                bold_font,
            ),
    )