'''IOSXR: Image Handler Class'''

# Genie
from genie.libs.clean.stages.iosxe.image_handler import ImageHandler as IosxeImageHandler


class ImageHandler(IosxeImageHandler):

    def __init__(self, device, images, *args, **kwargs):
        super().__init__(device, images, *args, **kwargs)
