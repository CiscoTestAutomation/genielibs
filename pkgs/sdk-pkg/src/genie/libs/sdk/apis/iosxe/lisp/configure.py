"""Common configure functions for lisp"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_lisp_enhanced_forwarding(device,instance_id,vlan) :
    """ configures enhanced forwarding in lisp 
        Args:
            device (`obj`): Device object
            instance_id (`str`): instance_id under lisp
            vlan (`int`): vlan number
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    cmd = [
              "router lisp",
              f"instance-id {instance_id}",
              'service ethernet',
              f'eid-table vlan {vlan}',
              'enhanced-forwarding'       
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure enhanced forwarding under lisp instance-id {instance_id} for vlan {vlan} "
            )

def unconfigure_lisp_enhanced_forwarding(device,instance_id,vlan) :
    """ unconfigures enhanced forwarding in lisp 
        Args:
            device (`obj`): Device object
            instance_id (`str`): instance_id under lisp
            vlan (`int`): vlan number
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    cmd = [
              "router lisp",
              f"instance-id {instance_id}",
              'service ethernet',
              f'eid-table vlan {vlan}',
              'no enhanced-forwarding'       
          ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure enhanced forwarding under lisp instance-id {instance_id} for vlan {vlan} "
            )

def configure_lisp_l2_flooding(device,instance_id,vlan,mcast_ip='239.0.0.1',packet1="arp-nd",packet2="unknown-unicast") :
    """ configures l2 flooding under lisp 
        Args:
            device (`obj`): Device object
            instance_id (`str`): instance_id under lisp
            vlan (`int`): vlan number
            mcast_ip('str'): broadcast-underlay ip, defaults to '239.0.0.1'
            packet1('str'):type of packet to flood,defaults to 'arp-nd'
            packet2('str'):type of packet to flood,defaults to 'unknown-unicast'
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    cmd = [
              "router lisp",
              f"instance-id {instance_id}",
              'service ethernet',
              f'eid-table vlan {vlan}',
              f'broadcast-underlay {mcast_ip}',       
              f'flood {packet1}',
              f'flood {packet2}',
          ]
   
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure l2 flooding under lisp instance-id {instance_id} for vlan {vlan} "
            )
    
def unconfigure_lisp_l2_flooding(device,instance_id,vlan,mcast_ip="239.0.0.1",packet1="arp-nd",packet2="unknown-unicast") :
    """ unconfigures l2 flooding under lisp 
        Args:
            device (`obj`): Device object
            instance_id (`str`): instance_id under lisp
            vlan (`int`): vlan number
            mcast_ip('str'): broadcast-underlay ip, defaults to '239.0.0.1'
            packet1('str'):type of packet to flood,defaults to 'arp-nd'
            packet2('str'):type of packet to flood,defaults to 'unknown-unicast'
        Returns:
            None
        Raises:
            SubCommandFailure
    """ 
    cmd = [
              "router lisp",
              f"instance-id {instance_id}",
              'service ethernet',
              f'eid-table vlan {vlan}',
              f'no broadcast-underlay {mcast_ip}',       
              f'no flood {packet1}',
              f'no flood {packet2}',
          ]
   
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure l2 flooding under lisp instance-id {instance_id} for vlan {vlan} "
            )
 
def configure_no_instance_lisp(device, instance_id):
    """ unconfigure instance_id router-lisp  
        Args:
            device (`obj`): Device object
            instance_id (`str`): instance_id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Removing the instance from {device}".format(device=device))
    cmd = ["router lisp",f"no instance-id {instance_id}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'It has no instance-id {instance_id} on {device}. Error:\n{e}')
