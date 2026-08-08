from typing import Any


def score_skills(skills: list[str]) -> tuple[int, str]:
    count = len(skills)

    if count >= 20:
        return 85, "Strong technical breadth, but relevance and depth still need review."

    if count >= 12:
        return 75, "Good skill coverage with room for more role-specific depth."

    if count >= 6:
        return 65, "Moderate skill coverage; more targeted technical skills would help."

    return 45, "The resume lists too few clearly identifiable skills."


def score_projects(projects: list[dict[str, Any]]) -> tuple[int, str]:
    if not projects:
        return 35, "No project section was identified."

    score = 55 + min(len(projects) * 10, 20)

    has_technologies = any(
        project.get("technologies")
        for project in projects
    )

    has_descriptions = any(
        project.get("description")
        for project in projects
    )

    if has_technologies:
        score += 10

    if has_descriptions:
        score += 10

    return min(score, 90), (
        "Projects are relevant and technically described, but deployment, "
        "testing, links, and measurable outcomes are not yet evaluated."
    )


def score_certifications(
    certifications: list[str],
) -> tuple[int, str]:
    count = len(certifications)

    if count >= 5:
        return 88, "Strong certification coverage supporting the target field."

    if count >= 3:
        return 78, "Good certification coverage with clear professional relevance."

    if count >= 1:
        return 65, "Some certification evidence is present."

    return 40, "No certifications were identified."


def score_experience(
    experience: list[dict[str, Any]],
) -> tuple[int, str]:
    if not experience:
        return 35, "No professional experience was identified."

    responsibilities = [
        responsibility
        for job in experience
        for responsibility in job.get("responsibilities", [])
    ]

    quantified = sum(
        any(character.isdigit() for character in item)
        for item in responsibilities
    )

    score = 55 + min(len(experience) * 8, 24)

    if quantified >= 2:
        score += 12
        reason = (
            "Professional experience is established and includes multiple "
            "quantified accomplishments."
        )
    elif quantified == 1:
        score += 6
        reason = (
            "Professional experience is established, but more accomplishments "
            "should be quantified."
        )
    else:
        reason = (
            "Professional experience is established, but the impact statements "
            "need more measurable results."
        )

    return min(score, 92), reason


def score_education(
    education: list[dict[str, Any]],
) -> tuple[int, str]:
    if education:
        return 80, "Education is clearly documented."

    return 45, "No education section was identified."


def calculate_overall_score(categories: dict[str, int]) -> int:
    weighted_score = (
        categories["skills"] * 0.25
        + categories["experience"] * 0.30
        + categories["projects"] * 0.20
        + categories["certifications"] * 0.15
        + categories["education"] * 0.10
    )

    return round(weighted_score)


def calculate_ats_score(analysis: dict) -> dict:
    skills = analysis.get("skills") or []
    projects = analysis.get("projects") or []
    certifications = analysis.get("certifications") or []
    experience = analysis.get("professional_experience") or []
    education = analysis.get("education") or []

    skills_score, skills_reason = score_skills(skills)
    projects_score, projects_reason = score_projects(projects)
    certifications_score, certifications_reason = score_certifications(
        certifications
    )
    experience_score, experience_reason = score_experience(experience)
    education_score, education_reason = score_education(education)

    categories = {
        "skills": skills_score,
        "experience": experience_score,
        "projects": projects_score,
        "certifications": certifications_score,
        "education": education_score,
    }

    reasons = {
        "skills": skills_reason,
        "experience": experience_reason,
        "projects": projects_reason,
        "certifications": certifications_reason,
        "education": education_reason,
    }

    strengths = [
        reason
        for category, reason in reasons.items()
        if categories[category] >= 80
    ]

    improvements = [
        reason
        for category, reason in reasons.items()
        if categories[category] < 80
    ]

    return {
        "overall_score": calculate_overall_score(categories),
        "categories": categories,
        "reasons": reasons,
        "strengths": strengths,
        "improvements": improvements,
    }