'''IOSXE implementation for checkcommands triggers'''

# import python
import time
import traceback
import logging
from copy import deepcopy

# import pyats
from pyats import aetest

# import genie.libs
from genie.libs.sdk.triggers.template.checkcommands import \
                       TriggerCheckCommands as CheckCommandsTemplate

from genie.libs.sdk.triggers.xe_sanity.checkcommands.libs.iosxe.checkcommands import \
                       get_requirements, verify_requirements, verify_switches

# import parser
from genie.libs.parser.iosxe.show_platform import ShowSwitchDetail, \
                                                  ShowRedundancy, \
                                                  ShowModule, ShowInventory,\
                                                  ShowPlatform, ShowVersion

from genie.libs.parser.iosxe.cat3k.c3850.show_platform import ShowEnvironmentAll
from genie.libs.parser.iosxe.show_power import ShowStackPower, ShowPowerInline
from genie.libs.parser.iosxe.show_crypto import ShowCryptoPkiCertificates


log = logging.getLogger(__name__)

class TriggerCheckCommands(CheckCommandsTemplate):
    '''Trigger for checking show commands action'''

    __description__ = """Check show commands to see if required status/values are matched.

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Check 'show switch detail'. Store active/standby switch,
           and full stack switches numbers if has any, otherwise, SKIP the trigger
        2. Check 'show inventory'. Store the image type ('Katana, Edison, Archimedes')
        3. Check 'show version'
        4. Check 'show redundancy'
        5. Check 'show module'
        6. Check 'show environment all'
        7. Check 'show platform'
        8. Check 'show stack-power' and 'show power inline <AP_connected_interface>'
           for Edison and Archimedes device
        9. Check 'show crypto pki certificates' for CISCO_IDEVID_SUDI and CISCO_IDEVID_SUDI_LEGACY
    """

    STACK_TYPE = {'AIR-CT5760':  'Katana',
                  'WS-C3850': 'Edison',
                  'WS-C3650': 'Archimedes'}

    @aetest.setup   # clean the cores after this section
    def stack_show_switch(self, uut, steps, timeout):
        '''check stack status.

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        # get output
        try:
            output = ShowSwitchDetail(device=uut).parse()
            self.full_stack = sorted(list(output['switch']['stack'].keys()))
        except Exception as e:
            self.skipped('Cannot get stack info from show switch', from_exception=e,
                         goto=['next_tc'])

        # get switch status and mode
        with steps.start('Get Active/Standby/Member switches '
          'which state is Ready', continue_=True) as step:
            requirements = {
                'active':
                   [['switch', 'stack', '(?P<stack>.*)','role', 'active'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'standby':
                   [['switch', 'stack', '(?P<stack>.*)','role', 'standby'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']],
                  'member':
                   [['switch', 'stack', '(?P<stack>.*)','role', 'member'],
                    ['switch', 'stack', '(?P<stack>.*)','state', 'ready']]
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show switch"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e, goto=['next_tc'])

        # check switch status and mode
        with steps.start('Check if Switches are all Ready', continue_=True) as step:
            try:
                verify_switches(keys_dict=ret, full_stack=self.full_stack)
            except Exception as e:
                step.failed("Not all switches up and Ready".format(requirements),
                                from_exception=e, goto=['next_tc'])

        # store active standby and full_stack information
        self.active = ret.get('active', {})[0].get('stack', '')
        self.standby = ret.get('standby', {})[0].get('stack', '')


        # Perform some SIF and Stack platform commands on active
        with steps.start('Perform some SIF and Stack '
          'platform commands on active', continue_=True) as step:

            uut.execute("show platform software sif switch %s R0 counters" % self.active)
            uut.execute("show platform software sif switch %s R0 topo" % self.active)
            uut.execute("show platform software stack-mgr switch %s R0 sdp-counters" % self.active)

    @aetest.test
    def stack_ha_redundancy_state(self, uut, steps, timeout):
        '''Checks if the stack comes to SSO.
           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            output = ShowRedundancy(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get stack info from show redundancy states', from_exception=e,
                         goto=['next_tc'])

        # get redundancy_state
        with steps.start('Get "sso" redundancy state, "Duplex" h/w mode, '
          'Up communications, ACTIVE/STANDBY HOT infomation', continue_=True) as step:
            requirements = {
                'active_state':
                   [['slot', 'slot {}'.format(self.active), 'curr_sw_state',
                     '(?P<active_state>ACTIVE)']],
                  'standby_state':
                   [['slot', 'slot {}'.format(self.standby), 'curr_sw_state',
                     '(?P<standby_state>STANDBY HOT)']],
                  'redundancy_mode':
                   [['red_sys_info', 'conf_red_mode', '(?P<redundancy_mode>sso)']],
                  'hw_mode':
                   [['red_sys_info', 'hw_mode', '(?P<hw_mode>Duplex)']],
                  'communications':
                   [['red_sys_info', 'communications', '(?P<communications>Up)']],
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show redundancy states"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e, goto=['next_tc'])

        # check redundancy_state to sso
        with steps.start('Perform Redundancy Check on Active IOS', continue_=True) as step:
            try:
                verify_requirements(reqs=requirements, keys_dict=ret)
            except Exception as e:
                step.failed("Could not reach SSO state".format(requirements),
                                from_exception=e, goto=['next_tc'])

    @aetest.test
    def verify_show_module (self, uut, steps, timeout):
        '''check module status. Ensure that the CLI shows the appropriate values

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            output = ShowModule(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get module info from show module', from_exception=e,
                         goto=['next_tc'])

        # get switch port/hw_ver/model/sw_ver/mac_address/serial_number
        with steps.start('Get port/hw_ver/model/sw_ver/mac_address'
          '/serial_number from all switches', continue_=True) as step:
            requirements = {
                'port':
                   [['switch', '(?P<stack>.*)','port', '(?P<port>.*)']],
                  'hw_ver':
                   [['switch', '(?P<stack>.*)','hw_ver', '(?P<hw_ver>.*)']],
                  'model':
                   [['switch', '(?P<stack>.*)','model', '(?P<model>.*)']],
                  'sw_ver':
                   [['switch', '(?P<stack>.*)','sw_ver', '(?P<sw_ver>.*)']],
                  'mac_address':
                   [['switch', '(?P<stack>.*)','mac_address', '(?P<mac_address>.*)']],
                  'serial_number':
                   [['switch', '(?P<stack>.*)','serial_number', '(?P<serial_number>.*)']],
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show module"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e)

        # check switch status and mode
        with steps.start('Check if all Switches have all information '
          'requires', continue_=True) as step:
            try:
                verify_requirements(reqs=requirements,
                                    full_stack=self.full_stack,
                                    keys_dict=ret)
            except Exception as e:
                step.failed("Show module output is not complete! Missing "
                  "switch number".format(requirements), from_exception=e)

    @aetest.test
    def verify_show_environment(self, uut, steps, timeout):
        '''Verify that all features of Platform manager are correctly functioning.

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            output = ShowEnvironmentAll(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get environment info from "show environment all"',
                from_exception=e)

        # get switch environment status
        with steps.start('Get system temperature state, fan state and power supply state'
          ' from all switches', continue_=True) as step:
            requirements = {
                'system_temperature_state':
                   [['switch', '(?P<stack>.*)','system_temperature_state',
                     '(?P<system_temperature_state>(ok|not present|invalid))']],
                'power_supply_state':
                   [['switch', '(?P<stack>.*)','power_supply', '(?P<ps>.*)',
                     'status', '(?P<power_supply_state>(ok|not present))']],
                'fan_state':
                   [['switch', '(?P<stack>.*)','fan', '(?P<fan>.*)', 'state',
                     '(?P<fan_state>(ok|not present))']],
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show environment all"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e)

        # check switch status and mode
        with steps.start('Check if all Switches have all '
          'information requires', continue_=True) as step:
            try:
                verify_requirements(reqs=requirements,
                                    full_stack=self.full_stack,
                                    keys_dict=ret)
            except Exception as e:
                step.failed("Show environment all output is not complete! "
                      "Missing switch number".format(requirements), from_exception=e)

    @aetest.test
    def verify_show_inventory(self, uut, steps, timeout):
        '''Verify show inventory. Ensure that the CLI shows the appropriate values

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            output = ShowInventory(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get info from "show inventory"',
                from_exception=e)

        # get switch inventory info
        with steps.start('Get PID, VID, and SN from "Active" Switch,'
          'and entries for all switches', continue_=True) as step:
            requirements = {
                'power_supply':
                   [['slot', '(?P<stack>.*)','other', '(?P<ps>.*)',
                     'name', '(?P<power_supply>.*)']],
                'active_pid':
                   [['slot', '%s' % self.active,'rp', '(.*)',
                     'pid', '(?P<pid>.*)']],
                'active_vid':
                   [['slot', '%s' % self.active,'rp', '(.*)',
                     'vid', '(?P<vid>.*)']],
                'active_sn':
                   [['slot', '%s' % self.active,'rp', '(.*)',
                     'sn', '(?P<sn>.*)']],
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show switch"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e)

        # check switch status and mode
        with steps.start('Check if all Switches have all information requires',
          continue_=True) as step:
            # check active switch pid vid and sn info
            for key in ['active_pid', 'active_vid','active_sn']:
                if key not in ret:
                    step.failed('%s is not available !' % key)
                else:
                    log.info('Active switch {s} {k} is {v}'.format(
                      s=self.active, k=key, v=ret[key]))
                    requirements.pop(key)

            pid = '-'.join(ret['active_pid'][0]['pid'].split('-')[:2])
            if pid in self.STACK_TYPE:
                log.info('{t} PID is detected'.format(t=self.STACK_TYPE[pid]))
                self.type = self.STACK_TYPE[pid]
            else:
                step.failed("Device PID is not detected")

            try:
                verify_requirements(reqs=requirements,
                                    full_stack=self.full_stack,
                                    keys_dict=ret)
            except Exception as e:
                step.failed("Show inventory output is not complete! "
                  "Missing switch number".format(requirements), from_exception=e)

    @aetest.test
    def verify_show_platform (self, uut, steps, timeout):
        '''Attempting Platform Manager: Log Check for show platform on Router

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            output = ShowPlatform(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get platform info from "show platform"',
                from_exception=e)

        # get switch environment status
        with steps.start('Get system platform infomration'
          ' from all switches', continue_=True) as step:
            requirements = {
                'slot_number':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'slot',
                     r'(?P<slot_number>\d+)']],
                'ports':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'ports',
                     r'(?P<ports>\d+)']],
                'model':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'name',
                     '(?P<model>.*)']],
                'serial_number':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'sn',
                     '(?P<serial_number>.*)']],
                'mac_address':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'mac_address',
                     '(?P<mac_address>.*)']],
                'hw_ver':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'hw_ver',
                     '(?P<hw_ver>.*)']],
                'sw_ver':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'sw_ver',
                     '(?P<sw_ver>.*)']],
                'role':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'role',
                     '(?P<role>(Active|Standby|Member))']],
                'priority':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'priority',
                     '(?P<priority>.*)']],
                'state':
                   [['slot', '(?P<stack>.*)','rp', '(.*)', 'state',
                     '(?P<state>.*)']],
                'switch_mac_address':
                   [['main', 'switch_mac_address', '(?P<switch_mac_address>.*)']],
                'mac_persistency_wait_time':
                   [['main', 'mac_persistency_wait_time', '(?P<mac_persistency_wait_time>.*)']],
            }
            try:
                ret = get_requirements(requirements=requirements, output=output)
            except Exception as e:
                step.failed("Cannot get stack required info from show platform"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e)

        # check switch status and mode
        with steps.start('Check if all Switches have all information '
          'requires', continue_=True) as step:
            # check active switch pid vid and sn info
            for key in ['switch_mac_address', 'mac_persistency_wait_time']:
                if key not in ret:
                    step.failed('Show platform output is not complete! '
                      'Missing {}'.format(key))
                else:
                    log.info('The {k} is {v}'.format(
                      k=key, v=ret[key]))
                    requirements.pop(key)

            try:
                verify_requirements(reqs=requirements,
                                    full_stack=self.full_stack,
                                    keys_dict=ret)
            except Exception as e:
                step.failed("Show platform output is not complete! Missing switch number".format(requirements),
                                from_exception=e)

    @aetest.test
    def verify_show_version (self, uut, steps, timeout):
        '''Platform Manager: Log Check for show version
           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        try:
            if hasattr(uut, 'workers'):
                with uut.allocate() as worker:
                    output = ShowVersion(device=worker).parse()
            else:
                output = ShowVersion(device=uut).parse()
        except Exception as e:
            self.skipped('Cannot get info from show version', from_exception=e,
                         goto=['next_tc'])

        # Check for Intermittent Issue
        with steps.start('Attempting to check message from show version', continue_=True) as step:
            expect_string = \
                'This product contains cryptographic features and is subject to United\n'\
                'States and local country laws governing import, export, transfer and\n'\
                'use. Delivery of Cisco cryptographic products does not imply\n'\
                'third-party authority to import, export, distribute or use encryption.\n'\
                'Importers, exporters, distributors and users are responsible for\n'\
                'compliance with U.S. and local country laws. By using this product you\n'\
                'agree to comply with applicable laws and regulations. If you are unable\n'\
                'to comply with U.S. and local laws, return this product immediately.\n'\
                '\n'\
                'A summary of U.S. laws governing Cisco cryptographic products may be found at:\n'\
                'http://www.cisco.com/wwl/export/crypto/tool/stqrg.html\n'\
                '\n'\
                'If you require further assistance please contact us by sending email to\n'\
                'export@cisco.com.\n'\
                '\n\n'\
                'Technology Package License Information:'

            log.info('Expected string is {}'.format(expect_string))

            for item in expect_string.splitlines():
                if item in uut.execute.result:
                    log.info('There is no corruption/missing data observed after Reload Reason. '
                             'Continuing Show Version testing...')
                else:
                    self.failed('Found missing string: {}'.format(item))

        # get version info
        with steps.start('Get version information', continue_=True) as step:
            req = {
                'copyright_or_technical_support':
                   [['version', 'image_type',
                     '(?P<copyright_or_technical_support>.*)']],
                  'rom':
                   [['version', 'rom', '(?P<rom>.*)']],
                  'boot_loader':
                   [['version', 'bootldr', '(?P<boot_loader>.*)']],
                  'host':
                   [['version', 'hostname', '(?P<host>.*)']],
                  'device_uptime':
                   [['version', 'uptime', '(?P<device_uptime>.*)']],
                  'control_processor_uptime':
                   [['version', 'uptime_this_cp', '(?P<control_processor_uptime>.*)']],
                  'reload_reason':
                   [['version', 'last_reload_reason', '(?P<reload_reason>.*)']],
                  'chassis':
                   [['version', 'chassis', '(?P<chassis>.*)']],
                  'memory':
                   [['version', 'main_mem', '(?P<memory>.*)']],
                  'processor_type':
                   [['version', 'processor_type', '(?P<processor_type>.*)']],
                  'processor_board_id':
                   [['version', 'chassis_sn', '(?P<processor_board_id>.*)']],
            }
            req_full_stack = {
                  'base_ethernet_mac_address':
                   [['version', 'switch_num', '(?P<stack>.*)', 'mac_address',
                     '(?P<base_ethernet_mac_address>.*)']],
                  'motherboard_assembly_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'mb_assembly_num',
                     '(?P<motherboard_assembly_number>.*)']],
                  'motherboard_serial_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'mb_sn',
                     '(?P<motherboard_serial_number>.*)']],
                  'model_revision_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'model_rev_num',
                     '(?P<model_revision_number>.*)']],
                  'motherboard_revision_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'mb_rev_num',
                     '(?P<motherboard_revision_number>.*)']],
                  'model_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'model_num',
                     '(?P<model_number>.*)']],
                  'system_serial_number':
                   [['version', 'switch_num', '(?P<stack>.*)', 'system_sn',
                     '(?P<system_serial_number>.*)']],
            }
            try:
                requirements = deepcopy(req)
                requirements.update(req_full_stack)
                ret = get_requirements(requirements=requirements,
                                       output=output)
            except Exception as e:
                step.failed("Cannot get version required info from show version"
                    "\nrequirements: {}".format(requirements),
                                from_exception=e)

        # Print the information
        with steps.start('Check and print the version info', continue_=True) as step:
            try:
                verify_requirements(reqs=req,
                                    keys_dict=ret, raise_exception=False)
                verify_requirements(reqs=req_full_stack,
                                    keys_dict=ret,
                                    raise_exception=False,
                                    full_stack=self.full_stack)
            except Exception as e:
                step.failed("Could not reach SSO state".format(requirements),
                                from_exception=e, goto=['next_tc'])

    @aetest.test
    def verify_show_power_inline (self, uut, steps, timeout):
        '''Platform Manager: Show power inline

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        try:
            output = ShowStackPower(device=uut).parse()
            entries = list(output['power_stack'].keys())
        except Exception as e:
            self.skipped('Cannot get platform info from "show stack-power"',
                from_exception=e)

        # Verification stack power switches num and stack switches num
        with steps.start('Verification stack power switches num and '
          'stack switches num', continue_=True) as step:
            if len(entries) != len(self.full_stack):
                self.failed('stack power switches: {n} vs stack switches: {n1}'\
                    .format(n=len(entries), n1=len(self.full_stack)))
            else:
                step.passed('stack power switches: {n} vs stack switches: {n1}'\
                    .format(n=len(entries), n1=len(self.full_stack)))

        # Extra debugging added by DEs request for a specific issue
        with steps.start('Extra debugging added by DEs request '
          'for a specific issue', continue_=True) as step:
            uut.execute("show stack-power detail")
            # this command is not supported anymore
            # uut.execute("test stack-power membership")

        if hasattr(self, 'type') and 'Kanata' in self.type:
            self.passed('Power check is not required! Inline power test case is skipped')

        # get switch environment status
        # TODO: will use lldp ops/parser to get interface which connecto to AP device
        intf = 'Gig1/0/13'
        with steps.start('Polling and verify inline power state '
          'for the interface {}'.format(intf),
          continue_=True) as step:
            while timeout.iterate():
                try:
                    output = ShowPowerInline(device=uut).parse(interface=intf)
                except Exception as e:
                    log.warning('Cannot get info from Parser\n{}'\
                        .format(traceback.format_exc()))
                    timeout.sleep()
                    continue

                requirements = {
                    'power_state':
                       [['interface', '(?P<interface>.*)','oper_state',
                         '(?P<power_state>on)']],
                    'power_budgeted_amount':
                       [['interface', '(?P<interface>.*)','power',
                         r'(?P<power_budgeted_amount>^(?!0)[\d\.]+)']],
                }
                try:
                    ret = get_requirements(requirements=requirements, output=output)
                except Exception as e:
                    log.warning('Cannot get required info from output\n{}'\
                        .format(traceback.format_exc()))
                    timeout.sleep()
                    continue

                # Verification of interface inline power state
                try:
                    verify_requirements(reqs=requirements,
                                        keys_dict=ret)
                except Exception as e:
                    log.warning('verify of inline power state is not all up\n{}'\
                        .format(traceback.format_exc()))
                    timeout.sleep()
                    continue
                else:
                    break
            else:
                self.failed('Cannot get power inline info from '
                  '"show power inline {}"'.format(intf))

    @aetest.test
    def verify_sudi_cert (self, uut, steps, timeout):
        '''Verify that SUDI certificates are installed in no more than timeout

           Args:
               uut (`obj`): Device object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        with steps.start('Checking the SUDI certificate in {t} seconds'\
          .format(t=int(timeout.timeout - time.time())), continue_=True) as step:
            while timeout.iterate():
                try:
                    output1 = ShowCryptoPkiCertificates(device=uut).\
                        parse(trustpoint_name='CISCO_IDEVID_SUDI')
                    output2 = ShowCryptoPkiCertificates(device=uut).\
                        parse(trustpoint_name='CISCO_IDEVID_SUDI_LEGACY')
                except Exception as e:
                    log.warning('Cannot get info from Parser\n{}'.format(traceback.format_exc()))
                    timeout.sleep()
                    continue

                req1 = {
                    'cisco_manufacturing_ca':
                       [['trustpoints', 'CISCO_IDEVID_SUDI', 'associated_trustpoints',
                         'certificate', 'issuer', 'cn',
                         '(?P<cisco_manufacturing_ca>^Cisco +Manufacturing +CA.*)']],
                    'cisco_root_ca':
                       [['trustpoints', 'CISCO_IDEVID_SUDI', 'associated_trustpoints',
                         'ca_certificate', 'issuer', 'cn',
                         '(?P<cisco_root_ca>^Cisco +Root +CA.*)']],
                }

                req2 = {
                    'cisco_manufacturing_ca':
                       [['trustpoints', 'CISCO_IDEVID_SUDI_LEGACY', 'associated_trustpoints',
                         'certificate', 'issuer', 'cn',
                         '(?P<cisco_manufacturing_ca>^Cisco +Manufacturing +CA.*)']],
                    'cisco_root_ca':
                       [['trustpoints', 'CISCO_IDEVID_SUDI_LEGACY', 'associated_trustpoints',
                         'ca_certificate', 'issuer', 'cn',
                         '(?P<cisco_root_ca>^Cisco +Root +CA.*)']],
                }
                try:
                    ret1 = get_requirements(requirements=req1, output=output1)
                    ret2 = get_requirements(requirements=req2, output=output2)
                except Exception as e:
                    log.warning('Cannot get required info from output\n{}'.format(traceback.format_exc()))
                    timeout.sleep()
                    continue

                # Verification of cn=Cisco Root CA and cn=Cisco Manufacturing CA
                try:
                    verify_requirements(reqs=req1, keys_dict=ret1)
                except Exception as e:
                    log.warning('Cannot find required info: {r}\n{e}'.format(r=req1, e=traceback.format_exc()))
                    timeout.sleep()
                    continue

                try:
                    verify_requirements(reqs=req2, keys_dict=ret2)
                except Exception as e:
                    log.warning('Cannot find required info: {r}\n{e}'.format(r=req2, e=traceback.format_exc()))
                    timeout.sleep()
                    continue
                else:
                    break
            else:
                self.failed('Failed to find the expected SUDI CA!!')

