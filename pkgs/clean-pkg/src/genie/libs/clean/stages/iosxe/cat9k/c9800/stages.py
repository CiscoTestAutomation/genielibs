"""IOSXE C9800 specific clean stages"""

# Python
import ipaddress
import logging

# Genie
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.metaparser.util.schemaengine import ListOf, Optional, Or
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def _get_wireless_management(device):
    """Return the wireless management testbed block, when present."""
    management = getattr(device, "management", {}) or {}
    return management.get("wireless", {}) or {}


def _resolve_wireless_management(device, values):
    """Resolve explicit stage values before wireless testbed defaults."""
    wireless = _get_wireless_management(device)
    return {
        key: wireless.get(key) if values.get(key) is None else values[key]
        for key in values
    }


def _vlan_in_list(vlan, vlan_list):
    """Return whether a VLAN is included in an IOS VLAN list or range."""
    if not vlan_list:
        return False

    for item in str(vlan_list).replace(" ", "").split(","):
        if item.lower() == "all":
            return True
        if item.isdigit() and int(item) == vlan:
            return True
        if "-" in item:
            start, end = item.split("-", 1)
            if start.isdigit() and end.isdigit():
                if int(start) <= vlan <= int(end):
                    return True
    return False


def _get_ip_interfaces(address, address_family):
    """Return the statically configured IP interfaces for an address family."""
    if not address:
        return []

    configured = address.get(address_family)
    if not isinstance(configured, list):
        configured = [configured] if configured else []

    dynamic_values = {f"{address_family}/dhcp"}
    if address_family == "ipv6":
        dynamic_values.add("ipv6/autoconfig")

    return [
        ipaddress.ip_interface(value)
        for value in configured
        if value not in dynamic_values
    ]


