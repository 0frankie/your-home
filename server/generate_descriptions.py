from google.genai import Client, types
import os
import random

# Initialize Gemini (Gen AI client)
client = Client()  # set up auth etc according to Google Gen AI

IMAGE_DIR = "./images"
OUTPUT_PATH = "gemini_image_captions.json"

def caption_image(image_path: str) -> str:
    # read the image bytes
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # send prompt + image to Gemini
    resp = client.models.generate_content(
        model="gemini-2.5-flash",  # choose appropriate Gemini model
        contents=[
            types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"),
            "Describe the room using format: Style, color scheme, layout, materials, lighting, and decor. Keep the description 1 short phrase, with a delimiter in between each aspect. For example: 'modern | bright white | with a canopy bed | natural wood accents | warm ambient lighting | indoor plants'"
        ]
    )
    # The model’s response text should be your standardized caption
    return resp.text.strip()

def process_directory():
    results = []
    i = 0
    index = random.randint(0, len(os.listdir(IMAGE_DIR)) - 1)
    for fname in os.listdir(IMAGE_DIR):
        if i < 13:
            i += 1
            print("Skipping", fname)
            continue
        if fname.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
            path = os.path.join(IMAGE_DIR, fname)
            print("Processing", fname)
            caption = caption_image(path)
            results.append({"filename": fname, "caption": caption})
            print("Caption:", caption)
            i += 1
            print(i)
        
        if i >= 10:  # limit to first 100 images for demo
            break
    return results

if __name__ == "__main__":
    data = process_directory()
    import json
    with open(OUTPUT_PATH, "w") as f:
        json.dump(data, f, indent=2)
    print("Done. Captions saved to", OUTPUT_PATH)
