# python
import logging
from copy import deepcopy
from operator import attrgetter
from json import dumps

# Genie Libs
from genie.libs import sdk

# ats
from pyats import aetest
from pyats.log.utils import banner
from pyats.datastructures import AttrDict

# abstract
from genie.abstract import Lookup

# import pcall
import importlib
try:
    pcall = importlib.import_module('pyats.async').pcall
except ImportError:
    from pyats.async_ import pcall
# # import pcall
# from pyats.async import pcall

# unicon
from unicon.eal.dialogs import Statement, Dialog

# Genie
from genie.utils.timeout import Timeout
from genie.utils.summary import Summary
from genie.conf.base import Base as ConfBase
from genie.ops.base import Base as OpsBase

# genie.libs
from genie.libs import ops
from genie.libs import conf
from genie.libs.sdk.libs.abstracted_libs.processors import load_config_precessor
from genie.libs.sdk.libs.utils.normalize import _to_dict
from genie.libs.sdk.libs.utils.normalize import merge_dict

log = logging.getLogger(__name__)

EXCLUDED_DEVICE_TYPES = ['tgn']


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

    # Create Summary
    summary = Summary(title='Summary', width=90)

    devices = []
    for dev in self.parent.mapping_data['devices']:
        device = testbed.devices[dev]
        if device.type in EXCLUDED_DEVICE_TYPES:
            msg = "    - This subsection is not supported for 'TGN' devices"
            summarize(summary, message=msg, device=dev)
            continue
        devices.append(device)

    device_dict = {}
    failed = False

    # We don't catch exceptions since failures will lead to passx in that
    # CommonSetup subsection
    asynchronous_boot_var_output = pcall(
        asynchronous_save_boot_variable,
        ckwargs={
            'self': self,
            'device_dict': device_dict},
        device=tuple(devices))

    for item in asynchronous_boot_var_output:
        for dev, res in item.items():
            if res == 'Failed':
                failed = True
                msg = "    - Failed to save boot variable or copy "\
                    "running-config to startup-config"
                summarize(summary, message=msg, device=dev)
            elif res == 'Skipped':
                msg = "    - Skipped saving boot variable or copy "\
                    "running-config to startup-config"
                summarize(summary, message=msg, device=dev)
            else:
                msg = "    - Successfully saved boot variable"
                summarize(summary, message=msg, device=dev)

    summary.print()

    if failed:
        self.passx("Issue while saving boot variable on one of the devices, "
                   "Check section summary for more details")


@aetest.subsection
def learn_the_system(self, testbed, steps, features=None):
    """Learn and store the system properties

       Args:
           testbed (`obj`): Testbed object
           steps (`obj`): aetest steps object
           features (`dict`): dict of components and the feature that contains the component.
                              ex. {'pim': ['autorp',],
                                   'bgp': ['confederationpeers', 'gracefulrestart']}


       Returns:
           None

       Raises:
           pyATS Results
    """
    log.info(
        banner(
            'Learn and store platform information, lldp neighbors'
            ', from PTS if PTS is existed, otherwise from show commands'))
    # get uut, having a uut is mandatory in Genie
    uut = testbed.devices['uut']

    lookup = Lookup.from_device(uut)

    # get platform PTS
    platform_pts = self.parameters.get(
        'pts',
        {}).get(
        'platform',
        {}).get(
            'uut',
        None)

    with steps.start("Store and learn platform information from 'show lldp neighbors detail' on {}"
                     .format(self.name)) as step:
        try:
            lookup.sdk.libs.abstracted_libs .subsection.learn_system(
                device=uut, steps=steps, platform_pts=platform_pts)
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
def learn_the_system_from_conf_ops(self, testbed, steps, features=None):
    """Learn and store the system properties

       Args:
           testbed (`obj`): Testbed object
           steps (`obj`): aetest steps object
           features (`dict`): dict of feature and attributes which want to learn.
                              ex. {'conf.pim.Pim': [
                                      'pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_intf]',
                                      'pim[vrf_attr][(.*)][address_family_attr][ipv4][send_rp_announce_group_list]'],
                                   'conf.bgp.Bgp': ['bgp[instance][(.*)][vrf_attr][(.*)][confederation_peers_as]']}
       Returns:
           None

       Raises:
           pyATS Results
    """
    def remove_parent_from_conf_dict(conf_dict):
        temp_dict = deepcopy(conf_dict)
        for key, val in temp_dict.items():
            if key == 'parent':
                conf_dict.pop('parent')
            if isinstance(val, dict):
                remove_parent_from_conf_dict(conf_dict[key])

    def store_structure(device, feature):

       # get feature and attributes
        [(ft, attr)] = feature.items()
        log.info(banner("Learning '{n}' feature with "
                        "attribues {a} on device {d}"
                        .format(n=ft, a=attr, d=device)))

        # perform lookup per device
        lib = Lookup.from_device(device)

        # attach ops and conf
        lib.conf = getattr(lib, 'conf', conf)
        lib.ops = getattr(lib, 'ops', ops)

        # create the ops/conf instance
        try:
            obj = attrgetter(ft)(lib)
        except Exception:
            raise AttributeError('Cannot load %s for '
                                 'device %s.' % (ft, device.name))
        # conf learn_config
        if issubclass(obj, ConfBase):
            ret = obj.learn_config(device=device, attributes=attr)
            ret = _to_dict(ret[0])
            # delete the non-used objects for pcall to retrun
            ret.pop('__testbed__')
            ret.pop('devices')
            ret.pop('interfaces')
            remove_parent_from_conf_dict(ret['device_attr'][device.name])

        elif issubclass(obj, OpsBase):
            ret = obj(device, attributes=attr)
            ret.learn()
            temp = AttrDict()
            temp.info = getattr(ret, 'info', {})
            ret = temp

        ret_dict = {}

        ret_dict.setdefault('lts', {}).\
            setdefault(ft, {}).setdefault(device.name, ret)

        # return the dictionary
        return ret_dict

    devices = []
    for name in testbed.devices:
        dev = testbed.devices[name]
        if not dev.is_connected():
            continue
        devices.append(dev)

    # create the abstract object list
    merged_dict = {}
    for ft in features:
        worker_devs = []
        worker_features = []
        for device in devices:
            worker_devs.append(device)
            worker_features.append({ft: features[ft]})
        # pcall for each feature
        ret = pcall(
            store_structure,
            device=worker_devs,
            feature=worker_features)
        [merge_dict(merged_dict, i) for i in ret]

    self.parent.parameters.update(merged_dict)

    # print out what we learned in LTS
    log.info('LTS information is \n{d}'.format(d=dumps(merged_dict, indent=5)))


