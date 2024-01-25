'''
 * The Recognize Anything Plus Model (RAM++)
 * Written by Xinyu Huang
'''
import argparse
import numpy as np
import random

import torch

from PIL import Image
from ram.models import ram_plus
from ram import inference_ram as inference
from ram import get_transform


parser = argparse.ArgumentParser(
    description='Tag2Text inferece for tagging and captioning')
parser.add_argument('--image',
                    metavar='DIR',
                    help='path to dataset',
                    default='images/demo/demo1.jpg')
parser.add_argument('--pretrained',
                    metavar='DIR',
                    help='path to pretrained model',
                    default='pretrained/ram_plus_swin_large_14m.pth')
parser.add_argument('--image-size',
                    default=384,
                    type=int,
                    metavar='N',
                    help='input image size (default: 448)')

# if __name__ == "__main__":

#     args = parser.parse_args()

#     device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#     transform = get_transform(image_size=args.image_size)

#     #######load model
#     model = ram_plus(pretrained=args.pretrained,
#                              image_size=args.image_size,
#                              vit='swin_l')
#     model.eval()

#     model = model.to(device)

#     image = transform(Image.open(args.image)).unsqueeze(0).to(device)

#     res = inference(image, model)
#     print("Image Tags: ", res[0])
#     # print("图像标签: ", res[1])


# write a function to get the tags independent of the args, taking all values as default
def get_tags_single_image(image_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform = get_transform(image_size=384)

    #######load model
    model = ram_plus(pretrained='pretrained/ram_plus_swin_large_14m.pth',
                             image_size=384,
                             vit='swin_l')
    model.eval()

    model = model.to(device)

    image = transform(Image.open(image_path)).unsqueeze(0).to(device)

    res = inference(image, model)
    # parse the tags to a list of strings, tags are separated by |
    image_tags = res[0].split('|')
    for i in range(len(image_tags)):
        image_tags[i] = image_tags[i].strip()
    return image_tags

def get_tags_from_image_list(image_list):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform = get_transform(image_size=384)

    #######load model
    model = ram_plus(pretrained='pretrained/ram_plus_swin_large_14m.pth',
                             image_size=384,
                             vit='swin_l')
    model.eval()

    model = model.to(device)

    # Return a dictionary where the key is iamge path and the value is the tags
    image_tags_dict = {}
    for image_path in image_list:
        image = transform(Image.open(image_path)).unsqueeze(0).to(device)
        res = inference(image, model)
        image_tags = res[0].split('|')
        for i in range(len(image_tags)):
            image_tags[i] = image_tags[i].strip()
        print(f"Tags for image {image_path}: {image_tags}")
        image_tags_dict[image_path] = image_tags

    return image_tags_dict
