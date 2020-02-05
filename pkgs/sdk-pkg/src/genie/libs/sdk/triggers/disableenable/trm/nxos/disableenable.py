'''NXOS implementation for trm disable/enable triggers'''

# import python
import time

from pyats import aetest
# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.disableenable.disableenable import \
                                      TriggerDisableEnable
from pyats.utils.objects import NotExists

# Which key to exclude Ops comparison
trm_exclude = ['maker','uptime']

class TriggerDisableEnableNgmvpn(TriggerDisableEnable):
    """Disable and enable feature ngmvpn when it is enabled."""

    __description__ = """Disable and enable feature ngmvpn when it is enabled.

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
        1. Learn Vxlan Ops object and verify if ngmvpn is enabled, if not, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Disable nv overlay feature with command "no feature ngmvpn"
           via Vxlan Conf object
        4. Verify the state of feature ngmvpn overlay is "disabled"
        5. Recover the device configurations to the one in step 2
        6. Verify the state of feature nv overlay is "enabled" and
           learn Vxlan Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.vxlan.vxlan.Vxlan': {
                                        'requirements': [['nve', 'enabled_ngmvpn', True]],
                                                        'kwargs': {'attributes': ['nve[enabled_ngmvpn]']},
                                                        'all_keys': True,
                                                        'exclude': trm_exclude}},
                      config_info={'conf.vxlan.Vxlan': {
                                    'requirements': [['device_attr', '{uut}', 'enabled_ngmvpn', True]],
                                    'verify_conf': False}},
                      verify_ops={'ops.vxlan.vxlan.Vxlan': {
                                    'requirements': [['nve', 'enabled_ngmvpn', False]],
                                    'kwargs': {'attributes': ['nve[enabled_ngmvpn]']},
                                    'exclude': trm_exclude }},
                      num_values={})

    feature_name = 'ngmvpn'

