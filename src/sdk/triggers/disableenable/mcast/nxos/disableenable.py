'''NXOS implementation for Mcast disable/enable triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable


# Which key to exclude for Mcast Ops comparison
mcast_exclude = ['maker']


class TriggerDisableEnablePim(TriggerDisableEnable):
    """Disable and enable feature Pim."""
    
    __description__ = """Disable and enable feature Pim.

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
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Mcast Ops object and store the Mcast vrf(s) with ipv4 feature enabled
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable pim feature with command "no feature pim"
           via Mcast Conf object
        4. Verify the state of feature pim is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature pim is "enabled" and 
           learn Mcast Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                        'requirements':[\
                                            ['info', 'vrf', '(?P<vrf>.*)', 'address_family', 'ipv4', 'enable', True]],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': mcast_exclude}},
                      config_info={'conf.mcast.Mcast':{
                                    'requirements':[['device_attr', '{uut}', 'vrf_attr', None, 'address_family_attr', 'ipv4', 'enabled', True]],
                                    'verify_conf':False}},
                      verify_ops={'ops.mcast.mcsat.Mcast':{
                                    'requirements':[\
                                        ['info', 'vrf', '(?P<vrf>.*)', 'address_family', 'ipv4', 'enable', False]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': mcast_exclude}})
    # feature name
    # used for creating checkpoint name and log information
    feature_name = 'pim'


class TriggerDisableEnablePim6(TriggerDisableEnable):
    """Disable and enable feature Pim6.

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
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn Mcast Ops object and store the Mcast vrf(s) with ipv6 feature enabled
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable pim6 feature with command "no feature pim6"
           via Mcast Conf object
        4. Verify the state of feature pim6 is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature pim6 is "enabled" and 
           learn Mcast Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.mcast.mcast.Mcast':{
                                        'requirements':[\
                                            ['info', 'vrf', '(?P<vrf>.*)', 'address_family', 'ipv6', 'enable', True]],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': mcast_exclude}},
                      config_info={'conf.mcast.Mcast':{
                                    'requirements':[['device_attr', '{uut}', 'vrf_attr', None, 'address_family_attr', 'ipv6', 'enabled', True]],
                                    'verify_conf':False}},
                      verify_ops={'ops.mcast.mcsat.Mcast':{
                                    'requirements':[\
                                        ['info', 'vrf', '(?P<vrf>.*)', 'address_family', 'ipv6', 'enable', False]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': mcast_exclude}})
    # feature name
    # used for creating checkpoint name and log information
    feature_name = 'pim6'