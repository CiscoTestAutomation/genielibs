'''Implementation for bgp modify triggers'''

# import python
import time
import collections

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.bgp import modify

class TriggerModifyBgpNeighborRoutemapIn(modify.TriggerModifyBgpNeighborRoutemapIn):
    """Modify and revert the inbound route-map for dynamically learned BGP neighbors(s)."""

    __description__ = """Modify and revert the inbound route-map for dynamically learned BGP neighbors(s).

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

                instance: `str`
                vrf: `vrf`
                neighbor: `str`
                address_family: `str`
                route_map: `str`
                bgp_id: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                    OR
                    interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn BGP Ops object and store the BGP neighbors(s) which has inbound route-map
           configured. SKIP the trigger if there is no BGP neighbors(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the inbound route-map of the learned BGP neighbor(s) from step 1
           with BGP Conf object
        4. Verify the inbound route-map of learned BGP neighbor(s) from step 3
           changes to the modified name in step 3
        5. Recover the device configurations to the one in step 2
        6. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    config_info = collections.OrderedDict()
    config_info['conf.route_policy.RoutePolicy'] =\
                     {'requirements':[],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'name': modify.TriggerModifyBgpNeighborRoutemapIn.new_name}}}

    config_info['conf.bgp.Bgp'] =\
                     {'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_in',
                                    modify.TriggerModifyBgpNeighborRoutemapIn.new_name]],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                          'address_family', '(?P<address_family>.*)',
                                                          'route_map_name_in', '(?P<route_map>.*)'],
                                                         ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True, 
                                        'kwargs':{'attributes':['info']},
                                        'exclude': modify.bgp_exclude}},
                      config_info=config_info,
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_in', modify.TriggerModifyBgpNeighborRoutemapIn.new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': modify.bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})


class TriggerModifyBgpNeighborRoutemapOut(modify.TriggerModifyBgpNeighborRoutemapOut):
    """Modify and revert the outbound route-map for dynamically learned BGP neighbors(s)."""

    __description__ = """Modify and revert the outbound route-map for dynamically learned BGP neighbors(s).

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

                    instance: `str`
                    vrf: `vrf`
                    neighbor: `str`
                    address_family: `str`
                    route_map: `str`
                    bgp_id: `int`

                    (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                        OR
                        interface: 'Ethernet1/1/1' (Specific value)

        steps:
            1. Learn BGP Ops object and store the BGP neighbors(s) which has inbound route-map
               configured. SKIP the trigger if there is no BGP neighbors(s) found
            2. Save the current device configurations through "method" which user uses
            3. Modify the outbound route-map of the learned BGP neighbor(s) from step 1
               with BGP Conf object
            4. Verify the outbound route-map of learned BGP neighbor(s) from step 3
               changes to the modified name in step 3
            5. Recover the device configurations to the one in step 2
            6. Learn BGP Ops again and verify it is the same as the Ops in step 1

        """

    config_info = collections.OrderedDict()
    config_info['conf.route_policy.RoutePolicy'] =\
                     {'requirements':[],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'name': modify.TriggerModifyBgpNeighborRoutemapOut.new_name}}}

    config_info['conf.bgp.Bgp'] =\
                     {'requirements':[['device_attr', '{uut}', 'vrf_attr', '(?P<vrf>.*)',
                                   'neighbor_attr','(?P<neighbor>.*)', 'address_family_attr',
                                   '(?P<address_family>.*)', 'nbr_af_route_map_name_out',
                                    modify.TriggerModifyBgpNeighborRoutemapOut.new_name]],
                      'verify_conf':False,
                      'kwargs':{'mandatory':{'bgp_id': '(?P<bgp_id>.*)'}}}

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                         'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                          '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                          'address_family', '(?P<address_family>.*)',
                                                          'route_map_name_in', '(?P<route_map>.*)'],
                                                         ['info', 'instance', '(?P<instance>.*)', 'bgp_id', '(?P<bgp_id>.*)']],
                                        'all_keys':True,
                                        'kwargs':{'attributes':['info']},
                                        'exclude': modify.bgp_exclude}},
                      config_info=config_info,
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements':[['info', 'instance', '(?P<instance>.*)', 'vrf',
                                                   '(?P<vrf>.*)', 'neighbor', '(?P<neighbor>.*)',
                                                   'address_family', '(?P<address_family>.*)',
                                                   'route_map_name_out', modify.TriggerModifyBgpNeighborRoutemapOut.new_name]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': modify.bgp_exclude}},
                      num_values={'vrf':1, 'instance':1, 'neighbor':1,
                                  'address_family':1})
