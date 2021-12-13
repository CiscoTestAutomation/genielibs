"""Common verify functions for mpls"""

# Python
import logging
from netaddr import IPNetwork
import re
import time

# Unicon
from unicon.core.errors import SubCommandFailure

# pyats
from pyats.utils.objects import find, R

# Genie
from genie.utils.timeout import Timeout
from genie.libs.sdk.libs.utils.normalize import GroupKeys
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Mpls
from genie.libs.sdk.apis.iosxe.mpls.get import get_mpls_ldp_peer_state

log = logging.getLogger(__name__)


def verify_mpls_forwarding_table_outgoing_label(
        device, ip, expected_label="", same_as_local=False,
        max_time=30, check_interval=10):
    """ Verify local and remote binding labels for ipv4

        Args:
            device (`obj`): Device object
            ip (`str`): IP address
            expected_label (`str`): Expected label
            same_as_local (`bool`):
                True if verify outgoing labels with local label
                False if verify outgoing labels with expected label
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
        Returns:
            result (`bool`): Verified result
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True

        try:
            out = device.parse('show mpls forwarding-table {}'.format(ip))
        except SchemaEmptyParserError:
            log.info("Device output is empty.")
            result = False
            timeout.sleep()
            continue

        reqs = R(['vrf', '(.*)',
                  'local_label', '(?P<local_label>.*)',
                  'outgoing_label_or_vc', '(?P<outgoing_label>.*)',
                  'prefix_or_tunnel_id', '(?P<prefix>.*)',
                  'outgoing_interface', '(?P<interface>.*)',
                  'next_hop', '(?P<next_hop>.*)'])
        found = find([out], reqs, filter_=False, all_keys=True)

        if found:
            keys = GroupKeys.group_keys(reqs=reqs.args, ret_num={},
                                        source=found, all_keys=True)
            for route in keys:
                if same_as_local:
                    log.info("Interface {route[interface]} has local label "
                             "'{route[local_label]}' and outgoing label "
                             "'{route[outgoing_label]}'".format(route=route))
                    if str(route['outgoing_label']) != str(route['local_label']):
                        result = False
                else:
                    log.info(
                        "Interface {route[interface]} outgoing label is "
                        "'{route[outgoing_label]}', exepected to have label "
                        "'{expected}'".format(route=route, 
                                              expected=expected_label))
                    if str(route['outgoing_label']) != str(expected_label):
                        result = False
        else:
            log.error("Could not find any mpls route for {}".format(ip))
            result = False

        if result is True:
            return result

        timeout.sleep()

    return result


def is_interface_igp_sync_mpls_enabled(
    interface, device, vrf="", parsed_output=""):
    """ Verifies if interface has LDP IGP sync enabled 
        from command 'show mpls ldp igp sync'
        
        Args:
            parsed_output ('dict')  : Output from parser
            interface ('str')       : Interface being checked
            vrf  ('str')            : vrf name
            device ('str')          : Device to be executed commands
        Raises:
            None

        Returns
            True
            False

    """

    if not parsed_output:
        try:
            parsed_output = device.parse(
                "show mpls ldp igp sync interface {intf}".format(
                    intf=interface
                )
            )
        except SchemaEmptyParserError:
            raise SchemaEmptyParserError(
                "Fail to parse 'show mpls ldp igp sync "
                "interface {intf}' command".format(intf=interface)
            )

    vrf = vrf if vrf else "default"

    try:
        igp_synchronization_enabled = (
            parsed_output["vrf"]
            .get(vrf, {})
            .get("interface", {})
            .get(interface, {})
            .get("ldp", {})
            .get("igp_synchronization_enabled", False)
        )

        sync_achieved = (
            parsed_output["vrf"]
            .get(vrf, {})
            .get("interface", {})
            .get(interface, {})
            .get("sync", {})
            .get("status", {})
            .get("sync_achieved", False)
        )
    except KeyError:
        return False

    return igp_synchronization_enabled and sync_achieved


def verify_mpls_binding_label(device, ipv4, vrf=None):
    """ Verify local and remote binding labels for ipv4

        Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            ipv4 (`str`): ipv4 with prefix
        Returns:
            verified result
        Raises:
            None
    """
    result = []
    try:
        out = device.parse("show mpls ldp bindings")
    except SchemaEmptyParserError:
        return result
    vrf = vrf if vrf else "default"
    lib_dict = None
    try:
        lib_dict = out["vrf"][vrf]["lib_entry"]
    except KeyError as ke:
        log.error("Could not find key, error: {}".format(str(ke)))
        return False

    if lib_dict and ipv4 in lib_dict:
        local = lib_dict[ipv4].get("label_binding").get("label")
        remote = lib_dict[ipv4].get("remote_binding").get("label")
        if local and remote:
            result.append(
                "Local label for {ipv4} is {local}".format(
                    ipv4=ipv4, local=list(local)
                )
            )
            result.append(
                "Remote label for {ipv4} is {remote}".format(
                    ipv4=ipv4, remote=list(remote)
                )
            )
    else:
        return result

    return "\n".join(result)

def verify_vc_state(device, state, destination_address, vc_id, output=None,
                    max_time=60, check_interval=10):

    """Verify VC state

        Args:
            device (`obj`): Device object
            state (`str`): State of the VC
            destination_address (`str`): Destination address of the vc
            vc_id ('str'): VC id 
        Returns:
            None
    """
    log.info(
        "Verify the vc state "
    )
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not output :
            out=device.parse("show mpls l2transport vc {vc_id}".format(
                                                          vc_id=vc_id))
        else:
            out=output
        if out.q.contains(destination_address):
            if out.q.contains(destination_address)\
                    .get_values("vc_status")[0].lower() == state:
                log.info("State of the vc {vc_id} is {state} for destination"
                        "{destination_address}".format(
                            vc_id=vc_id, state=state,
                            destination_address=destination_address))
                return True
            else:
                log.error(
                    "State of the vc {vc_id} is {state} for destination"
                    "{destination_address}".format(
                        vc_id=vc_id, state=state, 
                        destination_address=destination_address))
                timeout.sleep()
        else:
            log.error(
                "VC {vc_id} not found for destination {destination_address}"\
                    .format(vc_id=vc_id, 
                            destination_address=destination_address))
            timeout.sleep()
    return False            

def is_mpls_ldp_neighbor_in_state(
    device, interface, state, max_time=60, check_interval=10):
    """ Checks if ldp neighbor is in state

        Args:
            device ('obj'): device to use
            interface ('str'): interface to search under
            state ('str'): state

        return:
            True
            False
        Raises:
            None
    """
    log.info("Checking if ldp neighbor is in state: {}".format(state))
    timeout = Timeout(max_time, check_interval)

    while timeout.iterate():
        current_state = get_mpls_ldp_peer_state(device, interface)
        if current_state and state in current_state:
            return True

        timeout.sleep()

    return False



def verify_mpls_forwarding_table_has_prefix_in_subnet_range(
        device, subnet, max_time=120, check_interval=30):

    """ Verifies local label for entries with a prefix inside subnet

        Args:
            device ('obj'): Device to use
            subnet ('str'): Subnet to verify inside
            max_time ('int'): Max time to check
            check_interval ('int'): How often to check

        returns:
            True/False

        raises:
            N/A
    """
    log.info('Checking atleast one entry has a prefix in subnet {subnet} range'
             .format(subnet=subnet))

    try:
        subnet = IPNetwork(subnet)
    except Exception:
        log.info('Bad subnet provided')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse('show mpls forwarding-table')
        except SchemaEmptyParserError:
            log.info('Parser output is empty')
            timeout.sleep()
            continue


        for vrf in out.get('vrf'):
            for local_label in out['vrf'][vrf].get('local_label'):
                for out_label in out['vrf'][vrf]['local_label'][local_label]\
                        .get('outgoing_label_or_vc'):
                    for prefix in out['vrf'][vrf]['local_label'][local_label]\
                            ['outgoing_label_or_vc'][out_label]\
                                .get('prefix_or_tunnel_id'):
                        try:
                            pfx = IPNetwork(prefix)
                        except Exception:
                            continue

                        if pfx in subnet:
                            return True

        timeout.sleep()
    return False

def verify_mpls_forwarding_table_local_label_for_subnet(
        device, subnet, min_range, max_range, in_range=True, max_time=120, 
        check_interval=30):

    """ Verifies local label for entries with a prefix inside subnet

        Args:
            device ('obj'): Device to use
            subnet ('str'): Subnet to verify inside
            min_range ('int'): Minimum label
            max_range ('int'): Maximum label
            in_range ('bool'): True to verify between min_range/max_range, False to verify outside
            max_time ('int'): Max time to check
            check_interval ('int'): How often to check

        returns:
            True/False

        raises:
            N/A
    """

    log.info(
        'Checking all entries where the prefix falls inside subnet {subnet} '
        'range'.format(subnet=subnet))

    try:
        subnet = IPNetwork(subnet)
    except Exception:
        log.info('Bad subnet provided')
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        result = True

        try:
            out = device.parse('show mpls forwarding-table')
        except SchemaEmptyParserError:
            log.info('Parser output is empty')
            timeout.sleep()
            continue

        for vrf in out.get('vrf'):
            for local_label in out['vrf'][vrf].get('local_label'):
                for out_label in out['vrf'][vrf]['local_label'][local_label]\
                        .get('outgoing_label_or_vc'):
                    for prefix in out['vrf'][vrf]['local_label'][local_label]\
                            ['outgoing_label_or_vc'][out_label]\
                                .get('prefix_or_tunnel_id'):
                        try:
                            pfx = IPNetwork(prefix)
                        except Exception:
                            continue

                        if pfx in subnet:
                            if in_range \
                                    and min_range <= local_label <= max_range:
                                continue
                            elif in_range and \
                                    not min_range <= local_label <= max_range:
                                log.info(
                                    'Entry with prefix {prefix} has label '
                                    '{label} which is outside given range '
                                    '{range}. Expected to be inside.'.format(
                                        prefix=prefix, label=local_label,
                                        range='{}-{}'.format(min_range, 
                                                             max_range)))
                                result = False
                            elif not in_range \
                                and min_range <= local_label <= max_range:
                                log.info(
                                    'Entry with prefix {prefix] has label '
                                    '{label} which is inside given range '
                                    '{range}. Expected to be outside.'.format(
                                        prefix=prefix, label=local_label,
                                        range='{}-{}'.format(min_range, 
                                                             max_range)))
                                result = False
                            elif not in_range and \
                                    not min_range <= local_label <= max_range:
                                continue

        if result:
            return True

        timeout.sleep()

    return False
    
def verify_tunnels_state(device, tunnels,
                        prot="up", state="up",
                        max_time=15, check_interval=5,
                        parsed_output=None):

    """ Verifies if the tunnels created are up

        Args:
            prot ('str')  : state of the prot
			state ('str') : state of the tunnel
			tunnels ('list') : list of tunnels to be checked

        Raises:
            Exception

        Returns
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if not parsed_output:
            try:
                parsed_output1 = device.parse(
                        "show mpls traffic-eng tunnels brief"
                        )
            except SchemaEmptyParserError as se:
                pass
            
            tunnel_state=[]
            port_state=[]
            for tunnel in  tunnels:
                res=1
                if tunnel in parsed_output1.q.get_values('tunnel_id'):
                    tunnel_state1=parsed_output1.q.contains(tunnel)\
                        .get_values('state')[0]
                    if tunnel_state1 == state:
                        tunnel_state.append(tunnel)
                    else:
                        log.error("state of the tunnel {tunnel} is {state}"\
                            .format(tunnel=tunnel, state=tunnel_state1))
                        res=0
                    
                    port_state1=parsed_output1.q.contains(tunnel)\
                        .get_values('prot')[0]
                    if port_state1 == prot:
                        port_state.append(tunnel)
                    else:
                        log.error(
                            "protocol state of the tunnel {tunnel} is ""{prot}"\
                                .format(tunnel=tunnel, prot=port_state1))
                        res=0
                else:
                    log.error(
                        "Tunnel id {tunnel} not found in the output"\
                            .format(tunnel=tunnel))
                    return False
            if res:
                log.info("State of the tunnel {tunnel} is {state}".format(
                                tunnel=(','.join(tunnel_state)), state=state))
                log.info("Protocol state of the tunnel {tunnel} is {state}"\
                    .format(tunnel=(','.join(port_state)), state=state))

                return True
        timeout.sleep()
    return False
    
