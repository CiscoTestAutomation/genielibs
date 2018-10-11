'''NXOS Implementation for BGP modify triggers'''

# python
import re
import logging

log = logging.getLogger(__name__)

# ATS
from ats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping, Different
from genie.libs.sdk.triggers.modify.modify import TriggerModify

# Keys to exclude during verify_modification steps
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'last_reset',
               'keepalives', 'total', 'total_bytes', 'up_time',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens',
               'bgp_table_version', 'holdtime', 'keepalive_interval',
               'route_reflector_client', 'capability',
               'distance_internal_as', 'bgp_neighbor_counters', 'memory_usage',
               'total_entries', 'routing_table_version', 'total_memory',
               'path', 'prefixes', 'cluster_id']


class TriggerModifyBgpKeepaliveHoldtime(TriggerModify):
    """
       Modify the keepalive interval and holdtime configured under BGP and then restore the
       configuration by reapplying the whole running configuration

       trigger_datafile:
           Mandatory Arguments:
               timeout:
                   max_time (`int`): Maximum wait time for the trigger in seconds.
                                     Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15
                   method (`str`): Method to recover the device configuration.
                                   Supported methods:
                                       'checkpoint': Rollback the configuration
                                                     using checkpoint (nxos),
                                                     archive file (iosxe),
                                                     load the saved running-config
                                                     file on disk (iosxr)
           Optional Arguments:
               tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                    restored to the reference rate in seconds.
                                    Default: 60
               tgn_delay (`int`): Wait time between each poll to verify if traffic
                                  is resumed in seconds. Default: 10
               timeout_recovery:
                   Buffer recovery timeout make sure devices are recovered at the
                   end of the trigger execution. Used when previous timeouts have
                   been exhausted.
                   max_time (`int`): Maximum wait time for the last step of the
                                     trigger in seconds. Default: 180
                   interval (`int`): Wait time between iteration when looping is
                                     needed in seconds. Default: 15

       Steps:
           1. Learn BGP Ops configured on device. SKIP the trigger if there
              is no BGP configured on the device.
           2. Save the current device configurations using "method" specified.
           3. Modify the keepalive interval of BGP  pid learned in step 1 using
              Genie BGP Conf.
           4. Verify the change to keepalive interval config under BGP is
              reflected in device configuration.
           5. Restore the device configuration to the original configuration saved
              in step 2.
           6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
       """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(\
                requirements={\
                    'conf.bgp.Bgp':{
                        'requirements': [\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval','(?P<keepalive_interval>.*)'],
                            ['device_attr','{uut}', '_vrf_attr','(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']],
                        'all_keys': True,
                        'exclude': bgp_exclude},
                    'ops.bgp.bgp.Bgp':{
                        'requirements': [\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs': {'attributes': ['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements': [\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', 10],
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'holdtime', 20]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements': [\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs': {'attributes': ['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements': [\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', 10],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime', 20]],
                        'exclude': bgp_exclude}},
                num_values={'device':1, 'bgp_id':1,'vrf':1, 'instance':1, 'neighbor':1})


class TriggerModifyBgpKeepAliveInterval(TriggerModify):

    """Modify the keepalive interval configured under BGP and then restore the
    configuration by reapplying the whole running configuration"""

    __description__ = """Modify the keepalive interval configured under BGP and then restore the
    configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the keepalive interval of BGP  pid learned in step 1 using
           Genie BGP Conf.
        4. Verify the change to keepalive interval config under BGP is
           reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval','(?P<keepalive_interval>.*)'],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']],
                        'all_keys':True, 
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', 10],
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']],
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'keepalive_interval', 10],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'holdtime', '(?P<holdtime>.*)']],
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpGracefulRestartRestartTime(TriggerModify):

    """Modify the graceful restart restart-time configured under BGP and then 
    restore the configuration by reapplying the whole running configuration"""

    __description__ = """Modify the graceful restart restart-time configured under BGP and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the graceful restart restart-time of BGP  pid learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to graceful restart restart-time config under BGP
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart_restart_time', '(?P<graceful_restart_restart_time>.*)']],
                        'all_keys': True,
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'graceful_restart_restart_time', 170]],
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart_restart_time', 170]],
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpGracefulRestartStalePathTime(TriggerModify):
    """Modify the graceful restart stalepath-time configured under BGP and then 
    restore the configuration by reapplying the whole running configuration"""

    __description__ = """Modify the graceful restart stalepath-time configured under BGP and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the graceful restart stalepath-time of BGP pid learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to graceful restart stalepath-time config under
           BGP is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys':True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart_stalepath_time', '(?P<graceful_restart_stalepath_time>.*)']],
                        'all_keys': True,
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'graceful_restart_stalepath_time', 170]],
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude},
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart', True],
                            ['device_attr', '{uut}', '_vrf_attr', '(?P<vrf>.*)', 'graceful_restart_stalepath_time', 170]],
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpNeighborKeepAliveInterval(TriggerModify):
    """Modify the keepalive interval configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration"""

    __description__ = """Modify the keepalive interval configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the keepalive interval of BGP neighbor learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to keepalive interval config under BGP neighbor
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    @aetest.test
    def modify_configuration(self, uut, abstract, steps):
        super().modify_configuration(uut, abstract, steps)

        # Flap neighbor for config change to take effect
        cmd = "router bgp (?P<bgp_id>.*)\n"\
              " vrf (?P<vrf>.*)\n"\
              "  neighbor (?P<neighbor>.*)\n"\
              "   shutdown\n"\
              "   no shutdown"
        x = re.findall(r'\S+|\n', cmd)
        req = self.mapping._path_population([x], uut)
        req_str = []
        for item in req[0]:
            req_str.append(str(item))

        # combine command
        cmd = ' '.join(req_str)
        cmd = cmd.replace('vrf default \n', '')
        try:
            uut.configure(cmd)
        except Exception as e:
            self.failed("Unable to configure: '{c}'".format(c=cmd),
                        from_exception=e)

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'holdtime', '(?P<holdtime>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'keepalive_interval', '(?P<keepalive_interval>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'kwargs':{'attributes':['info']},
                        'all_keys': True,
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_holdtime', '(?P<holdtime>.*)'],
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_keepalive_interval', 10]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'keepalive_interval', 10],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'holdtime', '(?P<holdtime>.*)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1, 'holdtime': 1})


