"""Common configure functions for ip sla"""

import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_ip_sla_icmp_echo(device, entry_num, dest_ip=None, dest_hostname=None, source_ip=None, source_hostname=None, source_interface=None, vrf=None):
    """Configure ip sla icmp-echo on device
    
    Args:
        device (`obj`): Device object
        entry_num (`int`): Entry number
        dest_ip (`str`): Destination ip address
        dest_hostname (`str`): Destination hostname
        source_ip (`str`): Source ip address
        source_hostname (`str`): Source hostname
        source_interface (`str`): Source interface
        vrf (`str`): VRF
    
    Returns:
        None
    
    Raises:
        SubCommandFailure
        ValueError: If destination ip or hostname is not provided
    """
    cmd = []
    cmd.append(f"ip sla {entry_num}")
    dest = dest_ip if dest_ip else dest_hostname
    source = source_ip if source_ip else source_hostname

    if not dest:
        raise ValueError("Destination ip or hostname must be provided")
    else:
        if not source:
            cmd.append(f"icmp-echo {dest}")
        elif source_interface:
            cmd.append(f"icmp-echo {dest} source-interface {source_interface}")
        else:
            cmd.append(f"icmp-echo {dest} source-ip {source}")

    if vrf:
        cmd.append(f"vrf {vrf}")

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip sla icmp-echo on device {dev}. Error:\n{error}"
            .format(
                dev=device.name,
                error=e,
            ))
    
def unconfigure_ip_sla(device, entry_num):
    """Unconfigure ip sla on device
    
    Args:
        device (`obj`): Device object
        entry_num (`int`): Entry number
    
    Returns:
        None
    
    Raises:
        SubCommandFailure
    """
    try:
        device.configure("no ip sla {entry_num}".format(entry_num=entry_num))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ip sla on device {dev}. Error:\n{error}"
            .format(
                dev=device.name,
                error=e,
            ))
    
def configure_ip_sla_schedule(device, entry_num, ageout_time=None, life_time=None, start_time=None, recurring=False):
    """Configure ip sla schedule on device
        
    Args:
        device (`obj`): Device object
        entry_num (`int`): Entry number
        ageout_time (`str`): Ageout time
        life_time (`str`): Life time
        start_time (`str`): Start time
        recurring (`bool`): Recurring
        
    Returns:
        None
        
    Raises:
        SubCommandFailure
    """
    cmd = "ip sla schedule {entry_num}".format(entry_num=entry_num)
    if life_time:
        cmd += " life {life_time}".format(life_time=life_time)
    if start_time:
        cmd += " start-time {start_time}".format(start_time=start_time)
    if ageout_time:
        cmd += " ageout {ageout_time}".format(ageout_time=ageout_time)
    if recurring:
        cmd += " recurring"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip sla schedule on device {dev}. Error:\n{error}"
            .format(
                dev=device.name,
                error=e,
            ))
    
def unconfigure_ip_sla_schedule(device, entry_num):
    """Unconfigure ip sla schedule on device
    
    Args:
        device (`obj`): Device object
        entry_num (`int`): Entry number
    
    Returns:
        None
    
    Raises:
        SubCommandFailure
    """
    try:
        device.configure("no ip sla schedule {entry_num}".format(entry_num=entry_num))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure ip sla schedule on device {dev}. Error:\n{error}"
            .format(
                dev=device.name,
                error=e,
            ))
    
def configure_ip_sla_at_track(device, entry_num, track_num):
    """Configure ip sla track on device
    
    Args:
        device (`obj`): Device object
        entry_num (`int`): Entry number
        track_num (`int`): Track number
    
    Returns:
        None
    
    Raises:
        SubCommandFailure
    """
    try:
        device.configure(f"track {track_num} ip sla {entry_num}")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure ip sla track on device {dev}. Error:\n{error}"
            .format(
                dev=device.name,
                error=e,
            ))
