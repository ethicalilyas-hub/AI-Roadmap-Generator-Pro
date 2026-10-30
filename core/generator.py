
import json

from pydantic import ValidationError

from core.groq_client import get_groq_client, MODEL_NAME
from core.schemas import LearningRoadmap
from core.prompt_engine import build_roadmap_prompt


def generate_roadmap(
    field: str,
    current_level: str,
    target_level: str,
    daily_hours: float,
    preferred_duration: int,
    learning_goal: str,
) -> LearningRoadmap:

    # Connect to Groq
    client = get_groq_client()

    # Build the AI prompt
    prompt = build_roadmap_prompt(
        field=field,
        current_level=current_level,
        target_level=target_level,
        daily_hours=daily_hours,
        preferred_duration=preferred_duration,
        learning_goal=learning_goal,
    )

    # Generate roadmap
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a professional AI learning roadmap generator. "
                    "Return valid JSON only."
                ),
            },
            {
                "role": "user",
                "content": (
                    prompt
                    + "\n\nRequired JSON schema:\n"
                    + json.dumps(
                        LearningRoadmap.model_json_schema(),
                        indent=2,
                    )
                ),
            },
        ],
        response_format={"type": "json_object"},
        max_completion_tokens=8192,
        temperature=0.2,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("AI returned an empty response.")

    # Validate AI response
    try:
        roadmap_data = json.loads(content)

        roadmap = LearningRoadmap.model_validate(roadmap_data)

        return roadmap

    except (json.JSONDecodeError, ValidationError) as error:
        raise ValueError(
            "AI returned an invalid roadmap. Please try again."
        ) from error
