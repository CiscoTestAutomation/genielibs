'''IOSXE configure functions for iiot rep feature'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False, trunk=True):
    """Configures REP segment
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to configure
            segmentnum ('str'): Segment number to configure
            vlan ('str', 'optional'): Vlan to configure
            edge_port ('bool' 'optional'): Configure edge port
            no_neighbor ('bool' 'optional'): Configure no neighbor
            trunk('bool', 'optional'): Configure switchport trunk
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring REP segment {} on interfaces {}".format(segmentnum, intfs))

    if no_neighbor:
        rep_command = "rep segment {} edge no-neighbor".format(segmentnum)
    elif edge_port:
        rep_command = "rep segment {} edge".format(segmentnum)
    else:
        rep_command = "rep segment {}".format(segmentnum)
    
    for intf in intfs:
        if trunk:
            config_list = [
                "interface {}".format(intf),
                "switchport mode trunk",
                rep_command,
                "shut",
                "no shut"
            ]
        else:
            config_list = [
                "interface {}".format(intf),
                rep_command,
                "shut",
                "no shut"
            ]
        if vlan:
            config_list.append("switchport trunk allowed vlan {}".format(vlan))
            config_list.append("vlan {}".format(vlan))
        try:
            device.configure(config_list)
        except SubCommandFailure as e:
            raise SubCommandFailure("Error configuring interface {}: {}".format(intf, e))

def configure_fast_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False):
    """Configures fastREP 
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to configure
            segmentnum ('str'): Segment number to configure
            vlan ('str', 'optional'): Vlan to configure
            edge_port ('bool' 'optional'): Configure edge port
            no_neighbor ('bool' 'optional'): Configure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info("Configuring fastREP segment {} on interfaces {}".format(segmentnum, intfs))

    if no_neighbor:
        rep_command = "rep segment {} edge no-neighbor".format(segmentnum)
    elif edge_port:
        rep_command = "rep segment {} edge".format(segmentnum)
    else:
        rep_command = "rep segment {}".format(segmentnum)
    
    for intf in intfs:
        config_list = [
            "interface {}".format(intf),
            "switchport mode trunk",
            rep_command,
            "rep fastmode",
            "shut",
            "no shut"
        ]
        if vlan:
            config_list.append("switchport trunk allowed vlan {}".format(vlan))
            config_list.append("vlan {}".format(vlan))
        try:
            device.configure(config_list)
        except SubCommandFailure as e:
            raise SubCommandFailure("Error configuring interface {}: {}".format(intf, e))

def unconfigure_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False):
    """Unconfigures REP segment
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to unconfigure
            segmentnum ('int'): Segment number to unconfigure
            vlan ('str' 'optional'): Vlan to unconfigure
            edge_port ('bool' 'optional'): unconfigure edge port
            no_neighbor ('bool' 'optional'): unconfigure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring REP segment {} on interfaces {}".format(segmentnum, intfs))

    if no_neighbor:
        rep_command = "no rep segment {} edge no-neighbor".format(segmentnum)
    elif edge_port:
        rep_command = "no rep segment {} edge".format(segmentnum)
    else:
        rep_command = "no rep segment {}".format(segmentnum)
    
    for intf in intfs:
        config_list = [
            "interface {}".format(intf),
            rep_command,
            "no rep fastmode",
            "no switchport mode trunk",
            "no shut",
            "shut"
        ]
        if vlan:
            config_list.append("no switchport trunk allowed vlan {}".format(vlan))
            config_list.append("no vlan {}".format(vlan))
        try:
            device.configure(config_list)
        except SubCommandFailure as e:
            raise SubCommandFailure("Error unconfiguring interface {}: {}".format(intf, e))

def unconfigure_fast_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False):
    """Unconfigures fastREP
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to unconfigure
            segmentnum ('int'): Segment number to unconfigure
            vlan ('str' 'optional'): Vlan to unconfigure
            edge_port ('bool' 'optional'): unconfigure edge port
            no_neighbor ('bool' 'optional'): unconfigure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring fastREP segment {} on interfaces {}".format(segmentnum, intfs))
    
    if no_neighbor:
        rep_command = "no rep segment {} edge no-neighbor".format(segmentnum)
    elif edge_port:
        rep_command = "no rep segment {} edge".format(segmentnum)
    else:
        rep_command = "no rep segment {}".format(segmentnum)
    
    for intf in intfs:
        config_list = [
            "interface {}".format(intf),
            rep_command,
            "no rep fastmode",
            "no switchport mode trunk",
            "no shut",
            "shut"
        ]
        if vlan:
            config_list.append("no switchport trunk allowed vlan {}".format(vlan))
            config_list.append("no vlan {}".format(vlan))
        try:
            device.configure(config_list)
        except SubCommandFailure as e:
            raise SubCommandFailure("Error unconfiguring interface {}: {}".format(intf, e))
  
def configure_rep_ztp(device):
    """ Configure REP ZTP on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("rep ztp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure REP ZTP on device {device.name}. Error: {e}"
        )

def unconfigure_rep_ztp(device):
    """ Unconfigure REP ZTP on the device
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    try:
        device.configure("no rep ztp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure REP ZTP on device {device.name}. Error: {e}"
        )
