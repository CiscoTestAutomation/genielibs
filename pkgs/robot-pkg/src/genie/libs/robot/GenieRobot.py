import re
import os
import logging
import importlib
from copy import deepcopy
from collections import namedtuple

from robot.api.deco import keyword
from robot.libraries.BuiltIn import BuiltIn, RobotNotRunningError

from pyats.utils.objects import find, R
from pyats.aetest import executer
from pyats.datastructures.logic import Or
from pyats.results import (Passed, Failed, Aborted, Errored,
                         Skipped, Blocked, Passx)

from genie.utils.dq import Dq
from genie.utils.diff import Diff
from genie.utils.config import Config
from genie.harness.script import TestScript
from genie.utils.loadattr import load_attribute
from genie.utils.profile import unpickle, pickle
from genie.harness.discovery import GenieScriptDiscover
from genie.harness.datafile.loader import TriggerdatafileLoader,\
                                          VerificationdatafileLoader,\
                                          PtsdatafileLoader

log = logging.getLogger(__name__)


class GenieRobotException(Exception):
    pass


class GenieRobot(object):
    '''Genie RobotFramework library'''

    # Need to maintain the testscript object
    ROBOT_LIBRARY_SCOPE = "GLOBAL"

    ROBOT_LIBRARY_DOC_FORMAT = 'reST'

    def __init__(self):
        # save builtin so we dont have to re-create then everytime
        self.builtin = BuiltIn()

        try:
            self.ats_pyats = self.builtin.get_library_instance('pyats.robot.pyATSRobot')
        except RobotNotRunningError:
            # return early during libdoc generation
            return
        except RuntimeError:
            try:
                self.ats_pyats = self.builtin.get_library_instance('ats.robot.pyATSRobot')
            except RuntimeError:
                # No pyATS
                raise RuntimeError(
                    "Missing mandatory 'Library  pyats.robot.pyATSRobot' in the Setting section")

        self._genie_testscript = TestScript(Testscript)
        self._pyats_testscript = self.ats_pyats.testscript
        self.testscript.parameters['testbed'] = self.testbed

    @property
    def testbed(self):
        return self.ats_pyats.testbed

    @property
    def testscript(self):
        try:
            return self._genie_testscript
        except Exception:
            return self._pyats_testscript

    @keyword('use genie testbed "${testbed}"')
    def genie_testbed(self, testbed):
        '''*DEPRECATED* Please use the "use testbed "${testbed}" keyword instead.'''
        self.ats_pyats.use_testbed(testbed)
        self.testscript.parameters['testbed'] = self.testbed

        # Load Genie Datafiles (Trigger, Verification and PTS)

        # This make UUT mandatory. When learning, aka no trigger
        # the UUT are not mandatory
        self.loaded_yamls = True
        self._load_genie_datafile()
        if not self.trigger_datafile:
            self.loaded_yamls = False
            log.warning("Could not load the trigger datafile correctly, did you specify 'uut' device alias?")

    # Metaparser
    @keyword('parse "${parser:[^"]+}" on device "${device:[^"]+}"')
    def metaparser_on_device(self, parser, device):
        '''Call any `metaparser` parser and parse the device output.'''
        return self.metaparser_on_device_alias_context(device=device,
                                                       alias=None,
                                                       parser=parser)

    @keyword('parse "${parser:[^"]+}" on device "${device:[^"]+}" with '
             'context "${context}"')
    def metaparser_on_device_context(self, parser, device, context):
        '''Call any `metaparser` parser and parse the device output with
        a context (cli, xml, yang, ...)
        '''
        # Using `cli`, as its the default for RASTA
        return self.metaparser_on_device_alias_context(alias=None,
                                                       device=device,
                                                       parser=parser,
                                                       context=context)

    @keyword('parse "${parser:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def metaparser_on_device_alias(self, parser, device, alias):
        '''Call any `metaparser` parser and parse the device using a specific
        alias
        '''
        return self.metaparser_on_device_alias_context(alias=alias,
                                                       device=device,
                                                       parser=parser)

    @keyword('parse "${parser:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}" with context "${context}"')
    def metaparser_on_device_alias_context(self, parser, device, alias,
                                           context='cli'):
        '''Call any `metaparser` parser and parse the device using a specific
        alias with a context (cli, xml, yang, ...)
        '''
        device_handle = self._search_device(device)

        # Look for the alias. If it doesnt exist,  let it crash to the user as
        # only valid alias should be provided
        con = device_handle
        if alias:
            con = getattr(device_handle, alias)

        return con.parse(parser)

    # Genie Ops
    @keyword('learn "${feature:[^"]+}" on device "${device:[^"]+}"')
    def genie_ops_on_device(self, feature, device):
        '''Learn Ops feature on device'''
        return self.genie_ops_on_device_alias_context(feature=feature,
                                                      alias=None,
                                                      device=device)

    @keyword('learn "${feature:[^"]+}" on device "${device:[^"]+}" with '
             'context "${context:[^"]+}"')
    def genie_ops_on_device_context(self, feature, device, context):
        '''Learn Ops feature on device with a context (cli, xml, yang, ...)'''
        return self.genie_ops_on_device_alias_context(feature=feature,
                                                        alias=None,
                                                        context=context,
                                                        device=device)

    @keyword('learn "${feature:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def genie_ops_on_device_alias(self, feature, device, alias):
        '''Learn Ops feature on device using a specific alias'''
        return self.genie_ops_on_device_alias_context(feature=feature,
                                                        alias=alias,
                                                        device=device)

    @keyword('learn "${feature:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}" with context "${context:[^"]+}"')
    def genie_ops_on_device_alias_context(self, feature, device, alias,
                                          context='cli'):
        '''Learn Ops feature on device using a specific alias with a context
        (cli, xml, yang, ...)
        '''
        device_handle = self._search_device(device)

        # Look for the alias. If it doesnt exist,  let it crash to the user as
        # only valid alias should be provided
        con = device_handle
        if alias:
            con = getattr(device_handle, alias)
            device_handle.mapping[alias] = con

        # Find the feature for this device
        # 1) Directory must exists in genie.libs.ops.<feature>
        # 2) Then abstraction will kick in to find the right one.
        # 3) The directory syntax is <feature>.<feature.<Feature> 
        #    Where the class is capitalized but the directory/files arent.

        # First import genie.libs for abstraction
        package = 'genie.libs.ops'

        try:
            mod = importlib.import_module(package)
        except ImportError as e:
            raise ImportError("package 'genie' and library 'genie.libs' "
                              "are mandatory to have to learn '{f}' "
                              .format(f=feature)) from e

        # Now find the right library
        attr_name = '.'.join([feature.lower(), feature.lower(),
                              feature.title().replace('_', '')])

        # Find the right library with abstraction if needed
        # Get context in there
        added_context = False
        if hasattr(device_handle, 'custom') and\
           'abstraction' in device_handle.custom and\
           'order' in device_handle.custom['abstraction']:
               # Add context to it
               backup_abstraction = deepcopy(device_handle.custom['abstraction'])
               device_handle.custom['abstraction']['order'].append('context')
               device_handle.custom['abstraction']['context'] = context
               added_context = True



        try:
            cls = load_attribute(package, attr_name, device=device_handle)
        except Exception as e:
            msg = "Could not find {p}.{a} for device {d}"\
                  .format(p=package, a=attr_name, d=device_handle.name)
            raise Exception(msg) from e

        if added_context:
            device_handle.custom['abstraction'] = backup_abstraction

        # Call the Ops now
        ops = cls(device_handle)
        ops.learn()
        return ops

    @keyword('Run verification "${name:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def genie_run_verification_alias(self, name, device, alias):
        '''Call any verification defined in the verification datafile
           on device using a specific alias
        '''
        return self.genie_run_verification_alias_context(name=name,
                                                             alias=alias,
                                                             device=device,
                                                             context='cli')

    @keyword('Run verification "${name:[^"]+}" on device "${device:[^"]+}" '
             'with context "${context:[^"]+}"')
    def genie_run_verification_context(self, name, device, context):
        '''Call any verification defined in the verification datafile
           on device with a context (cli, xml, yang, ...)
        '''
        return self.genie_run_verification_alias_context(name=name,
                                                               alias=None,
                                                               device=device,
                                                               context=context)

    @keyword('Run verification "${name:[^"]+}" on device "${device:[^"]+}"')
    def genie_run_verification(self, name, device):
        '''Call any verification defined in the verification datafile
           on device
        '''
        return self.genie_run_verification_alias_context(name=name,
                                                               alias=None,
                                                               device=device,
                                                               context='cli')

    @keyword('Run verification "${name:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}" with context "${context:[^"]+}"')
    def genie_run_verification_alias_context(self, name, device, alias,
                                                 context):
        '''Call any verification defined in the verification datafile
           on device using a specific alias with a context (cli, xml, yang, ...)
        '''
        if not self.loaded_yamls:
            self.builtin.fail("Could not load the yaml files - Make sure you "
                              "have an uut device")

        # Set the variables to find the verification
        self.testscript.verification_uids = Or(name+'$')
        self.testscript.verification_groups = None
        self.testscript.verifications = deepcopy(self.verification_datafile)
        self.testscript.triggers = None

        # Modify the parameters to include context
        if name in self.testscript.verifications:
            # Add new parameters named context
            # No need to revert, as a deepcopy was taken, and after discovery
            # nothing is done with the datafiles after
            if 'devices' in self.testscript.verifications[name]:
                # For each device add context
                for dev in self.testscript.verifications[name]['devices']:
                    # To shorten the variable
                    verf = self.testscript.verifications[name]
                    if 'devices_attributes' not in verf or\
                        verf['devices_attributes'][dev] == 'None':
                        verf.setdefault('devices_attributes', {})
                        verf['devices_attributes'].setdefault(dev, {})
                        verf['devices_attributes'][dev] = {}

                    self.testscript.verifications[name]\
                                ['devices_attributes'][dev]['context'] = context

        self._run_genie_trigger_verification(name=name, alias=alias,
                                             device=device, context=context)

    @keyword('Run trigger "${name:[^"]+}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def genie_run_trigger_alias(self, name, device, alias):
        '''Call any trigger defined in the trigger datafile on device
        using a specific alias
        '''
        return self.genie_run_trigger_alias_context(name=name,
                                                    alias=alias,
                                                    device=device,
                                                    context='cli')

    @keyword('Run trigger "${name:[^"]+}" on device "${device:[^"]+}" '
             'with context "${context:[^"]+}"')
    def genie_run_trigger_context(self, name, device, context):
        '''Call any trigger defined in the trigger datafile on device
        with a context (cli, xml, yang, ...)
        '''
        return self.genie_run_trigger_alias_context(name=name,
                                                    alias=None,
                                                    device=device,
                                                    context=context)

    @keyword('Run trigger "${name:[^"]+}" on device "${device:[^"]+}"')
    def genie_run_trigger(self, name, device):
        '''Call any trigger defined in the trigger datafile on device
        '''
        return self.genie_run_trigger_alias_context(name=name,
                                                    alias=None,
                                                    device=device,
                                                    context='cli')

    @keyword('Run trigger "${name}" on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}" with context "${context:[^"]+}"')
    def genie_run_trigger_alias_context(self, name, device, alias, context):
        '''Call any trigger defined in the trigger datafile on device
        using a specific alias with a context (cli, xml, yang, ...)
        '''

        if not self.loaded_yamls:
            self.builtin.fail("Could not load the yaml files - Make sure you "
                              "have an uut device")

        # Set the variables to find the trigger
        device_handle = self._search_device(device)

        self.testscript.trigger_uids = Or(name+'$')
        self.testscript.trigger_groups = None
        self.testscript.triggers = deepcopy(self.trigger_datafile)
        self.testscript.verifications = None

        # Modify the parameters to include context
        self._add_abstraction_datafiles(datafile=self.testscript.triggers,
                                        name=name,
                                        context=context,
                                        device=device_handle)


        self._run_genie_trigger_verification(name=name, alias=alias,
                                                 device=device, context=context)

    @keyword('verify count "${number:[^"]+}" "${structure:[^"]+}" on device "${device:[^"]+}"')
    def verify_count(self, number, structure, device):
        '''Verify that a specific number of <...> is <...> on a device.

           Supports the same functionality as the alias keyword.
        '''
        return self.verify_count_alias(number, structure, device)

    @keyword('verify count "${number:[^"]+}" "${structure:[^"]+}" '
             'on device "${device:[^"]+}" using alias "${alias:[^"]+}"')
    def verify_count_alias(self, number, structure, device, alias=None):
        '''Verify that a specific number of <...> is <...> on a device using a
        specific alias

        Examples:

        .. code:: robotframework

           verify count "<number>" "bgp neighbors" on device "<device>"

           verify count "<number>" "bgp routes" on device "<device>"

           verify count "<number>" "ospf neighbors" on device "<device>"

           verify count "<number>" "interfaces neighbors" on device "<device>"

        '''
        # First word of action is the protocol
        # Last word is the expected value
        # the rest is the structure.
        protocol, structure = structure.split(' ', 1)

        # Make sure we support this protocol
        count = 0
        if protocol == 'bgp':
            # Load bgp
            if structure == 'neighbors':
                # then count the number of neighbor
                ops = self.genie_ops_on_device_alias('bgp', device, alias)
                rs = [R(['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', '([e|E]stablished)'])]

            elif structure == 'routes':
                # then count the number of routes
                ops = self.genie_ops_on_device_alias('bgp', device, alias)
                rs = [R(['table', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)', 'prefixes', '(?P<routes>.*)', '(?P<rest>.*)'])]

        elif protocol == 'ospf':
            # Load ospf
            if structure == 'neighbors':
                # then count the number of neighbor
                ops = self.genie_ops_on_device_alias('ospf', device, alias)
                rs = [R(['info', 'vrf', '(?P<vrf>.*)', 'address_family', '(?P<af>.*)', 'instance', '(?P<instance>.*)', 'areas', '(?P<areas>.*)', '(?P<mode>.*)', '(?P<interface>.*)', 'neighbors', '(?P<neighbors>.*)', 'state', '([f|F]ull)'])]

        elif protocol == 'interface':
            if structure == 'up':
                # then count the number of interface
                ops = self.genie_ops_on_device_alias('interface', device, alias)
                rs = [R(['info', '(?P<interface>.*)', 'oper_status', '([u|U]p)'])]

        count = len(find([ops], *rs, filter_=False, all_keys=True))
        if count != int(number):
            self.builtin.fail("Expected '{e}', but found '{f}'".format(e=number,
                                                                       f=count))

    @keyword('Verify NTP is synchronized on device "${device:[^"]+}"')
    def verify_ntp_synchronized(self, device):
        '''Verify that NTP is synchronized on this device

           Supports the same functionality as the alias keyword.
        '''
        return self.verify_ntp_synchronized_alias(device)

    @keyword('Verify NTP is synchronized on device "${device:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def verify_ntp_synchronized_alias(self, device, alias=None):
        '''Verify that NTP is synchronized on this device

           verify NTP is synchronized on device "<device>"
        '''

        ops = self.genie_ops_on_device_alias('ntp', device, alias)
        rs = [R(['info', 'clock_state', 'system_status', 'associations_address',
                 '(?P<neighbors>.*)'])]
        output = find([ops], *rs, filter_=False, all_keys=True)

        if not output:
            self.builtin.fail("{} does not have NTP synchronized".format(device))

    @keyword('Verify NTP is synchronized with "${server:[^"]+}" on '
             'device "${device:[^"]+}"')
    def verify_ntp_synchronized_server(self, server, device):
        '''Verify that a specific server is the synchronized ntp server

           Supports the same functionality as the alias keyword.
        '''
        return self.verify_ntp_synchronized_server_alias(server, device)

    @keyword('Verify NTP is synchronized with "${server:[^"]+}" on device '
             '"${device:[^"]+}" using alias "${alias:[^"]+}"')
    def verify_ntp_synchronized_server_alias(self, server, device, alias=None):
        '''Verify that a specific server is the synchronized ntp server

           verify "1.1.1.1" is synchronized ntp server on device "<device>"
        '''

        ops = self.genie_ops_on_device_alias('ntp', device, alias)
        rs = [R(['info', 'clock_state', 'system_status', 'associations_address',
                 '(?P<neighbors>.*)'])]
        output = find([ops], *rs, filter_=False, all_keys=True)

        if not output:
            self.builtin.fail("No synchronized server could be found! Was "
                              "expected '{}' to be synchronized".format(server))

        if output[0][0] != server:
            self.builtin.fail("Expected synchronized server to be '{}', but "
                              "found '{}'".format(server, output[0][0]))

    @keyword('Profile the system for "${feature:[^"]+}" on devices '
             '"${device:[^"]+}" as "${name:[^"]+}"')
    def profile_system(self, feature, device, name):
        '''Profile system as per the provided features on the devices
        '''
        return self._profile_the_system(feature=feature,
                                        device=device,
                                        context='cli',
                                        name=name,
                                        alias=None)

    @keyword('Profile the system for "${feature:[^"]+}" on devices '
             '"${device:[^"]+}" as "${name:[^"]+}" '
             'using alias "${alias:[^"]+}"')
    def profile_system_alias(self, feature, device, name, alias=None):
        '''Profile system as per the provided features on the devices
           filtered using alias
        '''

        try:
            device = self._search_device(alias).name
        except KeyError:
            msg = ["'{alias}' is not found in the testbed yaml file.".format(
                alias=alias)]

            self.builtin.fail('\n'.join(msg))

        return self._profile_the_system(feature=feature,
                                        device=device,
                                        context='cli',
                                        name=name,
                                        alias=alias)

    @keyword('dq query')
    def dq_query(self, data, filters):
        ''' Search dictionary using Dq filters

        Examples:

        .. code:: robotframework

            dq query    data=${data}   filters=contains('lc').not_contains('2').get_values('slot/world_wide_name')

        :param data: dictionary with data
        :param filters: Dq filter specification
        :return: dictionary, list, str or int

        '''
        if not isinstance(data, dict):
            raise GenieRobotException('Invalid data, dictionary expected, got %s' % type(data))
        if not Dq.query_validator(filters):
            raise GenieRobotException('Invalid filter')

        return Dq.str_to_dq_query(data, filters)

    def _profile_the_system(self, feature, device, context, name, alias):
        '''Profile system as per the provided features on the devices
        '''
        profiled = {}

        for dev in device.split(';'):

            for fet in feature.split(';'):

                if fet not in profiled:
                    profiled[fet] = {}
                if dev not in profiled[fet]:
                    profiled[fet][dev] = {}

                if fet == 'config':
                    log.info("Start learning device configuration")
                    profiled[fet][dev] = self._profile_config(dev)
                else:
                    log.info("Start learning feature {f}".format(f=fet))
                    learnt_feature = self.genie_ops_on_device_alias_context(
                        feature=fet.strip(), alias=None, device=dev)

                    profiled[fet][dev] = learnt_feature


        if os.path.isdir(os.path.dirname(name)):
            # the user provided a file to save as pickle
            pickle_file = pickle(profiled, pts_name = name)
            log.info('Saved system profile as file: %s' % pickle_file)
        else:
            self.testscript.parameters[name] = profiled
            log.info('Saved system profile as variable %s' % name)

    def _profile_config(self, device):
        device_handle = self._search_device(device)
        config = Config(device_handle.execute('show running-config'))
        config.tree()
        return config

    @keyword('Compare profile "${pts:[^"]+}" with "${pts_compare:[^"]+}" on '
             'devices "${devices:[^"]+}"')
    def compare_profile(self, pts, pts_compare, devices):
        '''Compare system profiles taken as snapshots during the run'''

        if os.path.isfile(pts):
            compare1 = unpickle(pts)
        else:
            compare1 = self.testscript.parameters[pts]

        if os.path.isfile(pts_compare):
            compare2 = unpickle(pts_compare)
        else:
            compare2 = self.testscript.parameters[pts_compare]



        exclude_list = ['device', 'maker', 'diff_ignore', 'callables',
                        '(Current configuration.*)', 'ops_schema']

        try:
            if 'exclude' in self.pts_datafile:
                exclude_list.extend(self.pts_datafile['exclude'])
        except AttributeError:
            pass

        msg = []
        for fet in compare1:
            failed = []
            feature_exclude_list = exclude_list.copy()

            # Get the information too from the pts_data
            try:
                feature_exclude_list.extend(self.pts_datafile[fet]['exclude'])
            except (KeyError, AttributeError):
                pass

            for dev in compare1[fet]:
                # Only compare for the specified devices
                if dev not in devices:
                    continue
                dev_exclude = feature_exclude_list.copy()
                try:
                    dev_exclude.extend(compare1[fet][dev].exclude)
                    # TODO - better fix,
                    dev_exclude.remove(None)
                except (AttributeError, ValueError):
                    pass

                diff = Diff(compare1[fet][dev], compare2[fet][dev],
                    exclude=dev_exclude)

                diff.findDiff()

                if len(diff.diffs):
                    failed.append((dev, diff))

            if failed:
                msg.append('\n' + '*'*10)
                msg.append("Comparison between {pts} and "
                           "{OPS} is different for feature '{f}' "
                           "for device:\n".format(pts=pts, OPS=pts_compare,
                                                  f=fet))
                for device, diff in failed:
                    msg.append("'{d}'\n{diff}".format(d=device,
                                                      diff=diff))

            else:
                message = "Comparison between {pts} and "\
                          "{OPS} is identical\n".format(pts=pts,
                          OPS=pts_compare)
                # print out message
                log.info(message)

        if msg:
            self.builtin.fail('\n'.join(msg))

        message = 'All Feature were identical on all devices'
        self.builtin.pass_execution(message)

    def _run_genie_trigger_verification(self, alias, device, context,
                                            name):
        try:
            device_handle = self._search_device(device)
        except Exception as e:
            raise Exception("Could not find '{d}'".format(d=device))

        genie_discovery = GenieScriptDiscover(self.testscript)

        # To call the __iter__ of the discovery which will force
        # The generator to return all the elements
        sections = list(genie_discovery)

        # Remove both common sections
        testcases = sections[1:-1]

        # Its possible multiple devices were found, only
        # keep the one with the correct device
        tc_to_run = []
        for tc in testcases:
            # Make sure the device match the right device and
            # Make sure it match the name, as
            # Or logic could match more than expected
            if tc.parameters['uut'] != device_handle or\
               not re.match(name+'\.', tc.uid):
                continue
            tc_to_run.append(tc)

        # Make sure only len of 1
        if len(tc_to_run) == 0:
            raise Exception("Could not find '{r}'".format(r=name))

        if len(tc_to_run) != 1:
            raise Exception("Requested to run '{r}' but more than one was "
                            "found '{v}'".format(r=name,
                                                 v=', '.join(tc_to_run)))

        # Get the testcase class
        cls = tc_to_run[0]
        # Add to Cls the context if any

        # Set the tags
        tags = cls.groups if hasattr(cls, 'groups') else []

        # Found our testcase - Now Execute it
        try:
            # Make sure its reset, as we dont need some of these functionalities
            executer.reset()
            result = cls()
        except Exception as e:
            # No need, as pyats has already logged the error
            pass

        # Maps the result RobotFramework
        self._convert_result(result, name, ' '.join(tags))

    def _add_abstraction_datafiles(self, datafile, name, device, context):
        '''Add context abstraction'''

        if name not in datafile or 'devices' not in datafile[name]:
            return datafile

        if device.name in datafile[name]['devices']:
            dev = device.name
        elif device.alias in datafile[name]['devices']:
            dev = device.alias
        else:
            return datafile

        # Nothing under device
        # Or device does not have abstraction
        if 'devices_attributes' not in datafile[name] or\
           datafile[name]['devices_attributes'] == 'None' or\
           'abstraction' not in datafile[name]['devices_attributes']:
            # Then add it at the trigger/verification level
            self._add_abstraction_at_level(datafile=datafile[name],
                                           context=context)
        else:
            # This there is information at device level and abstraction is there
            # Then add at device level
            self._add_abstraction_at_level(\
                    datafile=datafile[name]['devices_attributes'][dev],
                    context=context)
        return datafile

    def _add_abstraction_at_level(self, datafile, context):
        #    If abstraction does not exists, just add it
        #    If it already exists, then overwrite the information
        if 'abstraction' not in datafile:
            datafile['abstraction'] = {}

        datafile['abstraction']['context'] = context
        if 'order' not in datafile['abstraction']:
            datafile['abstraction']['order'] = []
        if 'context' not in datafile['abstraction']['order']:
            datafile['abstraction']['order'].append('context')

    def _convert_result(self, result, name, tags):
        ''''
            pyATS    RobotFramework  Reason
            Passed   Pass            Passed is a pass
            Failed   Fail            Failed is a fail
            Aborted  Fail            An abort is because of a failure
            Errored  Fail            An error is because of a failure
            Skipped  Pass            A skip is not a failure
            Blocked  Pass            A block is not a failure
            Passx    Pass            Passx is a pass with exception
        '''
        fail_group = [Failed, Aborted, Errored]
        pass_group = [Passed, Skipped, Blocked, Passx]

        if result in fail_group:
            self.builtin.fail('{n} has {r}'.format(n=name, r=result.name),
                              tags)

        if result in pass_group:
            self.builtin.pass_execution('{n} has {r}'.format(n=name,
                                                             r=result.name),
                                        tags)

        raise Exception('{r} is not a supported result'.format(r=result.name))

    def _search_device(self, name):
        try:
            # Find hostname and alias
            return self.testbed.devices[name]
        except KeyError:
            raise KeyError("Unknown device {}".format(name))
        except AttributeError as e:
            raise AttributeError(
                "Unable to find device {}, testbed not loaded properly?".format(
                    name)) from e

    def _load_genie_datafile(self):
        # Load the datafiles
        variables = self.builtin.get_variables()

        trigger_datafile = None
        if '${trigger_datafile}' in variables:
            trigger_datafile = variables['${trigger_datafile}']

        verification_datafile = None
        if '${verification_datafile}' in variables:
            verification_datafile = variables['${verification_datafile}']

        pts_datafile = None
        if '${pts_datafile}' in variables:
            pts_datafile = variables['${pts_datafile}']

        self.trigger_datafile, self.verification_datafile, pts_datafile, *_ =\
            self.testscript._validate_datafiles(self.testbed,
                                                trigger_datafile,
                                                verification_datafile,
                                                pts_datafile,
                                                None, None)

        if self.trigger_datafile:
            self.trigger_datafile = self.testscript._load(self.trigger_datafile,
                                                          TriggerdatafileLoader)
        if self.verification_datafile:
            self.verification_datafile = self.testscript._load(self.verification_datafile,
                                                               VerificationdatafileLoader)
        self.pts_datafile = self.testscript._load(pts_datafile,
                                                  PtsdatafileLoader)


class Testscript(object):
    pass
