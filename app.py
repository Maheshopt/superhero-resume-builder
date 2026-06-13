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

SYSTEM_PROMPT = (
    "You are a witty career coach who writes short, funny, LinkedIn-style "
    "parody resumes for superheroes. Keep it professional in tone but "
    "clearly humorous. Use clear sections: Headline, Summary, Core "
    "Superpowers, Experience, Education, and Skills. Keep it concise."
)


def _get_client() -> Groq:
    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not set. Create a .env file (see .env.example) "
            "or export the variable before running the app."
        )
    return Groq(api_key=api_key)


def build_resume(hero_name: str, superpower: str) -> str:
    """Generate a parody resume for the given hero and superpower."""
    hero_name = (hero_name or "").strip()
    superpower = (superpower or "").strip()
    if not hero_name or not superpower:
        return "Please enter both a hero name and a superpower."

    client = _get_client()
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
    return completion.choices[0].message.content


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
