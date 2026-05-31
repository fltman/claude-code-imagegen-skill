#!/usr/bin/env python3
"""
Generate images using Google Gemini via Google AI Studio.
Supports both text-to-image and image-to-image generation.
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: google-genai package not installed. Run: pip install google-genai")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv is optional

MODEL = "gemini-2.0-flash-preview-image-generation"


def get_client():
    """Initialize Google AI Studio client."""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY environment variable not set.")
        print("Set it with: export GOOGLE_API_KEY='your-key-here'")
        sys.exit(1)
    return genai.Client(api_key=api_key)


def get_image_mime_type(image_path: str) -> str:
    """Get MIME type based on file extension."""
    ext = Path(image_path).suffix.lower()
    mime_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return mime_types.get(ext, "image/jpeg")


def save_image(image_bytes: bytes, output_path: str) -> bool:
    """Save raw image bytes to a file."""
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(image_bytes)
    print(f"SUCCESS: Image saved to {output_path}")
    return True


def generate_from_text(prompt: str, output_path: str) -> bool:
    """Generate an image from a text prompt."""
    client = get_client()
    print(f"Generating image from prompt: {prompt[:100]}...")

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    return extract_and_save_image(response, output_path)


def generate_from_image(input_image: str, prompt: str, output_path: str) -> bool:
    """Generate an image based on an input image and prompt."""
    if not os.path.exists(input_image):
        print(f"ERROR: Input image not found: {input_image}")
        return False

    print(f"Generating image from: {input_image}")
    print(f"Prompt: {prompt[:100]}...")

    mime_type = get_image_mime_type(input_image)
    with open(input_image, "rb") as f:
        image_bytes = f.read()

    client = get_client()
    response = client.models.generate_content(
        model=MODEL,
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type=mime_type),
            types.Part.from_text(text=prompt),
        ],
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"]
        ),
    )

    return extract_and_save_image(response, output_path)


def extract_and_save_image(response, output_path: str) -> bool:
    """Extract image from API response and save to file."""
    if not response.candidates:
        print("ERROR: No response received from API")
        return False

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            return save_image(part.inline_data.data, output_path)
        if part.text:
            print(f"Model response: {part.text}")

    print("ERROR: No images found in response")
    return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate images using Google Gemini via Google AI Studio",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Text-to-image:
  python generate_image.py --prompt "A sunset over mountains" --output sunset.png

  # Image-to-image:
  python generate_image.py --input photo.jpg --prompt "Make it look like a watercolor painting" --output watercolor.png

Environment:
  GOOGLE_API_KEY  Your Google AI Studio API key (required)
        """
    )

    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Text prompt describing the image to generate"
    )
    parser.add_argument(
        "--output", "-o",
        default="generated_image.png",
        help="Output file path (default: generated_image.png)"
    )
    parser.add_argument(
        "--input", "-i",
        help="Optional input image for image-to-image generation"
    )

    args = parser.parse_args()

    if args.input:
        success = generate_from_image(args.input, args.prompt, args.output)
    else:
        success = generate_from_text(args.prompt, args.output)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
