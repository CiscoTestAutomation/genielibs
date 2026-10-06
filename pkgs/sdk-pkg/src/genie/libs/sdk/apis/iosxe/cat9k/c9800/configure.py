# Python
import logging
import re
from collections.abc import Mapping
from datetime import datetime

# pyats
from pyats.easypy import runtime
from pyats.utils.secret_strings import to_plaintext

# genie
from genie.libs.sdk.libs.abstracted_libs.iosxe.subsection import get_default_dir
from genie.libs.sdk.apis.iosxe.utils import recover_device_to_enable_state

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def _validate_wireless_management_mapping(value, name):
    """Validate the top-level shape used by management address fields."""
    if value is not None and not isinstance(value, Mapping):
        raise ValueError(f"{name} must be a mapping")


def _validate_wireless_management_routes(routes):
    """Validate route entries before any device configuration is applied."""
    _validate_wireless_management_mapping(routes, "routes")
    if routes is None:
        return

    for address_family in ("ipv4", "ipv6"):
        entries = routes.get(address_family, [])
        if not isinstance(entries, list):
            entries = [entries]
        for route in entries:
            if not isinstance(route, Mapping):
                raise ValueError(
                    f"routes.{address_family} entries must be mappings"
                )
            if not route.get("subnet") or not route.get("next_hop"):
                raise ValueError(
                    f"routes.{address_family} entries require subnet and "
                    "next_hop"
                )


def configure_wireless_management(
        device,
        interface=None,
        physical_interface=None,
        switchport=None,
        vlan=None,
        auto_negotiate=None,
        address=None,
        gateway=None,
        routes=None,
        ap_profile=None,
        credential_name=None):
    """Configure the wireless management interface on a C9800 controller.

    Explicit arguments take precedence over values in
    ``device.management.wireless``. The API configures the physical uplink,
    WMI Layer 3 interface, routes, wireless binding, and optional AP management
    user. WMI data is never read from ``device.interfaces``.

    Args:
        device (obj): Device object.
        interface (str): WMI Layer 3 interface, for example ``Vlan121``.
        physical_interface (str): Physical WMI uplink.
        switchport (str): Uplink mode: ``access``, ``trunk``, or ``no``.
        vlan (int): WMI VLAN ID for a switched uplink.
        auto_negotiate (bool): Configure negotiation auto on the uplink.
        address (dict): WMI address using the management address shape.
        gateway (dict): WMI gateway using the management gateway shape.
        routes (dict): WMI routes using the management routes shape.
        ap_profile (str): AP profile on which to configure ``mgmtuser``.
        credential_name (str): Device credential entry to use. Defaults to the
            AP profile name.

    Returns:
        None

    Example:
        >>> device.api.configure_wireless_management(
        ...     interface="Vlan121",
        ...     physical_interface="GigabitEthernet1",
        ...     switchport="trunk",
        ...     vlan=121,
        ...     auto_negotiate=True,
        ...     address={"ipv4": "192.0.2.10/24"},
        ...     routes={"ipv4": [{
        ...         "subnet": "198.51.100.0 255.255.255.0",
        ...         "next_hop": "192.0.2.1",
        ...     }]},
        ...     ap_profile="default-ap-profile",
        ... )
    """
    management = getattr(device, "management", {}) or {}
    wireless = management.get("wireless", {}) or {}

    def resolve(value, key):
        return wireless.get(key) if value is None else value

    interface = resolve(interface, "interface")
    physical_interface = resolve(physical_interface, "physical_interface")
    switchport = resolve(switchport, "switchport")
    vlan = resolve(vlan, "vlan")
    auto_negotiate = resolve(auto_negotiate, "auto_negotiate")
    address = resolve(address, "address")
    gateway = resolve(gateway, "gateway")
    routes = resolve(routes, "routes")
    ap_profile = resolve(ap_profile, "ap_profile")
    credential_name = resolve(credential_name, "credential_name")

    if not isinstance(interface, str) or not interface:
        raise ValueError("interface is required for wireless management")
    if physical_interface is not None and not isinstance(
            physical_interface, str):
        raise ValueError("physical_interface must be a string")

    valid_switchport_modes = {"access", "trunk", "no"}
    if switchport is not None and switchport not in valid_switchport_modes:
        raise ValueError(
            "switchport must be one of 'access', 'trunk', or 'no'"
        )

    if switchport in {"access", "trunk"}:
        if not physical_interface:
            raise ValueError(
                "physical_interface is required for a switched WMI uplink"
            )
        if vlan is None:
            raise ValueError("vlan is required for a switched WMI uplink")

    if vlan is not None:
        if isinstance(vlan, bool) or not isinstance(vlan, int):
            raise ValueError("vlan must be an integer")
        if not 1 <= vlan <= 4094:
            raise ValueError("vlan must be between 1 and 4094")

        svi_match = re.fullmatch(r"vlan\s*(\d+)", interface,
                                 flags=re.IGNORECASE)
        if svi_match and int(svi_match.group(1)) != vlan:
            raise ValueError(
                f"interface {interface} does not match VLAN {vlan}"
            )

    if auto_negotiate is not None and not isinstance(auto_negotiate, bool):
        raise ValueError("auto_negotiate must be a boolean")

    _validate_wireless_management_mapping(address, "address")
    _validate_wireless_management_mapping(gateway, "gateway")
    _validate_wireless_management_routes(routes)

    if credential_name and not ap_profile:
        raise ValueError("ap_profile is required when credential_name is used")

    username = password = None
    if ap_profile:
        selected_credential = credential_name or ap_profile
        credentials = getattr(device, "credentials", {}) or {}
        credential = credentials.get(selected_credential)
        if not credential:
            raise ValueError(
                f"device credential '{selected_credential}' was not found"
            )
        username = credential.get("username")
        password = credential.get("password")
        if not username or not password:
            raise ValueError(
                f"device credential '{selected_credential}' requires "
                "username and password"
            )
        password = to_plaintext(password)

    if switchport == "trunk":
        device.api.configure_interface_switchport_trunk(
            interfaces=[physical_interface], vlan_id=vlan, oper="add"
        )
        device.api.unshut_interface(interface=physical_interface)
    elif switchport == "access":
        device.api.configure_interface_switchport_access_vlan(
            interface=physical_interface, vlan=vlan, mode="access"
        )
        device.api.unshut_interface(interface=physical_interface)
    elif switchport == "no":
        routed_interface = physical_interface or interface
        device.configure([
            f"interface {routed_interface}",
            "no switchport",
            "no shutdown",
        ])

    negotiation_interface = physical_interface or interface
    if auto_negotiate:
        device.api.config_interface_negotiation(
            interface=negotiation_interface
        )

    if address is not None:
        # C9800 currently overrides this API with no_switchport=True. WMI SVIs
        # must disable that platform default and the generic management VRF
        # fallback so their addresses remain in the global routing table.
        device.api.configure_management_ip(
            interface=interface,
            address=address,
            no_switchport=False,
            fallback_to_management_vrf=False,
        )

    generic_gateway = management.get("gateway")
    generic_vrf = management.get("vrf")
    if gateway is not None:
        if (not generic_vrf and generic_gateway
                and generic_gateway != gateway):
            log.warning(
                "Skipping the wireless management gateway because it "
                "conflicts with the device management gateway in the global "
                "routing table; use wireless management routes for WMI "
                "reachability"
            )
        else:
            device.api.configure_management_gateway(gateway=gateway)

    if routes is not None:
        device.api.configure_management_routes(routes=routes)

    wireless_config = [f"wireless management interface {interface}"]
    if ap_profile:
        wireless_config.extend([
            "exit",
            f"ap profile {ap_profile}",
            f"mgmtuser username {username} password 0 {password} "
            f"secret 0 {password}",
        ])

    try:
        device.configure(wireless_config)
    except SubCommandFailure:
        # Do not include the rendered command list in the exception because it
        # may contain the AP management password.
        raise SubCommandFailure(
            f"Could not configure wireless management on {device.name}"
        ) from None


