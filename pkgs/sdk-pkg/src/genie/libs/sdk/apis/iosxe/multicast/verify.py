"""Common verify functions for mulicast"""

# Python
import logging
from netaddr import IPNetwork
import ipaddress
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

log = logging.getLogger(__name__)

def verify_ip_pim_vrf_neighbor(
    device, vrf, neighbors, max_time=60, check_interval=10):
    """Verify pim neighbors

    Args:
            device ('obj'): Device object
            vrf (`str`): vrf id
            neighbors (`list`): neighbors to be verified
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            ###Get the lspvif interface
            output=device.parse("show ip multicast mpls vif")
            lspvif_intf=output.q.get_values("interfaces")[0]

            out = device.parse(
                "show ip pim vrf {vrf} neighbor".format(vrf=vrf))
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        res = True
       
        ##Verify the neighbor has expected lspvif interface
        for neigh in neighbors:
            if neigh in out.q.get_values('neighbors'):
                if not lspvif_intf == out.q.contains(neigh).get_values('interface')[0]:
                    log.error("please verify the Lspvif interface for neighbor {neigh}, expected interface {lspvif_intf}"
                                                    .format(neigh=neigh,lspvif_intf=lspvif_intf))
                    res = False
                else:
                    log.info("got the expected neighbor {neigh} and Lspvif interface {lspvif_intf}"
                                                     .format(neigh=neigh,lspvif_intf=lspvif_intf))
            else:
                log.error("Neighbor {neigh} not found in the output, please verify!".format(neigh=neigh))
                res = False
        if res:
            return True
        timeout.sleep()
    return res
    
def verify_mpls_mldp_neighbor(
    device, neighbors, max_time=60, check_interval=10):
    """Verify mpls mldp neighbors

    Args:
            device ('obj'): Device object
            neighbors (`dict`): neighbors contains interface,ip address.
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    res = True        
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show mpls mldp neighbors")
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        ##verify neighbors count
        expected_neighbors=len(neighbors.keys())
        learnet_neighbors=len(out.q.get_values('mldp_peer'))
        if not expected_neighbors == learnet_neighbors:
            log.error("Verify the number of mldp neighbors learnet, expected neighbors {expected_neighbors}, learnet {learnet_neighbors}"
                        .format(expected_neighbors=expected_neighbors, learnet_neighbors=learnet_neighbors))
            res = False
            
        for neigh in neighbors.keys():
            neigh1= neigh
            neigh = neigh+":0"
            
            if neigh  in out.q.get_values('mldp_peer'):
                ##Verify the state
                state=out.q.contains(neigh).get_values('peer_state')[0].lower()
                if not state == "up":              
                    log.error("please verify the state of the neighbors {neigh1}".format(neigh1=neigh1))
                    res = False
                    
                ##Verify the path
                learnet_path = out.q.contains(neigh).get_values('path')[0]
                expected_path = neighbors.get(neigh1).get('ip_address')
                if not expected_path == learnet_path:
                    log.error("please verify the path {learnet_path} learnet for neighbor {neigh1}, expected path {expected_path}"
                                .format(learnet_path=learnet_path, neigh1=neigh1, expected_path=expected_path))
                    res = False
                    
                ##Verify the interface
                expected_interface = neighbors.get(neigh1).get('interface')
                learnet_interface = out.q.contains(neigh).get_values('ldp_interface')[0]
                if not expected_interface==learnet_interface:
                    log.error("Neighborship learnet on wrong interface {learnet_interface}, expected interface {expected_interface} "
                    .format(learnet_interface=learnet_interface, expected_interface=expected_interface))
            else:
                log.error("Neighbor {neigh1} not found in the output, please verify!".format(neigh1=neigh1))
                res = False
            if res:
                log.info("Got the expected peer {neigh1} with the state {state}, learnet via interface {expected_interface} with ip address {learnet_path}"
                        .format(neigh1=neigh1, state=state, expected_interface=expected_interface, learnet_path=learnet_path))
        if res:
            log.info("Got the expected number of paths {expected_neighbors} for {device}"
                .format(expected_neighbors=expected_neighbors, device=device.name))
            return True
        timeout.sleep()
    return res
    
