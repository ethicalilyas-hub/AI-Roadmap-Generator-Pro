
import streamlit as st
from pathlib import Path

from core.generator import generate_roadmap
from core.pdf_export import generate_pdf


# =====================================
# PAGE CONFIGURATION
# =====================================

st.set_page_config(
    page_title="AI Roadmap Generator Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================
# LOAD CUSTOM CSS
# =====================================

css_path = Path(__file__).parent / "assets" / "style.css"

if css_path.exists():
    st.markdown(
        f"<style>{css_path.read_text(encoding='utf-8')}</style>",
        unsafe_allow_html=True,
    )


# =====================================
# SESSION STATE
# =====================================

if "roadmap" not in st.session_state:
    st.session_state.roadmap = None


# =====================================
# SIDEBAR
# =====================================

with st.sidebar:

    st.markdown("## 🚀 Roadmap AI")

    st.caption("INTELLIGENT LEARNING PLATFORM")

    st.divider()

    st.markdown("### Navigation")

    st.markdown("🏠  Dashboard")
    st.markdown("✨  Generate Roadmap")
    st.markdown("📚  My Learning Plans")
    st.markdown("📊  Progress Analytics")

    st.divider()

    st.markdown("### About")

    st.caption(
        "An AI-powered platform that creates "
        "personalized learning journeys."
    )

    st.divider()

    st.caption("AI ROADMAP GENERATOR PRO")
    st.caption("Powered by Groq AI")


# =====================================
# HERO SECTION
# =====================================

st.markdown(
    """
    <div class="hero-card">
        <div class="small-label">
            YOUR PERSONAL AI LEARNING ARCHITECT
        </div>
        <h1>Build Your Future With AI</h1>
        <p>
            Generate intelligent, personalized learning roadmaps.
            Learn any skill, master any field, and achieve your goals.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================
# ROADMAP GENERATION FORM
# =====================================

st.markdown("## ✨ Create Your Learning Roadmap")

st.write(
    "Tell us about your learning goals. "
    "Our AI will design a personalized learning journey."
)

with st.form("roadmap_form"):

    col1, col2 = st.columns(2)

    with col1:

        field = st.text_input(
            "What do you want to learn?",
            placeholder="e.g. Cybersecurity, Python, AI, Web Development",
        )

        current_level = st.selectbox(
            "Your current skill level",
            ["Beginner", "Intermediate", "Advanced"],
        )

        daily_hours = st.number_input(
            "Daily study hours",
            min_value=0.5,
            max_value=16.0,
            value=3.0,
            step=0.5,
        )

    with col2:

        target_level = st.selectbox(
            "Your target skill level",
            ["Intermediate", "Advanced", "Job Ready", "Expert"],
        )

        preferred_duration = st.number_input(
            "Preferred learning duration (months)",
            min_value=1,
            max_value=60,
            value=6,
            step=1,
        )

        learning_goal = st.text_input(
            "What is your main goal?",
            placeholder="e.g. Build professional skills",
        )

    st.write("")

    generate_button = st.form_submit_button(
        "✨ Generate My AI Roadmap",
        use_container_width=True,
    )


# =====================================
# GENERATE ROADMAP
# =====================================

if generate_button:

    if not field.strip() or not learning_goal.strip():

        st.warning(
            "Please enter your learning field and goal."
        )

    elif len(field) > 120 or len(learning_goal) > 500:

        st.warning(
            "Please shorten your field or learning goal."
        )

    elif current_level == target_level:

        st.warning(
            "Please select a target level different from "
            "your current level."
        )

    else:

        try:

            with st.spinner(
                "AI is analyzing your goals and building your roadmap..."
            ):

                roadmap = generate_roadmap(
                    field=field.strip(),
                    current_level=current_level,
                    target_level=target_level,
                    daily_hours=daily_hours,
                    preferred_duration=preferred_duration,
                    learning_goal=learning_goal.strip(),
                )

                st.session_state.roadmap = roadmap

            st.success("Your personalized roadmap is ready!")

        except Exception:
            st.error(
                "Unable to generate your roadmap. "
                "Please check your API configuration and try again."
            )


# =====================================
# DISPLAY ROADMAP
# =====================================

roadmap = st.session_state.roadmap

if roadmap:

    st.divider()

    st.markdown("## 🎯 Your Personalized Roadmap")

    st.markdown(f"### {roadmap.roadmap_title}")
    pdf_data = generate_pdf(roadmap)

    st.download_button(
        label="📄 Download Complete Roadmap (PDF)",
        data=pdf_data,
        file_name="AI_Learning_Roadmap.pdf",
        mime="application/pdf",
        use_container_width=True,
    )

    st.write(roadmap.overview)

    # Statistics

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Estimated Duration",
        f"{roadmap.estimated_duration_months} Months",
    )

    col2.metric(
        "Weekly Study Hours",
        roadmap.weekly_study_hours,
    )

    col3.metric(
        "Learning Phases",
        len(roadmap.phases),
    )

    st.divider()

    # Tabs

    overview_tab, roadmap_tab, career_tab = st.tabs(
        [
            "📋 Overview",
            "🗺️ Learning Roadmap",
            "💼 Career Guidance",
        ]
    )

    # OVERVIEW TAB

    with overview_tab:

        st.markdown("### Prerequisites")

        for item in roadmap.prerequisites:
            st.markdown(f"- {item}")

        st.markdown("### Final Recommendations")

        for item in roadmap.final_recommendations:
            st.markdown(f"- {item}")

    # ROADMAP TAB

    with roadmap_tab:

        st.markdown("### Learning Journey")

        for phase in roadmap.phases:

            with st.expander(
                f"Phase {phase.phase_number}: {phase.title}",
                expanded=False,
            ):

                st.write(phase.objective)

                st.markdown(
                    f"**Duration:** {phase.duration_months} months"
                )

                st.markdown("#### Topics")

                for topic in phase.topics:
                    st.markdown(f"- {topic}")

                st.markdown("#### Weekly Learning Plan")

                for week in phase.weekly_plan:

                    st.markdown(
                        f"**Week {week.week}: {week.topic}**"
                    )

                    for objective in week.learning_objectives:
                        st.markdown(f"- {objective}")

                    for task in week.practical_tasks:
                        st.markdown(f"- Practical task: {task}")

                st.markdown("#### Practical Projects")

                for project in phase.projects:

                    st.markdown(f"**{project.name}**")

                    st.write(project.description)

                    st.caption(
                        f"Difficulty: {project.difficulty}"
                    )

                st.markdown("#### Learning Resources")

                for resource in phase.resources:

                    st.markdown(
                        f"- [{resource.name}]({resource.url}) "
                        f"— {resource.purpose}"
                    )

                st.markdown("#### Milestones")

                for milestone in phase.milestones:

                    st.markdown(f"**{milestone.title}**")

                    st.write(milestone.expected_outcome)

                    for criteria in milestone.completion_criteria:
                        st.markdown(f"- {criteria}")

    # CAREER TAB

    with career_tab:

        st.markdown("### Career Opportunities")

        for career in roadmap.career_opportunities:
            st.markdown(f"- 💼 {career}")

        st.info(
            "Career outcomes depend on practical skills, "
            "experience and market requirements."
        )

    st.divider()

    if st.button("🔄 Generate Another Roadmap"):
        st.session_state.roadmap = None
        st.rerun()

else:

    st.info(
        "Your generated learning roadmap will appear here."
    )

    st.markdown("### What You Can Generate")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 💻 Technology")
        st.caption("Python, AI, Web Development, Cybersecurity")

    with col2:
        st.markdown("#### 📈 Business")
        st.caption("Marketing, Entrepreneurship, Management")

    with col3:
        st.markdown("#### 🎨 Creative Skills")
        st.caption("Graphic Design, Video Editing, UI/UX")