class ConfigureWirelessManagement(BaseStage):
    """Configure and verify the C9800 wireless management interface.

    Missing configuration arguments are read by the stage and API from
    ``device.management.wireless``. WMI data is not read from
    ``device.interfaces``.

    Stage Schema
    ------------
    configure_wireless_management:

        interface (str, optional): WMI Layer 3 interface.
        physical_interface (str, optional): Physical WMI uplink.
        switchport (str, optional): ``access``, ``trunk``, or ``no``.
        vlan (int, optional): WMI VLAN ID.
        auto_negotiate (bool, optional): Configure uplink autonegotiation.
        address (dict, optional): WMI IPv4 and/or IPv6 addresses.
        gateway (dict, optional): WMI IPv4 and/or IPv6 gateway.
        routes (dict, optional): WMI IPv4 and/or IPv6 static routes.
        ap_profile (str, optional): AP profile for ``mgmtuser``.
        credential_name (str, optional): Device credential entry for the AP
            profile. Defaults to ``ap_profile`` in the API.
        max_time (int, optional): Maximum verification time. Defaults to 60.
        check_interval (int, optional): Verification interval. Defaults to
            10.

    Example
    -------
    configure_wireless_management:
        interface: Vlan121
        physical_interface: GigabitEthernet1
        switchport: trunk
        vlan: 121
        auto_negotiate: true
        address:
            ipv4: 192.0.2.10/24
        routes:
            ipv4:
                - subnet: 198.51.100.0 255.255.255.0
                  next_hop: 192.0.2.1
        ap_profile: default-ap-profile
    """

    MAX_TIME = 60
    CHECK_INTERVAL = 10

    schema = {
        Optional("interface"): str,
        Optional("physical_interface"): str,
        Optional("switchport"): str,
        Optional("vlan"): int,
        Optional("auto_negotiate"): bool,
        Optional("address"): {
            Optional("ipv4"): Or(str, list),
            Optional("ipv6"): Or(str, list),
        },
        Optional("gateway"): {
            Optional("ipv4"): Or(str, list),
            Optional("ipv6"): Or(str, list),
        },
        Optional("routes"): {
            Optional("ipv4"): ListOf({
                "subnet": str,
                "next_hop": str,
            }),
            Optional("ipv6"): ListOf({
                "subnet": str,
                "next_hop": str,
            }),
        },
        Optional("ap_profile"): str,
        Optional("credential_name"): str,
        Optional("max_time"): int,
        Optional("check_interval"): int,
    }

    exec_order = [
        "configure_wireless_management",
        "verify_wireless_management",
    ]

    def configure_wireless_management(
            self, device, steps, interface=None, physical_interface=None,
            switchport=None, vlan=None, auto_negotiate=None, address=None,
            gateway=None, routes=None, ap_profile=None,
            credential_name=None):
        """Configure WMI through the C9800 SDK API."""
        values = _resolve_wireless_management(device, {
            "interface": interface,
            "physical_interface": physical_interface,
            "switchport": switchport,
            "vlan": vlan,
            "auto_negotiate": auto_negotiate,
            "address": address,
            "gateway": gateway,
            "routes": routes,
            "ap_profile": ap_profile,
            "credential_name": credential_name,
        })

        if not any(value is not None for value in values.values()):
            self.skipped(
                "Wireless management values are not provided in the Clean "
                "or testbed YAML. Skipping wireless management "
                "configuration."
            )

        with steps.start(
                f"Configure wireless management on {device.name}") as step:
            missing = []
            if not values["interface"]:
                missing.append("interface")
            if values["switchport"] in {"access", "trunk"}:
                if not values["physical_interface"]:
                    missing.append("physical_interface")
                if values["vlan"] is None:
                    missing.append("vlan")
            if values["credential_name"] and not values["ap_profile"]:
                missing.append("ap_profile")

            if missing:
                step.failed(
                    "Missing required wireless management values in the "
                    "Clean and testbed YAML "
                    f"(device.management.wireless): {', '.join(missing)}"
                )

            try:
                device.api.configure_wireless_management(
                    interface=values["interface"],
                    physical_interface=values["physical_interface"],
                    switchport=values["switchport"],
                    vlan=values["vlan"],
                    auto_negotiate=values["auto_negotiate"],
                    address=values["address"],
                    gateway=values["gateway"],
                    routes=values["routes"],
                    ap_profile=values["ap_profile"],
                    credential_name=values["credential_name"],
                )
            except (AttributeError, SubCommandFailure, ValueError) as error:
                step.failed(
                    f"Failed to configure wireless management on "
                    f"{device.name}",
                    from_exception=error,
                )

    def verify_wireless_management(
            self, device, steps, interface=None, physical_interface=None,
            switchport=None, vlan=None, address=None, max_time=MAX_TIME,
            check_interval=CHECK_INTERVAL):
        """Verify the WMI uplink, SVI, and wireless binding."""
        values = _resolve_wireless_management(device, {
            "interface": interface,
            "physical_interface": physical_interface,
            "switchport": switchport,
            "vlan": vlan,
            "address": address,
        })
        interface = values["interface"]
        physical_interface = values["physical_interface"]
        switchport = values["switchport"]
        vlan = values["vlan"]
        expected_ipv4_interfaces = _get_ip_interfaces(
            values["address"], "ipv4"
        )
        expected_primary_ipv4 = (
            expected_ipv4_interfaces[0]
            if expected_ipv4_interfaces else None
        )
        expected_ipv6 = _get_ip_interfaces(values["address"], "ipv6")

        if switchport == "trunk":
            with steps.start(
                    f"Verify WMI VLAN {vlan} is forwarding on "
                    f"{physical_interface}") as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    try:
                        output = device.parse(
                            f"show interfaces {physical_interface} trunk"
                        )
                        interfaces = output.get("interface", {})
                        trunk = next(
                            (data for name, data in interfaces.items()
                             if name.lower() == physical_interface.lower()),
                            None,
                        )
                        if trunk and trunk.get("status") == "trunking":
                            active = trunk.get(
                                "vlans_allowed_active_in_mgmt_domain"
                            )
                            forwarding = trunk.get(
                                "vlans_in_stp_forwarding_not_pruned"
                            )
                            if (_vlan_in_list(vlan, active)
                                    and _vlan_in_list(vlan, forwarding)):
                                break
                    except Exception:
                        log.debug(
                            "Unable to verify WMI trunk state",
                            exc_info=True,
                        )
                    timeout.sleep()
                else:
                    step.failed(
                        f"VLAN {vlan} is not active and forwarding on "
                        f"{physical_interface}"
                    )

        with steps.start(
                f"Verify WMI interface {interface} is up/up") as step:
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                try:
                    output = device.parse(f"show ip interface {interface}")
                    svi = next(
                        (data for name, data in output.items()
                         if name.lower() == interface.lower()),
                        None,
                    )
                    expected_ipv4_addresses = {
                        ipv4_interface
                        for ipv4_interface in expected_ipv4_interfaces
                    }
                    configured_ipv4_addresses = {
                        ipaddress.ip_interface(ipv4_address)
                        for ipv4_address in (
                            svi.get("ipv4", {}) if svi else {}
                        )
                    }
                    if (svi and svi.get("enabled") is True
                            and svi.get("oper_status") == "up"
                            and expected_ipv4_addresses.issubset(
                                configured_ipv4_addresses)):
                        break
                except Exception:
                    log.debug(
                        "Unable to verify WMI interface state",
                        exc_info=True,
                    )
                timeout.sleep()
            else:
                step.failed(
                    f"WMI interface {interface} is not up/up with the "
                    "expected IPv4 addresses"
                )

        if expected_ipv6:
            with steps.start(
                    f"Verify WMI interface {interface} IPv6 addresses") as step:
                timeout = Timeout(max_time, check_interval)
                expected_ipv6_addresses = {
                    ipv6_interface.ip for ipv6_interface in expected_ipv6
                }
                while timeout.iterate():
                    try:
                        output = device.parse("show ipv6 interface brief")
                        interfaces = output.get("interface", {})
                        svi = next(
                            (data for name, data in interfaces.items()
                             if name.lower() == interface.lower()),
                            None,
                        )
                        configured_ipv6_addresses = {
                            ipaddress.ip_interface(ipv6_address).ip
                            for ipv6_address in (
                                svi.get("ipv6_addresses", []) if svi else []
                            )
                        }
                        if (svi and svi.get("interface_state") == "up"
                                and svi.get("protocol_state") == "up"
                                and expected_ipv6_addresses.issubset(
                                    configured_ipv6_addresses)):
                            break
                    except Exception:
                        log.debug(
                            "Unable to verify WMI IPv6 interface state",
                            exc_info=True,
                        )
                    timeout.sleep()
                else:
                    step.failed(
                        f"WMI interface {interface} is not up/up with all "
                        "expected IPv6 addresses"
                    )

        with steps.start(
                f"Verify {interface} is the wireless management interface"
        ) as step:
            try:
                output = device.parse("show wireless interface summary")
            except Exception as error:
                step.failed(
                    "Unable to parse wireless management interface summary",
                    from_exception=error,
                )

            interfaces = output.get("interfaces", {})
            summary = next(
                (data for name, data in interfaces.items()
                 if name.lower() == interface.lower()),
                None,
            )
            type_matches = (
                summary
                and summary.get("interface_type", "").lower()
                == "management"
            )
            vlan_matches = (
                vlan is None
                or (summary and summary.get("vlan_id") == vlan)
            )
            address_matches = (
                expected_primary_ipv4 is None
                or (summary
                    and summary.get("ip_address")
                    == str(expected_primary_ipv4.ip)
                    and summary.get("ip_netmask")
                    == str(expected_primary_ipv4.netmask))
            )
            if not (type_matches and vlan_matches and address_matches):
                step.failed(
                    f"Wireless management summary does not show {interface} "
                    "as Management with the expected VLAN and address"
                )


