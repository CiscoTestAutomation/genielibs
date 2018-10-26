# Python
import os
import re
import time
import yaml
import copy
import logging

# Ats
from ats.log.utils import banner
from ats.utils.objects import find, R, NotExists

# import pcall
from ats.async import pcall

# Abstract
from genie.abstract import Lookup

# Genie
from genie.utils.timeout import Timeout

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# genie.libs
from  genie.libs import ops
from  genie.libs import sdk
from genie.libs import parser
from genie.libs.sdk.libs.utils.normalize import GroupKeys


log = logging.getLogger(__name__)

def sleep_processor(section):
    '''Sleep prepostprocessor

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile
    '''

    if section and getattr(section, 'parameters', {}):
        sleep_time = section.parameters.get('sleep', None)
        if sleep_time:
            log.info("Sleeping for '{t}' seconds before "
                     "executing the testcase".format(t=sleep_time))
            time.sleep(sleep_time)

def learn_free_interfaces(section, configs):
    '''Learn from the system to find free unassigned interfaces
       (This is for Jonathan iosxe yang/cli comparator requirements)

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        configs (`dict`) : Contains the configuration file location

    Returns:
        AETEST results


    Raises:
        None

    '''

    if section and getattr(section, 'parameters', {}):

        testbed = section.parameters.get('testbed', {})
        uut = testbed.devices['uut']

        if os.path.isfile(configs):
            configs = yaml.load(open(configs))
        elif isinstance(configs, str):
            module = Lookup.from_device(uut)
            path = configs.split('.')
            for item in path:
                module = getattr(module, item)
            configs = module
        else:
            section.skipped('The configs type {} is not supported'
                .format(type(configs)))

        lookup = Lookup.from_device(uut)
        # learn the lldp neighbors
        if not hasattr(uut, 'lldp_mapping'):
            log.info(banner('Learn LLDP Neighbors'))
            # inital lldp ops object
            lldp_ops = lookup.ops.lldp.lldp.Lldp(uut,
                          attributes=['info[interfaces][(.*)][neighbors][(.*)][port_id]'])

            # learn the lldp ops
            try:
                lldp_ops.learn()
            except Exception as e:
                section.passx('Cannot learn lldp information',
                            from_exception=e)
            # store the lldp information
            uut.lldp_mapping = lldp_ops.info['interfaces']

        # find peer
        log.info(banner('Find {u} neighbors'))
        try:
            peer = sorted(configs.get('devices', {}))
            peer.remove('uut')
            peer = peer[0]
            peer_dev = testbed.devices[peer]
        except Exception as e:
            section.failed('Cannot find peer neighbors')

        log.info(banner('Find {u} interfaces connect to neighbor {p}'.format(u=uut.name, p=peer.name)))
        # find peer connection interfaces
        rs = R(['(?P<local_intf>.*)', 'neighbors', peer, 'port_id', '(?P<peer_intf>.*)'])
        ret = find([uut.lldp_mapping], rs, filter_=False, all_keys=True)
        if ret:
            values = GroupKeys.group_keys(
                        reqs=rs.args, ret_num={},  source=ret, all_keys=True)
        else:
            section.failed('No Peer inerface Found between {s} and {d}'.format(s=uut.name, d=peer))

        # get free(unassigned) interfaces
        log.info(banner('Find {u} free connected interfaces from {l}'.format(u=uut.name, l=values)))
        try:
            ip_out = lookup.parser.show_interface.ShowIpInterfaceBrief(uut).parse()
            ip_out_peer = lookup.parser.show_interface.ShowIpInterfaceBrief(peer_dev).parse()
        except Exception as e:
            section.failed('Cannot get information from show ip/ipv6 interface brief',
                from_exception=e)

        # initial local and peer intf
        local_intf = None
        peer_intf = None

        for item in values:
            if 'unassigned' in ip_out['interface'][item['local_intf']]['ip_address'] and \
               'unassigned' in ip_out_peer['interface'][item['peer_intf']]['ip_address'] :
               local_intf = item['local_intf']
               peer_intf = item['peer_intf']
               break

        # replace the configure data with learnt interfaces
        if local_intf and peer_intf:
            uut.local_intf = local_intf
            peer_dev.peer_intf = peer_intf
            for num, conf in sorted(configs['devices']['uut'].items()):
                conf['config'] = conf['config'].format(intf=local_intf)
                conf['unconfig'] = conf['unconfig'].format(intf=local_intf)
            for num, conf in sorted(configs['devices'][peer].items()):
                conf['config'] = conf['config'].format(intf=peer_intf)
                conf['unconfig'] = conf['unconfig'].format(intf=peer_intf)

