'''Common OS: Image Handler Class'''

import yaml

class BaseImageHandler(object):

    # In case this is not defined by the child
    # class this will prevent an AttributeError
    exception = None

    # In case this is not defined by the child class
    # we use a generic message
    EXPECTED_IMAGE_STRUCTURE_MSG = """
----------------------------------------------------
An invalid structure for 'images' has been provided:
----------------------------------------------------
{}"""

    def __init__(self, device, *args, **kwargs):

        if self.exception:
            # The child ImageHandler has deemed 'images' to have an
            # invalid structure so raise an exception to halt the
            # process and inform the user
            raise Exception(self.EXPECTED_IMAGE_STRUCTURE_MSG.format(
                yaml.dump(self.exception)))
        else:
            # No exception to raise - Set vars and continue as normal.
            # Go pyATS Clean Go!
            self.device = device

    def update_section(self, section_uid):
        ''' Initializes section dictionary and calls update method for
            respective method '''

        if (section_uid not in self.device.clean or
                not self.device.clean[section_uid]):
            self.device.clean[section_uid] = {}

        # call the ImageHandler update method
        if hasattr(self, 'update_' + section_uid):
            getattr(self, 'update_' + section_uid)()