class VerifyApAssociation(BaseStage):
    """ This stage verifies the given access point has configured.

    Stage Schema
    ------------
    verify_accesspoint_association:

        access_points(list):access_point to be verified if present

    Examples:
        verify_accesspoint_association:
            access_points:
                - "AP188B.4500.44C8"            
    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        'access_points': list,

    }
    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_accesspoint_association'
    ]

    def verify_accesspoint_association(self, device, steps, access_points, max_time=MAX_TIME,
                                       check_interval=CHECK_INTERVAL):
        for ap_name in access_points:
            with steps.start("Checking association for accesspoint {}".format(ap_name)) as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    # Fetch ap state from get_ap_state api
                    try:
                        ap_state = device.api.get_ap_state(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find access point state", from_exception=e)
                    # Fetch ap country from get_ap_country api
                    try:
                        ap_country = device.api.get_ap_country(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find country name", from_exception=e)

                    # Verify if the given accesspoint is configured
                    if ap_state.lower() == "registered" and ap_country != "":
                        step.passed('Access point {} has registered successfully with country as {}'. \
                                    format(ap_name, ap_country))
                    else:
                        log.warning('Access point {} has not yet registered'.format(ap_name))
                        timeout.sleep()
                else:
                    step.failed("Accesspoints failed to register to the controller")
