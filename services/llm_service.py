import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from services.prompt_builder import build_prompt

# ---------------------------------------------------------
# Environment
# ---------------------------------------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    timeout=200
)

MODEL = os.getenv(
    "OPENROUTER_MODEL",
    "qwen/qwen3-32b"
)

SYSTEM_PROMPT = """
You are Lumixa AI.

You are an intelligent Knowledge Assistant.

Rules:

- Answer only using the provided context.
- If the answer is not present, clearly say that you couldn't find it.
- Never hallucinate facts.
- Be concise and professional.
- When possible, organize answers using bullet points.
"""

# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

def stream_llm_response(messages, temperature=0.3):
    """
    Unified reusable streaming utility for all LLM generations in Lumixa AI.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            temperature=temperature,
            messages=messages,
            stream=True
        )
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
    except Exception as e:
        yield f"Sorry, I encountered an error during generation: {e}"


# ---------------------------------------------------------
# Summary
# ---------------------------------------------------------

def summarize_stream(text):
    # Truncate text if it is extremely long to prevent context-limit or timeout errors
    words = text.split()
    if len(words) > 12000:
        text = " ".join(words[:12000]) + "\n\n[Content truncated for summary due to length limits]"

    prompt = f"""
You are Lumixa AI.

Create a Summary of the following content.
Summarize the context in detail
Try to give more summary as much as possible
Generate a comprehensive summary while preserving all important concepts and details.
Instructions:

- Cover ALL major concepts.
- Do NOT skip important sections.
- Preserve the chronological flow whenever possible.
- Explain technical concepts clearly.
- Include important examples mentioned.
- Mention definitions when introduced.
- Keep important numbers, statistics and facts.
- Organize the summary into meaningful headings.
- Use bullet points where appropriate.
- Write in professional documentation style.
- The summary should be detailed rather than short.
- If the content is long, the summary should also be long.
- Never intentionally shorten the content.

Content:

{text}
"""
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    return stream_llm_response(messages, temperature=0.3)


def summarize(text):
    return "".join(list(summarize_stream(text)))


# ---------------------------------------------------------
# Insights
# ---------------------------------------------------------

def generate_insights(summary):
    prompt = f"""
Return ONLY valid JSON.

Schema

{{
    "takeaways":[
        "...",
        "...",
        "...",
        "...",
        "..."
    ],
    "topics":[
        "...",
        "...",
        "...",
        "...",
        "..."
    ]
}}

Do not include markdown.

Summary

{summary}
"""
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    try:
        content = "".join(list(stream_llm_response(messages, temperature=0.2))).strip()
        if content.startswith("```"):
            content = (
                content
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )
        return json.loads(content)
    except Exception:
        return {
            "takeaways": [],
            "topics": []
        }


# ---------------------------------------------------------
# Chat
# ---------------------------------------------------------

def ask_question_stream(
    question,
    context,
    messages=None
):
    if messages is None:
        messages = []

    prompt = build_prompt(
        messages=messages,
        context=context,
        question=question
    )

    api_messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": prompt
        }
    ]
    return stream_llm_response(api_messages, temperature=0.2)


def ask_question(
    question,
    context,
    messages=None
):
    return "".join(list(ask_question_stream(question, context, messages)))