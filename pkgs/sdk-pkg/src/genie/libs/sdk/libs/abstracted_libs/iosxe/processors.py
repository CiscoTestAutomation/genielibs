# Ats
import logging
from pyats.log.utils import banner
from pyats.utils.objects import find, R,NotExists

# genie.libs
from genie.libs import ops
from genie.libs.parser.iosxe.show_interface import ShowInterfacesCounters, \
                                                   ShowIpInterfaceBrief, \
                                                   ShowIpv6Interface
from genie.libs.sdk.libs.utils.normalize import GroupKeys

log = logging.getLogger(__name__)

def check_interface_counters(section, ports, keys, threshold):
    '''Check interface counters values are as epected

    Can be controlled via sections parameters which is provided by the
    triggers/verification datafile

    Args:
      Mandatory:
        section (`obj`): Aetest Subsection object.
        ports (`set`) : The port interfaces need to be checked
        keys (`list`) : The counters keys parser path list

    Returns:
        None


    Raises:
        None

    '''
    log.info(banner('Compare interfaces {i} counters values with given expected values {v}'
        .format(i=ports, v=threshold)))

    def islargerthan(val1, val2):
        assert val1 > val2

    # Get ping ip and vrf
    if section and getattr(section, 'parameters', {}):
        testbed = section.parameters.get('testbed', {})
        uut = testbed.devices['uut']

        # initial msg
        msg = ''

        log.info(banner('Get the counters data on {d} from "show interfaces counter"'
            .format(d=uut.name)))

        # check counters
        for port in ports:
            try:
                counter_output = ShowInterfacesCounters(uut).parse(interface=port)
            except Exception as e:
                section.failed('Cannot get counters information')

            # calculate the counters
            for path in keys:
                ret = find([counter_output], R(path), filter_=False)
                oper = threshold.split('(')[0]
                val2 = int(threshold.split('(')[1].split(')')[0])

                log.info(banner('Compare learned value {v1} is {o} expect value {v2}'
                    .format(v1=ret[0][0], v2=val2, o=oper)))
                try:
                    locals()[oper](val1=ret[0][0], val2=val2)
                except Exception as e:
                    section.failed('Get {k} value is {v1}, expect {t}'
                        .format(k=path, v1=ret[0][0], t=threshold), from_exception=e)
                msg += 'Get {k} value {v1} {t}\n'.format(k=path, v1=ret[0][0], t=threshold)

        log.info(msg)


def learn_routing(device, address_family, paths, ops_container=[], ret_container={}):
    '''Dynamic learn routing information by using the paths that specified,
    and store the data into dictionary.

    Args:
      Mandatory:
        device (`obj`): Device object
        address_family (`str`) : Value of address_family, could be ipv4/ipv6
        paths (`list`) : Ops paths to look for the desired routing values
      Optional:
        ops_container (`list`): Container to store the learned ops,
                                in case multiple learning
        ret_container (`dict`) : Container to store the learned routes
                                 to let parent update on it

    Returns:
        None. Instead of returned values, it will store the learned
              information in the container to let parent update on it.

              The container values for ret_container looks like below
              10.9.1.0/24: {
                 10.9.1.2: {'R5': {route: 10.9.1.0/24, intf: Vlan99, vrf: default}},
                 10.9.1.1: {'R1': {route: 10.9.1.0/24, intf: Vlan99, vrf: default}},
              }
              10.9.1.0/24: {
                 10.9.1.2: {'R5': {route: 10.9.1.0/24, intf: GigabitEthernet1/0/4, vrf: test2}},
                 10.9.1.1: {'R5': {route: 10.9.1.0/24, intf: Vlan99, vrf: test1}},
              }


    Raises:
        Exception: Routing ops cannot sucessfully learned

    '''
    log.info(banner(
        "learn routing info on device {}".format(device.name)))
    # get ip and vrf
    routing_ops = ops.routing.iosxe.routing.Routing(device)

    # learn the routing ops
    try:
        routing_ops.learn()
    except Exception as e:
        raise Exception('cannot learn routing ops: {}'.format(e))

    ops_container[device.name] = routing_ops

    log.info(banner(
        "Get routing groups from device {}".format(device.name)))

    rs = [R(p) for p in paths]
    ret = find([routing_ops], *rs, filter_=False, all_keys=True)
    if ret:
        groups = GroupKeys.group_keys(
                    reqs=paths, ret_num={},source=ret,all_keys=True)
        if groups:
            # learn interfaces ip
            if 'ipv4' in address_family:
                ip_out = ShowIpInterfaceBrief(device).parse()
                
            else:
                ip_out = ShowIpv6Interface(device).parse()
                
            for keys in groups:
                # find interface ip
                if 'ipv4' in  address_family:
                    intf_r = [R(['interface', keys['intf'], 'ip_address', '(?P<ip>.*)'])]
                else:
                    intf_r = [R([keys['intf'], 'ipv6', '(?P<ip_addr>.*)', 'ip', '(?P<ip>.*)']),
                              R([keys['intf'], 'ipv6', '(?P<ip_addr>.*)', NotExists('origin')])]
                ip = find([ip_out], *intf_r, filter_=False)
                if ip:
                    ip = ip[0][0]
                    ret_container.setdefault(keys['route'], {}).\
                        setdefault(ip, {}).update({device.name: keys})
