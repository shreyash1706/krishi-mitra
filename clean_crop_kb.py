import os
import re

INPUT_FOLDER = "kb/kb_crop"
OUTPUT_FOLDER = "kb/kb_crop_clean"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_markdown(text):

    # Remove HTML tags
    text = re.sub(r"<.*?>", " ", text)

    # Remove table separators and junk characters
    text = re.sub(r"\|", " ", text)

    # Remove multiple hashes like ##
    text = re.sub(r"#{2,}", "\n", text)

    # Remove repeated blank lines
    text = re.sub(r"\n\s*\n", "\n\n", text)

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".md"):

        with open(os.path.join(INPUT_FOLDER, file), "r", encoding="utf-8") as f:
            content = f.read()

        cleaned = clean_markdown(content)

        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as f:
            f.write(cleaned)

print("✅ All crop markdown files cleaned successfully!")