def configure_ignore_startup_config(device):
    """  To configure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to configure the device
    """

    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'confreg 0x2142'
            device.execute(cmd)
        else:
            cmd = 'config-register 0x2142'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure ignore startup config on {device.name}. Error:\n{e}")

def unconfigure_ignore_startup_config(device):
    """ To unconfigure ignore startup config.
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure : Failed to unconfigure the device
    """
    
    try:
        # If the device state is in rommon configure rommon variable
        if device.state_machine.current_state == 'rommon':
            cmd = 'confreg 0x2102'
            device.execute(cmd)
        else:
            cmd = 'config-register 0x2102'
            device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure ignore startup config on {device.name}. Error:\n{e}")


def collect_install_log(device, timeout=600, reconnect=False,
                         reconnect_timeout=None):
    """ Collect install failure logs from the device.
    Args:
        device (obj): Device object (required)
        timeout (int): timeout for show tech-support command (default: 600s)
        reconnect (bool): recover the connection and ensure enable mode
            before collecting logs (default: False)
        reconnect_timeout (int): timeout for the connection recovery.
            Defaults to `timeout` when not provided.
    Returns
        None
    """

    archive_filename = None

    if reconnect:
        recover_device_to_enable_state(
            device, timeout=reconnect_timeout or timeout)

    log.info("Logging the below to get the install failure logs from device")

    # Add timestamp to the show tech support filename
    timestamp = datetime.utcnow().strftime('%Y%m%dT%H%M%S%f')[:-3]
    file_name = f"show_tech_support_{timestamp}.txt"

    commands = [
        "show platform software install-manager chassis active r0 operation current detail",
        "show platform software install-manager chassis active r0 operation history detail",
    ]

    for command in commands:
        device.execute(command)

    show_tech_commands = [
        f"show tech-support install | append {file_name}"
    ]

    for command in show_tech_commands:
        device.execute(command, timeout=timeout)

    output = device.execute("request platform software trace archive", timeout=timeout)
    match = re.search(r'Done with creation of the archive file:\s*\[(.*?)\]', output)
    if match:
        archive_filename = match.group(1)

    try:
        # Get default directory to copy the files
        log.info("Getting default directory to copy the files")
        default_dir = get_default_dir(device)

        log.info(f"Copying file {file_name} to runinfo directory: {runtime.directory}")
        device.api.copy_from_device(local_path=f"{default_dir}{file_name}", remote_path=runtime.directory)
        if archive_filename:
            log.info(f"Copying archive file {archive_filename} to runinfo directory: {runtime.directory}")
            device.api.copy_from_device(local_path=f"{archive_filename}", remote_path=runtime.directory)

    except Exception as e:
        log.error(f"Failed to copy the install failure logs to runinfo directory: {e}", exc_info=True)
