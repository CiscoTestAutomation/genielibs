from genie.conf.base import API
from robot.libraries.BuiltIn import BuiltIn

import logging
log = logging.getLogger(__name__)

DOC_LINK = 'https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/apis/'


class GenieRobotApis:

    ROBOT_LIBRARY_SCOPE = "TEST CASE"

    def __init__(self):
        self.builtin = BuiltIn()
        self.api = API()

    def get_keyword_names(self):
        return self.api.function_data.keys()

    def get_keyword_documentation(self, kw):
        if kw == '__intro__':
            return "Available networking APIs provided by Genie"

        return ''.join(['''Checkout this url for detailed doc on this keyword:
        
        ''', DOC_LINK, kw])

    def run_keyword(self, name, args, kwargs):
        try:
            try:
                self.builtin.get_library_instance('pyats.robot.pyATSRobot')
                ats_pyats = 'pyats.robot.pyATSRobot'
            except RuntimeError:
                self.builtin.get_library_instance('ats.robot.pyATSRobot')
                ats_pyats = 'ats.robot.pyATSRobot'
            except RuntimeError:
                # No pyATS
                pass

            self.testbed = self.builtin.get_library_instance(ats_pyats).testbed
            device_name = kwargs.get('device')

            # if function takes device, pass device, if no then dont pass
            if device_name:
                device_handler = self._search_device(device_name)
                kwargs.pop('device', None)
                return self.api.get_api(name.strip().replace(' ', '_'), device_handler)(device_handler, *args, **kwargs)
            else:
                return self.api.get_api(name.strip().replace(' ', '_'))(*args, **kwargs)
        except RuntimeError:
            # No GenieRobot
            log.error('No testbed is found, did you import "genie.libs.robot.GenieRobot"?')


    def _search_device(self, name):
        try:
            # Find hostname and alias
            return self.testbed.devices[name]
        except KeyError:
            raise KeyError("Unknown device {}".format(name))
        except AttributeError as e:
            raise AttributeError(
                'No testbed found, did you use keyword "use testbed \"${testbed}\""?') from e
