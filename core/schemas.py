
from pydantic import BaseModel


class WeeklyPlan(BaseModel):
    week: int
    topic: str
    learning_objectives: list[str]
    practical_tasks: list[str]


class Project(BaseModel):
    name: str
    description: str
    difficulty: str
    skills_practiced: list[str]


class Resource(BaseModel):
    name: str
    resource_type: str
    url: str
    purpose: str


class Milestone(BaseModel):
    title: str
    expected_outcome: str
    completion_criteria: list[str]


class LearningPhase(BaseModel):
    phase_number: int
    title: str
    duration_months: float
    objective: str
    topics: list[str]
    weekly_plan: list[WeeklyPlan]
    projects: list[Project]
    resources: list[Resource]
    milestones: list[Milestone]


class LearningRoadmap(BaseModel):
    roadmap_title: str
    field: str
    current_level: str
    target_level: str
    estimated_duration_months: int
    weekly_study_hours: int
    overview: str
    prerequisites: list[str]
    phases: list[LearningPhase]
    career_opportunities: list[str]
    final_recommendations: list[str]