class TriggerModifyBgpNeighborEbgpMultihop(TriggerModify):
    """Modify the EBGP multihop configured under BGP neighbor and then 
    restore the configuration by reapplying the whole running configuration"""

    __description__ = """Modify the EBGP multihop configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the EBGP multihop of BGP neighbor learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to EBGP multihop config under BGP neighbor
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'ebgp_multihop_max_hop', '(?P<max_hop>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'ebgp_multihop', True],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_ebgp_multihop', True],
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_ebgp_multihop_max_hop', 80]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'ebgp_multihop', True],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'ebgp_multihop_max_hop', 80]],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpNeighborUpdateSource(TriggerModify):
    """Modify the update source configured under BGP neighbor and then 
    restore the configuration by reapplying the whole running configuration"""

    __description__ = """Modify the update source configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the update source of BGP neighbor learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to update source config under BGP neighbor
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'update_source', '(?P<update_source>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True, 
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_update_source', 'loopback100']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'update_source', 'loopback100']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpNeighborMaximumPrefix(TriggerModify):
    """Modify the maximum prefixes configured under BGP neighbor and then 
    restore the configuration by reapplying the whole running configuration"""
    
    __description__ = """Modify the maximum prefixes configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the maximum prefixes of BGP neighbor learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to maximum prefixes config under BGP neighbor
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'maximum_prefix_max_prefix_no', '(?P<maximum_prefix_max_prefix_no>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr', '(?P<neighbor>.*)', 'address_family_attr', '(?P<address_family>.*)', 'nbr_af_maximum_prefix_max_prefix_no', 163]],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'maximum_prefix_max_prefix_no', 163],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpNeighborPassword(TriggerModify):
    """Modify the password configured under BGP neighbor and then 
    restore the configuration by reapplying the whole running configuration"""
    
    __description__ = """Modify the password configured under BGP neighbor and then
    restore the configuration by reapplying the whole running configuration

    trigger_datafile:
        Mandatory Arguments:
            timeout:
                max_time (`int`): Maximum wait time for the trigger in seconds.
                                  Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15
                method (`str`): Method to recover the device configuration.
                                Supported methods:
                                    'checkpoint': Rollback the configuration
                                                  using checkpoint (nxos),
                                                  archive file (iosxe),
                                                  load the saved running-config
                                                  file on disk (iosxr)
        Optional Arguments:
            tgn_timeout (`int`): Maximum wait time for all traffic streams to be
                                 restored to the reference rate in seconds.
                                 Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic
                               is resumed in seconds. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the
                end of the trigger execution. Used when previous timeouts have
                been exhausted.
                max_time (`int`): Maximum wait time for the last step of the
                                  trigger in seconds. Default: 180
                interval (`int`): Wait time between iteration when looping is
                                  needed in seconds. Default: 15

    Steps:
        1. Learn BGP Ops configured on device. SKIP the trigger if there
           is no BGP configured on the device.
        2. Save the current device configurations using "method" specified.
        3. Modify the password of BGP neighbor learned in
           step 1 using  Genie BGP Conf.
        4. Verify the change to password config under BGP neighbor
           is reflected in device configuration.
        5. Restore the device configuration to the original configuration saved
           in step 2.
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1.
    """

    @aetest.test
    def modify_configuration(self, uut, abstract, steps):

        super().modify_configuration(uut, abstract, steps)

        # Flap neighbor for config change to take effect
        cmd = "router bgp (?P<bgp_id>.*)\n"\
              " vrf (?P<vrf>.*)\n"\
              "  neighbor (?P<neighbor>.*)\n"\
              "   shutdown\n"\
              "   no shutdown"
        x = re.findall(r'\S+|\n', cmd)
        req = self.mapping._path_population([x], uut)
        req_str = []
        for item in req[0]:
            req_str.append(str(item))

        # combine command
        cmd = ' '.join(req_str)
        cmd = cmd.replace('vrf default \n', '')
        try:
            uut.configure(cmd)
        except Exception as e:
            self.failed("Unable to configure: '{c}'".format(c=cmd),
                        from_exception=e)

    bgp_exclude = bgp_exclude + ['distance_local']

    mapping = Mapping(\
                requirements={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'password_text', '(?P<password_text>.*)'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'session_state', 'established'],
                            ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                        'all_keys': True,
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                config_info={\
                    'conf.bgp.Bgp':{
                        'requirements':[\
                            ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)', 'neighbor_attr','(?P<neighbor>.*)', 'nbr_password_text', 'asgrocks']],
                        'verify_conf':False,
                        'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}},
                verify_ops={\
                    'ops.bgp.bgp.Bgp':{
                        'requirements':[\
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'session_state', 'idle'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'address_family', '(?P<address_family>.*)', 'session_state', 'idle'],
                            ['info', 'instance', '(?P<instance>.*)', 'vrf', '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)', 'password_text', 'set (disabled)']],
                        'kwargs':{'attributes':['info']},
                        'exclude': bgp_exclude}},
                num_values={'instance':1, 'vrf':1, 'neighbor':1})


class TriggerModifyBgpVpnRd(TriggerModify):
    """Modify  dynamically learned BGP vrf(s) route-distinguisher."""

    __description__ = """Modify  dynamically learned BGP vrf(s) route-distinguisher.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery: 
                Buffer recovery timeout when the previous timeout has been exhausted,
                to make sure the devices are recovered before ending the trigger

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn BGP Ops object and store the BGP vrf(s) with route_distinguisher
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the learned BGP vrf(s) route-distinguisher from step 1 
           with BGP Conf object
        4. Verify the BGP vrf(s) route_distinguisher from step 3 are changed
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """
    MODIFY_RD = "1:1"

    @aetest.test
    def verify_modification(self, uut, abstract, steps):
        # modify self.keys to modify the address_family value
        for item in self.mapping.keys:
            try:
                ret = item['address_family'].split()
                ret[-1] = self.MODIFY_RD
                item['address_family'] = ' '.join(ret)
            except Exception:
                log.warning('Cannot modify address family RD information.'
                             'Mismatch is expected')

        super().verify_modification(uut, abstract, steps)

    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['table', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'route_distinguisher',
                                                           '(?P<rd>.*)'],
                                                           ['table', 'instance', '(?P<instance>.*)',
                                                           'vrf', '(?P<vrf>.*)', 'address_family',
                                                           '(?P<address_family>.*)', 'default_vrf',
                                                           '(?P<name>^(?!L3|vpn).*)']],
                                        'kwargs':{'attributes':['table', 'info']},
                                        'all_keys': True,
                                        'exclude': bgp_exclude},
                                    'ops.vrf.vrf.Vrf':{
                                          'requirements':[['info', 'vrfs', '(?P<name>^(?!default).*)',
                                                           'route_distinguisher', '(?P<rd>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': ['maker']}},
                      config_info={'conf.vrf.Vrf':{
                                     'requirements':[['device_attr', '{uut}', 'rd', MODIFY_RD]],
                                     'verify_conf':False,
                                     'kwargs':{'mandatory':{'name': '(?P<name>.*)'}}}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['table', 'instance', '(?P<instance>.*)',
                                                     'vrf', '(?P<vrf>.*)', 'address_family',
                                                     '(?P<address_family>.*)', 'route_distinguisher', MODIFY_RD]],
                                    'kwargs':{'attributes':['table', 'info']},
                                    'exclude': bgp_exclude + ['label_allocation_mode']},
                                  'ops.vrf.vrf.Vrf':{
                                        'requirements':[['info', 'vrfs', '(?P<name>.*)',
                                                         'route_distinguisher', MODIFY_RD]],
                                      'kwargs':{'attributes':['info']},
                                      'exclude': ['maker']}},
                      num_values={'vrf': 1, 'instance':1, 
                                  'address_family': 'all', 'rd': 1, 'name': 1})
