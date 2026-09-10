import json

from utils.pdf_reader import extract_text_from_pdf
from utils.workflow import agent_workflow


# ==================================================
# TEST RESUME
# ==================================================

pdf_path = "test_resume.pdf"

print("\n📄 Reading resume...")

resume_text = extract_text_from_pdf(pdf_path)

print("✅ Resume text extracted.")


# ==================================================
# TEST JOB DESCRIPTION
# ==================================================

job_description = """
We are looking for a Generative AI Engineer.

Required skills:
Python, Generative AI, LLMs, RAG, LangChain,
Vector Databases, Prompt Engineering and Git.

Responsibilities:
Build AI-powered applications, work with LLMs,
develop RAG systems, and create AI agents.
"""


# ==================================================
# INITIAL STATE
# ==================================================

initial_state = {
    "resume_text": resume_text,
    "job_description": job_description,
    "analysis": {}
}


# ==================================================
# RUN WORKFLOW
# ==================================================

print("\n" + "=" * 70)
print("🚀 STARTING AI RESUME & JOB MATCHING WORKFLOW")
print("=" * 70)

result = agent_workflow.invoke(initial_state)

analysis = result["analysis"]


# ==================================================
# DISPLAY RESULTS
# ==================================================

print("\n" + "=" * 70)
print("👤 CANDIDATE")
print("=" * 70)

print(
    analysis.get(
        "candidate_name",
        "Not available"
    )
)


print("\n" + "=" * 70)
print("🎓 EDUCATION")
print("=" * 70)

for item in analysis.get("education", []):

    print(f"• {item}")


print("\n" + "=" * 70)
print("💻 TECHNICAL SKILLS")
print("=" * 70)

for item in analysis.get("technical_skills", []):

    print(f"• {item}")


print("\n" + "=" * 70)
print("🚀 PROJECTS")
print("=" * 70)

for item in analysis.get("projects", []):

    print(f"• {item}")


print("\n" + "=" * 70)
print("💼 EXPERIENCE")
print("=" * 70)

for item in analysis.get("experience", []):

    print(f"• {item}")


print("\n" + "=" * 70)
print("📜 CERTIFICATIONS")
print("=" * 70)

for item in analysis.get("certifications", []):

    print(f"• {item}")


print("\n" + "=" * 70)
print("💼 JOB REQUIREMENTS")
print("=" * 70)

print("\nRequired Skills:")

for item in analysis.get(
    "required_job_skills",
    []
):

    print(f"• {item}")


print("\nPreferred Skills:")

for item in analysis.get(
    "preferred_job_skills",
    []
):

    print(f"• {item}")


print("\nResponsibilities:")

for item in analysis.get(
    "job_responsibilities",
    []
):

    print(f"• {item}")


print("\n" + "=" * 70)
print("🎯 SKILL MATCHING")
print("=" * 70)

print(
    f"\nMatch Score: "
    f"{analysis.get('match_score', 0)}%"
)


print("\nMatching Skills:")

for item in analysis.get(
    "matching_skills",
    []
):

    print(f"✅ {item}")


print("\nPartial Matches:")

for item in analysis.get(
    "partial_matches",
    []
):

    print(f"🟡 {item}")


print("\nMissing Skills:")

for item in analysis.get(
    "missing_skills",
    []
):

    print(f"❌ {item}")


print("\n" + "=" * 70)
print("⚠️ SKILL GAPS")
print("=" * 70)

print("\nTechnical Gaps:")

for item in analysis.get(
    "technical_gaps",
    []
):

    print(f"• {item}")


print("\nTools / Framework Gaps:")

for item in analysis.get(
    "tools_framework_gaps",
    []
):

    print(f"• {item}")


print("\nKnowledge Gaps:")

for item in analysis.get(
    "knowledge_gaps",
    []
):

    print(f"• {item}")


print("\n" + "=" * 70)
print("📚 RECOMMENDATIONS")
print("=" * 70)

print("\nSkills to Learn:")

for item in analysis.get(
    "skills_to_learn",
    []
):

    print(f"• {item}")


print("\nProject Ideas:")

for item in analysis.get(
    "project_ideas",
    []
):

    print(f"• {item}")


print("\nLearning Order:")

for item in analysis.get(
    "learning_order",
    []
):

    print(f"• {item}")


print("\n" + "=" * 70)
print("🎤 INTERVIEW QUESTIONS")
print("=" * 70)

print("\nTechnical:")

for item in analysis.get(
    "technical_questions",
    []
):

    print(f"• {item}")


print("\nProject:")

for item in analysis.get(
    "project_questions",
    []
):

    print(f"• {item}")


print("\nBehavioral:")

for item in analysis.get(
    "behavioral_questions",
    []
):

    print(f"• {item}")


print("\nSkill Gap:")

for item in analysis.get(
    "skill_gap_questions",
    []
):

    print(f"• {item}")


# ==================================================
# FINAL STATUS
# ==================================================

print("\n" + "=" * 70)
print("✅ WORKFLOW COMPLETED SUCCESSFULLY")
print("=" * 70)