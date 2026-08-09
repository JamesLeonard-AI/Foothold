def _status_score(status: str) -> float:
    scores = {
        "matched": 1.0,
        "partial": 0.5,
        "not_matched": 0.0,
    }

    return scores.get(status, 0.0)


def calculate_job_match_score(
    capability_results: list[dict],
    experience_status: str,
    education_status: str,
) -> int:
    category_scores = {}
    category_weights = {}

    # Canonical technical capabilities = 60%
    if capability_results:
        capability_points = sum(
            _status_score(result["status"])
            for result in capability_results
        )

        category_scores["capabilities"] = (
            capability_points / len(capability_results)
        ) * 100

        category_weights["capabilities"] = 0.60

    # Professional experience = 30%
    if experience_status != "not_required":
        category_scores["experience"] = (
            _status_score(experience_status) * 100
        )

        category_weights["experience"] = 0.30

    # Education = 10%
    if education_status != "not_required":
        education_scores = {
            "matched": 100,
            "equivalent": 60,
            "not_matched": 0,
        }

        category_scores["education"] = education_scores.get(
            education_status,
            0,
        )

        category_weights["education"] = 0.10

    total_weight = sum(category_weights.values())

    if total_weight == 0:
        return 0

    weighted_score = sum(
        category_scores[category] * weight
        for category, weight in category_weights.items()
    )

    normalized_score = weighted_score / total_weight

    return round(normalized_score)