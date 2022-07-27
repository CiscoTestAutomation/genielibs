'''Common OS: Image Handler Class'''


class BaseImageHandler(object):

    def __init__(self, device, *args, **kwargs):
        self.device = device

        # keep track of stages calling image handler
        self.history = []

        # By default, override images for stages, even if user specified
        # User can configure this via `image_handler.override_stage_images`
        # boolean in clean.yaml file
        self.override_stage_images = True

    def update_section(self, section_uid, update_history=False):
        ''' Initializes section dictionary and calls update method for
            respective method '''
        if update_history:
            self.history.append(section_uid)

        if (section_uid not in self.device.clean or
                not self.device.clean[section_uid]):
            self.device.clean[section_uid] = {}

        sections = section_uid.split("__")
        if len(sections) == 1:
            section_uid = sections[0]
            number = ''
        else:
            section_uid = sections[0]
            number = '__{}'.format(sections[1])

        # call the ImageHandler update method
        if hasattr(self, 'update_' + section_uid):
            getattr(self, 'update_' + section_uid)(number)

