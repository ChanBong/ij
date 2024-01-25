import subprocess
import json
from structure import EXIFImageMetadata, PhotoInfo
import yaml
import asyncio
from inference import get_tags_image, check_screenshot, get_face_ids, get_summary, get_tags_image_list
from database import add_photo_data, get_photo_data, photo_path_exists
from typing import List


async def aget_image_metadata(image_path):
    try:
        # Run exiftool command and capture its output as a JSON string
        result = subprocess.run(['exiftool', '-json', image_path], capture_output=True, text=True, check=True)

        # Parse the JSON string to a Python dictionary
        metadata_json = result.stdout
        metadata_dict = json.loads(metadata_json)

        metadata = EXIFImageMetadata(**metadata_dict[0])
        return metadata.__dict__

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
    
def get_image_metadata(image_path):
    try:
        # Run exiftool command and capture its output as a JSON string
        result = subprocess.run(['exiftool', '-json', image_path], capture_output=True, text=True, check=True)

        # Parse the JSON string to a Python dictionary
        metadata_json = result.stdout
        metadata_dict = json.loads(metadata_json)

        metadata = EXIFImageMetadata(**metadata_dict[0])
        return metadata.__dict__

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

def get_image_thumbnail(image_path):
    return "NOT IMPLEMENTED"

async def aprocess_image(image_path, injestion = True) -> PhotoInfo:

    if photo_path_exists(image_path):
        if injestion == True:
            print(f"Photo {image_path} already exists in the database. Skipping...")
            return None
        elif injestion == False:
            print(f"Since you asked to see the photo data, here it is:")
            return PhotoInfo(**get_photo_data(image_path))
    
    metadata_task = get_image_metadata(image_path)
    thumbnail_path = get_image_thumbnail(image_path)
    is_screenshot = check_screenshot(image_path)
    face_ids = get_face_ids(image_path)
    tags_task = get_tags_image(image_path)

    metadata_result = await metadata_task
    tags_result = await tags_task

    summary = get_summary(tags_result)

    photo_info = PhotoInfo(
        photo_path = image_path,
        thumbnail_photo_path=thumbnail_path,
        is_screenshot=is_screenshot,
        tags=tags_result,
        face_ids=face_ids,
        metadata_fields=metadata_result,
        summary=summary,
        part_of_which_album=[]
    )

    add_photo_data(photo_info.__dict__)

    return photo_info

def process_image(image_path, injestion = True, image_tags_dict = None) -> PhotoInfo:

    if photo_path_exists(image_path) and injestion == False:
        print(f"Photo {image_path} already exists in the database. Using cache values...")
        return PhotoInfo(**get_photo_data(image_path))
    elif photo_path_exists(image_path) and injestion == True:
        print(f"Photo {image_path} already exists in the database. Skipping...")
        return None
    
    print(f"Processing {image_path}...")
    print(f"Getting metadata...")
    metadata_result = get_image_metadata(image_path)
    thumbnail_path = get_image_thumbnail(image_path)
    is_screenshot = check_screenshot(image_path)
    face_ids = get_face_ids(image_path)
    print(f"Getting tags...")
    if image_tags_dict:
        tags_result = image_tags_dict[image_path]
    else:
        tags_result = get_tags_image(image_path)
    print(f"Getting summary...")
    summary = get_summary(tags_result)

    photo_info = PhotoInfo(
        photo_path = image_path,
        thumbnail_photo_path=thumbnail_path,
        is_screenshot=is_screenshot,
        tags=tags_result,
        face_ids=face_ids,
        metadata_fields=metadata_result,
        summary=summary,
        part_of_which_album=[]
    )

    add_photo_data(photo_info.__dict__)

    return photo_info


def aprocess_image_list(image_paths):
    for image_path in image_paths:
        asyncio.run(process_image(image_path))

def process_image_list(image_paths, injestion = True, get_tags = True) -> List[PhotoInfo]:
    """
    Process a list of image paths and return a list of PhotoInfo objects.
    """
    photo_info = []
    image_tags_dict = None
    
    if injestion and get_tags:
        image_tags_dict = get_tags_image_list(image_paths)

    for image_path in image_paths:
        photo_info.append(process_image(image_path, injestion = injestion, image_tags_dict = image_tags_dict))

    return photo_info

# result = asyncio.run(process_image('images/stock/phone_photo (7).jpg', injestion=False))
# print(result)