def verify_mpls_mldp_root(
    device, neighbors, max_time=60, check_interval=10):
    """Verify mpls mldp root

    Args:
            device ('obj'): Device object
            neighbors (`list`): neighbors to be verified
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    timeout = Timeout(max_time, check_interval)
    
    while timeout.iterate():
    
        try:
            out = device.parse("show mpls mldp root")
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        res = True        
  
        ##Veriy the expected root node and expected interface
        for neigh in neighbors:
            root_node = neigh[0]
            if root_node in out.q.get_values('root_node'):
                expected_intf = neigh[1]
                if not expected_intf.lower()== out.q.contains(root_node).get_values('interface')[0].lower():
                    log.error("please verify the interface for root node {root_node}, expected interface {expected_intf}"
                                                    .format(root_node=root_node, expected_intf=expected_intf))
                    res = False
                else:
                    log.info("got the expected root note {root_node} and interface {expected_intf}"
                                                     .format(root_node=root_node, expected_intf=expected_intf))
            else:
                log.error("Root node {root_node} not found in the output, please verify!".format(root_node=root_node))
                res = False
        if res:
            return True
        timeout.sleep()
    return res

def verify_mfib_vrf_hardware_rate(
        device,
        vrf,
        num_of_igmp_groups,
        var,
        max_time=60,
        check_interval=10):
    """Verify mfib vrf hardware rate

    Args:
            device ('obj'): Device object
            vrf (`str`): vrf name
            num_of_igmp_groups (`dict`): contains group ip with traffic sent pps and number of joins
                Eg:{"229.1.1.1":{'rate_pps':20000,'num_of_igmp_groups':10}
            var (`int`): variance
            max_time (`int`, optional): Max time, default: 60
            check_interval (`int`, optional): Check interval, default: 10
    """

    res = True

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse(
                "show ip mfib vrf {vrf} active".format(
                    vrf=vrf))
        except SubCommandFailure as e:
            timeout.sleep()
            continue

        ip_list, hw_rt = [], 0
        for ip in num_of_igmp_groups:
            exp_ip = ip
            for cnt in range(1, int(num_of_igmp_groups[ip]['num_of_igmp_groups'])):
                if exp_ip in output.q.get_values('groups'):
                    hw_rt = output.q.contains(
                        ip).get_values('hw_rate_utilized')[0]
                    rate1 = int(
                        num_of_igmp_groups[ip]['rate_pps']) / int(
                        num_of_igmp_groups[ip]['num_of_igmp_groups'])
                    max_r = int(rate1) + int(var)
                    min_r = int(rate1) - int(var)
                    if hw_rt >= min_r and hw_rt <= max_r:
                        ip_list.append(exp_ip)
                    else:
                        log.debug(
                            f"The ip {exp_ip} has unexpected hardware rate {hw_rt},"
                            f"while expected should be between {min_r} and {max_r}")
                        res = False
                else:
                    log.debug(f"{exp_ip} was not found in the output")
                    res = False
                exp_ip = str(ipaddress.ip_address(exp_ip) + 1)
            if res:
                ips = ",".join(ip_list)
                log.info(f"ip {ips} have expected hardware rate {hw_rt}")
                ip_list = []
        if res:
            return True
        timeout.sleep()
    return False
    
def verify_mfib_vrf_summary(
    device, vrf, s_g, g, g_m, max_time=60, check_interval=10):
    """Verify mfib vrf summary output

    Args:
            device ('obj'): Device object
            vrf (`str`): vrf name
            s_g (`int`): SSM group ip count
            g (`int`):  SM group ip count
            g_m (`int`): Bidir group ip count
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
    
        try:
            output=device.parse("show ip mfib vrf {vrf} summary".format(vrf=vrf))            
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        res = True
        
        ##Verify S,G value 
        if output.q.get_values('s_g')[0] == s_g:

            log.info("Got expected (S,G) value {s_g} for vrf {vrf}".format(s_g=s_g, vrf=vrf))
        else:
            u_s_g=output.q.get_values('s_g')[0]
            log.error("Got unexpected (S,G) value {u_s_g} for vrf {vrf} ,expected value {s_g}".format(u_s_g=u_s_g, vrf=vrf, s_g=s_g))
            res=False
            
        ##Verify *,G value
        if output.q.get_values('g')[0] == g:
            log.info("Got expected (*,G) value {g} for vrf {vrf}".format(g=g, vrf=vrf))
        else:
            u_g=output.q.get_values('g')[0]
            log.error("Got unexpected (*,G) value {u_g} for vrf {vrf} ,expected value {g}".format(u_g=u_g, vrf=vrf, g=g))
            res=False
            
        ##Verify G,M value
        if output.q.get_values('g_m')[0] >= g_m-2 or output.q.get_values('g_m')[0] <= g_m+3:
            log.info("Got expected (*,G/m) value {g_m} for vrf {vrf}".format(g_m=g_m, vrf=vrf))
        else:
            u_g_m=output.q.get_values('g_m')[0]
            log.error("Got unexpected (*,G/m) value {u_g_m} for vrf {vrf} ,expected value {g_m}".format(u_g_m=u_g_m, vrf=vrf, g_m=g_m))
            res=False
            
        if res:
            return True
            
        timeout.sleep()
    return res

def verify_mpls_mroute_groupip(
    device, 
    vrf, 
    groupip, 
    sourceip=None, 
    flag=None,
    outgng_intf=None,
    max_time=60, 
    check_interval=10,
    next_hop=None):
    """Verify SM, SSM group ip output

    Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            groupip (`str`): multicast group ip
            sourceip (`str`, optional): sourceip of the multicast group ip
            flag (`str`, optional): flag
            outgng_intf (`str`, optional): outgoing interface
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
            next_hop (`str`, optional): next hop address, default: None
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse("show ip multicast mpls vif")
            if next_hop:
                lspvif_intf = output.q.contains(next_hop).get_values("interfaces")[0]
            else:
                lspvif_intf = output.q.get_values("interfaces")[0]
            
            output2 = device.parse("show ip mroute vrf {vrf} {groupip}".format(vrf=vrf, groupip=groupip))
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        res = True
        ##Verify multicast groupip            
        if output2.q.get_values('multicast_group')[0] == groupip:
            log.info("Got expected multicast group {groupip}".format(groupip=groupip))
        else:
            log.error("groupip {groupip} not found for vrf {vrf}".format(groupip=groupip, vrf=vrf))
            res=False
            
        ##Verify the source ip
        if sourceip:
            if sourceip in output2.q.get_values('source_address'):
                log.info("Got expected source address {sourceip}".format(sourceip=sourceip))
            else:
                src_ip=output2.q.get_values('source_address')
                log.error("Got unexpected source address {src_ip}, expected source address {sourceip}".format(src_ip=src_ip, sourceip=sourceip))
                res=False
           
        ##Verify the flags           
        if flag in output2.q.contains(sourceip).get_values('flags')[0]:
            log.info("Got expected flag {flag} for source address {sourceip}".format(flag=flag, sourceip=sourceip))
        else:
            flags=output2.q.contains(sourceip).get_values('flags')[0]
            log.error("Got unexpected flag {flags} for source address{sourceip}".format(flags=flags, sourceip=sourceip))
            res=False
            
        ##Verify the incoming interface
        if lspvif_intf == output2.q.contains(sourceip).get_values('incoming_interface_list')[0]:
            log.info("Got expected incoming interface {lspvif_intf} for source address {sourceip}".format(lspvif_intf=lspvif_intf, sourceip=sourceip))
        else:
            incmg_intf=output2.q.contains(sourceip).get_values('incoming_interface_list')[0]
            log.error("Got unexpected incoming interface {incmg_intf} for source address {sourceip}".format(incmg_intf=incmg_intf, sourceip=sourceip))
            res=False
            
        ###Verify outgoing interface
        if outgng_intf.lower() == output2.q.contains(sourceip).get_values('outgoing_interface_list')[0].lower():
            log.info("Got expected outgoing interface {outgng_intf} for source address {sourceip}".format(outgng_intf=outgng_intf, sourceip=sourceip))
        else:
            out_intf=output2.q.contains(sourceip).get_values('outgoing_interface_list')[0].lower()
            log.error("Got unexpected outgoing interface {out_intf} for source address {sourceip}".format(out_intf=out_intf, sourceip=sourceip))
            res=False
            
        if res:
            return True
            
        timeout.sleep()
    return res

def verify_bidir_groupip(
        device, 
        vrf, 
        groupip, 
        upstream_intf=None, 
        outgng_intf=None,
        incmg_intf=None,        
        flag=None,
        output=None,    
        max_time=60, 
        check_interval=10):

    """Verify bidir multicast group ip output

    Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            groupip (`str`): multicast group ip
            upstream_intf (`str`, optional): sourceip of the multicast group ip
            incmg_intf (`str`, optional): incoming interface of the mullticast group ip
            flag (`str`, optional): flag
            outgng_intf (`str`, optional): outgoing interface
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            if not output:
                output = device.parse("show ip mroute vrf {vrf} {groupip}".format(vrf=vrf, groupip=groupip))
            else:
                output=output
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        res = True
        
        ##Verify the upstream
        if upstream_intf:
            upstream_intff=output.q.get_values('upstream_interface')[0]
            if upstream_intff.lower() == upstream_intf.lower():
                log.info("Got expected upstream interface {upstream_intf} for ip {groupip}"
                .format(upstream_intf=upstream_intf,groupip=groupip))
            else:
                log.error("Got unexpected upstream interface {upstream_intff}, expected upstream interface {upstream_intf}"
                .format(upstream_intff=upstream_intff,upstream_intf=upstream_intf))
                res = False

        ##Verify outgoing interface
        if outgng_intf:
            outgng_intff=output.q.get_values('outgoing_interface_list')[0]
            if outgng_intf.lower() in outgng_intff.lower():
                log.info("Got expected outgoing interface {outgng_intf} for ip {groupip}".format(outgng_intf=outgng_intf,groupip=groupip))
            else:
                log.error("Got unexpected outgoing interface {outgng_intff}, expected outgoing interface {outgng_intf}"
                .format(outgng_intff=outgng_intff,outgng_intf=outgng_intf))
                res = False

        ##Verify outgoing interface
        if incmg_intf:
            incmg_intff=output.q.get_values('incoming_interface_list')[0]
            if incmg_intf.lower() in incmg_intff.lower():
                log.info("Got expected incoming interface {incmg_intf} for ip {groupip}".format(incmg_intf=incmg_intf,groupip=groupip))
            else:
                log.error("Got unexpected incoming interface {incmg_intff}, expected incoming interface {incmg_intf}"
                .format(incmg_intff=incmg_intff,incmg_intf=incmg_intf))
                res = False
                
        ##Verify the flag
        if flag:
            flags=output.q.contains(groupip).get_values('flags')[0]
            if flag.lower() in flags.lower():
                log.info("Got expected flag {flag} for ip {groupip}".format(flag=flag,groupip=groupip))
            else:
                log.error("Got unexpected flag {flags}, expected flag {flag}".format(flags=flags,flag=flag))
                res = False
             
        if res:
            return True
            
        timeout.sleep()
    return res            

def verify_mpls_mldp_count(
    device, 
    mp2mp_entries, 
    p2mp_entries, 
    mldp_roots, 
    mldp_neighbors, 
    max_time=60, 
    check_interval=10):
    """Verify mpls mldp count

    Args:
            device ('obj'): Device object
            mp2mp_entries ('int'): number of m2mp entries
            p2mp_entries ('int'): number of p2mp entries
            mldp_roots ('int'): number of mldp root
            mldp_neighbors (`int`): number of mldp neighbotss
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        res = True
        try:
            out = device.parse("show mpls mldp count")
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        ##verify mp2mp entry
        if str(out.q.get_values('number_of_mp2mp_entries')[0]):
            expected_mp2mp_entries=out.q.get_values('number_of_mp2mp_entries')[0]
            if mp2mp_entries != expected_mp2mp_entries:
                res = False
        else:
            log.debug("no mp2mp entries found in the output, please verify!")
            res = False

        ##verify p2mp entries
        if str(out.q.get_values('number_of_p2mp_entries')[0]):
            expected_p2mp_entries=out.q.get_values('number_of_p2mp_entries')[0]
            if not (expected_p2mp_entries <= p2mp_entries and expected_p2mp_entries>= p2mp_entries):
                res = False
        else:
            log.debug("no p2mp entries found in the output")
            res = False    

        ##verify mldp root entries
        if out.q.get_values('total_number_of_mldp_roots')[0]:
            expected_mldp_roots=out.q.get_values('total_number_of_mldp_roots')[0]
            if mldp_roots != expected_mldp_roots:
                res = False
        else:
            res = False

        ##verify mldp neighbor entries
        if str(out.q.get_values('total_number_of_mldp_neighbors')[0]):
            expected_mldp_neighbors=out.q.get_values('total_number_of_mldp_neighbors')[0]
            if mldp_neighbors != expected_mldp_neighbors:
                res = False
        else:
            log.debug("no mldp neighbors found in the output")
            res = False   
            
        if res:
            return True
        timeout.sleep()
    return res


def verify_ip_mroute_mgroup_rpf_state(
    device, multicast_group, expected_rpf, ip_family, vrf=None,
    source_ip=None, max_time=30, check_interval=10):
    """Verify rpf info state for particular mcast group and source ip (if given)
        in 'show ip/ipv6 mroute {vrf <vrf>} <multicast_group> {<source_ip>}'

    Args:
            device ('obj'): Device object
            multicast_group (`str`): multicast group to be verified
            expected_rpf ('str',): expected rpf info.ex: Registering etc 
            ip_family ('str'): either ip ot ipv6
            vrf ('str', optional): vrf
            source_ip ('str',optional): source_ip to be verified
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    Returns:
            result(`bool`): verified result
    Raises:
            None

    """
    if ip_family not in ['ip','ipv6']:
        print("Please provide ip_family either as \'ip\' or \'ipv6\' only")
        return False
    # checking for source addr as *
    source_addr = '' if source_ip == '*' else source_ip
    if (source_ip and vrf):        
        cmd = f"show {ip_family} mroute vrf {vrf} {multicast_group} {source_addr}"    
    elif vrf:
        cmd = f"show {ip_family} mroute vrf {vrf} {multicast_group}"
    elif source_ip:
        cmd = f"show {ip_family} mroute {multicast_group} {source_addr}"
    else:
        cmd = f"show {ip_family} mroute {multicast_group}"

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse(cmd)
        except SubCommandFailure as e:
            timeout.sleep()
            continue        
        if out:
            family_type = 'ipv4' if ip_family == 'ip' else 'ipv6'
            vrf_name = 'default' if (not vrf) else vrf
            # verify for multicast_group in output
            if out['vrf'][vrf_name]['address_family'][family_type]:
                if source_ip:
                    rpf_info_list = out.q.contains(multicast_group).contains(\
                            source_ip).get_values("rpf_info")
                else:
                    rpf_info_list = out.q.contains(multicast_group)\
                            .get_values("rpf_info")
                rpf_info_list = [rpf.lower() for rpf in rpf_info_list]
                if expected_rpf.lower() in rpf_info_list:
                    return True
        timeout.sleep()
    return False


def verify_ip_mfib_hw_pkt_per_sec(
    device, multicast_group, source_ip, ip_family, rate=90, vrf=None, 
    max_time=30, check_interval=10
):
    """Verify for hw packet per sec will be >= rate if given 
       for particular mcast-group & source ip in 
           'show ip mfib multicast_group source_ip' - if no vrf, no ip_family
           'show ip mfib vrf <vrf> multicast_group source_ip' - if vrf given and no ip_family
           'show ipv6 mfib multicast_group source_ip' - if ip_family given and no vrf
           'show ipv6 mfib vrf <vrf> multicast_group source_ip' - if both vrf and ip_family given
           ex:
                (1.1.1.1,225.1.1.1) Flags: HW
                SW Forwarding: 0/0/0/0, Other: 11/0/11
                HW Forwarding:   6225553/705/115/634, Other: 0/0/0

    Args:
            device ('obj'): Device object
            multicast_group (`str`): multicast group to be verified
            source_ip ('str'): source_ip to be verified           
            ip_family ('str'): either ipv4 or ipv6 
            rate ('int', optional): the expected rate of pkts per sec  
            vrf ('str',optional): vrf   
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
            
    Returns:
            result(`bool`): verified result
    Raises:
            None

    """
    if ip_family not in ['ip','ipv6']:
        log.error("Please provide ip_family either as ip or ipv6 only")
        return False

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        # Get hw counters
        actual_hw_pkts_per_sec = device.api.get_ip_mfib_hw_pkts_per_sec(
            multicast_group=multicast_group,
            source_ip=source_ip,
            ip_family=ip_family,
            vrf=vrf
        )
        # incase of value is zero
        if actual_hw_pkts_per_sec != None:
            # Getting hw packets per second and storing it as int            
            if actual_hw_pkts_per_sec > rate:
                return True       
        timeout.sleep()
    return False


def verify_ip_pim_neighbor(
    device, expected_neighbor, expected_interface=None, max_time=30, 
    check_interval=10):
    """Verify pim neighbors and along with the interface configured incase of
       interface is given.

    Args:
            device ('obj'): Device object
            expected_neighbor (`str`): neighbor to be verified
            expected_interface ('str', optional): expected interface 
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    Returns:
            result(`bool`): verified result
    Raises:
            None

    """
    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            out = device.parse("show ip pim neighbor")
        except SubCommandFailure as e:
            timeout.sleep()
            continue
        if out:
            # Verify the neighbor has expected interface
            if expected_interface:
                # Getting corresponding neighbor attached to the interface
                neighbors_list = out.q.contains('interfaces').contains\
                    (expected_interface).get_values("neighbors")            
            else:
                # Getting all the neighbors
                neighbors_list = out.q.get_values("neighbors")
            
            if expected_neighbor in neighbors_list:
                return True

        timeout.sleep()
    return False


def verify_ip_mroute_group_and_sourceip(
    device, 
    groupip,
    sourceip,
    ip_family,
    vrf=None,  
    flags=None,
    incmg_intf=None,
    outgng_intf=None,
    incmg_extranet_vrf=None,
    extranet_rec=[],
    max_time=30, 
    check_interval=10):
    """
    Verify ip/ipv6 source&Multicast group ip and related data for particular
    source&group ip combination, in 'show ip/ipv6 mroute mgroup source'  
    Args:
            device (`obj`): Device object
            vrf (`str`): Vrf name
            groupip (`str`): multicast group ip
            ip_family ('str'): ip address family ip/ipv6
            sourceip (`str`, optional): sourceip of the multicast group ip
            flag (`str`, optional): flag
               checks the flag that each character in actual output 
               just like subset of a set
            incmg_intf('str', optional): incoming interface
            outgng_intf (`str` or 'list', optional): outgoing interface
            incmg_extranet_vrf (`str`, optional): incoming interface
            extranet_rec ('list', optional): ['extranet_vrf',extranet_src,extranet_grp,extranet_flags]
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """
    if ip_family not in ['ip','ipv6']:
        log.error("Please provide ip_family either as \'ip\' or \'ipv6\' only")
        return False
    # checking for * source
    source_addr = '' if sourceip == '*' else sourceip
    if vrf:
        cmd = f"show {ip_family} mroute vrf {vrf} {groupip} {source_addr}"
    else:
        cmd = f"show {ip_family} mroute {groupip} {source_addr}"

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse(cmd)            
        except SubCommandFailure as e:
            timeout.sleep()
            continue
        res = True
        if output:
            family_type = 'ipv4' if ip_family == 'ip' else 'ipv6'
            vrf_name = 'default' if (not vrf) else vrf            
            ##Verify multicast groupip            
            if not output['vrf'][vrf_name]['address_family'][family_type]:                
                res = False
        ##Verify the source ip related data
        if res and (sourceip in output.q.get_values('source_address')):
            log.info("Got expected source address {sourceip}".format(\
                sourceip=sourceip))
            source_ip_dict = output['vrf'][vrf_name]['address_family'][family_type]\
                ['multicast_group'][groupip]['source_address'][sourceip] 
           
            ##Verify the flags    
            if flags:       
                actual_flags=output.q.contains(sourceip).get_values('flags')[0]
                unmatched_flags = []
                unmatched_flags = [each_flag for each_flag in flags.lower() if each_flag not in actual_flags.lower()]
                if len(unmatched_flags) == 0:
                    log.info("Got expected flag {flags} for source ip "\
                        "{sourceip}".format(flags=flags,sourceip=sourceip))
                else:
                    log.error("Got mismatched flags {unmatched_flags} in "\
                            "actual flags {actual_flags}".format(unmatched_flags=unmatched_flags,\
                            actual_flags=actual_flags))
                    res=False

            ##Verify the incoming interface            
            if incmg_intf:
                # if incoming intf is null then the key will not appear in parsed data
                if 'incoming_interface_list' in source_ip_dict.keys():
                    actual_incmg_intf = output.q.contains(sourceip).get_values('incoming_interface_list')[0]
                    if incmg_intf.lower() in actual_incmg_intf.lower():
                            log.info("Got expected incoming interface {incmg_intf} for source address"\
                                " {sourceip}".format(incmg_intf=incmg_intf, sourceip=sourceip))
                    else:
                            log.error("Unable to find incoming interface {incmg_intf} for "\
                                "source address {sourceip}, actual incmg intf is {actual_incmg_intf}".\
                                format(incmg_intf=incmg_intf, sourceip=sourceip,actual_incmg_intf=actual_incmg_intf))
                            res=False
                    if incmg_extranet_vrf != None:
                        actual_incmg_extranet_vrf = output.q.contains('incoming_interface_list').get_values('lisp_vrf')[0]
                        if actual_incmg_extranet_vrf == incmg_extranet_vrf:
                            log.info("Got expected incoming extranet vrf {incmg_extranet_vrf} for source address"\
                                " {sourceip}".format(incmg_extranet_vrf=incmg_extranet_vrf, sourceip=sourceip))
                        else:
                            log.error("Unable to find incoming interface {incmg_extranet_vrf} for "\
                                "source address {sourceip}, actual incmg intf is {actual_incmg_extranet_vrf}".\
                                format(incmg_extranet_vrf=incmg_extranet_vrf, sourceip=sourceip,actual_incmg_extranet_vrf=actual_incmg_extranet_vrf))

                else:
                    log.error("Incoming interface list is Null")
                    res = False
            ###Verify outgoing interface
            if outgng_intf:
                if 'outgoing_interface_list' in source_ip_dict.keys():

                    actual_out_intf = output.q.contains(sourceip).get_values('outgoing_interface_list')[0]
                    actual_out_intf_list = output.q.contains(sourceip).get_values('outgoing_interface_list')



                    if isinstance(outgng_intf,str):
                        if outgng_intf.lower() in actual_out_intf.lower():
                            log.info("Got expected outgoing interface {outgng_intf} for "\
                                "source address {sourceip}".format(\
                                    outgng_intf=outgng_intf, sourceip=sourceip))
                        else:
                            log.error("Unable to find outgoing interface {outgng_intf} for "\
                                "source address {sourceip}, actual outgoing intf is {actual_out_intf}".format(\
                                outgng_intf=outgng_intf, sourceip=sourceip, actual_out_intf=actual_out_intf))
                            res=False
                    if isinstance(outgng_intf,list):
                        unmatched_intf = []
                        for intf in outgng_intf:
                            if intf not in actual_out_intf_list:
                                unmatched_intf.append(intf)
                        if unmatched_intf:
                            log.error("Unable to find outgoing interface"
                                f" {unmatched_intf} \n for source {sourceip},"
                                f" actual outgoing intf is {actual_out_intf}")
                            res=False
            # Verify Extranet interface
            if extranet_rec:
                if 'extranet_rx_vrf_list' in source_ip_dict.keys():
                    actual_extranet_out_vrf = output.q.contains(sourceip).get_values('extranet_rx_vrf_list')[0]
                    actual_extranet_src = output.q.contains(sourceip).get_values('e_src')[0]
                    actual_extranet_grp = output.q.contains(sourceip).get_values('e_grp')[0]
                    actual_extranet_flags = output.q.contains(sourceip).get_values('e_flags')[0]

                    if extranet_rec[0] == actual_extranet_out_vrf:
                        log.info("Got expected extranet vrf {extranet_rec} for "\
                            "source address {sourceip}".format(\
                                extranet_rec=extranet_rec[0], sourceip=sourceip))
                    else:
                        log.error("Unable to find outgoing extranet vrf {extranet_rec} for "\
                            "source address {sourceip}, actual outgoing extranet vrf is {actual_out_vrf}".format(\
                            extranet_rec=extranet_rec[0], sourceip=sourceip, actual_out_vrf=actual_extranet_out_vrf))
                        res=False

                    if extranet_rec[1] == actual_extranet_src:
                        log.info("Got expected extranet source {extranet_rec} for "\
                            "source address {sourceip}".format(\
                                extranet_rec=extranet_rec[1], sourceip=sourceip))
                    else:
                        log.error("Unable to find outgoing extranet source {extranet_rec} for "\
                            "source address {sourceip}, actual outgoing extranet source is {actual_out_src}".format(\
                            extranet_rec=extranet_rec[1], sourceip=sourceip, actual_out_src=actual_extranet_src))
                        res=False

                    if extranet_rec[2] == actual_extranet_grp:
                        log.info("Got expected extranet source {extranet_rec} for "\
                            "source address {sourceip}".format(\
                                extranet_rec=extranet_rec[2], sourceip=sourceip))
                    else:
                        log.error("Unable to find outgoing extranet source {extranet_rec} for "\
                            "source address {sourceip}, actual outgoing extranet source is {actual_out_grp}".format(\
                            extranet_rec=extranet_rec[2], sourceip=sourceip, actual_out_grp=actual_extranet_grp))
                        res=False

                    if extranet_rec[3] == actual_extranet_flags:
                        log.info("Got expected extranet source {extranet_rec} for "\
                            "source address {sourceip}".format(\
                                extranet_rec=extranet_rec[3], sourceip=sourceip))
                    else:
                        log.error("Unable to find outgoing extranet source {extranet_rec} for "\
                            "source address {sourceip}, actual outgoing extranet source is {actual_out_flag}".format(\
                            extranet_rec=extranet_rec[3], sourceip=sourceip, actual_out_flag=actual_extranet_flags))
                        res=False

                else:
                    log.error("Extranet receiver interface list is Null")
                    res = False

        elif not res:
            log.error("Unable to find the multicast group {}".format(groupip))
            res = False
        else:
            src_ip = output.q.get_values('source_address')
            log.error("Unable to find source address {sourceip}, actual "\
                "source address {src_ip}".format(sourceip=sourceip,\
                    src_ip=src_ip))
            res=False
            
        if res:
            return True
        timeout.sleep()

    return res
