# 🦸 Superhero Resume Builder

A fun Python + Gradio + Groq project that generates witty LinkedIn-style resumes for superheroes.

## Features
- Enter a hero name + superpower
- Generates a professional parody resume
- Built with Gradio UI + Groq backend

## Setup

1. Clone the repo:
   ```
   git clone https://github.com/Maheshopt/superhero-resume-builder.git
   cd superhero-resume-builder
   ```

2. (Optional but recommended) create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Add your Groq API key. Copy `.env.example` to `.env` and fill it in:
   ```
   cp .env.example .env
   ```
   Then edit `.env`:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```
   Get a free key at https://console.groq.com/keys

## Run

```
python app.py
```

Gradio will print a local URL (e.g. http://127.0.0.1:7860). Open it in your browser, enter a hero name and superpower, and click **Generate resume**.

## Configuration

- `GROQ_API_KEY` (required): your Groq API key.
- `GROQ_MODEL` (optional): the Groq model to use. Defaults to `llama-3.3-70b-versatile`.
