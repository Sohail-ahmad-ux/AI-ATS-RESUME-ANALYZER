import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import streamlit as st


# ==========================================
# ATS Gauge
# ==========================================

def ats_gauge(score):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,

            title={"text": "ATS Score"},

            gauge={
                "axis": {"range": [0, 100]},

                "bar": {"color": "#2563EB"},

                "steps": [

                    {"range": [0, 50], "color": "#FECACA"},

                    {"range": [50, 75], "color": "#FDE68A"},

                    {"range": [75, 100], "color": "#BBF7D0"}

                ],
            },
        )
    )

    fig.update_layout(height=350)

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# Skill Pie Chart
# ==========================================

def skill_pie_chart(matched, missing):

    data = pd.DataFrame({

        "Category": [

            "Matched",

            "Missing"

        ],

        "Count": [

            len(matched),

            len(missing)

        ]

    })

    fig = px.pie(

        data,

        values="Count",

        names="Category",

        hole=.5,

        title="Skill Match"

    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ==========================================
# Score Breakdown
# ==========================================

def score_bar_chart(result):

    scores = pd.DataFrame({

        "Category": [

            "Skill",

            "Experience",

            "Education",

            "Keyword",

            "Resume"

        ],

        "Score": [

            result["skill_score"],

            result["experience_score"],

            result["education_score"],

            result["keyword_score"],

            result["resume_quality_score"]

        ]

    })

    fig = px.bar(

        scores,

        x="Category",

        y="Score",

        text="Score",

        title="Score Breakdown"

    )

    fig.update_traces(

        textposition="outside"

    )

    fig.update_layout(

        yaxis_range=[0,100]

    )

    st.plotly_chart(

        fig,

        use_container_width=True

    )