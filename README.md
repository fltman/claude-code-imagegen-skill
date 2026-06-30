# Gemini Image Generation Skill for Claude Code

[![Support me on Patreon](https://img.shields.io/badge/Patreon-Support%20my%20work-FF424D?style=flat&logo=patreon&logoColor=white)](https://www.patreon.com/AndersBjarby)

A Claude Code skill and subagent for generating AI images with Google's Gemini model via the OpenRouter API. Supports both text-to-image and image-to-image (style transfer, editing, variations).

## What it does

- **`gemini-imagegen` skill** — wraps a Python script that calls Gemini through OpenRouter to create or transform images.
- **`image-creator` agent** — a subagent for image-generation tasks that uses the skill.

## Setup

Install dependencies and set your API key:

```bash
pip install openai python-dotenv
export OPENROUTER_API_KEY="your-openrouter-api-key"   # get one at https://openrouter.ai/keys
```

## Usage

Text-to-image:

```bash
python skills/gemini-imagegen/scripts/generate_image.py \
  --prompt "A serene Japanese garden with cherry blossoms" --output garden.png
```

Image-to-image:

```bash
python skills/gemini-imagegen/scripts/generate_image.py \
  --input photo.jpg --prompt "Transform into a watercolor painting style" --output watercolor.png
```

Arguments: `--prompt/-p` (required), `--output/-o`, `--input/-i`, `--model/-m` (default `google/gemini-3-pro-image-preview`).

To use it inside Claude Code, copy `skills/gemini-imagegen/` into `~/.claude/skills/` and `agents/image-creator.md` into `~/.claude/agents/`.

## Tech

Python (`openai` SDK pointed at OpenRouter) + Claude Code skill/subagent definitions.
