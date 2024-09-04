"""Common configure functions for prp/prp supervision frame vlan aware"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError


log = logging.getLogger(__name__)

def configure_prp_sup_vlan_aware(device, interface):
    """ Configures vlan aware on prp channel
    e.g.
    prp channel-group 1 supervisionFrameOption vlan-aware-enable

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring vlan aware on prp channel
    """
    configs = f"prp channel-group {interface} supervisionFrameOption vlan-aware-enable"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure supervision frame vlan aware mode on prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def unconfigure_prp_sup_vlan_aware(device, interface):
    """ Unconfigures vlan aware on prp channel
    e.g.
    no prp channel-group 1 supervisionFrameOption vlan-aware-enable

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed nconfiguring vlan aware on prp channel
    """
    configs = f"no prp channel-group {interface} supervisionFrameOption vlan-aware-enable"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure supervison frame vlan aware mode on prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def configure_prp_sup_vlan_aware_allowed_vlan_list(device, interface, vlan):
    """ Configures vlan aware allowed vlan list on prp channel
    e.g.
    prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan 30,40

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
            vlan (`str`): Vlan allowed list for prp channel supervision frames
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring vlan aware allowed vlan list on prp channel
    """
    configs = f"prp channel-group {interface} supervisionFrameOption vlan-aware-allowed-vlan {vlan}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure supervision frame vlan aware allowed vlan on prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )
def unconfigure_prp_sup_vlan_aware_allowed_vlan_list(device, interface):
    """ Unconfigures vlan aware allowed vlan list on prp channel
    e.g.
    no prp channel-group 1 supervisionFrameOption vlan-aware-allowed-vlan

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed unconfiguring vlan aware allowed vlan list on prp channel
    """
    configs = f"no prp channel-group {interface} supervisionFrameOption vlan-aware-allowed-vlan"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure supervision frame vlan aware allowed vlan on prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )
def configure_prp_static_vdan_entry(device, interface, mac):
    """ Configures static vdan entry
    e.g.
    prp channel-group 1 vdanMacaddress 00:00:01:00:00:11
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                mac (`str`): Mac address for prp channel supervision frames
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring static vdan entry for the prp channel
    """
    configs = f"prp channel-group {interface} vdanMacaddress {mac}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure static vdan entry for the prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def configure_prp_static_vdan_entry_with_vlan(device, interface, mac, vlan):
    """ Configures static vdan entry with VLAN
    e.g.
    prp channel-group 1 vdanMacaddress 00:00:01:00:00:11 vlan-id 10
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                mac (`str`): Mac address for prp channel supervision frames
                vlan (`int`): VLAN id for static vdan entry
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring static vdan entry with VLAN for the prp channel
    """
    configs = f"prp channel-group {interface} vdanMacaddress {mac} vlan-id {vlan}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure static vdan entry with VLAN for the prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def unconfigure_prp_static_vdan_entry(device, interface, mac):
    """ Unconfigures static vdan entry
    e.g.
    no prp channel-group 1 vdanMacaddress 00:00:01:00:00:11
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                mac (`str`): Mac address for prp channel supervision frames
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan aware allowed vlan list on prp channel
    """
    configs = f"no prp channel-group {interface} vdanMacaddress {mac}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure static vdan entry for the prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )
    
def configure_prp_sup_vlan_aware_reject_untagged(device, interface):
    """ Configures vlan aware reject untagged
    e.g.
    prp channel-group 1 supervisionFrameOption vlan-aware-reject-untagged
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan aware allowed vlan list on prp channel
    """
    configs = f"prp channel-group {interface} supervisionFrameOption vlan-aware-reject-untagged"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan aware reject untagged, Error: {error}'.format(
                error=e)
        )
def unconfigure_prp_sup_vlan_aware_reject_untagged(device, interface):
    """ Unconfigures vlan aware reject untagged
    e.g.
    no prp channel-group 1 supervisionFrameOption vlan-aware-reject-untagged
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan aware allowed vlan list on prp channel
    """
    configs = f"no prp channel-group {interface} supervisionFrameOption vlan-aware-reject-untagged"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure vlan aware reject untagged, Error: {error}'.format(
                error=e)
        )
    

def configure_prp_sup_vlan_id(device, interface, vlan):
    """ Configures vlan id for prp channel
    e.g.
    prp channel-group 1 supervisionFrameoption vlan-id 10
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                vlan (`str`): Vlan id for prp channel supervision frames
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan id for prp channel
    """
    configs = f"prp channel-group {interface} supervisionFrameoption vlan-id {vlan}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan id for prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def unconfigure_prp_sup_vlan_id(device, interface, vlan):
    """ Unconfigures vlan id for prp channel
    e.g.
    no prp channel-group 1 supervisionFrameoption vlan-id 10
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
                vlan (`str`): Vlan id for prp channel supervision frames
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan id for prp channel
    """
    configs = f"no prp channel-group {interface} supervisionFrameoption vlan-id {vlan}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure vlan id for prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def configure_prp_sup_vlan_tagged(device, interface):
    """ Configures vlan tagged for prp channel
    e.g.
    prp channel-group 1 supervisionFrameOption vlan-tagged
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan tagged for prp channel
    """
    configs = f"prp channel-group {interface} supervisionFrameOption vlan-tagged"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure vlan tagged for prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )

def unconfigure_prp_sup_vlan_tagged(device, interface):
    """ Unconfigures vlan tagged for prp channel
    e.g.
    no prp channel-group 1 supervisionFrameOption vlan-tagged
    
            Args:
                device (`obj`): Device object
                interface (`str`): Interface name
            Return:
                None
            Raise:
                SubCommandFailure: Failed configuring vlan tagged for prp channel
    """
    configs = f"no prp channel-group {interface} supervisionFrameOption vlan-tagged"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure vlan tagged for prp channel {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )
    
