# python
import logging

# Genie Libs
from genie.libs import sdk

# ats
from ats import aetest
from ats.log.utils import banner

# abstract
from genie.abstract import Lookup

# unicon
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.utils.timeout import Timeout

# genie.libs
from genie.libs import ops
from genie.libs.sdk.libs.abstracted_libs.processors import load_config_precessor

log = logging.getLogger(__name__)

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
    log.info(banner('Check boot information to see if they are consistent\n'
      'and save bootvar to startup-config'))
    # get uut
    devices = testbed.find_devices(alias='uut')

    for uut in devices:
        lookup = Lookup.from_device(uut)
        # get platform pts
        platform_pts = self.parameters.get('pts', {}).get('platform', {}).get('uut', None)
        
        try:
            lookup.sdk.libs.abstracted_libs.subsection.save_device_information(
                device=uut, platform_pts=platform_pts)
        except Exception as e:
            self.passx('Failed to save boot var or copy running-config to startup-config',
                        from_exception=e)

@aetest.subsection
def learn_the_system(self, testbed, steps):
    """Learn and store the system properties

       Args:
           testbed (`obj`): Testbed object
           steps (`obj`): aetest steps object

       Returns:
           None

       Raises:
           pyATS Results
    """
    log.info(banner('Learn and store platform information, lldp neighbors'
        ', from PTS if PTS is existed, otherwise from show commands'))
    # get uut
    devices = testbed.find_devices(alias='uut')

    for uut in devices:
        lookup = Lookup.from_device(uut)

        # get platform PTS 
        platform_pts = self.parameters.get('pts', {}).get('platform', {}).get('uut', None)

        try:
            lookup.sdk.libs.abstracted_libs\
                  .subsection.learn_system(device=uut, steps=steps, platform_pts=platform_pts)
        except Exception as e:
            step.passx('Cannot Learn and Store system info',
                        from_exception=e)

        # learn platform lldp neighbors
        with steps.start("learn platform lldp neighbors on device {}"
          .format(uut.name)) as step:

            # inital lldp ops object
            lldp_ops = lookup.ops.lldp.lldp.Lldp(
                           uut, attributes=['info[interfaces][(.*)][neighbors][(.*)][port_id]'])

            # learn the lldp ops
            try:
                lldp_ops.learn()
            except Exception as e:
                step.passx('Cannot learn lldp information',
                            from_exception=e)

            if not hasattr(lldp_ops, 'info'):
                step.passx('No LLDP neighbors')

            # store the lldp information
            uut.lldp_mapping = lldp_ops.info['interfaces']


@aetest.subsection
def load_config_as_string(self, testbed, steps, configs, connect=False):
    if connect:
        for name in self.parent.mapping_data['devices']:
            dev = testbed.devices[name]
            # connect with console
            try:
                dev.connect(via='a')
            except Exception as e:
                self.failed('Cannot connect the console on {}'.format(dev.name),
                  from_exception=e)
    try:
        load_config_precessor(self, configs)
    except Exception as e:
        self.passx('Cannot Load configuration',
                    from_exception=e)

    # disconnect the router from console 
    if connect:
        for name in self.parent.mapping_data['devices']:
            dev = testbed.devices[name]
            # connect with console
            try:
                dev.disconnect()
                dev.destroy()
            except Exception as e:
                self.passx('Cannot disconnect the console on {}'.format(dev.name),
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
    self.parent.default_file_system = {}
    for device in self.parent.mapping_data['devices']:
        dev = testbed.devices[device]
        lookup = Lookup.from_device(dev)
        try:
            self.parent.default_file_system[dev.name] = lookup.sdk.libs.\
                            abstracted_libs.subsection.get_default_dir(device=dev)
        except LookupError as e:
            log.info('Cannot find device {d} correspoding get_default_dir'.format(d=dev.name))
        except Exception as e:
            self.failed('Unable to learn system defaults', from_exception=e)
    if not self.parent.default_file_system:
        self.failed('Unable to set default directory')


    # TODO: Learn and save more system defaults in this section
    
