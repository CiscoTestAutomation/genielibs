'''Common OS: Image Handler Class'''


class BaseImageHandler(object):

    def __init__(self, device, *args, **kwargs):
        self.device = device

    def update_section(self, section_uid):
        ''' Initializes section dictionary and calls update method for
            respective method '''

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