def load_config_precessor(section, configs, unconfig=False, sleep=None):
    '''load configuration prepostprocessor

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        configs (`dict`) : Contains the configuration file location
        unconfig (`bool`) : True when apply the unconfigurations
                            Default as False
        sleep (`int`) : Sleep time after unconfiguration.

    Returns:
        AETEST results


    Raises:
        None

    '''
    log.info(banner('Load {} on devices'.format(
        'configurations' if not unconfig else 'unconfigurations')))

    if section and getattr(section, 'parameters', {}):

        testbed = section.parameters.get('testbed', {})
        # get uut in case there is need to store hardcode values
        uut = testbed.devices['uut']

        if os.path.isfile(configs):
            configs = yaml.load(open(configs))
        elif isinstance(configs, str):
            module = Lookup.from_device(uut)
            path = configs.split('.')
            for item in path:
                module = getattr(module, item)
            configs = module
        else:
            section.skipped('The configs type {} is not supported'
                .format(type(configs)))

        # copy dictionary without changing original configs
        # due to reuse it with conf/unconfig
        tmp_config = copy.deepcopy(configs)

        # Get hardcode values from uut
        for key, val in sorted(configs['devices']['uut'].items()):
            if not key.isdigit():
                if hasattr(section, 'mapping'):
                    # check if device
                    if key == 'peer':
                        uut.peer = testbed.devices[val]
                        tmp_config['devices']['uut'].pop(key)
                        continue                
                    section.mapping.requirements.setdefault('provided_values', {}).setdefault(key, val)
                tmp_config['devices']['uut'].pop(key)

        for dev in sorted(configs.get('devices', {})):

            device = testbed.devices[dev]
            
            # Sort the item; it is expected to be 
            # Sort them by the key, which needs to be an inter
            # 1, 2, 3, and so on
            for num, conf in sorted(tmp_config['devices'][dev].items()):
                if unconfig and 'unconfig' in conf:
                    conf['config'] = conf['unconfig']

                # replace the format syntax if has any
                conf['config'] = conf['config'].format(
                    **section.mapping.requirements.get('provided_values', {}) 
                        if hasattr(section, 'mapping') else {})

                log.info(banner("Applying configuration on '{d}'".format(d=device.name)))
                if os.path.isfile(conf['config']):
                    if 'invalid' not in conf:
                        # Set default
                        conf['invalid'] = []
                    try:
                        device.tftp.copy_file_to_device(device=device,
                                                        filename=conf['config'],
                                                        location='running-config',
                                                        vrf='management',
                                                        invalid=conf['invalid'])
                    except Exception as e:
                        log.error(str(e))
                        section.failed("Issue while applying the configuration "
                                    "on {d}".format(d=dev))
                elif isinstance(conf['config'], str):
                    try:
                        # Do you wish to continue? [yes]:
                        dialog = Dialog([
                            Statement(pattern=r'\[startup\-config\]\?.*',
                                                action='sendline()',
                                                loop_continue=True,
                                                continue_timer=False),
                            Statement(pattern=r'\[yes]\:.*',
                                                action='sendline()',
                                                loop_continue=True,
                                                continue_timer=False)
                        ])
                        device.configure(conf['config'], reply=dialog)
                    except Exception as e:                        
                        log.error(str(e))
                        section.failed("Issue while applying the configuration "
                                    "on {d}".format(d=dev))
                else:
                    section.failed('The configs type {} is not supported'
                        .format(type(conf['config'])))

                # sleep for x amount of time after
                if 'sleep'in conf and not unconfig:
                    log.info("Sleeping for '{s}' "
                             "seconds for waiting system is stable "
                             "after loading the configuration".format(s=conf['sleep']))
                    time.sleep(conf['sleep'])
        # extral sleep if sleep in config file is not enough
        # can change it from trigger yaml
        time.sleep(sleep) if sleep else None

