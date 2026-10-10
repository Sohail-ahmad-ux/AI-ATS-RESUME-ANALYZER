from langgraph.graph import StateGraph, START, END

from state import ATSState

from agents.resume_parser import resume_parser
from agents.jd_analyzer import jd_analyzer
from agents.skill_matcher import skill_matcher
from agents.ats_scorer import ats_scorer
from agents.feedback_agent import feedback_agent
from agents.interview_agent import interview_agent


# Create graph
builder = StateGraph(ATSState)


# ==========================
# Add Agents
# ==========================

builder.add_node("resume_parser", resume_parser)

builder.add_node("jd_analyzer", jd_analyzer)

builder.add_node("skill_matcher", skill_matcher)

builder.add_node("ats_scorer", ats_scorer)

builder.add_node("feedback_agent", feedback_agent)

builder.add_node("interview_agent", interview_agent)


# ==========================
# Workflow
# ==========================

builder.add_edge(START, "resume_parser")

builder.add_edge("resume_parser", "jd_analyzer")

builder.add_edge("jd_analyzer", "skill_matcher")

builder.add_edge("skill_matcher", "ats_scorer")

builder.add_edge("ats_scorer", "feedback_agent")

builder.add_edge("feedback_agent", "interview_agent")

builder.add_edge("interview_agent", END)


# ==========================
# Compile Graph
# ==========================

graph = builder.compile()