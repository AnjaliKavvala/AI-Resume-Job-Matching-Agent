import streamlit as st

from utils.pdf_reader import extract_text_from_pdf
from utils.workflow import agent_workflow


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="AI Resume & Job Matching Agent",
    page_icon="🤖",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        text-align: center;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    .skill-box {
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        background-color: #f5f5f5;
    }

    .score-box {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
        background-color: #f5f5f5;
        margin-bottom: 20px;
    }

    .score-number {
        font-size: 48px;
        font-weight: 700;
    }

    .footer {
        text-align: center;
        color: #777;
        margin-top: 40px;
        padding: 20px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🤖 AI-Powered Resume & Job Matching Agent</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Analyze your resume against a job description using Generative AI'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# INPUT SECTION
# ============================================================

col1, col2 = st.columns(2)


with col1:

    st.subheader("📄 Upload Resume")

    uploaded_file = st.file_uploader(
        "Upload your resume in PDF format",
        type=["pdf"]
    )


with col2:

    st.subheader("💼 Job Description")

    job_description = st.text_area(
        "Paste the job description here",
        height=250,
        placeholder=(
            "Example:\n\n"
            "We are looking for a Generative AI Engineer...\n"
            "Required skills: Python, LLMs, RAG..."
        )
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("")

analyze_button = st.button(
    "🚀 Analyze Resume",
    use_container_width=True
)


# ============================================================
# ANALYSIS
# ============================================================

if analyze_button:

    if uploaded_file is None:

        st.warning(
            "⚠️ Please upload your resume PDF."
        )

    elif not job_description.strip():

        st.warning(
            "⚠️ Please enter the job description."
        )

    else:

        with st.spinner(
            "🤖 AI is analyzing your resume and job description..."
        ):

            try:

                # ------------------------------------------------
                # EXTRACT RESUME TEXT
                # ------------------------------------------------

                resume_text = extract_text_from_pdf(
                    uploaded_file
                )

                if not resume_text.strip():

                    st.error(
                        "❌ Could not extract text from the PDF."
                    )

                    st.stop()


                # ------------------------------------------------
                # INITIAL WORKFLOW STATE
                # ------------------------------------------------

                initial_state = {

                    "resume_text": resume_text,

                    "job_description": job_description,

                    "analysis": {}

                }


                # ------------------------------------------------
                # RUN LANGGRAPH WORKFLOW
                # ------------------------------------------------

                result = agent_workflow.invoke(
                    initial_state
                )


                analysis = result.get(
                    "analysis",
                    {}
                )


            except Exception as e:

                st.error(
                    f"❌ Something went wrong: {e}"
                )

                st.stop()


        # ========================================================
        # SUCCESS MESSAGE
        # ========================================================

        st.success(
            "✅ Resume analysis completed successfully!"
        )


        # ========================================================
        # CANDIDATE INFORMATION
        # ========================================================

        st.markdown(
            '<div class="section-title">👤 Candidate Information</div>',
            unsafe_allow_html=True
        )

        candidate_name = analysis.get(
            "candidate_name",
            "Not available"
        )

        st.write(
            f"**Candidate:** {candidate_name}"
        )


        # ========================================================
        # MATCH SCORE
        # ========================================================

        st.markdown(
            '<div class="section-title">🎯 Job Match Score</div>',
            unsafe_allow_html=True
        )

        match_score = analysis.get(
            "match_score",
            0
        )

        score_col1, score_col2, score_col3 = st.columns(
            [1, 2, 1]
        )

        with score_col2:
            st.markdown(
                f"""
                <div class="score-box">
                <div class="score-number">{match_score}%</div>
                <div>Resume Match Score</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ========================================================
        # RESUME SUMMARY
        # ========================================================

        with st.expander(
            "📄 Resume Summary",
            expanded=True
        ):

            education = analysis.get(
                "education",
                []
            )

            technical_skills = analysis.get(
                "technical_skills",
                []
            )

            projects = analysis.get(
                "projects",
                []
            )

            experience = analysis.get(
                "experience",
                []
            )

            certifications = analysis.get(
                "certifications",
                []
            )


            st.markdown("### 🎓 Education")

            if education:

                for item in education:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No education information available."
                )


            st.markdown("### 💻 Technical Skills")

            if technical_skills:

                for item in technical_skills:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No technical skills identified."
                )


            st.markdown("### 🚀 Projects")

            if projects:

                for item in projects:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No projects identified."
                )


            st.markdown("### 💼 Experience")

            if experience:

                for item in experience:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No experience identified."
                )


            st.markdown("### 📜 Certifications")

            if certifications:

                for item in certifications:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No certifications identified."
                )


        # ========================================================
        # JOB REQUIREMENTS
        # ========================================================

        with st.expander(
            "💼 Job Requirements",
            expanded=True
        ):

            required_skills = analysis.get(
                "required_job_skills",
                []
            )

            preferred_skills = analysis.get(
                "preferred_job_skills",
                []
            )

            responsibilities = analysis.get(
                "job_responsibilities",
                []
            )


            st.markdown(
                "### Required Skills"
            )

            if required_skills:

                for item in required_skills:

                    st.write(
                        f"🔹 {item}"
                    )

            else:

                st.write(
                    "No required skills identified."
                )


            st.markdown(
                "### Preferred Skills"
            )

            if preferred_skills:

                for item in preferred_skills:

                    st.write(
                        f"🔹 {item}"
                    )

            else:

                st.write(
                    "No preferred skills identified."
                )


            st.markdown(
                "### Responsibilities"
            )

            if responsibilities:

                for item in responsibilities:

                    st.write(
                        f"🔹 {item}"
                    )

            else:

                st.write(
                    "No responsibilities identified."
                )


        # ========================================================
        # SKILL MATCHING
        # ========================================================

        with st.expander(
            "🎯 Skill Matching",
            expanded=True
        ):

            matching_skills = analysis.get(
                "matching_skills",
                []
            )

            partial_matches = analysis.get(
                "partial_matches",
                []
            )

            missing_skills = analysis.get(
                "missing_skills",
                []
            )


            st.markdown(
                "### ✅ Matching Skills"
            )

            if matching_skills:

                for item in matching_skills:

                    st.success(
                        item
                    )

            else:

                st.write(
                    "No direct skill matches found."
                )


            st.markdown(
                "### 🟡 Partial Matches"
            )

            if partial_matches:

                for item in partial_matches:

                    st.warning(
                        item
                    )

            else:

                st.write(
                    "No partial matches identified."
                )


            st.markdown(
                "### ❌ Missing Skills"
            )

            if missing_skills:

                for item in missing_skills:

                    st.error(
                        item
                    )

            else:

                st.write(
                    "No major missing skills identified."
                )


        # ========================================================
        # SKILL GAP ANALYSIS
        # ========================================================

        with st.expander(
            "⚠️ Skill Gap Analysis",
            expanded=True
        ):

            technical_gaps = analysis.get(
                "technical_gaps",
                []
            )

            tools_framework_gaps = analysis.get(
                "tools_framework_gaps",
                []
            )

            knowledge_gaps = analysis.get(
                "knowledge_gaps",
                []
            )


            st.markdown(
                "### 🔧 Technical Gaps"
            )

            if technical_gaps:

                for item in technical_gaps:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No technical gaps identified."
                )


            st.markdown(
                "### 🛠️ Tools / Framework Gaps"
            )

            if tools_framework_gaps:

                for item in tools_framework_gaps:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No tool or framework gaps identified."
                )


            st.markdown(
                "### 🧠 Knowledge Gaps"
            )

            if knowledge_gaps:

                for item in knowledge_gaps:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No major knowledge gaps identified."
                )


        # ========================================================
        # CAREER RECOMMENDATIONS
        # ========================================================

        with st.expander(
            "📚 Career Recommendations",
            expanded=True
        ):

            skills_to_learn = analysis.get(
                "skills_to_learn",
                []
            )

            project_ideas = analysis.get(
                "project_ideas",
                []
            )

            learning_order = analysis.get(
                "learning_order",
                []
            )


            st.markdown(
                "### 📖 Skills to Learn"
            )

            if skills_to_learn:

                for item in skills_to_learn:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No additional skills recommended."
                )


            st.markdown(
                "### 🚀 Project Ideas"
            )

            if project_ideas:

                for item in project_ideas:

                    st.write(
                        f"• {item}"
                    )

            else:

                st.write(
                    "No project ideas generated."
                )


            st.markdown(
                "### 📌 Recommended Learning Order"
            )

            if learning_order:

                for index, item in enumerate(
                    learning_order,
                    start=1
                ):

                    st.write(
                        f"{index}. {item}"
                    )

            else:

                st.write(
                    "No learning order generated."
                )


        # ========================================================
        # INTERVIEW PREPARATION
        # ========================================================

        with st.expander(
            "🎤 Interview Preparation",
            expanded=True
        ):

            technical_questions = analysis.get(
                "technical_questions",
                []
            )

            project_questions = analysis.get(
                "project_questions",
                []
            )

            behavioral_questions = analysis.get(
                "behavioral_questions",
                []
            )

            skill_gap_questions = analysis.get(
                "skill_gap_questions",
                []
            )


            st.markdown(
                "### 💻 Technical Questions"
            )

            if technical_questions:

                for index, question in enumerate(
                    technical_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            else:

                st.write(
                    "No technical questions generated."
                )


            st.markdown(
                "### 🚀 Project Questions"
            )

            if project_questions:

                for index, question in enumerate(
                    project_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            else:

                st.write(
                    "No project questions generated."
                )


            st.markdown(
                "### 🗣️ Behavioral Questions"
            )

            if behavioral_questions:

                for index, question in enumerate(
                    behavioral_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            else:

                st.write(
                    "No behavioral questions generated."
                )


            st.markdown(
                "### ⚠️ Skill Gap Questions"
            )

            if skill_gap_questions:

                for index, question in enumerate(
                    skill_gap_questions,
                    start=1
                ):

                    st.write(
                        f"**{index}.** {question}"
                    )

            else:

                st.write(
                    "No skill-gap questions generated."
                )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">

    🤖 Built with <b>LangGraph + Ollama + Gemma 3 + Streamlit</b>

    </div>
    """,
    unsafe_allow_html=True
)