# server/agent_card.py

AGENT_CARD = {
    "id": "echo-agent-v1",
    "name": "Echo Agent",
    "version": "1.0.0",
    "description": "A simple agent that echoes back any text it receives.",
    "url": "https://echo-a2a-agent-741297514794.us-central1.run.app",
    "capabilities": {
        "streaming": False,
        "pushNotifications": False
    },
    "defaultInputModes": ["text/plain"],
    "defaultOutputModes": ["text/plain"],
    "contact": {
        "email": "your_email@example.com"
    },
    "skills": [
        {
            "id": "echo",
            "name": "Echo",
            "description": "Returns the user message verbatim.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        },
        {
            "id": "summarise",
            "name": "Summarise",
            "description": "Returns a short one-sentence summary of the user message.",
            "inputModes": ["text/plain"],
            "outputModes": ["text/plain"],
        },
    ],
}


def validate_card(card: dict) -> bool:
    """
    Validate that an Agent Card contains all required top-level and skill fields.

    Required top-level fields:
    - id
    - name
    - version
    - description
    - url
    - capabilities
    - defaultInputModes
    - defaultOutputModes
    - contact
    - skills

    Required capabilities fields:
    - streaming
    - pushNotifications

    Required contact fields:
    - email

    Required skill fields for each skill:
    - id
    - name
    - description
    - inputModes
    - outputModes

    Returns:
        bool: True if all required fields are present, otherwise False.
    """
    required_fields = [
        "id",
        "name",
        "version",
        "description",
        "url",
        "capabilities",
        "defaultInputModes",
        "defaultOutputModes",
        "contact",
        "skills",
    ]

    for field in required_fields:
        if field not in card:
            return False

    if not isinstance(card["capabilities"], dict):
        return False

    required_capabilities = ["streaming", "pushNotifications"]
    for field in required_capabilities:
        if field not in card["capabilities"]:
            return False

    if not isinstance(card["contact"], dict):
        return False

    if "email" not in card["contact"]:
        return False

    if not isinstance(card["skills"], list) or len(card["skills"]) == 0:
        return False

    required_skill_fields = [
        "id",
        "name",
        "description",
        "inputModes",
        "outputModes",
    ]

    for skill in card["skills"]:
        if not isinstance(skill, dict):
            return False
        for field in required_skill_fields:
            if field not in skill:
                return False

    return True
