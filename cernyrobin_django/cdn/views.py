from django.shortcuts import render

import os
import uuid

def get_uuid():
    return str(uuid.uuid4())

def delete_image(image_name):
    if image_name is None:
        return

    image_path = "media/" + image_name

    if os.path.exists(image_path):
        os.remove(image_path)

def upload_image(image_file):
    if image_file is None:
        return None

    image_name = image_file.name
    image_extension = os.path.splitext(image_name)[1]

    if image_extension == ".jpg" or image_extension == ".jpeg" or image_extension == ".png":
        id = get_uuid()

        image_path = "media/" + id + image_extension

        with open(image_path, "wb+") as destination:
            for chunk in image_file.chunks():
                destination.write(chunk)

        return "/" + image_path
    else:
        return None