@aetest.subsection
def load_config_as_string(self, testbed, steps, configs, connect=False):
    if connect:
        for name in self.parent.mapping_data['devices']:
            dev = testbed.devices[name]
            # connect with console
            try:
                dev.connect(via='a')
            except Exception as e:
                self.failed(
                    'Cannot connect the console on {}'.format(
                        dev.name), from_exception=e)
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
                self.passx(
                    'Cannot disconnect the console on {}'.format(
                        dev.name), from_exception=e)


@aetest.subsection
def configure_replace(self, testbed, steps, devices, timeout=60):

    for name, dev in devices.items():
        log.info("Executing 'configure_replace' subsection on '{dev}'"
                 .format(dev=name))

        if name not in testbed.devices:
            log.warning("Skipping '{dev}' as it does not exist in the testbed"
                        .format(dev=name))
            continue

        device = testbed.devices[name]

        if not device.is_connected():
            log.warning("Skipping '{dev}' as it is not connected"
                        .format(dev=name))
            continue

        try:
            file_name = None
            file_location = None
            lookup = Lookup.from_device(device)
            if 'file_location' in dev:
                file_location = dev['file_location']
            else:
                file_location = lookup.sdk.libs.\
                    abstracted_libs.subsection.get_default_dir(
                        device=device)
                if 'file_name' not in dev:
                    log.error('Missing file_name for device {}'.format(name))
                    continue
            if 'file_name' in dev:
                file_name = dev['file_name']
            lookup.sdk.libs.abstracted_libs.subsection.configure_replace(
                device, file_location, timeout=dev.get(
                    'timeout', timeout), file_name=file_name)
        except Exception as e:
            self.failed("Failed to replace config : {}".format(str(e)))
        log.info("Configure replace is done for device {}".format(name))


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

    # Create Summary
    summary = Summary(title='Summary', width=150)

    for device in self.parent.mapping_data['devices']:
        dev = testbed.devices[device]
        lookup = Lookup.from_device(dev)

        # Skip in case of TGN device
        if dev.type in EXCLUDED_DEVICE_TYPES:
            log.info("This subsection is not supported for "
                     "TGN device '{}'".format(dev.name))
            msg = "    - This subsection is not supported for 'TGN' devices"
            summarize(summary, message=msg, device=dev.name)
            continue

        try:
            self.parent.default_file_system[dev.name] = lookup.sdk.libs.\
                abstracted_libs.subsection.get_default_dir(
                device=dev)
            msg = "    - Successfully learnt system default directory"
            summarize(summary, message=msg, device=device)
        except LookupError as e:
            log.info('Cannot find device {d} correspoding get_default_dir'.
                     format(d=dev.name))
            msg = "    - Didn't find device OS corresponding "\
                "'get_default_dir' implementation, Please contact Genie support"
            summarize(summary, message=msg, device=device)
        except Exception as e:
            msg = "    - Failed to learn system default directory"
            summarize(summary, message=msg, device=device)
            summary.print()
            self.failed('Unable to learn system default directory',
                        from_exception=e)

    summary.print()

    if not self.parent.default_file_system:
        # Create Summary
        summary = Summary(title='Summary', width=90)
        summary.add_message(
            "* Summary for device(s): "
            "{}".format(
                ', '.join(
                    self.parent.mapping_data['devices'])))
        summary.add_sep_line()
        msg = "    - Couldn't set system default directory"
        summarize(summary, message=msg)
        summary.print()
        self.failed('Unable to set system default directory')

    # TODO: Learn and save more system defaults in this section


def summarize(summary, message, device=None):
    '''A function for building the summary table messages'''

    if device:
        summary.add_message('* Summary for device: {}'.
                            format(device))
        summary.add_sep_line()

    summary.add_message(message)
    summary.add_subtitle_line()


def asynchronous_save_boot_variable(self, device, device_dict):
    '''Use asynchronous execution when saving boot variables on devices'''

    log.info(banner("Check boot information to see if they are consistent\n"
                    "and save bootvar to startup-config on device '{d}'".
                    format(d=device.name)))

    # get platform pts
    platform_pts = self.parameters.get('pts', {}).get('platform', {}).get(
        device.name, None)

    try:
        result = Lookup.from_device(device).sdk.libs.abstracted_libs.subsection.\
            save_device_information(device=device, platform_pts=platform_pts)
    except Exception as e:
        device_dict[device.name] = 'Failed'
    else:
        if result == 'Skipped':
            device_dict[device.name] = 'Skipped'
        else:
            device_dict[device.name] = 'Passed'

    return device_dict
