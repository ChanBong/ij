from geopy.geocoders import Nominatim

def dms_to_decimal(degrees, minutes, seconds, direction):
    decimal_degrees = float(degrees) + float(minutes)/60 + float(seconds)/(60*60)
    if direction in ['S', 'W']:
        decimal_degrees *= -1
    return decimal_degrees

def parse_dms_input(dms_input):
    parts = dms_input.split()

    # if the first item in parts is not an ineteger, remove it
    if not parts[0].isdigit():
        parts = parts[1:]

    degrees = float(parts[0])
    minutes = float(parts[2].strip("'"))
    seconds = float(parts[3].strip('"'))
    direction = parts[4]

    return degrees, minutes, seconds, direction

def get_location_from_coordinates(latitude, longitude):
    geolocator = Nominatim(user_agent="coordinate_converter")
    location = geolocator.reverse((latitude, longitude))
    return location

def get_latitude_longitude(dms_input):
    latitude_dms = parse_dms_input(dms_input[:dms_input.index('N')+1])
    longitude_dms = parse_dms_input(dms_input[dms_input.index('N')+1:])



    latitude = dms_to_decimal(*latitude_dms)
    longitude = dms_to_decimal(*longitude_dms)

    return latitude, longitude

def get_location(dms_input):
    latitude, longitude = get_latitude_longitude(dms_input)
    location = get_location_from_coordinates(latitude, longitude)
    return location.address