from llama_index.schema import TextNode, ImageNode
from typing import List
from llama_index.vector_stores.types import MetadataInfo, VectorStoreInfo
from structure import PhotoInfo


def get_nodes_from_objects(objs: List[PhotoInfo], image_files: List[str]) -> ImageNode:
    """Get nodes from objects."""
    nodes = []
    for image_file, obj in zip(image_files, objs):
        if obj is None:
            continue
        node = ImageNode(
            text=obj.summary,
            metadata={
                "image_tags": obj.tags,
                "image_metadata": obj.metadata_fields,
                "is_screenshot": obj.is_screenshot,
                "part_of_album": obj.part_of_which_album,
                "face_ids": obj.face_ids,
            },
            excluded_embed_metadata_keys=["image_file"],
            excluded_llm_metadata_keys=["image_file"],
            image_path=obj.photo_path,
        )
        nodes.append(node)
    return nodes

def get_node_from_obj(obj: PhotoInfo, image_file: str) -> ImageNode:
    return get_nodes_from_objects([obj], [image_file])[0]


def define_vector_info(return_json = False) -> VectorStoreInfo:
    vector_store_info = VectorStoreInfo(
        content_info="Details about photos stored in the vector store",
        metadata_info=[
            MetadataInfo(
                name="image_tags",
                description="The tags of the image",
                type="array",
            ),
            MetadataInfo(
                name="is_screenshot",
                description="Whether the image is a screenshot",
                type="boolean",
            ),
            MetadataInfo(
                name="part_of_album",
                description="The albums the image is part of",
                type="array",
            ),
            MetadataInfo(
                name="face_ids",
                description="The face ids present in the image",
                type="array",
            ),
            MetadataInfo(
                name="image_metadata",
                description="""
                The metadata of the image. Contains information about image location, create time etc.
                Schema :
                    {
                        'SourceFile': str = Field(..., 'path to the image'), 
                        'FileName': str = Field(..., 'name of the image file'), 
                        'Directory': str = Field(..., 'directory of the image file'), 
                        'FileSize': str = Field(..., 'size of the image file'),
                        'FileAccessDate': str = Field(..., 'date of last access of the image file in the format YYYY:MM:DD'), 
                        'FileAccessTime': str = Field(..., 'time of last access of the image file in the format HH:MM:SS'),
                        'TimeZone': str = Field(..., 'timezone of the image file in the format +/-HH:MM'),
                        'FileType': str = Field(..., 'type of the image file')
                        'Model': str = Field(..., 'model of the camera used to take the image'),
                        'ISO': int = Field(..., 'ISO value of the image'),
                        'FNumber': int = Field(..., 'FNumber of the image'),
                        'ExposureTime': str = Field(..., 'ExposureTime of the image of the form 1/{ExposureTime}'),
                        'FocalLength': str = Field(..., 'FocalLength of the image in mm'),
                        'CreateDate': str = Field(..., 'date of creation of the image in the format YYYY:MM:DD'), 
                        'CreateTime': str = Field(..., 'time of creation of the image in the format HH:MM:SS')
                        'DateTimeOriginal': str = Field(..., 'date and time of creation of the image in the format YYYY:MM:DD HH:MM:SS')
                        'ShutterSpeedValue': str = Field(..., 'shutter speed value of the image in the format 1/{ShutterSpeedValue}'),
                        'GPSLatitudeRef': str = Field(..., 'latitude reference of the image from [N, S]'),
                        'GPSLongitudeRef': str = Field(..., 'longitude reference of the image from [E, W]'),
                        'Make': str = Field(..., 'make of the camera used to take the image'),
                        'ImageWidth': int = Field(..., 'width of the image in pixels'),
                        'ImageHeight': int = Field(..., 'height of the image in pixels'),
                        'Megapixels': float = Field(..., 'megapixels of the image'),
                        'ShutterSpeed': str = Field(..., 'shutter speed of the image in the format 1/{ShutterSpeed}'),
                        'GPSLatitude': str = Field(..., 'latitude of the image in the format DD,MM,SS'),
                        'GPSLongitude': str = Field(..., 'longitude of the image in the format DD,MM,SS'),
                        'GPSPosition': str = Field(..., 'position of the image in the format DD,MM,SS'),
                        'Location': str = Field(..., 'location of the image')
                    }       
                """,
                type="object",
            ),
        ],
    )

    if return_json:
        return vector_store_info.json()
    else:
        return vector_store_info


# print(nodes[0].get_content(metadata_mode="all"))