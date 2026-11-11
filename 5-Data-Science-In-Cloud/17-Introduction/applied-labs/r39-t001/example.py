
"""Local educational example of a structural cloud-security rubric.

This is a simulation using fictional scenarios and keyword-based checks.
It does not connect to or assess real cloud infrastructure.
"""

import json


SCENARIOS = [
    {
        "name": "Cloud customer database",
        "asset": "Customer records stored in a cloud database",
        "threat": (
            "An unauthorized user accesses the database because "
            "it is publicly accessible"
        ),
        "control": (
            "Restrict database access using identity-based permissions "
            "and network access rules"
        ),
        "residual_risk": (
            "A compromised authorized account could still access "
            "permitted records"
        ),
    },
    {
        "name": "Cloud data processing",
        "asset": "",
        "threat": (
            "Unauthorized modification of datasets during cloud processing"
        ),
        "control": (
            "Use access restrictions and data integrity checks"
        ),
        "residual_risk": (
            "A compromised privileged account may still modify data"
        ),
    },
    {
        "name": "Real-time sentiment analysis",
        "asset": (
            "Streaming social media sentiment data and analysis results"
        ),
        "threat": (
            "Unauthorized access to the streaming service through "
            "exposed API credentials"
        ),
        "control": "Encrypt stored data",
        "residual_risk": (
            "Exposed credentials may still allow unauthorized access "
            "to the streaming service"
        ),
    },
]


# These keyword groups represent simple structural rubric rules.
THREAT_CATEGORIES = {
    "access": (
        "unauthorized access",
        "publicly accessible",
        "exposed api credentials",
    ),
    "integrity": (
        "unauthorized modification",
        "data tampering",
        "unauthorized alteration",
    ),
}

CONTROL_CATEGORIES = {
    "access": (
        "access restriction",
        "access control",
        "permissions",
        "network access",
        "authentication",
        "credential rotation",
    ),
    "integrity": (
        "integrity checks",
        "checksums",
        "versioning",
        "write permissions",
    ),
    "confidentiality": (
        "encryption",
        "encrypt",
    ),
}


def get_category(text, category_rules):
    """Identify categories using predefined keyword rules."""
    normalized_text = text.lower()

    for category, keywords in category_rules.items():
        if any(keyword in normalized_text for keyword in keywords):
            return category

    return None


def evaluate_scenario(scenario):
    """Check required fields and basic threat-control consistency.

    Returns PASS, FAIL, or REVIEW. Human review is still needed
    to judge the quality of the explanations.
    """
    required_fields = (
        "asset",
        "threat",
        "control",
        "residual_risk",
    )

    missing_fields = [
        field
        for field in required_fields
        if not isinstance(scenario.get(field), str)
        or not scenario[field].strip()
    ]

    if missing_fields:
        return {
            "scenario": scenario.get("name", "Unnamed scenario"),
            "status": "FAIL",
            "issues": [
                f"Missing or empty required field: {field}"
                for field in missing_fields
            ],
        }

    threat_category = get_category(
        scenario["threat"], THREAT_CATEGORIES
    )
    control_category = get_category(
        scenario["control"], CONTROL_CATEGORIES
    )

    if (
        threat_category is None
        or control_category is None
        or threat_category != control_category
    ):
        return {
            "scenario": scenario.get("name", "Unnamed scenario"),
            "status": "REVIEW",
            "issues": [
                "The control may not address the named threat. "
                "Human review is required."
            ],
        }

    return {
        "scenario": scenario.get("name", "Unnamed scenario"),
        "status": "PASS",
        "issues": [],
    }


def main():
    """Evaluate all fictional scenarios and print JSON results."""
    results = [
        evaluate_scenario(scenario)
        for scenario in SCENARIOS
    ]

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
