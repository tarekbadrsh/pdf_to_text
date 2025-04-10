import logging
import os
from typing import Any, Dict, List

import pytesseract
from dotenv import load_dotenv
from groq import Groq
from pdf2image import convert_from_path
from PIL import Image

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


def ocr_image(image_path: str) -> str:
    """Perform OCR on the image and return the extracted text."""
    logger.info(f"Performing OCR on image: {image_path}")
    image = Image.open(image_path)
    return pytesseract.image_to_string(image)


def ai_read_image(image_path: str) -> str:
    """Use Groq to extract text from the image."""
    logger.info(f"Using AI to read image: {image_path}")
    prompt = """
    Convert the following page to markdown.
    Return only the markdown with no explanation text.
    Do not exclude any content from the page.
    """
    content = "Please read and transcribe the text in this image."
    return groq_completion(prepare_messages(prompt, content, image_path))


def prepare_messages(
    prompt: str, content: str, image_path: str = None
) -> List[Dict[str, Any]]:
    """Prepares the messages to send to the Groq API."""
    messages = [
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


def initial_markdown_conversion(text: str, image_path: str = None) -> str:
    """Perform initial markdown conversion using Groq."""
    logger.info("Performing initial markdown conversion")
    prompt = "Convert the following text to markdown format, preserving structure and formatting:"
    messages = prepare_messages(prompt, text, image_path)
    return groq_completion(messages)


def feedback_loop(original_text: str, markdown: str, image_path: str = None) -> str:
    """Implement feedback loop to refine markdown."""
    logger.info("Starting feedback loop")
    prompt = f"""
    Compare the original text with the markdown conversion.
    Identify any discrepancies in structure, formatting, or content.
    Provide specific feedback on how to improve the markdown.
    Original text:
    {original_text}

    Current markdown:
    {markdown}
    """
    messages = prepare_messages(prompt, "Provide feedback for improvement")
    feedback = groq_completion(messages)
    logger.info(f"Feedback received: {feedback[:100]}...")

    # Use the feedback to improve the markdown
    improve_prompt = f"""
    Using the following feedback, improve the markdown conversion:
    {feedback}

    Current markdown:
    {markdown}
    """
    messages = prepare_messages(
        improve_prompt, "Improve the markdown based on feedback", image_path
    )
    return groq_completion(messages)


def meta_reasoning(
    original_text: str, markdown_versions: List[str], image_path: str = None
) -> str:
    """Implement meta-reasoning to select the best markdown version."""
    logger.info("Performing meta-reasoning")
    versions_text = "\n\n".join(
        [f"Version {i + 1}:\n{version}" for i, version in enumerate(markdown_versions)]
    )
    prompt = f"""
    Compare the following markdown versions with the original text:

    Original text:
    {original_text}

    Markdown versions:
    {versions_text}

    Analyze each version for accuracy, completeness, and proper markdown formatting.
    Select the best version or combine the best elements from multiple versions.
    Provide your reasoning and the final, optimized markdown.
    """
    messages = prepare_messages(
        prompt, "Perform meta-reasoning and provide optimized markdown", image_path
    )
    return groq_completion(messages)


def create_final_version(optimized_markdown: str, image_path: str) -> str:
    """Create a final version that matches the original text more closely."""
    logger.info("Creating final version")
    prompt = f"""
    Based on the following optimized markdown, create a final version that matches the original page text as closely as possible.
    Remove any additional text or explanations that were added during the optimization process.
    Ensure that the final output is clean, properly formatted markdown that represents only the content from the original PDF.

    Optimized markdown:
    {optimized_markdown}
    ---
    REMEMBER: The final output should only be the markdown, That matches the original page text with no additional text or explanations.
    """
    messages = prepare_messages(prompt, "Create final version", image_path)
    return groq_completion(messages)


def process_page(image_path: str, output_path: str) -> str:
    """Process a single page of a PDF"""
    try:
        logger.info(f"Processing page: {image_path}")
        # Step 1: OCR and AI Image Reading
        ocr_text = ocr_image(image_path)

        # Combine the results
        combined_text = f"OCR Text:\n{ocr_text}"

        # Step 2: Initial Markdown Conversion
        initial_markdown = initial_markdown_conversion(combined_text, image_path)

        # Step 3: Chain of Feedback
        improved_markdown = initial_markdown
        for i in range(1):  # Perform feedback loop twice
            logger.info(f"Feedback loop iteration {i + 1}")
            improved_markdown = feedback_loop(combined_text, improved_markdown)

        # Step 4: Create Final Version
        final_version = create_final_version(improved_markdown, image_path)

        # Save the results
        with open(output_path, "w") as f:
            formatted_final_version = format_markdown(final_version)
            f.write(formatted_final_version)

        logger.info(f"Processing complete for {image_path}")
        return final_version

    except Exception as error:
        logger.error(f"Error processing {image_path}: {error}")
        return ""


def main():
    file_name = "file.pdf"
    data = "./data"
    file_path = "./file.pdf"
    images_path = f"{data}/{file_name.split('.')[0]}/images"
    markdowns_path = f"{data}/{file_name.split('.')[0]}/markdowns"
    os.makedirs(data, exist_ok=True)
    os.makedirs(images_path, exist_ok=True)
    os.makedirs(markdowns_path, exist_ok=True)
    logger.info(f"Starting processing of PDF: {file_path}")
    images = convert_from_path(file_path, output_folder=images_path)
    for i, image in enumerate(images):
        image_path = f"{images_path}/page_{i + 1}.png"
        image.save(image_path, "PNG")
        output_path = f"{markdowns_path}/page_{i + 1}.md"
        process_page(image_path, output_path)

    logger.info("PDF processing complete")


if __name__ == "__main__":
    main()
