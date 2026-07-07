# Build prompt for the LLM


def build_prompt(
    messages,
    context,
    question
):

    conversation = ""

    for message in messages:

        role = message["role"].capitalize()

        conversation += (
            f"{role}: {message['content']}\n"
        )

    prompt = f"""
========================
SYSTEM
========================

You are Lumina AI.

Answer ONLY using the provided context.

If the answer is not present in the context,
reply with:

"I couldn't find this information in the uploaded knowledge."

Always explain clearly.

========================
CONVERSATION
========================

{conversation}

========================
CONTEXT
========================

{context}

========================
QUESTION
========================

{question}

========================
ANSWER
========================
"""

    return prompt