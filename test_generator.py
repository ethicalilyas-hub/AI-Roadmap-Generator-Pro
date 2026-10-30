
from core.generator import generate_roadmap


try:
    print("Generating AI roadmap... Please wait.")

    roadmap = generate_roadmap(
        field="Cybersecurity",
        current_level="Beginner",
        target_level="Advanced",
        daily_hours=3,
        preferred_duration=6,
        learning_goal="Develop practical cybersecurity skills",
    )

    print("\nROADMAP GENERATED SUCCESSFULLY!")

    print("\nTitle:", roadmap.roadmap_title)
    print("Field:", roadmap.field)

    print(
        "Estimated Duration:",
        roadmap.estimated_duration_months,
        "months",
    )

    print("\nOVERVIEW:")
    print(roadmap.overview)

    print("\nLEARNING PHASES:")

    for phase in roadmap.phases:

        print(f"\nPhase {phase.phase_number}: {phase.title}")
        print("Objective:", phase.objective)

        print("\nTopics:")

        for topic in phase.topics:
            print("-", topic)

        print("\nProjects:")

        for project in phase.projects:
            print("-", project.name)

except Exception as error:
    print("\nROADMAP GENERATION FAILED!")
    print(error)
