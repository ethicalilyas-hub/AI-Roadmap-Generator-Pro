
def build_roadmap_prompt(
    field: str,
    current_level: str,
    target_level: str,
    daily_hours: float,
    preferred_duration: int,
    learning_goal: str,
) -> str:

    return f"""
You are an expert curriculum designer, career strategist,
technical educator, and professional learning architect.

Create a comprehensive, personalized learning roadmap.

USER PROFILE:
Field: {field}
Current Level: {current_level}
Target Level: {target_level}
Daily Study Hours: {daily_hours}
Preferred Duration: {preferred_duration} months
Learning Goal: {learning_goal}

ROADMAP REQUIREMENTS:

1. Analyze the user's current knowledge.
2. Identify necessary prerequisites.
3. Estimate a realistic learning duration.
4. Divide the roadmap into logical learning phases.
5. Include weekly learning plans in every phase.
6. Include theory and practical exercises.
7. Suggest real-world projects with difficulty levels.
8. Recommend useful learning resources.
9. Define measurable milestones.
10. Suggest relevant career opportunities.

QUALITY RULES:

- Avoid generic learning plans.
- Arrange topics in logical prerequisite order.
- Start with fundamentals and progress to advanced skills.
- Make weekly activities achievable within the available time.
- Keep projects relevant to the selected field.
- Do not guarantee employment or expertise.
- Do not invent resource URLs.
- If the preferred duration is unrealistic, explain this
  in the overview and provide a more realistic estimate.
- Make the roadmap detailed and actionable.

OUTPUT RULE:
Return valid JSON matching the supplied LearningRoadmap
schema. Include every required field and use the correct
data types. Do not use Markdown code fences.
"""
