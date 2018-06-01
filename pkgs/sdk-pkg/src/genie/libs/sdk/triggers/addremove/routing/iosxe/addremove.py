'''IOSXE Implementation for routing addremove triggers'''

# python
from functools import partial

# import genie.libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove
from genie.libs.sdk.libs.abstracted_libs.processors import traceroute_loopback

# ATS
from ats import aetest
from ats.utils.objects import NotExists

# Which key to exclude for BGP Ops comparison
routing_exclude = ['maker', 'attributes']


class TriggerAddRemoveIpv4StaticRoutes(TriggerAddRemove):
    """Apply the ipv4 static routing to device, and remove the
    added ipv4 static routing.
    """

    __description__ = """Apply the ipv4 static routing to device, and remove the
    added ipv4 static routing.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn static_routing Ops object and store the routes info if has any.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of static routing with static_routing Conf object
        4. Verify the static_routing from step 3 has configured
        5. Remove the static_routing configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn static_routing Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ROUTE = '0.0.0.0/0'
    AF = 'ipv4'

    # will move below to datafile when subsection 
    # prepost processors passing from datafile suppported

    traceroute_info = [{'src': 'uut',
                        'dest': 'helper',
                        'protocol': AF,
                        'dest_route': '{next_hop}',
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'peer_num': 1}]

    @aetest.processors.post(partial(traceroute_loopback, traceroute_args=traceroute_info))
    @aetest.test
    def verify_configuration(self, uut, abstract, steps): 

        # replace the traceroute_info if has any
        if hasattr(self, 'traceroute_info'):
            for item_args in self.traceroute_info:
                for keys in self.mapping.keys:
                    item_args['dest_route'] = keys['next_hop']         
        super().verify_configuration(uut, abstract, steps)


    mapping = Mapping(requirements={'ops.static_routing.static_routing.StaticRoute':{
                                            'requirements':[['info', 'vrf', '(?P<vrf>.*)',
                                                             'address_family', AF,
                                                             'routes', NotExists(ADD_ROUTE)],
                                                            [NotExists('info')]],
                                            'kwargs':{'attributes':['info[vrf][(.*)][address_family][(.*)]']},
                                            'exclude': routing_exclude}},
                      config_info={'conf.static_routing.StaticRouting':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'vrf_attr', 'default',
                                                       'address_family_attr',AF,
                                                       'route_attr', ADD_ROUTE,
                                                       'next_hop_attr', '(?P<next_hop>.*)']],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.static_routing.static_routing.StaticRoute':{
                                      'requirements': [['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'active', True],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'index', 1],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'next_hop', '(?P<next_hop>.*)'],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list',  1, 'preference', 1],

                                                       ['info', 'vrf', 'default',
                                                        'address_family', AF,
                                                        'routes', ADD_ROUTE, 'route', ADD_ROUTE]],
                                            'kwargs':{'attributes':['info[vrf][(.*)][address_family][(.*)]']},
                                      'exclude': routing_exclude}},
                      num_values={'vrf':1, 'route': 'all'})


class TriggerAddRemoveIpv6StaticRoutes(TriggerAddRemoveIpv4StaticRoutes):
    """Apply the ipv6 static routing to device, and remove the
    added ipv6 static routing.
    """

    __description__ = """Apply the ipv6 static routing to device, and remove the
    added ipv6 static routing.

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iterations when looping is needed,
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
                interval (`int`): Wait time between iterations when looping is needed,
                                in second. Default: 15

    steps:
        1. Learn static_routing Ops object and store the routes info if has any.
        2. Save the current device configurations through "method" which user uses
        3. Add the configuration of static routing with static_routing Conf object
        4. Verify the static_routing from step 3 has configured
        5. Remove the static_routing configurations.
        6. Recover the device configurations to the one in step 2
        7. Learn static_routing Ops again and verify it is the same as the Ops in step 1

    """
    ADD_ROUTE = '::/0'
    AF = 'ipv6'

    
    traceroute_info = [{'src': 'uut',
                        'dest': 'helper',
                        'protocol': AF,
                        'dest_route': '(?P<next_hop>.*)',
                        'timeout_interval': 5,
                        'timeout_max_time': 60,
                        'peer_num': 1}]
    
    @aetest.processors.post(partial(traceroute_loopback, traceroute_args=traceroute_info))
    @aetest.test
    def verify_configuration(self, uut, abstract, steps):
        super().verify_configuration(uut, abstract, steps)

    mapping = Mapping(requirements={'ops.static_routing.static_routing.StaticRoute':{
                                            'requirements':[['info', 'vrf', '(?P<vrf>.*)',
                                                             'address_family', AF,
                                                             'routes', NotExists(ADD_ROUTE)],
                                                            [NotExists('info')]],
                                            'kwargs':{'attributes':['info[vrf][(.*)][address_family][(.*)]']},
                                            'exclude': routing_exclude},
                                    'ops.routing.routing.Routing':{
                                            'requirements':[['info', 'vrf', '(?P<vrf>.*)',
                                                             'address_family', AF, 'routes',
                                                             '(?P<route>.*)', 'source_protocol', 'connected'],
                                                            ['info', 'vrf', '(?P<vrf>.*)',
                                                             'address_family', AF, 'routes',
                                                             '(?P<route>.*)', 'next_hop', 'outgoing_interface',
                                                             '(?P<out_intf>.*)', 'outgoing_interface', '(?P<out_intf>.*)']],
                                            'kwargs': {'attributes': ['info[vrf][(.*)][address_family][ipv6][routes][(.*)]']},
                                            'exclude': routing_exclude}},
                      config_info={'conf.static_routing.StaticRouting':{
                                      'requirements':[['device_attr', '{uut}',
                                                       'vrf_attr', 'default',
                                                       'address_family_attr',AF,
                                                       'route_attr', ADD_ROUTE,
                                                       'next_hop_attr', '(?P<next_hop>.*)']],
                                      'verify_conf':False,
                                      'kwargs':{}}},
                      verify_ops={'ops.static_routing.static_routing.StaticRoute':{
                                      'requirements': [['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'active', True],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'index', 1],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list', 1, 'next_hop', '(?P<next_hop>.*)'],

                                                       ['info', 'vrf', 'default', 'address_family', AF,
                                                        'routes', ADD_ROUTE, 'next_hop',
                                                        'next_hop_list',  1, 'preference', 1],

                                                       ['info', 'vrf', 'default',
                                                        'address_family', AF,
                                                        'routes', ADD_ROUTE, 'route', ADD_ROUTE]],
                                      'kwargs':{'attributes':['info[vrf][(.*)][address_family][(.*)]']},
                                      'exclude': routing_exclude}},
                      num_values={'vrf':1, 'route': 'all'})