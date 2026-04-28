async def handle_task(request) -> str:
    text_parts = [p.text for p in request.message.parts if p.type == "text"]
    combined = ' '.join(text_parts).strip()

    if combined.lower().startswith("!summarise"):
        return "This is a short summary of the provided text."
    return combined