def ping_devices(section, ping_parameters, expect_result='passed'):
    '''PING prepostprocessor. Will ping two ends ip addresses 
    from given devices ( learned by alias )

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        ping_parameters (`list`) : list of ping needed parameters

    Returns:
        AETEST results


    Raises:
        None

    '''
    log.info(banner('Dynamic learn the source and destination devices routing\n'
        'information and issue pings to see if the passing percentage is expected'))
    # Get ping ip and vrf     
    if not section or not getattr(section, 'parameters', {}):
        return

    # get testbed object
    testbed = section.parameters.get('testbed', {})

    # store the learned routing ops
    routing_opses = {}
    peers = {}

    # ping roll up result
    ping_pass = True
    relearn = False

    for item in ping_parameters:
        src = testbed.devices[item['src']]
        dest = testbed.devices[item['dest']]
        log.info(banner(
            "Get sorce device {s} and destnation device {d}"
                .format(s=src.name, d=dest.name)))
        lookup = Lookup.from_device(src)

        # create timeout for looping the ping
        timeout = Timeout(max_time=item['timeout_max_time'],
            interval=item['timeout_interval'])

        # determine af
        af = 'ipv4' if item['ping']['proto'] == 'ip' else 'ipv6'

        # routing path for getting desired routes
        paths = [['info', 'vrf', '(?P<vrf>.*)', 'address_family',
                  af, 'routes', '(?P<route>.*)',
                  'source_protocol', 'connected'],
                 ['info', 'vrf', '(?P<vrf>.*)', 'address_family',
                  af, 'routes', '(?P<route>.*)', 'next_hop',
                  'outgoing_interface', '(?P<intf>.*)',
                  'outgoing_interface', '(?P<intf>.*)']]

        while timeout.iterate():
            for dev in [src, dest]:
                if dev.name  not in routing_opses or relearn:

                    # learn the routing ops
                    try:
                        ret = lookup.sdk.libs.abstracted_libs.processors.learn_routing(
                                    dev, af, paths, ops_container=routing_opses, ret_container=peers)
                    except Exception as e:
                        log.warning('Cannot learn routing information on {d}\n{e}'
                            .format(d=dev.name, e=e)) 
                        relearn = True
                        ping_pass = False
                        timeout.sleep()
                        continue


            # trim the ones not a peer
            trim_item = []
            for group in peers:
                if len(peers[group].keys()) != 2:
                    trim_item.append(group)
            for group in trim_item:
                peers.pop(group)

            if not peers:
                log.warning('No peer routes learned, Try again')
                relearn = True
                ping_pass = False
                timeout.sleep()
                continue
            else:
                # has the routes, no need relearn it again
                relearn = False

            log.info('Get the routing group information as {}'.format(peers))

            ping_values = []

            # select ip and vrf to ping
            for key in list(peers.keys())[:item['peer_num']]:
                routes = list(peers[key].keys())
                for route in peers[key]:
                    if src.name in peers[key][route]:
                        # ping during peer devices
                        routes.remove(route)
                        peer_route = routes[0]
                        if peers[key][route][src.name]['vrf'] == 'default':
                            ping_values.append({'addr': peer_route.split('/')[0]})
                        else:
                            ping_values.append({'addr': peer_route.split('/')[0],
                                           'command': 'ping vrf {}'.format(peers[key][route][src.name]['vrf'])})
                        break

            for ping_item in ping_values:
                item['ping'].update(ping_item)
                log.info(banner('Ping with args {a} on {d}'.format(a=item['ping'], d=src.name)))
                try:
                    out = src.ping(**item['ping'])
                except SubCommandFailure as e:
                    if 'pass' in expect_result:
                        log.warning('ping failed\n{}, try again.'.format(e))
                        ping_pass = False
                        break
                    else:
                        log.info('ping failed as expected')
                        ping_pass = True
                        break

                ret = re.search('Success +rate +is +(\d+) +percent', out)
                perc = ret.groups()[0]
                if perc == str(item['exp_succ_perc']):
                    log.info('ping successed with {}% percent'.format(item['exp_succ_perc']))
                    ping_pass = True
                    break
                else:
                    log.warning('ping failed. Expected percent: {e} But got: {r}'
                        .format(e=item['exp_succ_perc'], r=perc))
                    ping_pass = False
                    break

            if ping_pass:
                break
            else:
                timeout.sleep()
                continue

        if not ping_pass:
            section.passx('PING PRE POST PROCESSOR FAILED, SKIPPED THE TRIGGER')

