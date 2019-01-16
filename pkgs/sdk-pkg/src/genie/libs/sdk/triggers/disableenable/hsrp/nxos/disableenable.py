'''NXOS implementation for hsrp disable/enable triggers'''

# import python
import time

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable


# Which key to exclude for HSRP Ops comparison
hsrp_exclude = ['maker']


class TriggerDisableEnableHsrp(TriggerDisableEnable):
    """Disable and enable feature hsrp when there is hsrp group(s)."""
    
    __description__ = """Disable and enable feature hsrp when there is hsrp group(s).

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
            static:
                The keys below are dynamically learnt by default.
                However, they can also be set to a custom value when provided in the trigger datafile.

                interface: `str`
                address_family: `str`
                version: `int`
                groups: `int`
                standby_router: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn HSRP Ops object and store the HSRP group(s)
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable HSRP feature with command "no feature hsrp"
           via HSRP Conf object
        4. Verify the state of feature hsrp is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature hsrp is "enabled" and 
           learn HSRP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.hsrp.hsrp.Hsrp':{
                            'requirements':[
                                ['info', '(?P<interface>.*)',\
                                 'address_family', '(?P<address_family>.*)',\
                                 'version', '(?P<version>.*)',\
                                 'groups', '(?P<groups>.*)',\
                                 'standby_router',\
                                 '(?P<standby_router>).*'],
                            ],
                            'exclude': hsrp_exclude}},
                      config_info={'conf.hsrp.Hsrp':{
                                     'requirements':[
                                        ['device_attr', '{uut}',\
                                         'enabled', True]],
                                     'verify_conf':False}})

    # feature name
    # used for creating checkpoint name and log information
    feature_name = 'hsrp_engine'
