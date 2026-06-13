"""Superhero Resume Builder.

A small Gradio app that uses Groq's chat completions API to generate a witty,
LinkedIn-style parody resume for a superhero based on their name and superpower.
"""

import os

import gradio as gr
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
MODERATION_MODEL = os.environ.get("GROQ_MODERATION_MODEL", "openai/gpt-oss-safeguard-20b")

SYSTEM_PROMPT = (
    "You are a witty career coach who writes short, funny, LinkedIn-style "
    "parody resumes for superheroes. Keep it professional in tone but "
    "clearly humorous. Use clear sections: Headline, Summary, Core "
    "Superpowers, Experience, Education, and Skills. Keep it concise.\n"
    "Content policy: keep everything PG-13 and good-natured. Cartoonish, "
    "fictional villainy (world domination, chaos, doomsday devices) is fine, "
    "but never produce hate speech or slurs, insults aimed at real people, "
    "sexual content, profanity, or anything that encourages or glorifies "
    "self-harm, suicide, or real-world violence and cruelty. If the requested "
    "hero or superpower would require such content, instead write a clean, "
    "lighthearted parody resume that avoids the harmful theme."
)

MODERATION_POLICY = (
    "You are a content safety classifier. Decide if the TEXT is unsafe.\n"
    "UNSAFE = contains or glorifies any of: hate speech or slurs, harassment "
    "or insults toward a person, self-harm or suicide encouragement, sexual "
    "content, or graphic real-world violence or cruelty.\n"
    "SAFE = lighthearted superhero parody, including cartoonish fictional "
    "villainy (world domination, chaos) WITHOUT real-world hate, slurs, "
    "sexual content, self-harm, or graphic cruelty.\n"
    "Reply with exactly one word: SAFE or UNSAFE."
)

REFUSAL_MESSAGE = (
    "Sorry — I can only build lighthearted, family-friendly superhero resumes. "
    "That request leads to content I can't generate. Try a fun hero name and "
    "superpower instead!"
)


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file (see .env.example) "
            "or export the variable before running the app."
        )
    return Groq(api_key=api_key)


def _is_unsafe(client: Groq, text: str) -> bool:
    """Return True if `text` violates the content policy.

    Uses a Groq safety classifier. On any classifier error we fail closed
    (treat the content as unsafe) so harmful output is never shown.
    """
    try:
        result = client.chat.completions.create(
            model=MODERATION_MODEL,
            messages=[
                {"role": "system", "content": MODERATION_POLICY},
                {"role": "user", "content": text},
            ],
            temperature=0,
            max_tokens=2000,
        )
        verdict = (result.choices[0].message.content or "").strip().upper()
        return "UNSAFE" in verdict
    except Exception:
        return True


def build_resume(hero_name: str, superpower: str) -> str:
    """Generate a parody resume for the given hero and superpower."""
    hero_name = (hero_name or "").strip()
    superpower = (superpower or "").strip()
    if not hero_name or not superpower:
        return "Please enter both a hero name and a superpower."

    client = _get_client()

    if _is_unsafe(client, f"Hero name: {hero_name}\nSuperpower: {superpower}"):
        return REFUSAL_MESSAGE

    user_prompt = (
        f"Write a parody LinkedIn-style resume for the superhero "
        f'"{hero_name}" whose main superpower is "{superpower}".'
    )

    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.8,
        max_tokens=800,
    )
    resume = completion.choices[0].message.content

    if _is_unsafe(client, resume):
        return REFUSAL_MESSAGE

    return resume


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="Superhero Resume Builder") as demo:
        gr.Markdown(
            "# 🦸 Superhero Resume Builder\n"
            "Enter a hero name and superpower to generate a witty, "
            "LinkedIn-style parody resume."
        )
        with gr.Row():
            hero_name = gr.Textbox(label="Hero name", placeholder="e.g. Captain Caffeine")
            superpower = gr.Textbox(label="Superpower", placeholder="e.g. infinite energy at 3am")
        generate_btn = gr.Button("Generate resume", variant="primary")
        output = gr.Markdown(label="Resume")

        generate_btn.click(fn=build_resume, inputs=[hero_name, superpower], outputs=output)
        hero_name.submit(fn=build_resume, inputs=[hero_name, superpower], outputs=output)
        superpower.submit(fn=build_resume, inputs=[hero_name, superpower], outputs=output)

    return demo


if __name__ == "__main__":
    build_ui().launch()