def debug_dumper(section, commands):
    '''debug_dumper prepostprocessor. Execute user specified show commands
    on results ( fail or pass)

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        commands (`dict`) : Dict of show commands on which routers.

    Returns:
        None


    Raises:
        None

    '''
    log.info(banner('Execute the show commands on the given result from the yaml if meet the conditions'))
    
    if section and getattr(section, 'parameters', {}):
        testbed = section.parameters.get('testbed', {})

        for name in commands.keys():
            dev = testbed.devices[name]

            # check when pass/fail to execute the commands
            for res, cmds in commands[name].items():
                if res in section.result.name:
                    for cmd in cmds:
                        try:
                            dev.execute(cmd)
                        except Exception:
                            pass

def traceroute_loopback(section, traceroute_args, action='traceroute'):
    '''traceroute prepostprocessor

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        traceroute_args (`list`) : list of traceroute needed parameters

    Returns:
        None


    Raises:
        None

    '''
    log.info(banner('Dynamic learn the source and destination devices loopback interface routing\n'
        'information and issue traceroute on source device to see if given route is in the traceroute table'))

    if not section or not getattr(section, 'parameters', {}):
        return

    # Get ping ip and vrf
    testbed = section.parameters.get('testbed', {})

    # store the learned routing ops
    routing_opses = {}
    peers = {}

    for item in traceroute_args:
        src = testbed.devices[item['src']]
        dest = testbed.devices[item['dest']]
        log.info(banner(
            "Get source device {s} and destination device {d}"
                .format(s=src.name, d=dest.name)))
        lookup = Lookup.from_device(src)

        # determine af
        af = 'ipv6' if item['protocol'] == 'ipv6' else 'ipv4'

        paths = [['info', 'vrf', '(?P<vrf>.*)', 'address_family',
                  af, 'routes', '(?P<route>.*)',
                  'source_protocol', 'connected'],
                 ['info', 'vrf', '(?P<vrf>.*)', 'address_family',
                  af, 'routes', '(?P<route>.*)', 'next_hop',
                  'outgoing_interface', '(?P<intf>Loopback.*)',
                  'outgoing_interface', '(?P<intf>Loopback.*)']]

        if dest.name  not in routing_opses:
            # learn the routing ops
            try:
                ret = lookup.sdk.libs.abstracted_libs.processors.learn_routing(
                            dest, af, paths, ops_container=routing_opses, ret_container=peers)
            except Exception as e:
                log.warning('Cannot learn routing information on {d}\n{e}'
                    .format(d=dest.name, e=e)) 
                relearn = True
                ping_pass = False
                timeout.sleep()
                continue

        # get ip address from returned peers value which is  
        # {'1.1.1.0/24': {'1.1.1.1': {'R5': {'intf': 'Loopback1', 'vrf': 'default', 'route': '1.1.1.0/24'}}}}
        peers = [ ip for item in peers.values() for ip in item ]

        log.info(banner('Get the routing group information as {}'.format(peers)))

        # ping roll up result
        ping_pass = True

        # select ip and vrf to ping
        for key in list(peers)[:item['peer_num']]:
            route = key.split('/')[0]
            #timeout
            timeout = Timeout(max_time=item['timeout_max_time'],
                interval=item['timeout_interval'])

            while timeout.iterate():
                try:
                    if 'ping' in action:
                        log.info(banner('ping {r} on {d}'.format(r=route, d=src.name)))
                        out = src.ping(addr=route)
                    else:
                        log.info(banner('Traceroute {r} to check if {e} in table on {d}'
                            .format(r=route, d=src.name, e=item['dest_route'])))
                        out = src.execute(command='traceroute {}'.format(route))
                except SubCommandFailure as e:
                    log.warning('{a} failed\n{e}, try again.'.format(e=e, a=action))
                    ping_pass = False
                    timeout.sleep()
                    continue

                if item['dest_route'] in out:
                    log.info('Traceroute successed to {}'.format(item['dest_route']))
                    ping_pass = True
                    break
                elif '100' in out:
                    log.info('Ping successed to {}'.format(route))
                    ping_pass = True
                    break
                else:
                    log.warning('Traceroute failed. Expected route: {e} But got: {r}'
                        .format(e=item['dest_route'], r=out))
                    ping_pass = False
                    timeout.sleep()
                    continue

        if not ping_pass:
            section.passx('TRACEROUTE PRE POST PROCESSOR FAILED, SKIPPED THE TRIGGER')

