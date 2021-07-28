"""Common configure functions for mpls"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)


def config_mpls_ldp_on_interface(device, interface):
    """ Config ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring ldp on {interface} on {device}".format(interface=interface, device=device.name))

    try:
        device.configure(["interface {interface}".format(interface=interface), "mpls ip"])
    except SubCommandFailure:
        raise SubCommandFailure(
            'Could not activate "mpls ip" on interface {interface}'.format(
                interface=interface
            )
        )

def config_mpls_ldp_on_device(device):
    """ Config ldp on Device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring ldp on {device}".format(device=device.name))

    try:
        device.configure("mpls ip")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ip" on {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )

def remove_mpls_ldp_from_device(device):
    """ Remove ldp from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring device
    """
    try:
        log.info('Removing mpls ldp from device {device}'.format(
            device=device.name))
        device.configure("no mpls ip")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ip" from {device}, Error: {error}'.format(
                device=device.name, error=e
            )
        )


def remove_mpls_ldp_from_interface(device, interface):
    """ Remove ldp on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing ldp on {interface} on {device}".format(
        interface=interface, device=device.name))

    try:
        device.configure(["interface {interface}".format(interface=interface), "no mpls ip"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ip" from interface {interface}, '
            'Error: {error}'.format(interface=interface, error=e
            )
        )

def config_mpls_lable_protocol(device, interface=None):
    """ Config mpls lable protocol on interface or device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface to be configured
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    try:
        if interface is not None:
            log.info(
                    'Configuring mpls label protocol ldp on '
                    'interface {interface}'.format(interface=interface))
            device.configure(["interface {interface}".format(
                interface=interface), "mpls label protocol ldp"])
        else:
            log.info('Configuring mpls label protocol ldp on '
                    'device {device}'.format(device=device.name))
            device.configure("mpls label protocol ldp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls label protocol ldp", '
            'Error: {error}'.format(error=e)
        )


def remove_mpls_lable_protocol_from_device(device):
    """ Remove mpls label protocol from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls label protocol ldp "
            "from device {device}".format(device=device.name))

    try:
        device.configure("no mpls label protocol ldp")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls label protocol ldp" from device {device}, '
            'Error: {error}'.format(device=device.name, error=e)
        )


def config_mpls_ldp_router_id_on_device(device, interface, force=None):
    """ Config mpls ldp router id on device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """

    log.info("Configuring mpls ldp router id on interface {intf} "
            "on device {device}".format(intf=interface, device=device.name))

    config = "mpls ldp router-id {intf}".format(intf=interface)
    if force:
        config += " force"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ldp router-id" on interface {intf} '
            'on device {device}, Error: {error}'.format(
                intf=interface, device=device.name, error=e)
        )


def remove_mpls_ldp_router_id_from_device(device, interface):
    """ Remove mpls ldp router id from device

        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls ldp router id from device {device}".format(
            device=device.name))

    try:
        device.configure("no mpls ldp router-id {intf}".format(
            intf=interface))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ldp router-id" from interface {intf} '
            'on device {device}, Error: {error}'.format(
                device=device.name, intf=interface, error=e)
        )


def config_mpls_ldp_explicit_on_device(device):
    """ Config mpls ldp explicit on device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring mpls ldp explicit on device {device}".format(
            device=device.name))

    try:
        device.configure("mpls ldp explicit-null")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "mpls ldp explicit-null" '
            'on device {device}, Error: {error}'.format(
                device=device.name, error=e)
        )


def remove_mpls_ldp_explicit_from_device(device):
    """ Remove mpls ldp explicit from device

        Args:
            device (`obj`): Device object
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Removing mpls ldp explicit from device {device}".format(
            device=device.name))

    try:
        device.configure("no mpls ldp explicit-null")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not remove "mpls ldp explicit-null" '
            'from device {device}, Error: {error}'.format(
                device=device.name, error=e)
        )


def config_speed_nonego_on_interface(device, interface):
    """ Configure speed nonego on interface

        Args:
            device (`obj`): Device object
            interface ('str'): Interface to be configured
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring interface
    """
    log.info("Configuring speed nonego on interface {interface}".format(
            interface=interface))

    try:
        device.configure(["interface {interface}".format(
            interface=interface), "speed nonego"])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not activate "speed nonego" on '
            'interface {interface}, Error: {error}'.format(
                interface=interface, error=e)
        )


def config_encapsulation_on_interface(device, vlan, interface):
    """ Configure encapsulation on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            vlan  (`str`): Vlan to be configured with encapsulation

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "encapsulation dot1Q {vlan}".format(vlan=vlan),
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure encapsulation on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e)
        )


