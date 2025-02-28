# Python
import datetime
import os
import re
import time
import yaml
import copy
import logging
import shutil
import zipfile
import importlib

# pyats
from pyats.async_ import pcall
from pyats.easypy import runtime
from pyats.aetest import Testcase, skip
from pyats.aetest.sections import SetupSection
from pyats.log.utils import banner
from pyats.results import TestResult, Passed, Failed, Skipped, Passx, Aborted, Errored
from pyats.utils.objects import find, R, NotExists

# import pcall
from pyats.async_ import pcall


# Abstract
from genie.abstract import Lookup

# Genie
from genie.harness.exceptions import GenieTgnError
from genie.harness.utils import connect_device
from genie.utils.profile import pickle_traffic, unpickle_traffic, unpickle_stream_data
from genie.utils.timeout import Timeout

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Statement, Dialog

# genie.libs
from genie.libs import ops
from genie.libs import sdk
from genie.libs import parser
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.utils import Dq

# 3rd party
import requests

log = logging.getLogger(__name__)


def _get_connection_class(section):

    conn_class_name = None
    for dev in section.parameters['testbed'].find_devices(type='tgn'):
        for con in dev.connections:
            try:
                conn_class_name = dev.connections[con]['class'].__name__
            except BaseException:
                continue
    return conn_class_name

def verify_ping(section, devices):
    '''
    'verify_ping' processor to verity ping result

    arguments:
      devices('dict'): device name with ping parameters

    example:

    global_processors:
      pre:
        verify_ping: verify_ping
          method: genie.libs.sdk.libs.abstracted_libs.processors.verify_ping
          parameters:
            devices:
              ce1:
                - address: 1.1.1.10
                  source: 1.1.1.1
                  expected_min_success_rate: 100
                - address: 2001::1:1:1:10
                  source: 2001::1:1:1:1
                  expected_min_success_rate: 100
    '''

    def _verify_ping(device, ping_args):
        '''
        Internal function _verify_ping for pcall
        '''
        results = []
        for ping_list in ping_args:
            res = device.api.verify_ping(**ping_list)
            results.append(res)

        if len(results) > 0:
            return all(results)
        else:
            return False

    testbed = runtime.testbed
    ikwargs = []
    for dev in devices:
        device = testbed.devices[dev]
        ikwargs.append({'device': device, 'ping_args': devices[dev]})

    results = pcall(_verify_ping, ikwargs=ikwargs)

    if len(results) > 0:
        if not all(results):
            section.failed('Ping failed.')

