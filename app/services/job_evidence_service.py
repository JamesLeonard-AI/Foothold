from app.services.llm import ask_llm_json


EVIDENCE_SCHEMA = {
    "type": "object",
    "properties": {
        "capability_results": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "enum": [
                            "ai_solution_development",
                            "agent_architecture_rag",
                            "ai_platform_administration",
                            "enterprise_integrations",
                            "data_pipelines",
                            "api_connectivity",
                            "workflow_automation",
                            "debugging",
                            "monitoring_observability",
                            "documentation_enablement",
                        ],
                    },
                    "status": {
                        "type": "string",
                        "enum": [
                            "matched",
                            "partial",
                            "not_matched",
                        ],
                    },
                    "evidence": {
                        "type": "string",
                    },
                },
                "required": [
                    "category",
                    "status",
                    "evidence",
                ],
                "additionalProperties": False,
            },
        },
        "experience_status": {
            "type": "string",
            "enum": [
                "matched",
                "partial",
                "not_matched",
                "not_required",
            ],
        },
        "experience_evidence": {
            "type": "string",
        },
        "education_status": {
            "type": "string",
            "enum": [
                "matched",
                "equivalent",
                "not_matched",
                "not_required",
            ],
        },
        "education_evidence": {
            "type": "string",
        },
    },
    "required": [
        "capability_results",
        "experience_status",
        "experience_evidence",
        "education_status",
        "education_evidence",
    ],
    "additionalProperties": False,
}


def evaluate_resume_evidence(
    resume_analysis: dict,
    job_requirements: dict,
) -> dict:
    required_capabilities = [
        capability
        for capability in job_requirements["capabilities"]
        if capability["required"]
    ]

    prompt = f"""
You are a strict resume-evidence evaluator.

Evaluate the candidate only against the supplied canonical job capabilities.

Do not create, remove, split, merge, rename, or reclassify capabilities.

For every supplied capability, return exactly one capability result.

Status rules:

matched:
The resume contains clear and direct evidence that the candidate satisfies
the overall capability.

partial:
The resume contains meaningful related evidence, but does not fully satisfy
the capability or important details are missing.

not_matched:
The resume contains insufficient evidence for the capability.

Evidence rules:

- Evaluate the overall capability, not each named technology as a separate score.
- Use the details list to judge the depth and completeness of the match.
- Missing a specifically named platform may prevent a full match when that
  platform is central to the requirement.
- Related technologies may support a partial match, but do not automatically
  count as a full match.
- Professional experience requirements must be supported by the
  professional_experience section.
- Projects, certifications, coursework, education, or skills marked as learning
  do not count as professional employment.
- Technical capabilities may be supported by meaningful evidence from
  professional experience, projects, skills, or certifications.
- Do not assume experience that is not explicitly supported by the resume.
- In-progress projects may demonstrate technical capability but do not prove
  production deployment experience.
- Monitoring or observability requires evidence of logs, metrics, monitoring,
  alerting, or performance evaluation. General testing or quality-review logic
  alone is not sufficient for a full match.
- Enterprise integration experience requires evidence of integration work.
  General API knowledge alone is not sufficient for a full match when the job
  specifically expects enterprise platform integration.
- Keep evidence explanations concise and factual.

Experience:
- Return "not_required" if experience_requirement is empty.
- Return "matched" only when professional experience clearly satisfies it.
- Return "partial" when professional experience is meaningfully related but
  does not fully satisfy it.
- Otherwise return "not_matched".

Education:
- Return "not_required" if education_requirement is empty.
- Return "matched" if the resume directly satisfies it.
- Return "equivalent" only when the job explicitly allows equivalent experience
  and the professional resume evidence reasonably supports equivalency.
- Otherwise return "not_matched".

Resume Analysis:
{resume_analysis}

Required Capabilities:
{required_capabilities}

Experience Requirement:
{job_requirements["experience_requirement"]}

Education Requirement:
{job_requirements["education_requirement"]}
"""

    return ask_llm_json(
        prompt=prompt,
        schema=EVIDENCE_SCHEMA,
    )