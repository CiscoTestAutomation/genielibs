from genie.libs.clean.stages.image_handler import BaseImageHandler


class ImageHandler(BaseImageHandler):
    '''Linux: Image Handler Class

    Linux devices do not use images for clean. This is a no-op ImageHandler
    that satisfies the abstract lookup when images are present in clean YAML.
    '''

    def __init__(self, device, images, *args, **kwargs):
        # Linux devices do not use images
        self.image = []
        super().__init__(device, *args, **kwargs)

    def update_image_references(self, section):
        pass
