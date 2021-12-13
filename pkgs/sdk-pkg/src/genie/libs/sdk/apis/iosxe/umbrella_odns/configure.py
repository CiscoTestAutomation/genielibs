"""Common configure functions for umbrella odns"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_umbrella_in_out(
    device, 
    in_interface=None,
    in_tag=None, 
    out_interface=None,
):
    """ Enable Umbrella IN and OUT over interface 
        Args:
            device ('obj'):uut device to use
            in_interface ('str'): enable Umbrella in over this interface, default value is None
            in_tag ('str'): configure device tag with umbrella in, default value is None
            out_interface ('str'): enable Umbrella out over this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: Umbrella IN OUT not enable over interface
    """
    cmd = []
    if in_interface:
        cmd.append("interface {}".format(in_interface))
        cmd.append("umbrella in {}".format(in_tag))
    if out_interface:
        cmd.append("interface {}".format(out_interface))
        cmd.append("umbrella out")
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Enable Umbrella. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_umbrella_in_out(
    device, 
    in_interface=None,
    in_tag=None, 
    out_interface=None,
):
    """ Unconfigure Umbrella IN and OUT over interface 
        Args:
            device ('obj'):uut [device to use]
            in_interface ('str'): Disable Umbrella in over this interface, default value is None
            in_tag ('str'): configure device tag with umbrella in, default value is None
            out_interface ('str'): Disable Umbrella out over this interface, default value is None
        Returns:
            console output
        Raises:
            SubCommandFailure: Umbrella IN OUT not Disable  over interface
    """
    cmd = []
    if in_interface:
        cmd.append("interface {}".format(in_interface))
        cmd.append("no umbrella in {}".format(in_tag))
    if out_interface:
        cmd.append("interface {}".format(out_interface))
        cmd.append("no umbrella out")

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Disaable Umbrella. Error:\n{error}".format(error=e)
        )
    return out

def configure_umbrella_global_parameter_map(
    device, 
    token_key=None,
    api_key=None, 
    secret_key=None,
    org_id=None,
    local_bypass_name=None,
    dnscrypt=None,
    udp_timeout=30,
):
    """ Enable Umbrella  parameter-map Globally
        Args:
            device ('obj'): device to use
            token_key ('str'): Configure Token key for device registration, default value is None
            api_key ('str'): Configure Token key for device registration, , default value is None
            secret_key ('str'): Configure secret key with api key for device registration, default value is None, Example: 34cc188ffba47b5ab18290a62ae5e0m
            org_id ('str'): Configure org id with api key for device registration, default value is None, Example: 2549304
            local_bypass_name ('str'): Configure local domain bypass for non umbrella lookup, default value is None
            dnscrypt ('str'): This is to disable/enable DNSCrypt, default value is None
            udp_timeout('int'): This is for device registration reattempt, value range 1-30sec, default value is 30. 
        Returns:
            console output
        Raises:
            SubCommandFailure: Umbrella parameter-map configuration
    """
    cmd = ["parameter-map type umbrella global"]
    cmd.append("udp-timeout {}".format(udp_timeout))
    if dnscrypt == None:
        cmd.append("no dnscrypt")
    else:
        cmd.append("dnscrypt")

    if token_key:
        cmd.append("token {}".format(token_key))
    if api_key:
        cmd.append("api-key {}".format(api_key))
        cmd.append("orgid {}".format(org_id))
        cmd.append("secret 0 {}".format(secret_key))
    if local_bypass_name:
        cmd.append("local-domain {}".format(local_bypass_name))        

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Cofnigure Umbrella parameter-map. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_umbrella_global_parameter_map(
    device, 
):
    """ Disable Umbrella  parameter-map Globally
        Args:
            device ('obj'): device to use
        Returns:
            console output
        Raises:
            SubCommandFailure: Umbrella parameter-map un-configuration
    """
    cmd = ["no parameter-map type umbrella global"]       
    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Cofnigure Umbrella parameter-map. Error:\n{error}".format(error=e)
        )
    return out

def configure_umbrella_local_bypass(
    device, 
    local_bypass_name,
    domain,
):
    """ Cofigure local domain bypass regex
        Args:
            device ('obj'): device to use
            local_bypass_name ('str'): Name of local domain bypass
            domain ('str'): Regex pattern.
        Returns:
            console output
        Raises:
            SubCommandFailure: Local domain bypass 
    """
    cmd = []
    cmd.append("parameter-map type regex {}".format(local_bypass_name))
    cmd.append("pattern .*{}.*".format(domain))

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local domain. Error:\n{error}".format(error=e)
        )
    return out

def unconfigure_umbrella_local_bypass(
    device, 
    local_bypass_name,
):
    """ Un-Cofigure local domain bypass regex
        Args:
            device ('obj'): device to use
            local_bypass_name ('str'): Name of local domain bypass
        Returns:
            console output
        Raises:
            SubCommandFailure: unconifgure Local domain bypass 
    """
    cmd = ["no parameter-map type regex {}".format(local_bypass_name)]

    try:
        out = device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not Un-configure local domain. Error:\n{error}".format(error=e)
        )
    return out


