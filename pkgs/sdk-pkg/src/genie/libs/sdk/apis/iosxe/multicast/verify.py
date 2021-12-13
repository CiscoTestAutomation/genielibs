"""Common verify functions for mulicast"""

# Python
import logging
from netaddr import IPNetwork
import re

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
    device, vrf, num_of_igmp_groups, var, rate_pps, max_time=60, check_interval=10):
    """Verify mfib vrf hardware rate
    Args:
            device ('obj'): Device object
            neighbors (`list`): neighbors to be verified
            max_time (`int`, optional): Max time, default: 30
            check_interval (`int`, optional): Check interval, default: 10
    """

    res = True

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output=device.parse("show ip mfib vrf {vrf} active".format(vrf=vrf))            
        except SubCommandFailure as e:
            timeout.sleep()
            continue
            
        ip_list,hd_rt=[],0
        
        ##Verify wether the ips learnet have expected harware rate or not
        for ip in output.q.get_values('groups'):
            hd_rt=output.q.contains(ip).get_values('hw_rate_utilized')[0]
            rate1 = int(rate_pps)/int(num_of_igmp_groups)
            max_r = int(rate1)+int(var)
            min_r = int(rate1)-int(var)
            if hd_rt>= min_r and hd_rt<=max_r:
                ip_list.append(ip)
            else:
                log.error("The ip {ip} has unexpected hardware rate {hd_rt}, while expected should be between {min_r} and {max_r}".format(ip=ip, hd_rt=hd_rt, min_r=min_r, max_r=max_r))
                res = False             
            
        if res:
            ips=",".join(ip_list)
            log.info("ip {ip_list} have expected hardware rate {hd_rt}".format(ip_list=ips,hd_rt=hd_rt))
            return True
            
        timeout.sleep()
    return res
    
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
    check_interval=10):
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
    """

    timeout = Timeout(max_time, check_interval)
    while timeout.iterate():
        try:
            output = device.parse("show ip multicast mpls vif")
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