def get_uut(section, attribute, **kwargs):
    '''Get uut with provided features from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        attribute (`str`) : attribute that want to get on device
        vrf(`str`): vrf name specific.
                    If nothing give, choose any non-default vrfs

    Returns:
        AETEST results


    Raises:
        None

    '''
    log.info(banner('Finding device which has feature "%s"' % attribute))

    if section and getattr(section, 'parameters', {}):
        # get testbed
        testbed = section.parameters.get('testbed', {})

        # get default uut
        uut = testbed.devices['uut']

        # check if feature uut has previously learned
        if section.parent.parameters.get('%s_uut' % attribute, None):
            section.parameters['uut'] = getattr(uut, '%s_uut' % attribute)
            
            log.info('Feature %s has previously learned\n'
                'Found device: %s' % (attribute, section.parameters['uut'].name))
            return

        # get LTS
        lts_dict = section.parent.parameters.get('lts', None)
        if not lts_dict:
            log.info('No LTS is learned, Use default uut %s '
                'for testcase %s' % (uut.name, section.uid))
            return 

        # get devices specific feature R object,
        try:
            rs = globals()['_get_%s_device' % attribute](kwargs.get('vrf', None))
        except Exception as e:
            section.skipped('%s device cannot be found:\n%s' %(attribute, str(e)))
            
        # find the returned feature 
        req_msg = '\n'.join([str(re.args) for re in rs])
        log.info('Find requirements from LTS:\n{}'.format(req_msg))
        ret = find([lts_dict], *rs, filter_=False)

        if not ret:
            log.info('Feature "%s" is not found in LTS, will '
                'use default uut %s' % (attribute, uut.name))
            return

        # unchange uut if uut in the lts
        if True in [uut.name in i[1] for i in ret]:
            log.info('Finding device which has feature '
                '"%s"\n[Unchanged] device: uut %s' % (attribute, uut.name))
            return

        # choose one from it to change uut for this section
        section.parameters['uut'] = testbed.devices[ret[0][1][1]]

        # assign feature uut to uut object -- 
        # in case multiple triggers looks for the same uut, save time
        section.parent.parameters['%s_uut' % attribute] = section.parameters['uut']

        # change secion id
        section.uid = '%s.%s' % (section.uid.split('.')[0], section.parameters['uut'].name)

        # print logger
        log.info('Finding device which has feature '
            '"%s"\n[Changed] device: %s' % (attribute, section.parameters['uut'].name))

