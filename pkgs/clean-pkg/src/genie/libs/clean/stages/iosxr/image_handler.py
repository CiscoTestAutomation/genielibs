'''IOSXR: Image Handler Class'''

# Python
import os

# Genie
from genie.libs.clean.stages.image_handler import ImageHandler as CommonImageHandler


class ImageHandler(CommonImageHandler):


    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)

