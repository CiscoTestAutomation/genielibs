"""Common configure functions for ISIS"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_isis_net_address(device, process_id, net_address):
    """ Configure ISIS network address

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            net_address ('str'): Net Address
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " net {net_address}\n"
            " !\n".format(
                process_id=process_id,
                net_address=net_address,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ISIS on {device}".format(
                device=device.name,
            )
        )

def configure_isis_metric_style(device, process_id,
    address_family, metric_style):
    """ Configure ISIS metric style

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            address_family ('str'): Address family to be configured
            metric_style ('str'): Metric style
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " address-family {address_family}\n"
            "  metric-style {metric_style}\n"
            " !\n".format(
                process_id=process_id,
                address_family=address_family,
                metric_style=metric_style,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ISIS on {device}".format(
                device=device.name,
            )
        )

def configure_isis_prefix_sid(device, process_id, interface, 
    prefix_sid, address_family):
    """ Configure ISIS prefix-sid

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface ('str'): Interface to configure
            prefix_sid ('str'): Prefix-Sid
            address_family ('str'): Address family to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  address-family {address_family}\n"
            "   prefix-sid absolute {prefix_sid}\n"
            "  !\n"
            " !\n".format(
                process_id=process_id,
                interface=interface,
                prefix_sid=prefix_sid,
                address_family=address_family,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ISIS on {device}".format(
                device=device.name,
            )
        )

def configure_isis_metric(device, process_id, interface, metric, address_family):
    """ Configure ISIS metric

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface ('str'): Interface to configure
            metric ('str'): Metric value
            address_family ('str'): Address family to be configured
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  address-family {address_family}\n"
            "   metric {metric}\n"
            "  !\n"
            " !\n".format(
                process_id=process_id,
                interface=interface,
                metric=metric,
                address_family=address_family,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure ISIS on {device}".format(
                device=device.name,
            )
        )

def configure_isis_md5_authentication(device, process_id, interface, hello_password):
    """ Configure MD5 authentication

        Args:
            device ('obj'): Device object
            process_id ('str'): Router ISIS process ID
            interface ('str'): Interface to configure
            hello_password ('str'): Authentication password
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(
            "router isis {process_id}\n"
            " interface {interface}\n"
            "  hello-password hmac-md5 {hello_password}\n"
            " !\n"
            "!\n".format(
                process_id=process_id,
                interface=interface,
                hello_password=hello_password,
            )
        )
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure MD5 authentication under interface {interface}".format(
                interface=interface,
            )
        )
