
# Genie Libs
from genie.libs import sdk

# ats
from ats import aetest

# abstract
from genie.abstract import Lookup

@aetest.subsection
def save_bootvar(self, testbed):
    """Check boot information and save bootvar to startup-config

       Args:
           testbed (`obj`): Testbed object

       Returns:
           None

       Raises:
           pyATS Results
    """
    # get uut
    devices = testbed.find_devices(aliases=['uut'])

    # change the xml version to corresponding one.
    for uut in devices:
        lookup = Lookup.from_device(uut)
        try:
            pass_flag = lookup.sdk.libs.abstracted_libs.subsection.save_device_information(device=uut)
        except Exception as e:
            self.passx('Failed to save boot var or copy running-config to startup-config',
                        from_exception=e)

@aetest.subsection
def learn_system_defaults(self, testbed):
    """Execute commands to learn default system information

       Args:
           testbed (`obj`): Testbed object

       Returns:
           None

       Raises:
           pyATS Results
    """

    # Get default memory location
    dev = testbed.devices['uut']
    lookup = Lookup.from_device(dev)
    try:
        self.parent.default_file_system = {}
        self.parent.default_file_system[dev.name] = lookup.sdk.libs.\
                        abstracted_libs.subsection.get_default_dir(device=dev)
    except Exception as e:
        self.failed('Unable to learn system defaults', from_exception=e)
    if not self.parent.default_file_system:
        self.failed('Unable to set default directory')


    # TODO: Learn and save more system defaults in this section