def verify_vc_destination_sect(device, vc_id, destination_peer,
                    vc_state, output_interface, preferred_path=None,
                    preferred_path_state=None,
                    Parsed_output=None, max_time=15, check_interval=5):
        
    """ Verifies the required field in destionation section of VC detail

        Args:
            destination_peer ('str')  : Address of the Peer VC
            vc_id ('str') : vc id of the circuit
			vc_state ('str') : state of the VC
			output_interface ('str') : output interface of the VC
            preferred_path('str') : Preferred path of the vc
            preferred_path_state ('str') : Preferred path state of the vc
            Parsed_output: output of the section passed
        Raises:
            Exception

        Returns
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():  
        result = True
        if not Parsed_output:
            try:
                parsed_output1 = \
                    device.parse("show mpls l2 vc {vc_id} detail | \
                                 sect Destination address".format(vc_id=vc_id))
            except SchemaEmptyParserError as se:
                pass
        else:
            parsed_output1 = Parsed_output    
        dest=parsed_output1.q.get_values('destination_address')[0]
        if destination_peer == dest:
            log.info(
                "Got the expected destionation peer address {destination_peer}"
                    .format(destination_peer=destination_peer))
        else:
            log.error("Got unexpected destionation peer address {dest}"
                      .format(dest=dest))
            result=False
            
        state = parsed_output1.q.get_values('vc_status')[0]
        if vc_state.lower() == state.lower():
            log.info("Got the expected vc state {vc_state}"
                     .format(vc_state=vc_state))
        else:
            log.error("Got unexpected VC state {state}".format(state=state))
            result=False
        
        intf = parsed_output1.q.get_values('output_interface')[0]
        if output_interface.lower() == intf.lower():
            log.info("Got the expected vc state {output_interface}"
                            .format(output_interface=output_interface))
        else:
            log.error("Got unexpected output interface {intf}"
                      .format(intf=intf))
            result=False
            
        if preferred_path:
            ppath=parsed_output1.q.get_values('preferred_path')[0]
            ppath_state=parsed_output1.q.get_values('preferred_path_state')[0]
            if preferred_path.lower() == ppath.lower():
                log.info("Got the expected preferred_path {preferred_path}"
                    .format(preferred_path=preferred_path))
                if not preferred_path_state == ppath_state:
                    log.error("Got the unexpected preferred_path state "
                              "{ppath_state}".format(ppath_state=ppath_state))
                    result=False
            else:
                log.error("Got unexpected preferred path {ppath}"
                          .format(ppath=ppath))
                result=False
        if result:
            return True
        timeout.sleep()
    return False
    
def verify_mpls_ping(
    device, address=None, mask=None, expected_max_success_rate=100, 
    expected_min_success_rate=0,count=None, source=None, vc_id=None, 
    tunnel_id=None, vrf=None, max_time=60, check_interval=10,):
    """Verify ping

    Args:
            device ('obj'): Device object
            address ('str'): Address value
            mask (`str`):  mask of the ip address
            expected_max_success_rate (int): Expected maximum success rate
            expected_min_success_rate (int): Expected minimum success rate
            count ('int'): Count value for ping command
            source ('str'): Source IP address, default: None
            vrf (`str`): vrf id
            vc_id (`str`): vc id
            tunnel_id (`str`): tunnel id
            max_time (`int`): Max time, default: 30
            check_interval (`int`): Check interval, default: 10
    """

    p = re.compile(r"Success +rate +is +(?P<rate>\d+) +percent.*")

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        if address and mask:
            cmd = 'ping mpls ip {address} {mask} repeat {count}'.format(
                    address=address,
                    mask=mask, count=count)
        elif vc_id and address:
            cmd = "ping mpls pseudowire {address} {vc_id}"\
                .format(address=address, vc_id=vc_id)
        elif tunnel_id:
            cmd = "ping mpls traffic-eng tunnel {tunnel_id}"\
                .format(address=address, tunnel_id=tunnel_id)
        else:
            log.info('Need to pass address as argument')
            return False
        try:
            out = device.execute(
                cmd, 
                error_pattern=['% No valid source address for destination'])
        except SubCommandFailure as e:
            timeout.sleep()
            continue

        rate = int(p.search(out).groupdict().get('rate', 0))

        if expected_max_success_rate >= rate >= expected_min_success_rate:
            return True

        timeout.sleep()
    return False

def verify_mpls_forwarding_table_vrf_mdt(device, 
        vrf, 
        prefix_type, 
        expected_prefix,
        bytes_labeled_switched, 
        mdt_cnt=1, 
        max_time=20, 
        check_interval=10):
        
    """ Verifies counters for mdt in mpls forwarding-table

        Args:
            vrf ('str')  : vrf name
            prefix_type ('str') : prefix type 
			expected_prefix ('str') : expected prefix 
			bytes_labeled_switched ('str') : counter value
            mdt_cnt ('int'): mdt data configured
            max_time (`int`, optional): Max time, default: 20
            check_interval (`int`, optional): Check interval, default: 10
        Raises:
            Exception

        Returns
            Boolean
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():  
        result = True
        try:
            parsed_output1 = device.parse("show mpls forwarding-table vrf {vrf}".format(vrf=vrf))
            time.sleep(20)
            parsed_output2=device.parse("show mpls forwarding-table vrf {vrf}".format(vrf=vrf))
        except SchemaEmptyParserError as se:
            pass

        count=0
        ###Verify counters are incrementing or not for mentioned prefix
        for labels in parsed_output1.q.get_values("local_label"):
            if parsed_output1.q.contains(labels).contains(prefix_type):
                learnet_prefix = parsed_output1.q.contains(labels).get_values('prefix_or_tunnel_id')[0]
                if learnet_prefix == expected_prefix:
                    first_counter=parsed_output1.q.contains(labels).get_values("bytes_label_switched")[0]
                    second_counter=parsed_output2.q.contains(labels).get_values("bytes_label_switched")[0]
                    if (int(second_counter)-int(first_counter))>int(bytes_labeled_switched):
                        log.info("Packets are flowing on prefix {expected_prefix}, 1st counter-->{first_counter}, second counter {second_counter}"
                                                     .format(expected_prefix=expected_prefix, first_counter=first_counter, second_counter=second_counter))
                        count+=1
                    else:
                        log.error("Packets are not flowing on prefix {expected_prefix},1st counter-->{first_counter}, second counter {second_counter}, please verify!"
                                                     .format(expected_prefix=expected_prefix, first_counter=first_counter, second_counter=second_counter))
                        result=False
                else:
                    log.error("Got unexpected {learnet_prefix}, expected {expected_prefix} please verify!"
                    .format(learnet_prefix=learnet_prefix,expected_prefix=expected_prefix))
                    result=False
                        
        if count == mdt_cnt:
            log.info("Got expected number of mdt configured {mdt_cnt}".format(mdt_cnt=mdt_cnt))
        else:
            log.error("Got unexpected number of mdt {count}, while expected number of mdt to be {mdt_cnt}, please verify!"
            .format(count=count, mdt_cnt=mdt_cnt))
            result = False
            
        if result:
            return True
        timeout.sleep()
    return False

