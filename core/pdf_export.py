
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf(roadmap):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=45,
        leftMargin=45,
        topMargin=45,
        bottomMargin=45,
    )

    styles = getSampleStyleSheet()

    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Title"],
        fontSize=23,
        textColor=colors.HexColor("#4338CA"),
        alignment=TA_CENTER,
        spaceAfter=15,
    ))

    styles.add(ParagraphStyle(
        name="SectionTitle",
        parent=styles["Heading2"],
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=15,
        spaceAfter=8,
    ))

    styles.add(ParagraphStyle(
        name="SmallText",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
    ))

    story = []

    def add_text(text, style="BodyText"):
        safe_text = escape(str(text))
        story.append(Paragraph(safe_text, styles[style]))
        story.append(Spacer(1, 6))

    def add_list(items):
        for item in items:
            add_text(f"&bull; {escape(str(item))}", "SmallText")

    # Cover heading
    story.append(Paragraph(
        "AI LEARNING ROADMAP",
        styles["MainTitle"]
    ))

    add_text(roadmap.roadmap_title, "Heading1")

    # Overview
    story.append(Paragraph("Roadmap Overview", styles["SectionTitle"]))

    add_text(roadmap.overview)

    # Summary
    story.append(Paragraph("Learning Summary", styles["SectionTitle"]))

    summary = [
        ["Field", roadmap.field],
        ["Current Level", roadmap.current_level],
        ["Target Level", roadmap.target_level],
        ["Estimated Duration",
         f"{roadmap.estimated_duration_months} Months"],
        ["Weekly Study Hours", str(roadmap.weekly_study_hours)],
    ]

    table = Table(summary, colWidths=[150, 300])

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1),
         colors.HexColor("#E0E7FF")),
        ("TEXTCOLOR", (0, 0), (-1, -1),
         colors.HexColor("#1E1B4B")),
        ("GRID", (0, 0), (-1, -1), 0.5,
         colors.HexColor("#C7D2FE")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))

    story.append(table)

    # Prerequisites
    story.append(Paragraph("Prerequisites", styles["SectionTitle"]))
    add_list(roadmap.prerequisites)

    # Learning phases
    story.append(Paragraph("Learning Journey", styles["SectionTitle"]))

    for phase in roadmap.phases:

        story.append(Paragraph(
            f"Phase {phase.phase_number}: {escape(phase.title)}",
            styles["Heading2"]
        ))

        add_text(f"Objective: {phase.objective}")
        add_text(f"Duration: {phase.duration_months} months")

        add_text("Topics", "Heading3")
        add_list(phase.topics)

        add_text("Weekly Learning Plan", "Heading3")

        for week in phase.weekly_plan:
            add_text(f"Week {week.week}: {week.topic}", "Heading4")
            add_list(week.learning_objectives)
            add_list(week.practical_tasks)

        add_text("Practical Projects", "Heading3")

        for project in phase.projects:
            add_text(project.name, "Heading4")
            add_text(project.description, "SmallText")
            add_text(f"Difficulty: {project.difficulty}", "SmallText")
            add_list(project.skills_practiced)

        add_text("Learning Resources", "Heading3")

        for resource in phase.resources:
            add_text(resource.name, "Heading4")
            add_text(f"Type: {resource.resource_type}", "SmallText")
            add_text(f"URL: {resource.url}", "SmallText")
            add_text(resource.purpose, "SmallText")

        add_text("Milestones", "Heading3")

        for milestone in phase.milestones:
            add_text(milestone.title, "Heading4")
            add_text(milestone.expected_outcome)
            add_list(milestone.completion_criteria)

    # Career guidance
    story.append(Paragraph(
        "Career Opportunities",
        styles["SectionTitle"]
    ))

    add_list(roadmap.career_opportunities)

    # Final recommendations
    story.append(Paragraph(
        "Final Recommendations",
        styles["SectionTitle"]
    ))

    add_list(roadmap.final_recommendations)

    # Footer
    def add_footer(canvas, document):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawCentredString(
            A4[0] / 2,
            25,
            f"AI Roadmap Generator Pro | Page {document.page}"
        )
        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_footer,
        onLaterPages=add_footer,
    )

    return buffer.getvalue()
