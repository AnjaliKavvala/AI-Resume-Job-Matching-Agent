from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from utils.analyzer import resume_job_analysis


class AgentState(TypedDict):
    resume_text: str
    job_description: str
    analysis: Any


# --------------------------------------------------
# AI RESUME & JOB MATCHING AGENT
# --------------------------------------------------

def analysis_node(state: AgentState):

    print("\n🤖 AI Resume & Job Matching Agent running...")

    result = resume_job_analysis(
        state["resume_text"],
        state["job_description"]
    )

    print("✅ AI analysis completed.")

    return {
        "analysis": result
    }


# --------------------------------------------------
# BUILD LANGGRAPH WORKFLOW
# --------------------------------------------------

workflow = StateGraph(AgentState)


workflow.add_node(
    "resume_job_matching_agent",
    analysis_node
)


workflow.add_edge(
    START,
    "resume_job_matching_agent"
)


workflow.add_edge(
    "resume_job_matching_agent",
    END
)


# --------------------------------------------------
# COMPILE WORKFLOW
# --------------------------------------------------

agent_workflow = workflow.compile()