def verify_mpls_forwarding_table_gid_counter(device, 
        prefix_type,
        bytes_labeled_switched, 
        max_time=20, 
        check_interval=10):
        
    """ Verifies counters for gid in mpls forwarding-table

        Args:
            prefix_type ('str')  : prefix type 
			bytes_labeled_switched ('str') : counter value
            max_time (`int`, optional): Max time, default: 20
            check_interval (`int`, optional): Check interval, default: 10
        Raises:
            Exception

        Returns
            None
    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():  
        result = True
        try:
            parsed_output1 = device.parse("show mpls forwarding-table | sect gid")
            time.sleep(20)
            parsed_output2=device.parse("show mpls forwarding-table | sect gid")
        except SchemaEmptyParserError as se:
            pass
        
        ###Verify counters are incrementing or not for mentioned prefix
        for labels in parsed_output1.q.get_values("local_label"):
            first_counter=parsed_output1.q.contains(labels).get_values("bytes_label_switched")[0]
            second_counter=parsed_output2.q.contains(labels).get_values("bytes_label_switched")[0]
            prefix=parsed_output1.q.contains(labels).get_values('prefix_or_tunnel_id')[0]
            if (int(second_counter)-int(first_counter))>int(bytes_labeled_switched):
                log.info("Packets are flowing on prefix {prefix}, 1st counter-->{first_counter}, second counter {second_counter}"
                                             .format(prefix=prefix, first_counter=first_counter, second_counter=second_counter))
            else:
                log.error("Packets are not flowing on prefix {prefix},1st counter-->{first_counter}, second counter {second_counter}, please verify!"
                                             .format(prefix=prefix, first_counter=first_counter, second_counter=second_counter))
                result=False

        if result:
            return True

        timeout.sleep()
    return False