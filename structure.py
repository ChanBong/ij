from pydantic import BaseModel, Field, validator
from typing import Optional
import pytz
from location_utils import get_location

class PhotoInfo(BaseModel):
    """  
    Use these fields to describe a photo. Make sure to add a summary of the fields here.
    - photo_path
    - thumbnail_photo_path
    - metadata_fields : Another Pydantic Class
    - is_screenshot
    - tags
    - part_of_which_album 
    - face_ids
    - summary
    """
    
    photo_path: str = Field(..., description="The path to the photo")
    thumbnail_photo_path: str = Field(..., description="The path to the thumbnail of the photo")
    is_screenshot: bool = Field(..., description="Whether the photo is a screenshot")
    tags: list = Field(..., description="The tags of the photo")
    part_of_which_album: list = Field(..., description="The albums the photo is part of")
    face_ids: list = Field(..., description="The face ids of the photo")
    metadata_fields: dict = Field(..., description="The metadata fields of the photo")
    summary: str = Field(..., description="The summary of the photo")


class EXIFImageMetadata:
    def __init__(self, **kwargs):
        allowed_keys = [
            'SourceFile', 'FileName', 'Directory', 'FileSize', 'FileAccessDate',
            'FileType', 'Model', 'ISO', 'FNumber', 'ExposureTime', 'FocalLength',
            'CreateDate', 'CreateTime', 'DateTimeOriginal', 'ShutterSpeedValue',
            'GPSLatitudeRef', 'GPSLongitudeRef', 'Make', 'ImageWidth', 'ImageHeight',
            'Megapixels', 'ShutterSpeed', 'GPSLatitude', 'GPSLongitude', 'GPSPosition'
        ]
        for key in allowed_keys:
            if key == 'CreateDate':
                create_date_value = kwargs.get(key, None)
                if create_date_value:
                    date, time = create_date_value.split(' ')
                    setattr(self, 'CreateDate', date)
                    setattr(self, 'CreateTime', time)
                else:
                    setattr(self, 'CreateDate', None)
                    setattr(self, 'CreateTime', None)
            elif key == 'FileAccessDate':
                access_date_value = kwargs.get(key, None)
                if access_date_value:
                    date, time_with_timezone = access_date_value.split(' ')
                    if '+' in time_with_timezone:
                        timezone_sign = '+'
                        time, timezone = time_with_timezone.split('+')
                    elif '-' in time_with_timezone:
                        timezone_sign = '-'
                        time, timezone = time_with_timezone.split('-')
                    setattr(self, 'FileAccessDate', date)
                    setattr(self, 'FileAccessTime', time)
                    setattr(self, 'TimeZone', timezone_sign + timezone)
                else:
                    setattr(self, 'FileAccessDate', None)
                    setattr(self, 'FileAccessTime', None)
                    setattr(self, 'TimeZone', None)
            elif key == 'GPSPosition' in kwargs:
                gps_position = kwargs.get(key, None)
                if gps_position:
                    address = get_location(gps_position)
                    setattr(self, 'Location', address)
                else:
                    setattr(self, 'Location', None)
            else:
                setattr(self, key, kwargs.get(key, None))