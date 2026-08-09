from app.services.llm import ask_llm_json


JOB_REQUIREMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "capabilities": {
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
                    "required": {
                        "type": "boolean",
                    },
                    "details": {
                        "type": "array",
                        "items": {"type": "string"},
                    },
                },
                "required": [
                    "category",
                    "required",
                    "details",
                ],
                "additionalProperties": False,
            },
        },
        "experience_requirement": {
            "type": "string",
        },
        "education_requirement": {
            "type": "string",
        },
    },
    "required": [
        "capabilities",
        "experience_requirement",
        "education_requirement",
    ],
    "additionalProperties": False,
}


def extract_job_requirements(
    job_description: str,
) -> dict:
    prompt = f"""
You are a precise job-requirement extraction system.

Map the job description into the fixed capability categories below.

Do not create new categories.
Do not split one capability into multiple scored requirements merely because
the job description names multiple tools or platforms.

Fixed capability categories:

1. ai_solution_development
   Designing or building AI solutions, agents, multi-step systems, or AI integrations.

2. agent_architecture_rag
   Agent architecture, RAG, retrieval strategies, grounding, context design,
   vector databases, or knowledge-base architecture.

3. ai_platform_administration
   AI platform configuration, administration, agent deployment, access controls,
   workspace organization, or platform management.

4. enterprise_integrations
   Integration with enterprise systems or named business platforms such as
   Salesforce, Totango, Jira, Redshift, Snowflake, or similar systems.

5. data_pipelines
   Data orchestration, ETL, field mapping, transformations, data quality,
   warehouse pipelines, or related data-flow responsibilities.

6. api_connectivity
   REST APIs, webhooks, custom connectors, integration frameworks,
   or custom connectivity development.

7. workflow_automation
   Workflow automation, orchestration, trigger logic, multi-step workflows,
   or business-process automation.

8. debugging
   Technical troubleshooting, debugging, root-cause analysis, log review,
   or hypothesis-driven technical problem solving.

9. monitoring_observability
   Monitoring, observability, metrics, logging, alerting,
   performance evaluation, or iterative improvement of deployed AI systems.

10. documentation_enablement
    SOPs, capability guides, enablement materials, training, demos,
    office hours, stakeholder support, or program-champion enablement.

Rules:

- Include each category at most once.
- Set required=true only when the job clearly expects that capability.
- Use details to preserve specific technologies, platforms, or sub-requirements.
- Multiple named tools within the same capability belong in the same details list.
- Do not infer capabilities unsupported by the job description.
- experience_requirement must contain only the professional experience requirement.
- education_requirement must contain only the education requirement.
- Use an empty string when no experience or education requirement exists.
- Do not place degree requirements inside capabilities.
- Do not place years-of-experience requirements inside capabilities.

Job Description:
{job_description}
"""

    return ask_llm_json(
        prompt=prompt,
        schema=JOB_REQUIREMENT_SCHEMA,
    )