def sleep_processor(section, sleep=None):
    '''Sleep prepostprocessor

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile
    '''

    if sleep:
        # prefer sleep in `parameters` under processors
        sleep_time = sleep
    else:
        # keep for backward compatibility
        # if no sleep under processor is given, look for section parameters
        if section and getattr(section, 'parameters', {}):
            sleep_time = section.parameters.get('sleep', None)
            log.warning(
                "Please set `sleep` under processor like below:\n\n"
                "processors:\n"
                "  pre|post:\n"
                "    sleep_processor:\n"
                "      method: genie.libs.sdk.libs.abstracted_libs.sleep_processor\n"
                "      parameters:\n"
                "        sleep: {sleep_time}\n".format(
                    sleep_time=sleep_time))

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
            configs = yaml.safe_load(open(configs))
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
            lldp_ops = lookup.ops.lldp.lldp.Lldp(
                uut, attributes=['info[interfaces][(.*)][neighbors][(.*)][port_id]'])

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

        log.info(
            banner(
                'Find {u} interfaces connect to neighbor {p}'.format(
                    u=uut.name,
                    p=peer.name)))
        # find peer connection interfaces
        rs = R(['(?P<local_intf>.*)', 'neighbors',
                peer, 'port_id', '(?P<peer_intf>.*)'])
        ret = find([uut.lldp_mapping], rs, filter_=False, all_keys=True)
        if ret:
            values = GroupKeys.group_keys(
                reqs=rs.args, ret_num={}, source=ret, all_keys=True)
        else:
            section.failed(
                'No Peer inerface Found between {s} and {d}'.format(
                    s=uut.name, d=peer))

        # get free(unassigned) interfaces
        log.info(
            banner(
                'Find {u} free connected interfaces from {l}'.format(
                    u=uut.name,
                    l=values)))
        try:
            ip_out = lookup.parser.show_interface.ShowIpInterfaceBrief(
                uut).parse()
            ip_out_peer = lookup.parser.show_interface.ShowIpInterfaceBrief(
                peer_dev).parse()
        except Exception as e:
            section.failed(
                'Cannot get information from show ip/ipv6 interface brief',
                from_exception=e)

        # initial local and peer intf
        local_intf = None
        peer_intf = None

        for item in values:
            if 'unassigned' in ip_out['interface'][item['local_intf']]['ip_address'] and \
               'unassigned' in ip_out_peer['interface'][item['peer_intf']]['ip_address']:
                local_intf = item['local_intf']
                peer_intf = item['peer_intf']
                break

        # replace the configure data with learnt interfaces
        if local_intf and peer_intf:
            uut.local_intf = local_intf
            peer_dev.peer_intf = peer_intf
            for _, conf in sorted(configs['devices']['uut'].items()):
                conf['config'] = conf['config'].format(intf=local_intf)
                conf['unconfig'] = conf['unconfig'].format(intf=local_intf)
            for _, conf in sorted(configs['devices'][peer].items()):
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
            configs = yaml.safe_load(open(configs))
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
                    section.mapping.requirements.setdefault(
                        'provided_values', {}).setdefault(key, val)
                tmp_config['devices']['uut'].pop(key)

        for dev in sorted(configs.get('devices', {})):

            device = testbed.devices[dev]

            # Sort the item; it is expected to be
            # Sort them by the key, which needs to be an inter
            # 1, 2, 3, and so on
            for _, conf in sorted(tmp_config['devices'][dev].items()):
                if unconfig and 'unconfig' in conf:
                    conf['config'] = conf['unconfig']

                # replace the format syntax if has any
                conf['config'] = conf['config'].format(
                    **section.mapping.requirements.get('provided_values', {})
                    if hasattr(section, 'mapping') else {})

                log.info(
                    banner(
                        "Applying configuration on '{d}'".format(
                            d=device.name)))
                if os.path.isfile(conf['config']):
                    if 'invalid' not in conf:
                        # Set default
                        conf['invalid'] = []
                    try:
                        device.tftp.copy_file_to_device(
                            device=device,
                            filename=conf['config'],
                            location='running-config',
                            vrf='management',
                            invalid=conf['invalid'])
                    except Exception as e:
                        log.error(str(e))
                        section.failed(
                            "Issue while applying the configuration "
                            "on {d}".format(
                                d=dev))
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
                        section.failed(
                            "Issue while applying the configuration "
                            "on {d}".format(
                                d=dev))
                else:
                    section.failed('The configs type {} is not supported'
                                   .format(type(conf['config'])))

                # sleep for x amount of time after
                if 'sleep'in conf and not unconfig:
                    log.info(
                        "Sleeping for '{s}' "
                        "seconds for waiting system is stable "
                        "after loading the configuration".format(
                            s=conf['sleep']))
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
    log.info(
        banner(
            'Dynamic learn the source and destination devices routing\n'
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
                if dev.name not in routing_opses or relearn:

                    # learn the routing ops
                    try:
                        ret = lookup.sdk.libs.abstracted_libs.processors.learn_routing(
                            dev, af, paths, ops_container=routing_opses, ret_container=peers)
                    except Exception as e:
                        log.warning(
                            'Cannot learn routing information on {d}\n{e}' .format(
                                d=dev.name, e=e))
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
                            ping_values.append(
                                {'addr': peer_route.split('/')[0]})
                        else:
                            ping_values.append({'addr': peer_route.split(
                                '/')[0], 'command': 'ping vrf {}'.format(peers[key][route][src.name]['vrf'])})
                        break

            for ping_item in ping_values:
                item['ping'].update(ping_item)
                log.info(
                    banner(
                        'Ping with args {a} on {d}'.format(
                            a=item['ping'],
                            d=src.name)))
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

                ret = re.search(r'Success +rate +is +(\d+) +percent', out)
                perc = ret.groups()[0]
                if perc == str(item['exp_succ_perc']):
                    log.info(
                        'ping successed with {}% percent'.format(
                            item['exp_succ_perc']))
                    ping_pass = True
                    break
                else:
                    log.warning(
                        'ping failed. Expected percent: {e} But got: {r}' .format(
                            e=item['exp_succ_perc'], r=perc))
                    ping_pass = False
                    break

            if ping_pass:
                break
            else:
                timeout.sleep()
                continue

        if not ping_pass:
            section.passx(
                'PING PRE POST PROCESSOR FAILED, SKIPPED THE TRIGGER')


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
    log.info(banner(
        'Execute the show commands on the given result from the yaml if meet the conditions'))

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
    log.info(
        banner(
            'Dynamic learn the source and destination devices loopback interface routing\n'
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

        if dest.name not in routing_opses:
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
        # {'10.4.1.0/24': {'10.4.1.1': {'R5': {'intf': 'Loopback1', 'vrf': 'default', 'route': '10.4.1.0/24'}}}}
        peers = [ip for item in peers.values() for ip in item]

        log.info(banner('Get the routing group information as {}'.format(peers)))

        # ping roll up result
        ping_pass = True

        # select ip and vrf to ping
        for key in list(peers)[:item['peer_num']]:
            route = key.split('/')[0]
            # timeout
            timeout = Timeout(max_time=item['timeout_max_time'],
                              interval=item['timeout_interval'])

            while timeout.iterate():
                try:
                    if 'ping' in action:
                        log.info(
                            banner(
                                'ping {r} on {d}'.format(
                                    r=route,
                                    d=src.name)))
                        out = src.ping(addr=route)
                    else:
                        log.info(
                            banner(
                                'Traceroute {r} to check if {e} in table on {d}' .format(
                                    r=route,
                                    d=src.name,
                                    e=item['dest_route'])))
                        out = src.execute(
                            command='traceroute {}'.format(route))
                except SubCommandFailure as e:
                    log.warning(
                        '{a} failed\n{e}, try again.'.format(
                            e=e, a=action))
                    ping_pass = False
                    timeout.sleep()
                    continue

                if item['dest_route'] in out:
                    log.info(
                        'Traceroute successed to {}'.format(
                            item['dest_route']))
                    ping_pass = True
                    break
                elif '100' in out:
                    log.info('Ping successed to {}'.format(route))
                    ping_pass = True
                    break
                else:
                    log.warning(
                        'Traceroute failed. Expected route: {e} But got: {r}' .format(
                            e=item['dest_route'], r=out))
                    ping_pass = False
                    timeout.sleep()
                    continue

        if not ping_pass:
            section.passx(
                'TRACEROUTE PRE POST PROCESSOR FAILED, SKIPPED THE TRIGGER')


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

            log.info(
                'Feature %s has previously learned\n'
                'Found device: %s' %
                (attribute, section.parameters['uut'].name))
            return

        # get LTS
        lts_dict = section.parent.parameters.get('lts', None)
        if not lts_dict:
            log.info('No LTS is learned, Use default uut %s '
                     'for testcase %s' % (uut.name, section.uid))
            return

        # get devices specific feature R object,
        try:
            rs = globals()[
                '_get_%s_device' %
                attribute](
                kwargs.get(
                    'vrf',
                    None))
        except Exception as e:
            section.skipped(
                '%s device cannot be found:\n%s' %
                (attribute, str(e)))

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
            log.info(
                'Finding device which has feature '
                '"%s"\n[Unchanged] device: uut %s' %
                (attribute, uut.name))
            return

        # choose one from it to change uut for this section
        section.parameters['uut'] = testbed.devices[ret[0][1][1]]

        # assign feature uut to uut object --
        # in case multiple triggers looks for the same uut, save time
        section.parent.parameters['%s_uut' %
                                  attribute] = section.parameters['uut']

        # change secion id
        section.uid = '%s.%s' % (section.uid.split(
            '.')[0], section.parameters['uut'].name)

        # print logger
        log.info(
            'Finding device which has feature '
            '"%s"\n[Changed] device: %s' %
            (attribute, section.parameters['uut'].name))


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

        log.info(
            banner(
                'Get device %s interface ip and vrf information' %
                device))

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
                    if routing_dict['vrf'][vrf]['address_family'][af]['routes'][route].get(
                            'source_protocol', '') in ['direct', 'local']:
                        continue
                    ip = route.split('/')[0]

                    if new_intf_dict.get(
                        'vrf',
                        {}).get(
                        vrf,
                        {}).get(
                        'address_family',
                        {}) .get(
                        af,
                        {}).get(
                        'ip',
                        {}).get(
                            ip,
                            {}):
                        ret.setdefault(
                            device,
                            {}).setdefault(
                            'vrf',
                            {}) .setdefault(
                            vrf,
                            {}).setdefault(
                            'address_family',
                            {}) .setdefault(
                            af,
                            {}).setdefault(
                            'ip',
                            {}).setdefault(
                            ip,
                            {}) .update(
                                new_intf_dict.get(
                                    'vrf',
                                    {}).get(
                                        vrf,
                                        {}) .get(
                                            'address_family',
                                            {}).get(
                                                af,
                                                {}).get(
                                                    'ip',
                                                    {}).get(
                                                        ip,
                                    {}))

        return ret

    log.info(banner('Get uut neighbors'))
    if section and getattr(section, 'parameters', {}):
        # get testbed
        testbed = section.parameters.get('testbed', {})

        # get default uut
        uut = section.parameters.get('uut', getattr(
            section, 'uut', testbed.devices['uut']))

        # get LTS
        lts_dict = section.parent.parameters.get('lts', {})\
            .get('ops.interface.interface.Interface', None)

        if not lts_dict:
            section.skipped(
                'No LTS is learned, No peer found for uut %s' %
                uut.name)

        # learning ops routing ops
        lookup = Lookup.from_device(uut)
        route_ret = lookup.ops.routing.routing.Routing(uut, attributes=[
            'info[vrf][(.*)][address_family][(.*)][routes][(.*)][source_protocol]',
            'info[vrf][(.*)][address_family][(.*)][routes][(.*)][active]'])
        route_ret.learn()

        # find if uut routing table has the route from other deivces interfaces
        # ip address
        worker_devices = []
        worker_dicts = []
        for dev, intf_dict in lts_dict.items():
            worker_devices.append(dev)
            worker_dicts.append(intf_dict)

        ret = pcall(
            get_peer,
            device=worker_devices,
            intf_dict=worker_dicts,
            ckwargs={
                'routing_dict': getattr(
                    route_ret,
                    'info',
                    {}),
                'uut': uut})
        uut.neighbors = {}
        [uut.neighbors.update(i) for i in ret]

        log.info(
            'Get uut {u} neighbors information \n{d}'.format(
                u=uut.name, d=yaml.dump(
                    uut.neighbors)))


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
        vrf = r'(?P<vrf>^(?!default)\w+$)'

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
        vrf = r'(?P<vrf>^(?!default)\w+$)'

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
        vrf = r'(?P<vrf>^(?!default)\w+$)'

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

# ==============================================================================
# processor: restore_running_configuration
# ==============================================================================

def restore_running_configuration(section,
                                  devices=None,
                                  iteration=10,
                                  interval=60,
                                  compare=False,
                                  compare_exclude=[],
                                  reload_timeout=1200,
                                  no_crypto_pki_trustpoint=False,
                                  timeout=60):
    '''Trigger Pre-Processor:
        * Restore running configuration from default directory
    '''

    def _restore_running_configuration(section, device, iteration, interval,
                                       compare, compare_exclude, reload_timeout, no_crypto_pki_trustpoint, timeout):
        '''
        Internal function _restore_running_configuration for pcall 
        '''
        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk': sdk})
        restore = lookup.sdk.libs.abstracted_libs.restore.Restore()

        if hasattr(section, 'trigger_config'):
            restore.to_url = section.trigger_config[device.name]
        else:
            section.failed("processor: 'save_running_configuration' not "
                           "executed before running processor: "
                           "'restore_running_configuration'")

        # delete crypto pki trustpoint configs
        if no_crypto_pki_trustpoint:
            out = device.execute('sh run | i crypto pki trustpoint', timeout=timeout)
            if 'crypto pki trustpoint' in out:
                unconfig = ['no '+line for line in out.splitlines()]
                if unconfig:
                    device.configure(unconfig)

        # Restore configuration from default directory
        try:
            restore.restore_configuration(device=device,
                                          method='config_replace',
                                          abstract=lookup,
                                          iteration=iteration,
                                          interval=interval,
                                          compare=compare,
                                          compare_exclude=compare_exclude,
                                          reload_timeout=reload_timeout,
                                          timeout=timeout)
        except Exception as e:
            log.error(e)
            return False

        else:
            log.info("Restored running-configuration from device")
            return True


    log.info(banner("processor: 'restore_running_configuration'"))

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    ikwargs = []
    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        ikwargs.append({'device': device})
    ckwargs = {
        'section': section,
        'iteration': iteration,
        'interval': interval,
        'compare': compare,
        'compare_exclude': compare_exclude,
        'reload_timeout': reload_timeout,
        'no_crypto_pki_trustpoint': no_crypto_pki_trustpoint,
        'timeout': timeout
    }

    returns = pcall(_restore_running_configuration,
                    ckwargs=ckwargs,
                    ikwargs=ikwargs)

    if returns != [] and not all(returns):
        section.failed("Unable to restore running-configuration from device")

# ==============================================================================
# processor: save_running_configuration
# ==============================================================================

def save_running_configuration(section, devices=None, copy_to_standby=False, no_crypto_pki_trustpoint=False, timeout=60):
    '''Trigger Pre-Processor:
        * Save running configuration to default directory
    '''

    def _save_running_configuration(section, device, copy_to_standby, no_crypto_pki_trustpoint, timeout):
        '''
        Internal function _restore_running_configuration for pcall 
        '''

        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk': sdk})
        restore = lookup.sdk.libs.abstracted_libs.restore.Restore()

        # Get default directory
        save_dir = getattr(section.parent, 'default_file_system', {})
        if not save_dir or device not in save_dir:
            section.parent.default_file_system = {}
            section.parent.default_file_system[
                device.
                name] = lookup.sdk.libs.abstracted_libs.subsection.get_default_dir(
                    device=device)
            save_dir = section.parent.default_file_system

        # delete crypto pki trustpoint configs
        if no_crypto_pki_trustpoint:
            out = device.execute('sh run | i crypto pki trustpoint', timeout=timeout)
            unconfig = ['no '+line for line in out.splitlines()]
            if unconfig:
                device.configure(unconfig)

        # Save configuration to default directory
        try:
            location = restore.save_configuration(device=device,
                                                  method='config_replace',
                                                  abstract=lookup,
                                                  default_dir=save_dir,
                                                  copy_to_standby=copy_to_standby,
                                                  timeout=timeout)
        except Exception as e:
            log.error(e)
            section.failed("Unable to save running-configuration to device")
        else:
            log.info("Saved running-configuration to device")
            return device.name, location

    # Init
    log.info(banner("processor: 'save_running_configuration'"))

    # Init
    section.trigger_config = {}

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    ikwargs = []
    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        ikwargs.append({'device': device})
    ckwargs = {'section': section, 'copy_to_standby': copy_to_standby, 'no_crypto_pki_trustpoint': no_crypto_pki_trustpoint, 'timeout': timeout}

    returns = pcall(_save_running_configuration,
                    ckwargs=ckwargs,
                    ikwargs=ikwargs)
    for ret in returns:
        section.trigger_config[ret[0]] = ret[1]

# ==============================================================================
# processor: clear_logging
# ==============================================================================


def clear_logging(section, devices=None):
    '''Trigger Pre-Processor:
        * Clear logging on device
    '''

    # Init
    log.info(banner("processor: 'clear_logging'"))

    # Execute on section devices if devices list not specified
    if not devices:
        devices = [section.parameters['uut'].name]

    for dev in devices:
        device = section.parameters['testbed'].devices[dev]
        # Abstract
        lookup = Lookup.from_device(device, packages={'sdk': sdk})
        clear_log = lookup.sdk.libs.abstracted_libs.clear_logging.ClearLogging()

        # Clear logging on device
        try:
            log.info("Clear logging on device {}".format(dev))
            clear_log.clear_logging(device)
        except Exception as e:
            log.error(e)
            section.failed("Unable to clear logging on device")
        else:
            log.info("Cleared logging successfully on device")

# ==============================================================================
# processor: execute_command
# ==============================================================================


def pre_execute_command(section,
                        devices=None,
                        sleep_time=0,
                        max_retry=1,
                        save_to_file='',
                        zipped_folder=''):
    '''
    Execute commands as processors in parallel. 
    This can be run only with specified condition and the log can be archived with text file or zip file.

    Args:
        section (`obj`): Aetest Subsection object.
        devices (`dict`): Device dictionary with command lists.
        sleep_time (`int`): Sleep after all commands (unit: seconds).
        max_retry (`int`): Retry issuing command in case any error (max_retry 1 by default).
        save_to_file (`str`): Mode for saving output files (per_device or per_command).
        zipped_folder (`bool`): Archive folder into a zip file.

    Returns:
        AETEST results.

    Raises:
        None
    '''
    # Init
    log.info(banner("processor: 'execute_command'"))

    # Sanitize arguments
    if save_to_file and save_to_file not in ['per_device', 'per_command']:
        section.errored(
            "`save_to_file` in datafile must be `per_device` or `per_command`")
    if not save_to_file and isinstance(zipped_folder, bool):
        log.warning(
            "`zipped_folder` was ignored because `save_to_file` was not set in datafile"
        )
    elif save_to_file and not isinstance(zipped_folder, bool):
        section.errored("`zipped_folder` must be True or False in datafile")

    # Prepare save location
    folder_name = None
    if save_to_file:
        # Setup folder for saving outputs
        now = datetime.datetime.now()
        timestamp_format = '%Y%m%d_%H%M%S'
        folder_log = '_'.join(
            [section.parent.uid, section.uid,
             'pre_execute_command', now.strftime(timestamp_format)])
        folder_name = runtime.directory + '/' + folder_log

        try:
            os.mkdir(folder_name)
            log.info(f"Folder `{folder_name}` created for `save_to_file` with mode {save_to_file}")
        except Exception:
            section.errored(f"Failed to create folder `{folder_name}` for `save_to_file`")

        if zipped_folder:
            try:
                zip = zipfile.ZipFile(folder_name + '.zip', 'w', zipfile.ZIP_DEFLATED)
            except Exception:
                section.errored(f"Failed to create zip file: {folder_name + '.zip'} for `save_to_file`")

    def _pre_execute_command(dev, cmd, device, save_to_file, folder_name):
        # Command execution logic, now isolated for parallel processing
        for _ in range(max_retry + 1):
            try:
                exec_cmd = cmd.get('cmd', '')
                pattern = cmd.get('pattern', '')
                answer = cmd.get('answer', '')
                cmd_timeout = cmd.get('timeout', 60)

                # If pattern is provided, set up dialog
                if pattern:
                    if isinstance(pattern, str):
                        pattern = [pattern]
                    statement_list = [
                        Statement(
                            pattern=p,
                            action='sendline({})'.format(answer),
                            loop_continue=True,
                            continue_timer=False
                        ) for p in pattern
                    ]
                    dialog = Dialog(statement_list)
                    output = device.execute(exec_cmd, reply=dialog, timeout=cmd_timeout)
                else:
                    output = device.execute(exec_cmd, timeout=cmd_timeout)

                # Handle save to file logic here based on mode
                file_name = None
                if save_to_file == 'per_device':
                    file_name = os.path.join(folder_name, f"{dev}.txt")
                elif save_to_file == 'per_command':
                    file_name = os.path.join(folder_name, f"{dev}_{device.api.slugify(exec_cmd)}.txt")

                if file_name:
                    with open(file_name, 'a') as f:
                        f.write(output)
                        log.info(f"File {file_name} saved to folder {folder_name}")

                # Successful command execution
                log.info(f"Successfully executed command '{exec_cmd}' on device {device.name}")
                return True

            except SubCommandFailure as e:
                log.error(f'Failed to execute "{exec_cmd}" on device {device.name}: {e}')
                device.api.reconnect_device()
        else:
            section.failed(f'Reached max number of {max_retry} retries, command execution has failed')
        return False

    ikwargs = []
    result_list = []

    for dev in devices:
        if dev == 'uut':
            device = section.parameters['uut']
        else:
            if dev in section.parameters['testbed'].devices.names or dev in section.parameters['testbed'].devices.aliases:
                device = section.parameters['testbed'].devices[dev]
            else:
                section.errored(f"Failed to find a device {dev} in testbed yaml")

        # Skip if not connected
        if not device or not device.is_connected():
            continue

        for cmd in devices[dev].get('cmds', []):
            if not cmd.get('condition') or section.result in list(map(TestResult.from_str, cmd['condition'])):
                ikwargs.append({'dev': dev, 'cmd': cmd, 'device': device, 'save_to_file': save_to_file, 'folder_name': folder_name})

    pcall_return = pcall(_pre_execute_command, ikwargs=ikwargs)
    result_list.extend(pcall_return)

    if zipped_folder and result_list:
        for fname in os.listdir(folder_name):
            zip.write(os.path.join(folder_name, fname), fname)

        try:
            zip.close()
            log.info(f"Zip file `{folder_name}.zip` was created with mode {save_to_file}")
        except Exception:
            section.errored(f"Failed to close zip file: {folder_name}.zip")

        try:
            shutil.rmtree(folder_name)
            log.info(f"Folder `{folder_name}` was deleted because the folder was zipped.")
        except Exception:
            section.errored(f"Failed to delete folder which was zipped. Folder: {folder_name}")

    if sleep_time and any(result_list):
        log.info(f"Sleeeping for {sleep_time} seconds")
        time.sleep(sleep_time)


def post_execute_command(section,
                         sleep_time=0,
                         max_retry=1,
                         save_to_file='',
                         zipped_folder='',
                         valid_section_results=None,
                         devices=None,
                         server_to_store=None):
    '''
    Execute commands or APIs as processors. The CLI command output can be stored in
    text files per device or per command and optionally archived in a zip file.

    APIs are executed against devices in parallel. If API output is returned, it is logged
    via info level. Returned API data is currently not stored in text files.

    Can be controlled via sections parameters which is provided by the datafile

    Args:
        section (`obj`): Aetest Subsection object.
        devices (`dict`): Devices dictionary from postprocessor definition.
        sleep_time (`int`): sleep after all commands (unit: seconds)
        max_retry (`int`): Retry issuing command in case any error (max_retry 1 by default)
        save_to_file (`str`): Set either one of below modes when show output needs to be saved as file.
                               Folder for the processor is generated and store files in the folder. (Disabled by default)
                                 per_device : file generated per device
                                 per_command : file generated per command
        zipped_folder (`bool`): Set if archive folder needs to be zipped.
                                 If True, a zip file will be generated and the folder with text files will be removed.
        valid_section_results (`list`): If provided, the section result should be in this list
                                        so commands and/or APIs get executed
        server_to_store ('dict'): a dictionary with the following fields:
                                {server_in_testbed: <name of the server that user want to store the log into.
                                                    The server should be specified in testbed>
                                 protocol: <protocol that'd be used, e.g. tftp, sftp, scp>
                                 remote_path: <the path to the directory in the server that log would be stored on>}

    Returns:
        AETEST results

    Raises:
        None
    '''
    # If valid_section_results is defined and result isn't in it,
    # log a warning message and don't run command
    if valid_section_results and section.result.name not in valid_section_results:
        log.warning('{result} not in {valid_section_results}. post_execute_command will not run'.format(
            result=section.result.name,
            valid_section_results=valid_section_results,
        ))
        return

    # Init
    log.info(banner("processor: 'post_execute_command'"))

    # Execute APIs against devices in parallel
    pcall(_post_execute_device_api,
          cargs=(section,),
          iargs=[(dev, devices[dev]) for dev in devices])

    # Sanitize arguments
    if save_to_file and save_to_file not in ['per_device', 'per_command']:
        section.errored(
            "`save_to_file` in datafile must be `per_device` or `per_command`")
    if not save_to_file and isinstance(zipped_folder, bool):
        log.warning(
            "`zipped_folder` was ignored because `save_to_file` was not set in datafile"
        )
    elif save_to_file and not isinstance(zipped_folder, bool):
        section.errored("`zipped_folder` must be True or False in datafile")

    # Prepare save location
    if save_to_file:
        file_list = {}
        now = datetime.datetime.now()
        timestamp_format = '%Y%m%d_%H%M%S'
        folder_log = '_'.join(
            [section.parent.uid, section.uid,
             'post_execute_command', now.strftime(timestamp_format)])
        folder_name = runtime.directory + '/' + folder_log
        try:
            os.mkdir(folder_name)
            log.info(
                "Folder `{folder}` is created for `save_to_file` with mode {mode}".format(folder=folder_name, mode=save_to_file))
        except Exception:
            section.errored(
                "Failed to create folder `{folder_name}` for `save_to_file`".format(folder_name=folder_name))
        if zipped_folder:
            try:
                zip = zipfile.ZipFile(folder_name + '.zip', 'w',
                                      zipfile.ZIP_DEFLATED)
            except Exception:
                section.errored(
                    "Failed to create zip file: {file} for `save_to_file`".
                    format(file=folder_name + '.zip'))

    sleep_if_cmd_executed = False

    def _post_execute_command(dev, device):
        # Execute list of commands given in yaml
        for cmd in devices[dev].get('cmds', []):
            if not cmd.get('condition') or section.result in list(
                    map(TestResult.from_str, cmd['condition'])):

                exec_cmd = cmd.get('cmd', '')
                pattern = cmd.get('pattern', '')
                answer = cmd.get('answer', '')
                cmd_sleep = cmd.get('sleep', 0)
                cmd_timeout = cmd.get('timeout', 60)

                for _ in range(max_retry + 1):
                    try:
                        # Handle prompt if pattern and answer is in the datafile
                        if pattern:
                            if isinstance(pattern, str):
                                pattern = [pattern]
                            statement_list = [Statement(pattern=p,
                                                         action='sendline({})'.format(answer), 
                                                         loop_continue=True, 
                                                         continue_timer=False) for p in pattern]
                            dialog = Dialog(statement_list)
                            output = device.execute(exec_cmd,
                                                    reply=dialog,
                                                    timeout=cmd_timeout)
                        else:
                            output = device.execute(exec_cmd,
                                                    timeout=cmd_timeout)

                        # Save output to file as per device or command
                        if save_to_file == 'per_device':
                            file_name = os.path.join(folder_name, f"{dev}.txt")
                            with open(file_name, 'a') as f:
                                output = '+' * 10 + ' ' + datetime.datetime.now(
                                ).strftime(
                                    '%Y-%m-%d %H:%M:%S.%f'
                                ) + ': ' + dev + ': executing command \'' + exec_cmd + '\' ' + '+' * 10 + '\n' + output + '\n'
                                f.write(output)
                                log.info(
                                    "File {file} saved to folder {folder}".format(file=file_name, folder=folder_name))
                            if zipped_folder:
                                file_list.update({file_name: dev})
                        elif save_to_file == 'per_command':
                            file_name = os.path.join(folder_name, f"{dev}_{device.api.slugify(exec_cmd)}.txt")
                            with open(file_name, 'w') as f:
                                output = '+' * 10 + ' ' + datetime.datetime.now(
                                ).strftime(
                                    '%Y-%m-%d %H:%M:%S.%f'
                                ) + ': ' + dev + ': executing command \'' + exec_cmd + '\' ' + '+' * 10 + '\n' + output + '\n'
                                f.write(output)
                                log.info(
                                    "File {file} saved to folder {folder}".format(file=file_name, folder=folder_name))
                            if zipped_folder or server_to_store:
                                file_list.update({file_name: dev})

                    except SubCommandFailure as e:
                        log.error(
                            'Failed to execute "{cmd}" on device {d}: {e}'.format(cmd=exec_cmd, d=device.name, e=str(e)))
                        device.destroy()
                        log.info('Trying to recover after execution failure')
                        connect_device(device)
                    else:
                        log.info(
                            "Successfully executed command '{cmd}' on device {d}".format(cmd=exec_cmd, d=device.name))
                        # Sleep if any command is successfully executed
                        sleep_if_cmd_executed = True
                        break
                else:
                    section.failed('Reached max number of {} retries, command '
                                   'execution has failed'.format(max_retry))

                if cmd_sleep:
                    log.info("Sleeping for {sleep_time} seconds".format(sleep_time=cmd_sleep))
                    time.sleep(cmd_sleep)

    ikwargs = []
    for dev in devices:
        if dev == 'uut':
            device = section.parameters['uut']
        else:
            if dev in section.parameters['testbed'].devices.names or dev in section.parameters['testbed'].devices.aliases:
                device = section.parameters['testbed'].devices[dev]
            else:
                section.errored("Failed to find a device {device} in testbed yaml".format(device=dev))

        # Skip if device is not connected
        if not device or not device.is_connected():
            continue

        ikwargs.append({'dev': dev, 'device': device})

    pcall(_post_execute_command, ikwargs=ikwargs)

    if server_to_store:
        _store_in_server_func(section, server_to_store, file_list, list(devices.keys()))

    if zipped_folder:
        for fname, sname in file_list.items():
            try:
                zip.write(fname, sname)
            except Exception:
                section.errored("Failed to add file `{file}` to zip file {zip}".format(file=sname + '.txt', zip=folder_name + '.zip'))
        try:
            zip.close()
            log.info("Zip file `{zip}` was created with mode {mode}".format(zip=folder_name + '.zip', mode=save_to_file))
        except Exception:
            section.errored("Failed to close zip file: {file}".format(file=folder_name + '.zip'))
        try:
            shutil.rmtree(folder_name)
            log.info("Folder `{folder}` was deleted because the folder was zipped".format(folder=folder_name))
        except Exception:
            section.errored("Failed to delete folder which was zipped. Folder: {folder}".format(folder=folder_name))

    if sleep_time and sleep_if_cmd_executed:
        log.info("Sleeping for {sleep_time} seconds".format(sleep_time=sleep_time))
        time.sleep(sleep_time)


def _store_in_server_func(section, server_to_store, file_list, devices):

    '''
    section (`obj`): section of the testcase data
    server_to_store (`dict`): a dictionary like :
                    {server_in_testbed: <name of the server that user want to store the log into.
                                        The server should be specified in testbed>
                    protocol: <protocol that'd be used, e.g. tftp, sftp, scp>
                    remote_path: <the path to the directory in the server that log would be stored on>}
    file_list(`obj`): list of file created per command and device
    devices (`obj`): device that commands are running on
    '''

    if not file_list:
        section.errored('No file has been generated to be stored')

    try:
        server_in_testbed = server_to_store['server_in_testbed']
        server = section.parameters['testbed'].servers[server_in_testbed]['server']
    except Exception as e :
        section.errored(str(e))

    # default protocol is sftp
    protocol = server_to_store.get('protocol', 'sftp')
    remote_path = server_to_store['remote_path']

    # common keyword arguments common for each call
    ckwargs = {
                'testbed':section.parameters['testbed'],
                'protocol': protocol,
                'server': server,
                'remote_path': remote_path
              }

    # copying the files generated based on each device to the server
    for dev in devices:

        # arguments that is individual for each parallel call
        ikwargs = []
        device = section.parameters['testbed'].devices[dev]

        for local_path, file_name in file_list.items():
            if dev in file_name:
                ikwargs.append({'local_path': local_path})

        pcall(device.api.copy_to_server, ikwargs=ikwargs, ckwargs=ckwargs)


def _post_execute_device_api(section, device, parameters):
    """ Execute the API specified in the devices argument.
    This is a helper method for the post_execute_command function.

    If the API returns data, logs the returned data via info level.

    Args:
        section (TestSection): test section object with parameters
        device (str): device name to execute against
        parameters (dict): Device parameters, list of APIs and arguments for the APIs.

    Returns:
        None

    Raises:
        ValueError if API arguments field is specified but not a dictionary.
    """
    if device == 'uut':
        device_obj = section.parameters['uut']
    else:
        if device in section.parameters[
                'testbed'].devices.names or device in section.parameters[
                    'testbed'].devices.aliases:
            device_obj = section.parameters['testbed'].devices[device]
        else:
            log.error(
                "Failed to find a device {device} in testbed yaml".format(
                    device=device))
            device_obj = None
    # if device not in TB or not connected, then skip
    if not device_obj or not device_obj.connected:
        return
    # Return if no APIs specified for this device
    if not parameters.get('apis'):
        return
    log.info(banner("Post execute API for device '{}'".format(device_obj.name)))
    # execute list of APIs given in yaml
    for api in parameters.get('apis', []):
        output = None
        api_module = api.get('module')
        if api_module:
            exec_module = importlib.import_module(api_module)
        else:
            exec_module = None
        exec_api = api.get('api')
        exec_arguments = api.get('arguments')
        if exec_api:
            if exec_arguments and not isinstance(exec_arguments, dict):
                raise ValueError('API arguments should be a dictionary')

            if exec_module:
                log.info(banner("{} executing api: '{}.{}'".format(
                    device_obj.name, api_module, exec_api
                )))
                api_func = getattr(exec_module, exec_api)
                if exec_arguments:
                    output = api_func(device_obj, **exec_arguments)
                else:
                    output = api_func(device_obj)
            else:
                log.info(banner("{} executing api: '{}'".format(
                    device_obj.name, exec_api
                )))
                api_method = getattr(device_obj, 'api')
                api_func = getattr(api_method, exec_api)
                if exec_arguments:
                    output = api_func(**exec_arguments)
                else:
                    output = api_func()

        if output:
            log.info(output)


# ==============================================================================
# processor: skip_setup_if_stable
# ==============================================================================


def pre_skip_setup_if_stable(section):
    params = section.parent.parameters

    # Check if last section was passed
    if ('previous_section_result' in params and
            params['previous_section_result'] == Passed):

        # Get function decorated by aetest.setup
        for item in section:
            if (hasattr(item, 'function') and
                    hasattr(item.function, '__testcls__') and
                    item.function.__testcls__ == SetupSection):

                # Save function so we dont have to find it during post
                params['section_setup_func'] = \
                    getattr(section, item.uid).__func__

                # affix skip decorator to setup_func
                skip.affix(section=params['section_setup_func'],
                           reason='Previous trigger passed. Device still '
                                  'in good state. No need to re-configure.')

                # Can only have one setup section per trigger
                break


def post_skip_setup_if_stable(section):
    params = section.parent.parameters
    params['previous_section_result'] = section.result

    if ('section_setup_func' in params and
            hasattr(params['section_setup_func'], '__processors__')):
        getattr(params['section_setup_func'], '__processors__').clear()

# ==============================================================================
# processor: skip_by_defect_status
# ==============================================================================


def skip_by_defect_status(section, defect_id, status=['R']):

    if not status:
        status = ['R']
    url = 'http://wwwin-metrics.cisco.com/cgi-bin/ws/ws_ddts_query_new.cgi/ws/ws_ddts_query_new.cgi?expert=_id:{}&type=json'.format(
        defect_id)
    try:
        if not defect_id:
            raise Exception('The defect id is not provided.')
        request = requests.get(url, timeout=29)
        if not request.ok:
            raise Exception(
                'The website is unreachable due to {}'.format(
                    request.reason))
        value = request.json()
        if not value:
            raise Exception('the defect id does not exist')
    except Exception as e:
        e = 'Timeout occurred. If you are an external user you cannot use this processor in your datafile.' if isinstance(
            e, requests.exceptions.ReadTimeout) else str(e)
        log.error(e)
    else:
        if value[0]['Status'] not in status:
            section.skipped(
                'The section skipped since the defect_id provided ({}) has an inappropriate status'.format(defect_id))

# ==============================================================================
# processor: stop_traffic
# ==============================================================================


def stop_traffic(section, wait_time=30):
    '''Trigger Processor:
        * Stops traffic on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'stop_traffic'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Successfully connected to traffic generator device "
                     "'{}'".format(dev.name))

        # Stop traffic on TGN
        try:
            dev.stop_traffic(wait_time=wait_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to stop traffic on '{}'".format(dev.name))
        else:
            log.info("Stopped traffic on '{}'".format(dev.name))

# ==============================================================================
# processor: start_traffic
# ==============================================================================


def start_traffic(section, wait_time=30):
    '''Trigger Processor:
        * Starts traffic on traffic generator device
    '''

    # Init

    log.info(banner("processor: 'start_traffic'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Successfully connected to traffic generator device "
                     "'{}'".format(dev.name))

        # Start traffic on TGN
        try:
            dev.start_traffic(wait_time=wait_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to start traffic on '{}'".format(dev.name))
        else:
            log.info("Started traffic on '{}'".format(dev.name))

# ==============================================================================
# processor: disconnect_traffic_device
# ==============================================================================


def disconnect_traffic_device(section, wait_time=30):
    '''Trigger Processor:
        * Disconnect from traffic generator device
    '''

    # Init

    log.info(banner("processor: 'disconnect_traffic_device'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        try:
            dev.disconnect()
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to disconnect from traffic generator "
                           "device '{}'".format(dev.name))
        else:
            log.info("Disconnected from traffic generator device '{}'".
                     format(dev.name))

# ==============================================================================
# processor: connect_traffic_device
# ==============================================================================


def connect_traffic_device(section, wait_time=30):
    '''Trigger Processor:
        * Connects to traffic generator device
    '''

    # Init
    log.info(banner("processor: 'connect_traffic_device'"))

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        try:
            dev.connect(via='tgn')
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to connect to traffic generator device "
                           "'{}'".format(dev.name))
        else:
            log.info("Connected to traffic generator device '{}'".
                     format(dev.name))

# ==============================================================================
# processor: compare_traffic_profile
# ==============================================================================


def compare_traffic_profile(
        section,
        clear_stats=True,
        clear_stats_time=30,
        view_create_interval=30,
        view_create_iteration=10,
        loss_tolerance=1,
        rate_tolerance=2,
        section_profile=''):
    '''Trigger Post-Processor:
        * Create a traffic profile
        * Compare it to 'golden' traffic profile created in common_setup (if executed)
        * Compare it to trigger's golden profile (if provided)
    '''

    log.info(banner("processor: 'compare_traffic_profile'"))

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'compare_traffic_profile' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'compare_traffic_profile' processor
    if 'compare_traffic_profile' in section.parameters and\
       section.parameters['compare_traffic_profile'] is False:
        # User has elected to disable execution of this processor
        log.info(
            "SKIP: Processor 'compare_traffic_profile' skipped - parameter"
            " 'compare_traffic_profile' set to False in trigger YAML")
        return

    if _get_connection_class(section) == 'GenieTgn':
        log.info("SKIP: Processor not supported for Ixia statictgn connection"
                 " implementation")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    # Init
    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Create traffic profile
        try:
            section.tgn_profile = dev.create_traffic_streams_table(
                clear_stats=clear_stats,
                clear_stats_time=clear_stats_time,
                view_create_interval=view_create_interval,
                view_create_iteration=view_create_iteration)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to create traffic profile of configured "
                           "streams on traffic generator device '{}'".
                           format(dev.name))
        else:
            log.info(
                "Created traffic profile of configured streams on traffic "
                "generator device '{}'".format(
                    dev.name))

        # Copy traffic profile to runtime logs
        try:
            pickle_traffic(tgn_profile=section.tgn_profile,
                           tgn_profile_name='{}_traffic_profile'.\
                           format(section.uid.strip('.uut')))
        except Exception as e:
            log.error(e)
            section.failed("Error while saving section golden traffic profile "
                           "to runtime logs")
        else:
            log.info("Saved traffic profile to runtime logs")

        # Compare current traffic profile to section's golden traffic profile
        if section_profile:
            log.info("Comparing current traffic profile to user provided "
                     "golden traffic for section '{}'".format(section.uid))
            try:
                unpicked_section_profile = unpickle_traffic(section_profile)
            except Exception as e:
                log.error(e)
                section.failed("Error unpacking golden traffic profile into "
                               "table format")
            else:
                log.info("User provided golden profile:")
                log.info(unpicked_section_profile)

            # Compare profiles
            try:
                dev.compare_traffic_profile(profile1=section.tgn_profile,
                                            profile2=unpicked_section_profile,
                                            loss_tolerance=loss_tolerance,
                                            rate_tolerance=rate_tolerance)
            except GenieTgnError as e:
                log.error(e)
                section.failed(
                    "Comparison between current traffic profile and "
                    "section golden traffic profile failed")
            else:
                log.info("Comparison between current traffic profile and "
                         "section golden traffic profile passed")

        # Compare current traffic profile to common_setup generated golden
        # traffic profile
        else:
            log.info(
                "Comparing current traffic profile with golden traffic "
                "profile generated in common_setup: profile_traffic subsection")

            # Compare it to common_setup golden profile
            if dev.get_golden_profile().field_names:
                try:
                    dev.compare_traffic_profile(
                        profile1=section.tgn_profile,
                        profile2=dev.get_golden_profile(),
                        loss_tolerance=loss_tolerance,
                        rate_tolerance=rate_tolerance)
                except GenieTgnError as e:
                    log.error(e)
                    section.failed(
                        "Comparison between current traffic profile "
                        "and common_setup:profile_traffic failed")
                else:
                    log.info("Comparison between current traffic profile "
                             "and common_setup:profile_traffic passed")
            else:
                log.info("SKIP: Comparison of current traffic profile "
                         "with common setup traffic profile skipped."
                         "\n'common setup:profile_traffic' has not been "
                         "executed.")

# ==============================================================================
# processor: check_traffic_loss
# ==============================================================================


def check_traffic_loss(section, max_outage=120, loss_tolerance=15,
                       rate_tolerance=2, check_interval=60, check_iteration=10,
                       stream_settings='', clear_stats=False,
                       clear_stats_time=30, pre_check_wait=''):

    # Init
    log.info(banner("processor: 'check_traffic_loss'"))

    if _get_connection_class(section) == 'GenieTgn':
        return _check_traffic_loss_tcl(section)
    else:
        return _check_traffic_loss(section, max_outage=max_outage,
                                   loss_tolerance=loss_tolerance,
                                   rate_tolerance=rate_tolerance,
                                   check_interval=check_interval,
                                   check_iteration=check_iteration,
                                   stream_settings=stream_settings,
                                   clear_stats=clear_stats,
                                   clear_stats_time=clear_stats_time,
                                   pre_check_wait=pre_check_wait)


def _check_traffic_loss(
        section,
        max_outage=120,
        loss_tolerance=15,
        rate_tolerance=2,
        check_interval=60,
        check_iteration=10,
        stream_settings='',
        clear_stats=False,
        clear_stats_time=30,
        pre_check_wait=''):
    '''Trigger Post-Processor:
        * Check traffic loss after trigger execution
        * Controlled via section parameters provided in the trigger datafile
    '''

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'check_traffic_loss' processor
    if 'check_traffic_loss' in section.parameters and\
       section.parameters['check_traffic_loss'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - parameter "
                 "'check_traffic_loss' set to False in trigger YAML")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Check if user provided stream information
        streams_dict = {}
        if stream_settings:
            streams_dict = unpickle_stream_data(
                file=stream_settings,
                copy=True,
                copy_file='{}_stream_data'. format(
                    section.uid.strip('.uut')))
            # Print to logs
            log.info(
                "User has provided outage/tolerance values for the following streams:")
            for stream in streams_dict['traffic_streams']:
                log.info("-> {}".format(stream))
            # Check if streams passed in are valid
            for stream in streams_dict['traffic_streams']:
                if stream not in dev.get_traffic_stream_names():
                    log.error("WARNING: Traffic item '{}' was not found in "
                              "configuration but provided in traffic streams "
                              " YAML".format(stream))

        # Check for traffic loss
        log.info("Checking for traffic outage/loss on all configured traffic streams")
        try:
            dev.check_traffic_loss(max_outage=max_outage,
                                   loss_tolerance=loss_tolerance,
                                   rate_tolerance=rate_tolerance,
                                   check_iteration=check_iteration,
                                   check_interval=check_interval,
                                   outage_dict=streams_dict,
                                   clear_stats=clear_stats,
                                   clear_stats_time=clear_stats_time,
                                   pre_check_wait=pre_check_wait)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Traffic outage/loss observed for configured "
                           "traffic streams.")
        else:
            log.info("Traffic outage/loss is within expected thresholds for "
                     "all traffic streams.")


def _check_traffic_loss_tcl(section):
    '''Trigger Post-Processor:
        * Check traffic loss after trigger execution
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check disable processor
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'check_traffic_loss' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Get parameters from trigger
    traffic_loss = False
    delay = section.parameters.get('tgn_delay', 10)
    tgn_max_outage = section.parameters.get('tgn_max_outage', 60)
    tgn_max_outage_ms = section.parameters.get('tgn_max_outage_ms', None)
    tgn_resynch_traffic = section.parameters.get('tgn_resynch_traffic', True)

    # Get TGN devices from testbed
    testbed = section.parameters['testbed']

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(section.parent, 'mapping_data') or \
           tgn_device.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {tgn_device.name} not specified in mapping datafile")
            return

        # Check if TGN is connected
        if not tgn_device.is_connected():
            log.info("TGN '{}' not connected.".format(tgn_device.name))
            return

        # Set connection alias
        tgn_alias = getattr(
            tgn_device, section.parent.mapping_data['devices'][tgn_device.name]['context'])

        # Check for traffic loss
        log.info(banner("Check for traffic loss"))

        if tgn_max_outage_ms:
            try:
                log.info("Verify traffic outage")
                # Traffic loss is not expected beyond max_outage seconds
                tgn_alias.\
                    calculate_absolute_outage(max_outage_ms=tgn_max_outage_ms)
                log.info("PASS: Traffic stats OK")
            except GenieTgnError:
                traffic_loss = True
        else:
            try:
                # Verify traffic is restored within timeout if there is a loss
                tgn_alias. poll_traffic_until_traffic_resumes(
                    timeout=tgn_max_outage, delay_check_traffic=delay)
                log.info("PASS: Traffic stats OK")
            except GenieTgnError:
                traffic_loss = True

        # Traffic loss observed
        if traffic_loss:
            log.error("FAIL: Traffic stats are showing failure")
            # Resynch traffic stats to steady state
            if tgn_resynch_traffic:
                log.info("Traffic loss is seen and re-synch traffic now")
                try:
                    tgn_alias.get_reference_packet_rate()
                    log.info("PASS: Traffic stats initialized - steady state "
                             "reached after Re-synch")
                except GenieTgnError:
                    log.error("FAIL: Traffic stats initialized - steady state "
                              "not reached after Re-synch")

            # Fail the processor so that the trigger reports a 'fail'
            section.failed()

# ==============================================================================
# processor: clear_traffic_statistics
# ==============================================================================


def clear_traffic_statistics(section, clear_stats_time=30):

    # Init
    log.info(banner("processor: 'clear_traffic_statistics'"))

    if _get_connection_class(section) == 'GenieTgn':
        return _clear_traffic_statistics_tcl(section)
    else:
        return _clear_traffic_statistics(
            section, clear_stats_time=clear_stats_time)


def _clear_traffic_statistics(section, clear_stats_time=30):
    '''Trigger Pre-Processor:
        * Clear statistics on TGN device before execution of a trigger
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check if user has disabled all traffic prcoessors with 'check_traffic'
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'clear_traffic_statistics' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Check if user wants to disable only 'clear_traffic_statistics' processor
    if 'clear_traffic_statistics' in section.parameters and\
       section.parameters['clear_traffic_statistics'] is False:
        # User has elected to disable execution of this processor
        log.info(
            "SKIP: Processor 'clear_traffic_statistics' skipped - parameter"
            " 'clear_traffic_statistics' set to False in trigger YAML")
        return

    # Find TGN devices
    tgn_devices = section.parameters['testbed'].find_devices(type='tgn')
    if not tgn_devices:
        log.info("SKIP: Traffic generator devices not found in testbed YAML")
        return

    for dev in tgn_devices:
        if dev.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {dev.name} not specified in mapping datafile")
            return

        # Connect to TGN
        if not dev.is_connected():
            try:
                dev.connect(via='tgn')
            except GenieTgnError as e:
                log.error(e)
                section.failed("Unable to connect to traffic generator device "
                               "'{}'".format(dev.name))
            else:
                log.info("Successfully connected to traffic generator device "
                         "'{}'".format(dev.name))

        # Clear traffic statistics
        try:
            dev.clear_statistics(wait_time=clear_stats_time)
        except GenieTgnError as e:
            log.error(e)
            section.failed("Unable to clear traffic statistics on traffic "
                           "generator device '{}'".format(dev.name))
        else:
            log.info("Cleared traffic statistics on traffic generator device "
                     "'{}'".format(dev.name))


def _clear_traffic_statistics_tcl(section):
    '''Trigger Pre-Processor:
        * Clear statistics on TGN device before execution of a trigger
        * Controlled via section parameters provided in the triggers datafile
    '''

    # Check disable processor
    if 'check_traffic' in section.parameters and\
       section.parameters['check_traffic'] is False:
        # User has elected to disable execution of this processor
        log.info("SKIP: Processor 'clear_traffic_statistics' skipped - "
                 "parameter 'check_traffic' set to False in trigger YAML")
        return

    # Get parameters from trigger
    tgn_max_outage_ms = section.parameters.get('tgn_max_outage_ms', None)

    # Get TGN devices from testbed
    testbed = section.parameters['testbed']

    for dev in testbed.find_devices(type='tgn'):

        # Set TGN device
        tgn_device = dev

        # Check if device is found in mapping context
        if not hasattr(section.parent, 'mapping_data') or\
           tgn_device.name not in section.parent.mapping_data['devices']:
            log.info(f"Traffic generator device {tgn_device.name} not specified in mapping datafile")
            return

        # Check if TGN is connected
        if not tgn_device.is_connected():
            log.info("TGN '{}' not connected.".format(tgn_device.name))
            return

        # Set connection alias
        tgn_alias = getattr(
            tgn_device, section.parent.mapping_data['devices'][tgn_device.name]['context'])

        if tgn_max_outage_ms:
            try:
                tgn_alias.clear_stats()
            except GenieTgnError as e:
                log.error("Unable to clear traffic generator statistics",
                          from_exception=e)

# ==============================================================================
# processor: disable_clear_traffic
# ==============================================================================


def disable_clear_traffic(section, clear_stats_time=10):

    log.info("Processor 'clear_traffic_statistics' disabled  - "
             "for enabling check the trigger YAML")

    return

def delete_configuration(section, devices, include_os=None, exclude_os=None,
    templates_dir=None, template_name=None, jinja2_parameters=None,
    exclude_devices=None, include_devices=None, timeout=60):

    '''
    Delete configuration on device as processors. 
    Will removing configuration by passing arguments in Jinja2 template
 
    Can be controlled via sections parameters which is provided by the datafile

    Example:
        sections:
            Setup:
                processors:
                    pre:
                        delete_configuration:
                            method: genie.libs.sdk.libs.abstracted_libs.processors.delete_configuration
                                parameters:
                                    templates_dir: Directory path where Jinja2 template is saved
                                    template_name: Template name in templates_dir directory
                                    jinja2_parameters:
                                        learn_interface: 'interface_list' # Key is flag to check learn interface. Value is the variable name in template
                                        host_name: Hostname # Optional or any other arguments required in Jinja2 template
                                    devices: Optional -> When none, will try to fetch all devices from testbed yaml file.
                                        all: # In case need to apply configuration on all devices
                                            templates_dir: Directory path where Jinja2 template is saved
                                            template_name: Template name in templates_dir directory
                                            timeout: Timeout value for delete configuration
                                            jinja2_parameters: # Passing Jinja2 parameters
                                                learn_interface: 'interface_list' # Key is flag to check learn interface. Value is the variable name in template
                                                host_name: Hostname # Optional or any other arguments required in Jinja2 template
                                        GenieRouter: # Device
                                            templates_dir: Directory path where Jinja2 template is saved
                                            template_name: Template name in templates_dir directory
                                            timeout: Timeout value for delete configuration
                                            jinja2_parameters: # Passing Jinja2 parameters
                                                learn_interface: 'interface_list' # Key is flag to check learn interface. Value is the variable name in template
                                                ipv4_management_interface_learn: Learn management interface.
                                                host_name: Hostname # Optional or any other arguments required in Jinja2 template
    Args:
        section (`obj`) : Aetest Subsection object.
        Parameters: Parameters passed from trigger data file.
            devices:
                templates_dir: Directory path where Jinja2 template is saved
                template_name: Template name in templates_dir directory
                timeout: Timeout value for delete configuration. Default to 60.
                jinja2_parameters:
                    learn_interface: 'interface_list' # Key is flag to check learn interface. Value is the variable name in template
                    host_name: Hostname # Optional or any other arguments required in Jinja2 template

    Returns:
        AETEST results

    Raises:
        None
    '''

    log.info(banner("processor: 'delete_configuration'"))

    if exclude_devices:
        log.info("Excluded devices by exclude_devices: {exclude_devices}".format(
            exclude_devices=exclude_devices))

    if include_devices:
        log.info("Included devices by include_devices: {include_devices}".format(
            include_devices=include_devices))

    if include_os:
        log.info("Included OS by include_os: {include_os}"
                    .format(include_os=include_os))

    if exclude_os:
        log.info("Excluded OS by exclude_os: {exclude_os}"
                    .format(exclude_os=exclude_os))

    # Initialize testbed object
    testbed = section.parameters['testbed']

    device_config = {}
    for name, dev in devices.items():
        if name == 'all':
            for testbed_device in list(testbed.devices.keys()):
                device_dict = device_config.setdefault(testbed_device, {})
                templates_dir_local = dev.get('templates_dir', templates_dir)
                template_name_local = dev.get('template_name', template_name)
                timeout_local = dev.get('timeout', timeout)
                jinja2_parameters_local = dev.get('jinja2_parameters', {} if not jinja2_parameters else jinja2_parameters)
                device_dict.update({'templates_dir': templates_dir_local})
                device_dict.update({'template_name': template_name_local})
                device_dict.update({'jinja2_parameters': jinja2_parameters_local})
                device_dict.update({'timeout': timeout_local})
        else:
            device_dict = device_config.setdefault(name, {})
            templates_dir_local = dev.get('templates_dir', templates_dir)
            template_name_local = dev.get('template_name', template_name)
            timeout_local = dev.get('timeout', timeout)
            jinja2_parameters_local = dev.get('jinja2_parameters', {} if not jinja2_parameters else jinja2_parameters)
            device_dict.update({'templates_dir': templates_dir_local})
            device_dict.update({'template_name': template_name_local})
            device_dict.update({'jinja2_parameters': jinja2_parameters_local})
            device_dict.update({'timeout': timeout_local})

    # Loop each devices passed in datafile with it's parameters
    for name, dev in device_config.items():

        if exclude_devices and name in exclude_devices:
            continue

        if include_devices and name not in include_devices:
            continue

        if name not in testbed.devices:
            log.warning("Skipping '{dev}' as it does not exist in the testbed"
                        .format(dev=name))
            continue

        # Find device from testbed yaml file based on device name
        device = testbed.devices[name]

        if include_os and device.os not in include_os:
            continue

        if exclude_os and device.os in exclude_os:
            continue

        # Check if device is connected
        if not device.is_connected():
            log.warning("Skipping '{dev}' as it is not connected"
                        .format(dev=name))
            continue

        log.info("Executing 'delete_configuration' processor on '{dev}'"
                 .format(dev=name))

        try:
            # Check if templates_dir and template_name is passed, else fail the section
            templates_dir_local = dev.get('templates_dir', templates_dir)
            template_name_local = dev.get('template_name', template_name)
            timeout_local = dev.get('timeout', timeout)
            log.info("loading config file {}/{}".format(templates_dir_local,template_name_local))

            # Initialize Jinja2 parameters
            jinja2_parameters_local = dev.get('jinja2_parameters', {} if not jinja2_parameters else jinja2_parameters).copy()
            jinja2_parameters_local.update({'templates_dir': templates_dir_local})
            jinja2_parameters_local.update({'template_name': template_name_local})
            jinja2_parameters_local.update({'timeout': timeout_local})

            # Check if need to learn interfaces from yaml file
            interface_learn_name = jinja2_parameters_local.pop('interface_learn', False)
            if interface_learn_name:
                interface_list = []
                for interface in device.interfaces:
                    interface_list.append(interface)
                jinja2_parameters_local.update({interface_learn_name: interface_list})
                log.info('Interfaces found on device {}: {}'.format(
                    device.name, interface_list))

            ipv4_management_interface_learn = jinja2_parameters_local.pop('ipv4_management_interface_learn', None)

            if ipv4_management_interface_learn:
                variable_name = ipv4_management_interface_learn.get('variable_name')
                interface_name = ipv4_management_interface_learn.get('interface_name')
                ipv4_mgt_int = device.api.get_interface_ip_address(
                        interface=interface_name,
                        address_family='ipv4',
                    )
                if ipv4_mgt_int:
                    ipv4_mgt_int = ipv4_mgt_int.split('/')[0]
                    jinja2_parameters_local.update({variable_name: ipv4_mgt_int})
                    log.info('IPv4 management interface found on device {}: {}'.format(
                        device.name, ipv4_mgt_int))
                else:
                    log.info('IPv4 management interface not found')
            device.api.configure_by_jinja2(**jinja2_parameters_local)
        except Exception as e:
            section.failed(
                "Failed to configure the device {} with the error: {}".format(
                    device.name, str(e)))

def configure_replace(section, devices, timeout=60):
    '''
    Configure replace device as processors. Will replace device configuration based on file_name and file_location
    provided.
 
    Can be controlled via sections parameters which is provided by the datafile

    Example:
        sections:
            Cleanup:
                processors:
                    post: # Can set pre/post based on requirement
                        configure_replace:
                            method: genie.libs.sdk.libs.abstracted_libs.processors.configure_replace
                            parameters:
                                timeout: 60. Default timeout value for all devices.
                                devices:
                                    GenieRouter: # Device
                                        file_location: Config file location
                                        file_name: Config file name
                                        timeout: 300. Timeout value for particular device.
    Args:
        section (`obj`) : Aetest Subsection object.
        devices (`list`): List of devices from sections
        timeout (`int`): Timeout values for all devices. Default is 60. 

    Returns:
        AETEST results

    Raises:
        None
    '''

    log.info(banner("processor: 'configure_replace'"))

    # Initialize testbed object
    testbed = section.parameters['testbed']

    # Loop each devices passed in datafile with it's parameters
    for name, dev in devices.items():
        log.info("Executing 'configure_replace' processor on '{dev}'"
                 .format(dev=name))

        if name not in testbed.devices:
            log.warning("Skipping '{dev}' as it does not exist in the testbed"
                        .format(dev=name))
            continue

        # Find device from testbed yaml file based on device name
        device = testbed.devices[name]

        # Check if device is connected
        if not device.is_connected():
            log.warning("Skipping '{dev}' as it is not connected"
                        .format(dev=name))
            continue

        try:
            file_name = None
            file_location = None
            lookup = Lookup.from_device(device)
            if 'file_location' in dev:
                file_location = dev['file_location']
            else:
                file_location = lookup.sdk.libs.\
                    abstracted_libs.subsection.get_default_dir(
                        device=device)
                if 'file_name' not in dev:
                    log.error('Missing file_name for device {}'.format(name))
                    continue
            if 'file_name' in dev:
                file_name = dev['file_name']

            # Call configure_replace method based on device os
            lookup.sdk.libs.abstracted_libs.subsection.configure_replace(
                device, file_location, timeout=dev.get(
                    'timeout', timeout), file_name=file_name)

        except Exception as e:
            section.failed("Failed to replace config : {}".format(str(e)))
        log.info("Configure replace is done for device {}".format(name))

def reconnect(section, devices, include_os=None, exclude_os=None,
    exclude_devices=None, include_devices=None):

    '''
    Reconnect devices as processors. 
    Will removing configuration by passing arguments in Jinja2 template
 
    Can be controlled via sections parameters which is provided by the datafile

    Example:
        sections:
            Setup:
                processors:
                    post:
                        reconnect:
                            method: genie.libs.sdk.libs.abstracted_libs.processors.reconnect
                            parameters:
                                include_os: List of os to be included
                                exclude_os: List of os to be excluded
                                exclude_devices: List of devices to be excluded
                                include_devices: List of devices to be excluded
                                devices: Optional -> When none, will try to fetch all devices from testbed yaml file.
                                    all: # In case need to apply configuration on all devices
                                        max_time: Maximum time to retry connection
                                        check_interval: Repeat after intervale
                                        sleep_disconnect: Sleep after disconnect
                                        connect_parameters:
                                            <key>: <value>
                                    GenieRouter: # Device
                                        max_time: Maximum time to retry connection
                                        check_interval: Repeat after intervale
                                        sleep_disconnect: Sleep after disconnect
                                        connect_parameters:
                                            <key>: <value>
    Args:
        section (`obj`) : Aetest Subsection object.
        Parameters: Parameters passed from trigger data file.
            include_os: List of os to be included
            exclude_os: List of os to be excluded
            exclude_devices: List of devices to be excluded
            include_devices: List of devices to be excluded
            devices:
                GenieRouter: # Device
                    max_time: Maximum time to retry connection
                    check_interval: Repeat after intervale
                    sleep_disconnect: Sleep after disconnect
                    connect_parameters:
                        <key>: <value>
    Returns:
        AETEST results

    Raises:
        None
    '''

    log.info(banner("processor: 'reconnect'"))

    if exclude_devices:
        log.info("Excluded devices by exclude_devices: {exclude_devices}".format(
            exclude_devices=exclude_devices))

    if include_devices:
        log.info("Included devices by include_devices: {include_devices}".format(
            include_devices=include_devices))

    if include_os:
        log.info("Included OS by include_os: {include_os}"
                    .format(include_os=include_os))

    if exclude_os:
        log.info("Excluded OS by exclude_os: {exclude_os}"
                    .format(exclude_os=exclude_os))

    # Initialize testbed object
    testbed = section.parameters['testbed']

    device_config = {}
    for name, dev in devices.items():
        if name == 'all':
            for testbed_device in list(testbed.devices.keys()):
                device_dict = device_config.setdefault(testbed_device, {})
                sleep_disconnect_local = dev.get('sleep_disconnect', 60)
                connect_parameters_local = dev.get('connect_parameters', {})
                device_dict.update({'sleep_disconnect': sleep_disconnect_local})
                device_dict.update({'connect_parameters': connect_parameters_local})
        else:
            device_dict = device_config.setdefault(name, {})
            sleep_disconnect_local = dev.get('sleep_disconnect', 60)
            connect_parameters_local = dev.get('connect_parameters', {})
            device_dict.update({'sleep_disconnect': sleep_disconnect_local})
            device_dict.update({'connect_parameters': connect_parameters_local})

    # Loop each devices passed in datafile with it's parameters
    for name, dev in device_config.items():

        if exclude_devices and name in exclude_devices:
            continue

        if include_devices and name not in include_devices:
            continue

        if name not in testbed.devices:
            log.warning("Skipping '{dev}' as it does not exist in the testbed"
                        .format(dev=name))
            continue

        # Find device from testbed yaml file based on device name
        device = testbed.devices[name]

        if include_os and device.os not in include_os:
            continue

        if exclude_os and device.os in exclude_os:
            continue

        # Check if device is connected
        if not device.connected:
            log.warning("Skipping '{dev}' as it is not connected"
                        .format(dev=name))
            continue

        log.info("Executing 'reconnect' processor on '{dev}'"
                 .format(dev=name))

        try:
            # Check if templates_dir and template_name is passed, else fail the section
            sleep_disconnect_local = dev.get('sleep_disconnect', None)
            connect_parameters_local = dev.get('connect_parameters', {})

            log.info("Destroying current connection")
            device.destroy_all()
            log.info("Connection destroyed")
            via_local = connect_parameters_local.pop('via', None)
            if not via_local:
                via_local = Dq(device.connections).contains('defaults').get_values('via', 0)
            if via_local:
                dev['connect_parameters'].update({'via': via_local})

            device.connect(**connect_parameters_local)

        except Exception as e:
            section.failed(
                "Failed to configure the device {} with the error: {}".format(
                    device.name, str(e)))