from inference_ram_plus import get_tags_single_image, get_tags_from_image_list
import os
import yaml
from openai import OpenAI

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

os.environ['OPENAI_API_KEY'] = config['openai_api_key']
client = OpenAI()

def check_screenshot(image_path):
    return False

async def aget_tags_image(image_path):
    return get_tags_single_image(image_path)

def get_tags_image(image_path):
    return get_tags_single_image(image_path)

def get_tags_image_list(image_list):
    return get_tags_from_image_list(image_list)

def get_face_ids(image_path):
    return []

def get_summary(image_tags):
    tag_string = ', '.join(image_tags)
    prompt = f"An image has been described through tags, these are the tags used: {tag_string}. String these tags together into a full English description of the image, do not make up any details not described by those tags. Do not try to describe how the image feels."

    response = client.chat.completions.create(
        model = "gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are ImageCaptionGPT"},
            {"role": "user", "content": f"{prompt}"}
        ]
    )

    print(response)
    caption = response.choices[0].message.content
    return caption