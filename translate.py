import logging
import os
from typing import Any, Dict, List

from dotenv import load_dotenv
from groq import Groq

from processor.image import encode_image_to_base64
from processor.text import format_markdown

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

###################### Groq ######################
groq_model = "meta-llama/llama-4-maverick-17b-128e-instruct"
groq_api_key = os.environ.get("GROQ_API_KEY")


def prepare_messages(
    prompt: str, content: str, image_path: str
) -> List[Dict[str, Any]]:
    """Prepares the messages to send to the Groq API."""
    messages = [
        {
            "role": "system",
            "content": """You are a professional translator.
            **Translator Instructions**
            - Translate the given content into the target language
            - Return **only the translated text**; avoid additional explanations
            - Ensure translations are accurate and _precisely match_ the source content's intent
            - **Do not** engage in dialogue or answer user queries—your sole role is to translate
            - Maintain strict adherence to formatting (e.g., preserve **bold**, *italics* ... etc).
            > *Note:* All responses should focus exclusively on translation quality without deviations.""",
        },
        {"role": "user", "content": prompt},
        {"role": "user", "content": content},
    ]
    if image_path:
        base64_image = encode_image_to_base64(image_path)
        messages.append(
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    }
                ],
            }
        )
    return messages


def groq_completion(messages: List[Dict[str, Any]]) -> str:
    """Get completion from Groq API."""
    logger.info("Sending request to Groq API")
    groq = Groq(api_key=groq_api_key)
    completion = groq.chat.completions.create(
        model=groq_model,
        messages=messages,
        max_tokens=8192,
    )
    return completion.choices[0].message.content


def translate_text(text: str, image_path: str, target_language: str) -> str:
    """Translate text using Groq AI."""
    prompt = f"Translate the following text to {target_language}, preserving all formatting and structure"
    messages = prepare_messages(prompt, text, image_path)
    return groq_completion(messages)


def process_content(
    text_file_path: str, image_file_path: str, output_path: str, target_language: str
) -> str:
    """Process content (text or image) and translate to target language"""
    try:
        logger.info(f"Processing content: {text_file_path}")

        # For text files, read the content first
        with open(text_file_path, "r") as f:
            content = f.read()
        translated_content = translate_text(content, image_file_path, target_language)

        # Save the results
        with open(output_path, "w") as f:
            formatted_content = format_markdown(translated_content)
            f.write(formatted_content)

        logger.info(f"Translation complete for {text_file_path}")
        return translated_content

    except Exception as error:
        logger.error(f"Error processing {text_file_path}: {error}")
        return ""


def main():
    # Configuration options
    file_name = "file.pdf"
    data = "./data"
    text_input_dir = f"{data}/{file_name.split('.')[0]}/markdowns"  # Directory containing files to translate
    image_input_dir = f"{data}/{file_name.split('.')[0]}/images"  # Directory containing files to translate
    translations_dir = f"{data}/{file_name.split('.')[0]}/translations"  # Directory for translated output
    target_language = "English"  # Target language for translation

    # Ensure directories exist
    os.makedirs(translations_dir, exist_ok=True)

    # Process all files in the input directory
    for filename in os.listdir(text_input_dir):
        page_number = filename.split("_")[1].split(".")[0]
        logger.info(f"Starting translation page {page_number}")
        text_file_path = os.path.join(text_input_dir, filename)
        image_file_name = filename.replace(".md", ".png")
        image_file_path = os.path.join(image_input_dir, image_file_name)
        # Skip directories
        if os.path.isdir(text_file_path):
            continue

        # Create output filename
        output_path = f"{translations_dir}/page_{page_number}.md"

        # Process the file
        process_content(text_file_path, image_file_path, output_path, target_language)

    logger.info("Translation process complete")


if __name__ == "__main__":
    main()
