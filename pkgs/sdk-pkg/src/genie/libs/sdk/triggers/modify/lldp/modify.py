'''Implementation for LLDP modify triggers'''

# import python
import time
import logging
from collections import OrderedDict

# import ATS
from pyats import aetest
from pyats.datastructures.logic import Not
from pyats.utils.objects import find, R

# import genie.libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify
from genie.libs.sdk.libs.utils.normalize import GroupKeys


# Which key to exclude for LLDP Ops comparison
lldp_exclude = ['maker', 'counters', 'management_address']

log = logging.getLogger(__name__)

class TriggerModifyLldpTimer(TriggerModify):
    """Modify and revert the LLDP timer"""

    __description__ = """Modify and revert the LLDP timer.

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
        1. Learn LLDP Ops object to check if LLDP enabled on peer routers,
           otherwise SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Modify the LLDP timer to user defined value with LLDP Conf object on peer routers
        4. Verify the LLDP timer from step 3
           changes to the modified value in step 3,
           verify LLDP neighbors are not changed
        5. Recover the device configurations to the one in step 2
        6. Learn LLDP Ops again and verify it is the same as the Ops in step 1

    """

    mapping = Mapping(requirements={'ops.lldp.lldp.Lldp': {
                                       'requirements':[\
                                            ['info', 'enabled', True],
                                            ['info', 'interfaces', '(?P<intf>.*)',
                                             'neighbors', '(?P<peer>.*)', 'neighbor_id', '(?P<neighbor>.*)']
                                        ],
                                       'all_keys': True,
                                       'kwargs':{'attributes':['info[enabled]',
                                                               'info[interfaces][(.*)][neighbors][(.*)]']},
                                       'exclude': lldp_exclude}},
                      config_info={'conf.lldp.Lldp':{
                                     'requirements':[['device_attr', '{uut}', 'hello_timer', 5]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.lldp.lldp.Lldp':{
                                    'requirements':[['info', 'hello_timer', 5],],
                                    'kwargs':{'attributes':['info[hello_timer]',
                                                            'info[enabled]',
                                                            'info[interfaces][(.*)][neighbors][(.*)]']},
                                    'exclude': lldp_exclude}},
                      num_values={'intf': 'all', 'neighbor': 1, 'peer': 'all'})