def get_uut_neighbor(section, **kwargs):
    '''Get uut neighbors from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.

    Returns:
        AETEST results


    Raises:
        None

    '''
    def get_peer(device, intf_dict, routing_dict, uut):

        log.info(banner('Get device %s interface ip and vrf information' % device))

        # rebuild interface dict to has structure as 
        # vrf[<vrf>][address_family][af][ip][<ip>][interface][<intf>]
        new_intf_dict = {}
        intf_dict = getattr(intf_dict, 'info')
        for intf in intf_dict:
            if intf_dict[intf].get('vrf'):
                vrf_dict = new_intf_dict.setdefault('vrf', {})\
                            .setdefault(intf_dict[intf].pop('vrf'), {})
            else:
                continue
            for af in intf_dict[intf]:
                if af not in ['ipv4', 'ipv6']:
                    continue
                af_dict = vrf_dict.setdefault('address_family', {})\
                            .setdefault(af, {})
                for ip in intf_dict[intf][af]:
                    ip_dict = af_dict.setdefault('ip', {})\
                                .setdefault(intf_dict[intf][af][ip]['ip'], {})
                    ip_dict['interface'] = intf

        # find routing ip to see if it is from other deivce
        # if yes, then store the device into to uut neighbors
        ret = {}
        for vrf in routing_dict.get('vrf', {}):
            for af in routing_dict['vrf'][vrf]['address_family']:
                for route in routing_dict['vrf'][vrf]['address_family'][af]['routes']:
                    if routing_dict['vrf'][vrf]['address_family'][af]\
                        ['routes'][route].get('source_protocol', '') in ['direct', 'local']:
                        continue
                    ip = route.split('/')[0]

                    if new_intf_dict.get('vrf', {}).get(vrf, {}).get('address_family', {})\
                        .get(af, {}).get('ip', {}).get(ip, {}):
                        ret.setdefault(device, {}).setdefault('vrf', {})\
                            .setdefault(vrf, {}).setdefault('address_family', {})\
                                .setdefault(af, {}).setdefault('ip', {}).setdefault(ip, {})\
                                    .update(new_intf_dict.get('vrf', {}).get(vrf, {})\
                                            .get('address_family', {}).get(af, {}).get('ip', {}).get(ip, {}))

        return ret

    log.info(banner('Get uut neighbors'))
    if section and getattr(section, 'parameters', {}):
        # get testbed
        testbed = section.parameters.get('testbed', {})

        # get default uut
        uut = section.parameters.get('uut', getattr(section, 'uut', testbed.devices['uut']))

        # get LTS
        lts_dict = section.parent.parameters.get('lts', {})\
                    .get('ops.interface.interface.Interface', None)

        if not lts_dict:
            section.skipped('No LTS is learned, No peer found for uut %s' % uut.name)

        # learning ops routing ops
        lookup = Lookup.from_device(uut)
        route_ret = lookup.ops.routing.routing.Routing(uut, attributes=[
                'info[vrf][(.*)][address_family][(.*)][routes][(.*)][source_protocol]',
                'info[vrf][(.*)][address_family][(.*)][routes][(.*)][active]'])
        route_ret.learn()

        # find if uut routing table has the route from other deivces interfaces ip address
        worker_devices = []
        worker_dicts = []
        for dev, intf_dict in lts_dict.items():
            worker_devices.append(dev)
            worker_dicts.append(intf_dict)

        ret = pcall(get_peer, device=worker_devices, intf_dict=worker_dicts,
              ckwargs={'routing_dict': getattr(route_ret, 'info', {}), 'uut': uut})
        uut.neighbors = {}
        [uut.neighbors.update(i) for i in ret]

        log.info('Get uut {u} neighbors information \n{d}'.format(u=uut.name, d=yaml.dump(uut.neighbors)))


def _get_auto_rp_interface_device(vrf):
    '''Get device which has auto-rp 'up' interface from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        vrf (`str`) : vrf information that want the feaure on

    Returns:
        AETEST results


    Raises:
        None

    '''
    # check if uut has auto_rp feature
    if not vrf:
        vrf = '(?P<vrf>^(?!default)\w+$)'

    reqs = [['conf.pim.Pim', '(?P<dev>.*)', 'device_attr',
             '(?P<dev>.*)', '_vrf_attr', vrf, '_address_family_attr',
             'ipv4', 'send_rp_announce_intf', '(?P<intf>.*)']]

    rs = [R(r) for r in reqs]
    return rs

def _get_bsr_rp_device(vrf):
    '''Get device which has bsr_rp from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        vrf (`str`) : vrf information that want the feaure on

    Returns:
        AETEST results


    Raises:
        None

    '''    
    # check if uut has bsr_rp feature
    if not vrf:
        vrf = '(?P<vrf>^(?!default)\w+$)'

    reqs = [['ops.pim.pim.Pim', 'vrf', vrf, 'address_family',
             '(.*)', 'rp', 'bsr', '(?P<bsr>.*)']]
    rs = [R(r) for r in reqs]
    return rs

def _get_static_rp_device(vrf):
    '''Get device which has static_rp from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        vrf (`str`) : vrf information that want the feaure on

    Returns:
        AETEST results


    Raises:
        None

    '''    
    # check if uut has bsr_rp feature
    if not vrf:
        vrf = '(?P<vrf>^(?!default)\w+$)'

    reqs = [['ops.pim.pim.Pim', 'vrf', vrf, 'address_family',
             '(.*)', 'rp', 'static_rp', '(?P<static_rp>.*)']]
    rs = [R(r) for r in reqs]
    return rs

def _get_msdp_device(vrf):
    '''Get device which has msdp from learned LTS in common_setup

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        vrf (`str`) : vrf information that want the feaure on

    Returns:
        AETEST results


    Raises:
        None

    '''    
    # check if uut has msdp feature
    if not vrf:
        vrf = '(?P<vrf>.*)'

    reqs = [['ops.msdp.msdp.Msdp', '(?P<dev>.*)', 'info', 'vrf', vrf, 'peer',
             '(?P<peer>.*)', 'session_state', 'established']]
    rs = [R(r) for r in reqs]
    return rs
