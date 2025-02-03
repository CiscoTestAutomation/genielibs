'''IOSXE configure functions for iiot rep feature'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False, edge_primary=False, edge_pref=False):
    """Configures REP segment
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to configure
            segmentnum ('str'): Segment number to configure
            vlan ('str', 'optional'): Vlan to configure
            edge_port ('bool' 'optional'): Configure edge port
            edge_primary('bool' 'optional'): Configure edge primary
            edge_pref ('bool' 'optional'): Configure edge primary preferred
            no_neighbor ('bool' 'optional'): Configure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring REP segment {} on interfaces {}".format(segmentnum, intfs))

    rep_command = "rep segment {}".format(segmentnum)
    if no_neighbor:
        rep_command += " edge no-neighbor"
    elif edge_port:
        rep_command += " edge"
    elif edge_primary and edge_pref:
        rep_command += " primary preferred"
    elif edge_primary:
        rep_command += " primary"
    
    for intf in intfs:
        config_list = [
            "interface {}".format(intf),
            "switchport mode trunk",
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

def configure_fast_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False, edge_primary=False, edge_pref=False):
    """Configures fastREP 
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to configure
            segmentnum ('str'): Segment number to configure
            vlan ('str', 'optional'): Vlan to configure
            edge_port ('bool' 'optional'): Configure edge port
            edge_primary ('bool' 'optional'): Configure edge primary
            edge_pref ('bool' 'optional'): Configure edge primary preferred
            no_neighbor ('bool' 'optional'): Configure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.info("Configuring fastREP segment {} on interfaces {}".format(segmentnum, intfs))

    rep_command = "rep segment {}".format(segmentnum)
    if no_neighbor:
        rep_command += " edge no-neighbor"
    elif edge_port:
        rep_command += " edge"
    elif edge_primary and edge_pref:
        rep_command += " primary preferred"
    elif edge_primary:
        rep_command += " primary"
    
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

def unconfigure_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False, edge_primary=False, edge_pref=False):
    """Unconfigures REP segment
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to unconfigure
            segmentnum ('int'): Segment number to unconfigure
            vlan ('str' 'optional'): Vlan to unconfigure
            edge_port ('bool' 'optional'): unconfigure edge port
            edge_primary ('bool' 'optional'): unconfigure edge primary
            edge_pref ('bool' 'optional'): unconfigure edge primary preferred
            no_neighbor ('bool' 'optional'): unconfigure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring REP segment {} on interfaces {}".format(segmentnum, intfs))

    rep_command = "no rep segment {}".format(segmentnum)
    if no_neighbor:
        rep_command += " edge no-neighbor"
    elif edge_port:
        rep_command += " edge"
    elif edge_primary and edge_pref:
        rep_command += " primary preferred"
    elif edge_primary:
        rep_command += " primary"
    
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

def unconfigure_fast_rep_segment(device, intfs, segmentnum, vlan=None, edge_port=False, no_neighbor=False, edge_primary=False, edge_pref=False):
    """Unconfigures fastREP
        Args:
            device ('obj'): Switch object
            intfs ('list'): List of interfaces to unconfigure
            segmentnum ('int'): Segment number to unconfigure
            vlan ('str' 'optional'): Vlan to unconfigure
            edge_port ('bool' 'optional'): unconfigure edge port
            edge_primary('bool' 'optional'): unconfigure edge primary
            edge_pref ('bool' 'optional'): unconfigure edge primary preferred
            no_neighbor ('bool' 'optional'): unconfigure no neighbor
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring fastREP segment {} on interfaces {}".format(segmentnum, intfs))
    
    rep_command = "no rep segment {}".format(segmentnum)
    if no_neighbor:
        rep_command += " edge no-neighbor"
    elif edge_port:
        rep_command += " edge"
    elif edge_primary and edge_pref:
        rep_command += " primary preferred"
    elif edge_primary:
        rep_command += " primary"
    
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
        
def configure_interface_rep_ztp(device, intfs, segment, vlan=None):
    """ Configure REP ZTP on the interface
        Args:
            device ('obj'): Device object
            interface ('list'): Interface list
            segment ('str'): Segment value
            vlan ('str' 'optional'): Vlan to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring rep ztp on interface")

    for intf in intfs:
        config = [
            f"interface {intf}",
            f"switchport mode trunk",
            f"rep segment {segment}",
            "rep ztp-enable",
        ]
        if vlan:
            config.append(f"vlan {vlan}")
            config.append(f"switchport trunk allowed vlan {vlan}")
        try:
            device.configure(config)
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Could not configure rep ztp on {intf}. Error:\n{e}")

def unconfigure_interface_rep_ztp(device, intfs, segment, vlan=None):
    """ Unconfigure REP ZTP on the interface
        Args:
            device ('obj'): Device object
            intfs ('str'): Interface list
            segment ('str'): Segment value
            vlan ('str', optional): vlan to unconfigure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring rep ztp on interface")
    
    for intf in intfs:
        config = [
            f'interface {intf}',
            f'no rep segment {segment}',
            "no rep ztp-enable",
            f"no switchport mode trunk",
        ]
        if vlan:
            config.append(f"no switchport trunk allowed vlan {vlan}")
            config.append(f"no vlan {vlan}")
        try:
            device.configure(config)
        except SubCommandFailure as e:
            raise SubCommandFailure(f"Could not unconfigure rep ztp on {intf}. Error:\n{e}")