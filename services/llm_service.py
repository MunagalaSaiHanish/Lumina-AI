import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from services.prompt_builder import build_prompt

# ---------------------------------------------------------
# Load Environment Variables
# ---------------------------------------------------------

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "qwen/qwen3-32b"

# ---------------------------------------------------------
# Generate Summary
# ---------------------------------------------------------

def summarize(text):

    prompt = f"""
You are an expert AI assistant.

Generate a professional summary of the following content.

Requirements:

- Clear
- Concise
- Easy to understand
- Preserve important concepts

Content:

{text}
"""

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0.3,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content


# ---------------------------------------------------------
# Generate Key Takeaways & Topics
# ---------------------------------------------------------

def generate_insights(summary):

    prompt = f"""
Read the following summary.

Return ONLY valid JSON.

Format:

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

Summary:

{summary}
"""

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0.2,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    content = response.choices[0].message.content.strip()

    if content.startswith("```"):

        content = (
            content
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

    try:

        return json.loads(content)

    except Exception:

        return {

            "takeaways": [],

            "topics": []

        }


# ---------------------------------------------------------
# Ask Question
# ---------------------------------------------------------

def ask_question(

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

    response = client.chat.completions.create(

        model=MODEL,

        temperature=0.2,

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]

    )

    return response.choices[0].message.content