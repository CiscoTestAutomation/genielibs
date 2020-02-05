'''IOSXE implementation for Reload triggers'''

# import python
import logging

# import pyats
from pyats import aetest
from pyats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.ha.ha import \
                       TriggerReload as CommonReload, \
                       TriggerReloadLc

# from genie.libs import parser
from genie.libs.parser.iosxe.show_platform import ShowPlatform

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'rp_uptime', 'sn', 'main_mem', 'issu',
                    'switchover_reason', 'config_register', 'chassis_sn',
                    'sn', 'name']


class TriggerReload(CommonReload):
    """Reload the whole device."""

    __description__ = """Reload the whole device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10

    steps:
        1. Learn Platform Ops object and store the "ok, active|ok, standby|Ready"
           switch(es) if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload"
        3. Learn Platform Ops again and verify the state of RP(s) is 
           "ok, active|ok, standby", verify every member status is "Ready",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'rp', '(?P<rp>.*)',
                                              'state', '(?P<state>ok, active|ok, standby|Ready)'],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'state', '(ok, active|ok, standby|Ready)'],
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'swstack_role', '(Active|Standby|Member)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all'})


class TriggerReloadWithPriority(TriggerReloadLc):

    @aetest.setup
    def verify_prerequisite(self, uut, abstract, steps, timeout):
        '''Learn Ops object and verify the requirements.

           If the requirements are not satisfied, then skip to the next
           testcase.

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object
               timeout (`timeout obj`): Timeout Object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        self.timeout = timeout
        try:
            self.pre_snap = self.mapping.learn_ops(device=uut,
                                                   abstract=abstract,
                                                   steps=steps,
                                                   timeout=self.timeout)
        except Exception as e:
            self.skipped('Cannot learn the feature', from_exception=e,
                         goto=['next_tc'])
            
        for stp in steps.details:
            if stp.result.name == 'skipped':
                self.skipped('Cannot learn the feature', goto=['next_tc'])

        self.print_local_verifications()

        # get and store the member priority list
        try:
            out = ShowPlatform(device=uut).parse()
            # inital priority storage
            priority_dict = {}
            priority_list = []
            if 'slot' in out:
                for slot in out['slot']:
                    for rp in out['slot'][slot]['rp']:
                        if out['slot'][slot]['rp'][rp]['role'] == 'Member':
                            priority_dict[slot] = \
                                out['slot'][slot]['rp'][rp]['priority']
                            priority_list.append(out['slot'][slot]['rp'][rp]['priority'])
                            
                if len(list(set(priority_list))) != 1:
                    # sorted the slot priority
                    # sorted with priority from low to high
                    # [(<switch_number>, <priority>)]
                    # [('2', '1'), ('3', '1'), ('1', '3')]
                    priority_list = sorted(priority_dict.items(), key=lambda x: x[1])

                    # update the verify_ops requirements
                    # The next standby switch will be the memeber
                    # with highest priority
                    for ops, requirements in self.mapping._verify_ops_dict.items():
                        if 'platform' in ops:
                            self.mapping._verify_ops_dict[ops]['requirements'].append(
                                ['slot', 'rp', '{}'.format(priority_list[-1][0]),
                                 'swstack_role', 'Standby'])
                else:                    
                    # update the verify_ops requirements
                    # If all memeber with same priority, the standby will be
                    # randomly from the members
                    for ops, requirements in self.mapping._verify_ops_dict.items():
                        if 'platform' in ops:
                            self.mapping._verify_ops_dict[ops]['requirements'].append(
                                ['slot', 'rp', '(?P<members>.*)',
                                 'swstack_role', '(Standby|Member)'])
        except Exception as e:
            log.warn('Cannot get the member priority. \n{}'.format(str(e)))


class TriggerReloadActiveRP(TriggerReloadWithPriority):
    """Reload active switch on device."""

    __description__ = """Reload active switch on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'active'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                active_rp: `str`
                standby_rp: `str`
                members: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                   OR
                   interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Platform Ops object and store the "active" and "standby" switch
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload slot <lc>"
        3. Learn Platform Ops again and verify the role of "active" switch changes to "standby",
           verify the role of "standby" switch changes to "member",
           verify the role of "member" switch with highest priority changes to "standby",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<active_rp>.*)',
                                              'swstack_role', 'Active'],
                                            ['slot', 'rp', '(?P<active_rp>.*)',
                                              'state', 'Ready']],
                                            [['slot', 'rp', '(?P<standby_rp>.*)',
                                              'swstack_role', 'Standby'],
                                            ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'Ready']],
                                            [['slot', 'rp', '(?P<members>.*)',
                                              'swstack_role', 'Member'],
                                            ['slot', 'rp', '(?P<members>.*)',
                                              'state', 'Ready']],
                                            [['redundancy_communication', True]],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<active_rp>.*)',
                                           'swstack_role', 'Member'],
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'swstack_role', 'Active']],
                                    'exclude': platform_exclude}},
                      num_values={'active_rp':1, 'standby_rp':1, 'members': 'all'})


class TriggerReloadStandbyRP(TriggerReloadWithPriority):
    """Reload standby switch on device."""

    __description__ = """Reload standby switch on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            lcRole (`str`): The role of LC which is 'standby'
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                standby_rp: `str`
                members: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                   OR
                   interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Platform Ops object and store the "standby" switch and "member" switch(es)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload slot <lc>"
        3. Learn Platform Ops again and verify role of "standby" switch changes to "member",
           verify the role of "member" switch with highest priority changes to "standby",
           and verify left attributes from the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            [['slot', 'rp', '(?P<standby_rp>.*)',
                                              'swstack_role', 'Standby'],
                                            ['slot', 'rp', '(?P<standby_rp>.*)',
                                              'state', 'Ready']],
                                            [['slot', 'rp', '(?P<members>.*)',
                                              'swstack_role', 'Member'],
                                            ['slot', 'rp', '(?P<members>.*)',
                                              'state', 'Ready']],
                                            [['redundancy_communication', True]],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<standby_rp>.*)',
                                           'swstack_role', 'Member']],
                                    'exclude': platform_exclude}},
                      num_values={'standby_rp':1, 'members': 'all'})


class TriggerReloadMember(TriggerReloadLc):
    """Reload member switch on device."""
    
    __description__ = """Reload member switch on device.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                members: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                   OR
                   interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Platform Ops object and store the "member" switch(es)
           if has any, otherwise, SKIP the trigger
        2. Do reload by command "reload slot <lc>"
        3. Learn Platform Ops again and the ops are the same as the Ops in step 1
        4. Update platform PTS if feature pts is enabled,
           Update global/local veirifications if enabled

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'rp', '(?P<members>.*)',
                                              'swstack_role', 'Member'],
                                            ['slot', 'rp', '(?P<members>.*)',
                                              'state', 'Ready']
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<members>.*)',
                                           'state', 'Ready']],
                                    'exclude': platform_exclude}},
                      num_values={'members': 1})