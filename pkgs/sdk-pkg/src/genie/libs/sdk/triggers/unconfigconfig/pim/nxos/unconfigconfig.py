'''NXOS Implementation for Pim unconfigconfig triggers'''

# ats
from pyats.utils.objects import NotExists


# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

# Which key to exclude for Pim Ops comparison
pim_exclude = ['maker', ]


class TriggerUnconfigConfigPimNeighborFilter(TriggerUnconfigConfig):
    """Unconfigure and reapply the whole configurations of dynamically
    learned PIM interface(s)'s neighbor-filter."""

    __description__ = """Unconfigure and reapply the whole configurations of dynamically
    learned PIM interface(s)'s neighbor-filter.

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

                vrf: `str`
                interface: `str`
                address_family: `str`
                neighbor_filter: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)
    steps:
        1. Learn Pim Ops object and store the "up" PIM interface(s)'s neighbor-filter
           if has any, otherwise, SKIP the trigger
        2. Save the current device configurations through "method" which user uses
        3. Unconfigure the learned PIM interface(s)'s neighbor-filter from step 1 
           with Pim Conf object
        4. Verify the PIM interface(s)'s neighbor-filter from step 3
           are no longer existed
        5. Recover the device configurations to the one in step 2
        6. Learn Pim Ops again and verify it is the same as the Ops in step 1

    """
    # Mapping of Information between Ops and Conf
    # Also permit to dictate which key to verify
    mapping = Mapping(requirements={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'address_family', '(?P<address_family>.*)',
                                     'neighbor_filter', '(?P<neighbor_filter>.*)'],
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'address_family', '(?P<address_family>.*)',
                                     'oper_status', 'up']],
                                'kwargs':{'attributes': [
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbor_filter]']},
                                'exclude': pim_exclude}},
                      config_info={'conf.pim.Pim':{
                                       'requirements':[
                                         ['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                          'address_family_attr', '(?P<address_family>.*)', 'interface_attr',
                                          '(?P<interface>.*)', 'neighbor_filter', '(?P<neighbor_filter>.*)']],
                                       'verify_conf':False,
                                       'kwargs':{}}},
                      verify_ops={
                          'ops.pim.pim.Pim':{
                                'requirements':[\
                                    ['info', 'vrf', '(?P<vrf>.*)', 'interfaces',
                                     '(?P<interface>.*)', 'address_family', '(?P<address_family>.*)',
                                     NotExists('neighbor_filter')]],
                                'kwargs':{'attributes': [
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][oper_status]',
                                    'info[vrf][(.*)][interfaces][(.*)][address_family][(.*)][neighbor_filter]']},
                                'exclude': pim_exclude}},
                      num_values={'vrf': 1, 'address_family': 1, 'interface': 1})

