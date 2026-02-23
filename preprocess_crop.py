import os
import re

INPUT_FOLDER = "kb/kb_crop"
OUTPUT_FOLDER = "kb/kb_crop_clean"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def clean_text(text):
    # remove html tags
    text = re.sub(r"<.*?>", "", text)

    # remove markdown table rows
    text = re.sub(r"\|.*?\|", "", text)

    # remove headers
    text = re.sub(r"#+", "", text)

    # remove extra whitespace
    text = re.sub(r"\s+", " ", text)

    return text.strip()

for file in os.listdir(INPUT_FOLDER):
    if file.endswith(".md"):
        with open(os.path.join(INPUT_FOLDER, file), "r", encoding="utf-8") as f:
            raw = f.read()

        cleaned = clean_text(raw)

        with open(os.path.join(OUTPUT_FOLDER, file), "w", encoding="utf-8") as f:
            f.write(cleaned)

print("✅ Crop KB cleaned successfully!")