def config_xconnect_on_interface(device, interface, neighbor, vcid):
    """ Configure xconnect neighbor on Interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            neighbor (`str`): Neighbor to be configured on xconnect
            vcid (`str`): Vcid to be configured through xconnect


        Returns:
            None

        Raises:
            SubCommandFailure
    """
    try:
        device.configure(
            [
                "interface {interface}".format(interface=interface),
                "xconnect {neighbor} {vcid} encapsulation mpls".format(
                    neighbor=neighbor, vcid=vcid)
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure xconnect neighbor on interface {interface}. "
            "Error:\n{error}".format(interface=interface, error=e)
        )

def configure_service_internal(device):
    """ Configures service internal on device"""

    try:
        device.configure("service internal")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure service internal on device. "
            "Error:\n{error}".format(error=e)
        )

def configure_mpls_ldp_nsr(device):
    """ Configures mpls ldp nsr on device
        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("mpls ldp nsr")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls ldp nsr on device. "
            "Error:\n{error}".format(error=e)
        )

def unconfigure_mpls_ldp_nsr(device):
    """ Unconfigures mpls ldp nsr on device
        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("no mpls ldp nsr")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure mpls ldp nsr on device. "
            "Error:\n{error}".format(error=e)
        )


def configure_mpls_ldp_graceful_restart(device):
    """ Configures mpls ldp graceful restart on device

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("mpls ldp graceful-restart")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls ldp graceful restart on device. "
            "Error:\n{error}".format(error=e)
        )

def unconfigure_mpls_ldp_graceful_restart(device):
    """ Unconfigures mpls ldp graceful restart on device

        Args:
            device (`obj`): Device object

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure("no mpls ldp graceful-restart")
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure mpls ldp graceful restart on device. "
            "Error:\n{error}".format(error=e)
        )


def configure_pseudowire_encapsulation_mpls(device, pseudowire_class):
    """ Configures pseudowire encapsulation mpls

        Args:
            device (`obj`): Device object
            pseudowire_class (`str`): Pseudowire class be applied

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
       device.configure(
            [
                "pseudowire-class {pw_class}".format(pw_class=pseudowire_class),
                "encapsulation mpls",
                "interworking vlan"
            ]
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure pseudowire encapsulation mpls on device. "
            "Error:\n{error}".format(error=e)
        )

def unconfigure_pseudowire_encapsulation_mpls(device, pseudowire_class):
    """ Unconfigures pseudowire encapsulation mpls

        Args:
            device (`obj`): Device object
            pseudowire_class (`str`): Pseudowire class be applied

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
       device.configure(
           "no pseudowire-class {pw_class}".format(
               pw_class=pseudowire_class)
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't unconfigure pseudowire encapsulation mpls on device. "
            "Error:\n{error}".format(error=e)
        )


def configure_mpls_pseudowire_xconnect_on_interface(device, interface, ip, vlan, pw_class):
    """ Configures mpls xconnect pseudowire class on interface

        Args:
            device (`obj`): Device object
            interface (`str`): Interface on which the edge trunk config to be applied
            ip (`str`): IP address to be configured with xconnect
            vlan (`str`): Vlan id to be configured
            pw_class (`str`): Pseudowire class be applied

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            [
                "interface {intf}".format(intf=interface),
                "xconnect {ip} {vlan} encapsulation mpls pw-class "
                "{pw_class}".format(ip=ip, vlan=vlan,pw_class=pw_class)
            ]
        )

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Couldn't configure mpls xconnect pseudowire class on "
            "interface {intf} on device. "
            "Error:\n{error}".format(intf=interface, error=e)
        )

