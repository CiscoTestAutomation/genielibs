"""Common configure functions for sisf"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_ipv6_dhcp_guard_policy(device, policy_name, device_role=None, trusted_port=False):
    """ Configures ipv6 dhcp guard policy {policy_name}
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be configured
            device_role ('str'): role of the  device
            trusted_port ('bool'): True indicating the port is a trusted port
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 dhcp guard policy {policy_name}
    """
    log.info(
        "Configuring ipv6 dhcp guard policy {policy_name}, device role {device_role} and trusted port {trusted_port}"
        .format(
            policy_name=policy_name,
            device_role=device_role,
            trusted_port=trusted_port
            )
    )

    try:
        if device_role and trusted_port:
             device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "device-role {device_role}".format(device_role=device_role),
             "trusted-port"
             ])

        elif trusted_port:
         device.configure(
             ["ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
              "trusted-port"
             ]
           )

        elif not trusted_port:
            device.configure(
                [
                "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
                "no trusted-port"
                ]
            )
        elif device_role:
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "device-role {device_role}".format(device_role=device_role)
             ])
        else:
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "no trusted-port",
             "device-role {device_role}".format(device_role=device_role)
             ]
           )

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure ipv6 dhcp guard policy {policy_name}"
            .format(policy_name=policy_name)
        )


def unconfigure_ipv6_dhcp_guard_policy(device, policy_name, device_role=False, trusted_port=False):
    """ Unconfigures ipv6 dhcp guard policy {policy_name}
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be unconfigured
            device_role ('bool'): True indicating set device role to its default value
            trusted_port ('bool'): True indicating set trusted_port to its default value
        Returns:
            None
        Raises:
            SubCommandFailure: "Failed to unconfigure ipv6 dhcp guard policy {policy_name} with
            unconfigure device role {device_role} and unconfigure trusted port {trusted_port}"
    """
    log.info(
        """Unconfiguring ipv6 dhcp guard policy {policy_name},
           unconfigure device role {device_role} and unconfigure trusted port {trusted_port}"""
        .format(
            policy_name=policy_name,
            device_role=device_role,
            trusted_port=trusted_port
        )
    )

    try:
        if device_role and trusted_port:
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "no device-role",
             "no trusted-port"
             ])

        elif trusted_port:
         device.configure(
             ["ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
              "no trusted-port"
             ]
           )

        elif device_role:
          device.configure(
             [
             "ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
             "no device-role"
             ])


    except SubCommandFailure:
        raise SubCommandFailure(
            """Failed to unconfigure ipv6 dhcp guard policy {policy_name} with
               unconfigure device role {device_role} and unconfigure trusted port {trusted_port}"""
            .format(
                policy_name=policy_name,
                device_role=device_role,
                trusted_port=trusted_port
            )
        )


def remove_ipv6_dhcp_guard_policy(device, policy_name):
    """ Remove IPv6 DHCP Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 DHCP guard policy
    """
    log.debug(
        "Removing IPv6 DHCP Guard Policy with name={policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        device.configure([
            "no ipv6 dhcp guard policy {policy_name}".format(policy_name=policy_name),
        ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 DHCP Guard Policy {policy_name}".format(
                policy_name=policy_name
            )
        )


def configure_ipv6_nd_suppress_policy(device, policy_name, mode):
    """ Configure ipv6 nd suppress policy {mode}
    Args:
        device ('obj'): device to use
        policy_name ('str'): name of the policy to be configured
        mode ('str'): mode for policy (dad-proxy, full-proxy, mc-proxy)
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure ipv6 nd suppress policy {policy_name} with mode {mode}
    """
    log.info(
        "Configuring ipv6 nd suppress policy name={policy_name} with mode {mode}"
        .format(
            policy_name=policy_name,
            mode=mode
            )
        )

    try:
        device.configure([
            "ipv6 nd suppress policy {policy_name}".format(policy_name=policy_name),
            "mode {mode}".format(mode=mode)
        ])

    except:
        raise SubCommandFailure(
        "Failed to configure ipv6 nd suppress policy {policy_name} with mode {mode}"
           .format(
            policy_name=policy_name,
            mode=mode
            )
        )


def unconfigure_ipv6_nd_suppress_policy(device, policy_name, mode):
    """ Unconfigures ipv6 nd suppress policy {mode}
    Args:
        device ('obj'): device to use
        policy_name ('str'): name of the policy to be uconfigured
        mode ('bool'): True indicating set mode to its default value
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure ipv6 nd suppress policy {policy_name} with mode {mode}
    """
    log.info(
        "Unconfiguring ipv6 nd suppress policy {policy_name} with unconfigure mode {mode}"
        .format(
            policy_name=policy_name,
            mode=mode
            )
        )

    try:
        if mode:
            device.configure([
                "ipv6 nd suppress policy {policy_name}".format(policy_name=policy_name),
                "no mode"
            ])
    except:
        raise SubCommandFailure(
        "Failed to unconfigure ipv6 nd suppress policy {policy_name} with unconfigure mode {mode}"
           .format(
            policy_name=policy_name,
            mode=mode
            )
        )


def remove_ipv6_nd_suppress_policy(device, policy_name):
    """ Remove IPv6 ND Suppress Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 ND suppress policy
    """
    log.debug(
        "Removing IPv6 IPv6 ND suppress policy with name={policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        device.configure([
            "no ipv6 nd suppress policy {policy_name}".format(policy_name=policy_name),
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 ND suppress policy {policy_name}".format(
                policy_name=policy_name
            )
        )


def configure_device_tracking_upgrade_cli(device, force=False, revert=False):
    """ Configures device-tracking upgrade-cli {option}
    Args:
        device ('obj'): device to use
        force ('bool'): option to force the upgrade
        revert: ('bool'): option to revert the upgrade
    Returns:
        None
    Raises:
        SubCommandFailure: "Failed to configure device-tracking upgrade-cli with
        force {force} and revert {revert}"
    """
    log.info(
        "Configuring device-tracking upgrade-cli with force {force} and revert {revert}"
        .format(
            force=force,
            revert=revert
            )
        )

    try:
        if force and not revert:
            device.configure([
                "device-tracking upgrade-cli force",
            ])
        elif revert and not force:
            device.configure([
                "device-tracking upgrade-cli revert",
            ])
        else:
            raise SubCommandFailure(
                """Failed to configure device-tracking upgrade-cli with force {force} and revert {revert}.
                   force and revert cannot have the same value"""
                .format(
                    force=force,
                    revert=revert
                    )
                )
    except:
        raise SubCommandFailure(
            "Failed to configure device-tracking upgrade-cli with force {force} and revert {revert}"
            .format(
                force=force,
                revert=revert
                )
            )


def configure_ip_dhcp_snooping(device, vlan_range=None):
    """ Configures ip dhcp snooping vlan {vlan_range}
    Args:
        device ('obj'): device to use
        vlan_range ('str'): vlan range from (1-4096), example: 1,3-5,7,9-11
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure ip dhcp snooping vlan {vlan_range}
    """
    log.info(
        "Configuring ip dhcp snooping vlan {vlan_range}"
        .format(vlan_range=vlan_range)
        )

    try:
        device.configure(["ip dhcp snooping vlan {vlan_range}".format(vlan_range=vlan_range)])

    except:
        raise SubCommandFailure("Failed to configure ip dhcp snooping vlan {vlan_range}"
                                .format(vlan_range=vlan_range))


def unconfigure_ip_dhcp_snooping(device, vlan_range):
    """ Unconfigures ip dhcp snooping vlan {vlan_range}
    Args:
        device ('obj'): device to use
        vlan_range ('str'): vlan range from (1-4096), example: 1,3-5,7,9-11
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure ip dhcp snooping vlan {vlan_range}
    """
    log.info(
        "Configuring ip dhcp snooping vlan {vlan_range}"
        .format(vlan_range=vlan_range)
        )

    try:
        device.configure(["no ip dhcp snooping vlan {vlan_range}".format(vlan_range=vlan_range)])

    except:
        raise SubCommandFailure("Failed to unconfigure ip dhcp snooping vlan {vlan_range}"
                                .format(vlan_range=vlan_range))


def attach_ipv6_dhcp_guard_policy(device, policy_name, vlan=None, interface=None):
    """ Attaches the given ipv6 dhcp guard policy to an interface or vlan(s)
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be attached
            interface (str): interface to attach policy to
            vlan (str): vlan or vlan range to attach the policy to. e.g: 1-10,15
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to attach ipv6 dhcp guard policy {policy_name}
    """
    log.info(
        "Attaching ipv6 dhcp guard policy {policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        if interface:
            device.configure([
                "interface {interface}".format(interface = interface),
                "ipv6 dhcp guard attach-policy {policy_name}".format(policy_name = policy_name)
            ])
        else:
            device.configure([
                "vlan configuration {vlan}".format(vlan = vlan),
                "ipv6 dhcp guard attach-policy {policy_name}".format(policy_name = policy_name)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to attach ipv6 dhcp guard policy {policy_name}"
            .format(policy_name=policy_name)
        )


def detach_ipv6_dhcp_guard_policy(device, policy_name, vlan=None, interface=None):
    """ Detaches the given ipv6 dhcp guard policy from an interface or vlan(s)
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be detached
            interface (str): interface to detach policy from
            vlan (str): vlan or vlan range to detach the policy from e.g: 1-10,15
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to detach ipv6 dhcp guard policy {policy_name}
    """
    log.info(
        "Detaching ipv6 dhcp guard policy {policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        if interface:
            device.configure([
                "interface {interface}".format(interface = interface),
                "no ipv6 dhcp guard attach-policy {policy_name}".format(policy_name = policy_name)
            ])
        else:
            device.configure([
                "vlan configuration {vlan}".format(vlan = vlan),
                "no ipv6 dhcp guard attach-policy {policy_name}".format(policy_name = policy_name)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to deatach ipv6 dhcp guard policy {policy_name}"
            .format(policy_name=policy_name)
        )


def attach_ipv6_nd_suppress_policy(device, policy_name, vlan=None, interface=None):
    """ Attaches the given ipv6 nd suppress policy to an interface or vlan(s)
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be attached
            interface (str): interface to attach policy to
            vlan (str): vlan or vlan range to attach the policy to. e.g: 1-10,15
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to attach ipv6 nd suppress policy {policy_name}
    """
    log.info(
        "Attaching ipv6 nd suppress policy {policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        if interface:
            device.configure([
                "interface {interface}".format(interface = interface),
                "ipv6 nd suppress attach-policy {policy_name}".format(policy_name = policy_name)
            ])
        else:
            device.configure([
                "vlan configuration {vlan}".format(vlan = vlan),
                "ipv6 nd suppress attach-policy {policy_name}".format(policy_name = policy_name)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to attach ipv6 nd suppress policy {policy_name}"
            .format(policy_name=policy_name)
        )


def detach_ipv6_nd_suppress_policy(device, policy_name, vlan=None, interface=None):
    """ Detaches the given ipv6 nd suppress policy to an interface or vlan(s)
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be detached
            interface (str): interface to detach policy from
            vlan (str): vlan or vlan range to detach the policy from. e.g: 1-10,15
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to detach ipv6 nd suppress policy {policy_name}
    """
    log.info(
        "Detaching ipv6 nd suppress policy {policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        if interface:
            device.configure([
                "interface {interface}".format(interface = interface),
                "no ipv6 nd suppress attach-policy {policy_name}".format(policy_name = policy_name)
            ])
        else:
            device.configure([
                "vlan configuration {vlan}".format(vlan = vlan),
                "no ipv6 nd suppress attach-policy {policy_name}".format(policy_name = policy_name)
            ])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to detach ipv6 nd suppress policy {policy_name}"
            .format(policy_name=policy_name)
        )


def config_device_tracking_policy(device, policy, options=None):
    """ Configure a device-tracking policy with specified options
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options:
                dictionary contains any of the following keys:
                    cache_guard ('str', optional):             cache poisoning guard mode
                    data_glean ('str', optional):              source address gleaning
                    destination_glean ('str', optional):       destination address gleaning
                    device_role ('str', optional):             device role
                    distribution_switch ('str', optional):     hostname of ip address
                    limit_address_count ('dict', optional):
                        all ('int', optional):                 max value
                        ipv4 ('int', optional):                address limit for ipv4 per mac
                        ipv6 ('int', optional):                address limit for ipv6 per mac
                    origin ('str', optional):                  configure origin of the policy
                    prefix_glean ('str', optional):            glean prefixes in RA and DHCP-PD traffic
                    protocol ('dict', optional):
                        name ('dict'):                         name can be arp, dhcp4, dhcp6, ndp, or udp
                            prefix_list ('str'):               name of prefix-list
                    security_level ('str', optional):          security level
                    tracking ('str', optional):                tracking behavior
                    trusted_port ('bool', optional):           setup trusted port
                    vpc ('int', optional):                     setup vpc port
                ex.)
                    [
                        {
                            "cache_guard": "ipv4",
                            "data_glean": "log-only",
                            "destination_glean": "log-only",
                            "device_role": "node",
                            "distribution-switch": ""10.10.10.10"",
                            "limit_address_count": {
                                "all": 1000,
                                "ipv4": 50,
                                "ipv6": 10
                            },
                            "origin": "cli",
                            "prefix_glean": "only",
                            "protocol": {
                                "arp": {
                                    "prefix_list": "name1"
                                },
                                "dhcp4": {
                                    "prefix_list": "name2"
                                }
                            },
                            "security_level": "guard",
                            "tracking": "enable",
                            "trusted_port": True,
                            "vpc": 10
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure device-track policy
    """
    config = []
    config.append("device-tracking policy {policy}".format(policy=policy))

    prefix_list = [
        "cache-guard",
        "data-glean",
        "destination-glean",
        "device-role",
        "distribution-switch",
        "limit-address-count",
        "origin",
        "prefix-glean",
        "protocol",
        "security-level",
        "tracking",
        "trusted-port",
        "vpc",
    ]

    if options:
        for option in options:
            for prefix in prefix_list:
                key = prefix.replace("-", "_")
                param = option.get(key, None)
                if param:
                    if key == "limit_address_count":
                        prefix = "limit address-count"
                        for k, v in param.items():
                            if k == "all":
                                config.append("{prefix} {val}".format(prefix=prefix, val=v))
                            else:
                                config.append("{prefix} {key} {val}".format(prefix=prefix,
                                                                            key=k, val=v))
                    elif key == "trusted_port":
                        config.append("{prefix}".format(prefix=prefix))
                    elif key == "protocol":
                        for protocol in param.keys():
                            prefix_list = param.get(protocol, {}).get("prefix_list", None)
                            if prefix_list:
                                config.append("{prefix} {protocol} prefix-list {prefix_list}"
                                              .format(prefix=prefix, protocol=protocol,
                                                      prefix_list=prefix_list))
                    else:
                        config.append("{prefix} {value}".format(prefix=prefix, value=param))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure device-track policy command"
        )


def unconfig_device_tracking_policy(device, policy, options=None):
    """ Remove specified options for device-tracking policy
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options to be removed or reset:
                dictionary contains any of the following keys:
                    cache_guard ('bool', optional)
                    data_glean ('bool', optional)
                    destination_glean ('bool', optional)
                    device_role ('bool', optional)
                    distribution_switch ('bool', optional)
                    limit_address_count ('bool', optional)
                    origin ('bool', optional)
                    prefix_glean ('bool', optional)
                    protocol ('dict', optional)
                        name ('bool')
                    tracking ('bool', optional)
                    trusted_port ('bool', optional)
                    vpc ('int', optional)
                ex.)
                    [
                        {
                            "cache_guard": True,
                            "data_glean": True,
                            "destination_glean": True,
                            "device_role": True,
                            "distribution-switch": True,
                            "limit_address_count": True,
                            "origin": True,
                            "prefix_glean": True,
                            "protocol": {
                                "arp": True,
                                "dhcp4": True
                            },
                            "security_level": True,
                            "tracking": True,
                            "trusted_port": True,
                            "vpc": 10
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove device-track policy configurations
    """
    config = []
    config.append("device-tracking policy {policy}".format(policy=policy))

    prefix_list = [
        "cache-guard",
        "data-glean",
        "destination-glean",
        "device-role",
        "distribution-switch",
        "limit-address-count",
        "origin",
        "prefix-glean",
        "protocol",
        "security-level",
        "tracking",
        "trusted-port",
        "vpc",
    ]

    if options:
        for option in options:
            for prefix in prefix_list:
                key = prefix.replace("-", "_")
                param = option.get(key, None)
                if param:
                    if key == "protocol":
                        for protocol, value in param.items():
                            if value is True:
                                config.append("no protocol {protocol}".format(protocol=protocol))
                    if key == "vpc":
                        config.append("no {prefix} {vpc}".format(prefix=prefix, vpc=param))
                    else:
                        if key == "limit_address_count":
                            prefix = "limit address-count"
                        if param is True:
                            config.append("no {prefix}".format(prefix=prefix))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to remove device-track policy configurations"
        )


def remove_device_tracking_policy(device, client_policy_name,  server_policy_name=None):
    """ Remove device-tracking policy
        Args:
            device ('obj'): device to use
            client_policy_name('str'): name of a policy to be removed
            server_policy_name('str', optional): name of another policy to be removed. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing device tracking policy
    """

    config = []
    policy_list = [p for p in [client_policy_name, server_policy_name] if p is not None]

    log.debug('Removing device tracking policy/policies {policy_list}'.format(policy_list=policy_list))

    for policy in policy_list:
        config.append("no device-tracking policy {policy}".format(policy=policy))

    try:
       device.configure(config)
    except SubCommandFailure:
        log.warning(
            "Could not remove device tracking policy/policies {policy_list}" \
            .format(policy_list=policy_list), exc_info=True
        )
        raise


def config_ipv6_nd_raguard_policy(device, policy, options=None):
    """ Configure an ipv6 nd raguard policy with specified options
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options:
                dictionary contains following keys:
                    device_role ('str', optional):             device role
                    hop_limit ('dict', optional):
                        max ('int'):                           maximum hop limit
                        min ('int'):                           minimum hop limit
                    managed_config_flag ('bool', optional):    enable M flag
                    match ('dict', optional):
                        ipv6 ('str'):                          access list to match
                        ra ('str'):                            prefix list to match
                    other_config_flag ('bool', optional):      enable O flag
                    router_preference ('dict', optional):      enable router preference flag
                    trusted_port ('bool', optional):           setup trusted port
                ex.)
                    [
                        {
                            "device_role": "host",
                            "hop_limit": {
                                "max": 100,
                                "min": 50
                            },
                            "managed_config_flag": True,
                            "match": {
                                "ipv6": "test",
                                "ra": "bar"
                            },
                            "other_config_flag": False,
                            "router_preference": "high",
                            "trusted_port": True,
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 nd raguard policy
    """
    config = []
    config.append("ipv6 nd raguard policy {policy}".format(policy=policy))

    if options:
        for option in options:
            param = option.get("device_role", None)
            if param:
                config.append("device-role {role}".format(role=param))

            param = option.get("hop_limit", {}).get("max", None)
            if param:
                config.append("hop-limit maximum {max}".format(max=param))

            param = option.get("hop_limit", {}).get("min", None)
            if param:
                config.append("hop-limit minimum {min}".format(min=param))

            param = option.get("managed-config-flag", None)
            if param is True:
                config.append("managed-config-flag on")
            elif param is False:
                config.append("managed-config-flag off")

            param = option.get("match", {}).get("ipv6", None)
            if param:
                config.append("match ipv6 access-list {access_list}".format(access_list=param))

            param = option.get("match", {}).get("ra", None)
            if param:
                config.append("match ra prefix-list {prefix_list}".format(prefix_list=param))

            param = option.get("other-config-flag", None)
            if param is True:
                config.append("other-config-flag on")
            elif param is False:
                config.append("other-config-flag off")

            param = option.get("router-preference", None)
            if param:
                config.append("router-preference maximum {max}".format(max=param))

            param = option.get("trusted-port", None)
            if param:
                config.append("trusted-port")

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure ipv6 nd raguard command"
        )


def unconfig_ipv6_nd_raguard_policy(device, policy, options=None):
    """ Remove specified options for ipv6 nd raguard policy
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options to be removed or reset:
                dictionary contains following keys:
                    device_role ('bool', optional)
                    hop_limit ('dict', optional)
                        max ('bool')
                        min ('bool')
                    managed_config_flag ('bool', optional)
                    match ('dict', optional)
                        ipv6 ('bool')
                        ra ('bool')
                    other_config_flag ('bool', optional)
                    router_preference ('bool', optional)
                    trusted_port ('bool', optional)
                ex.)
                    [
                        {
                            "device_role": True,
                            "hop_limit": {
                                "max": True,
                                "min": True
                            },
                            "managed_config_flag": True,
                            "match": {
                                "ipv6": True,
                                "ra": True
                            },
                            "other_config_flag": True,
                            "router_preference": True,
                            "trusted_port": True,
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove ipv6 nd raguard policy configurations
    """
    config = []
    config.append("ipv6 nd raguard policy {policy}".format(policy=policy))

    if options:
        for option in options:
            if option.get("device_role", False):
                config.append("no device-role")

            if option.get("hop_limit", {}).get("max", False):
                config.append("no hop-limit maximum")
            if option.get("hop_limit", {}).get("min", False):
                config.append("no hop-limit minimum")

            if option.get("managed_config_flag", False):
                config.append("no managed-config-flag")

            if option.get("match", {}).get("ipv6", False):
                config.append("no match ipv6 access-list")
            if option.get("match", {}).get("ra", False):
                config.append("no match ra prefix-list")

            if option.get("other_config_flag", False):
                config.append("no other-config-flag")

            if option.get("router_preference", False):
                config.append("no router-preference maximum")

            if option.get("trusted_port", False):
                config.append("no trusted-port")

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to remove ipv6 nd raguard policy configurations"
        )


def config_ipv6_source_guard_policy(device, policy, options=None):
    """ Configure an ipv6 source-guard policy with specified options
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options:
                dictionary contains following keys:
                    deny ('str', optional):         block data traffic
                    permit ('str', optional):       allow data traffic
                    trusted ('bool', optional):     setup trusted port
                    validate ('str', optional):     validate source of received data traffic
                ex.)
                    [
                        {
                            "deny": "global-autoconf",
                            "permit": "link-local",
                            "trusted": True,
                            "validate": "address",
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure ipv6 source-guard policy
    """
    config = []
    config.append("ipv6 source-guard policy {policy}".format(policy=policy))

    prefix_list = [
        "deny",
        "permit",
        "trusted",
        "validate",
    ]

    if options:
        for option in options:
            for prefix in prefix_list:
                param = option.get(prefix, None)
                if param:
                    if prefix == "trusted" and param is True:
                        config.append("trusted")
                    else:
                        config.append("{prefix} {value}".format(prefix=prefix, value=param))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure ipv6 source-guard policy command"
        )


def unconfig_ipv6_source_guard_policy(device, policy, options=None):
    """ Remove specified options for ipv6 source-guard policy
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            options ('list'): list of policy configuration options to be removed or reset:
                dictionary contains following keys:
                    deny ('bool', optional)
                    permit ('bool', optional)
                    trusted ('bool', optional)
                    validate ('dict', optional)
                        source ('bool')
                ex.)
                    [
                        {
                            "deny": True,
                            "permit": True,
                            "trusted": True,
                            "validate": {
                                "address": True,
                                "prefix": True,
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove ipv6 source-guard policy configurations
    """
    config = []
    config.append("ipv6 source-guard policy {policy}".format(policy=policy))

    prefix_list = [
        "deny global-autoconf",
        "permit link-local",
        "trusted",
        "validate",
    ]

    if options:
        for option in options:
            for prefix in prefix_list:
                key = prefix.split()[0]
                param = option.get(key, None)
                if param:
                    if key == "validate":
                        for k in param.keys():
                            config.append("no {key} {k}".format(key=key, k=k))
                    else:
                        config.append("no {prefix}".format(prefix=prefix))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to remove ipv6 source-guard policy configurations"
        )


def remove_ipv6_source_guard_policy(device, policy_name):
    """ Configure IPv6 Source Guard Policy
        Args:
            device ('obj'): device to use
            policy_name ('str'): name of the policy to be removed
        Returns:
            None
        Raises:
            SubCommandFailure: Failed removing IPv6 Source Guard policy
    """
    log.debug(
        "Removing ipv6 source-guard policy with name={policy_name}"
        .format(policy_name=policy_name)
    )

    try:
        device.configure([
            "no ipv6 source-guard policy {policy_name}".format(policy_name=policy_name),
        ])
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not remove IPv6 source guard policy {policy_name}".format(
                policy_name=policy_name
            )
        )


def device_tracking_attach_policy(device, policy, interface=None, vlan=None):
    """ Attach device tracking policy to a target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to attach device-tracking policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("device-tracking attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to attach device-tracking policy"
        )


def device_tracking_detach_policy(device, policy, interface=None, vlan=None):
    """ Detach device-tracking policy from target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to detach device-tracking policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("no device-tracking attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to detach device-tracking policy"
        )


def ipv6_nd_raguard_attach_policy(device, policy, interface=None, vlan=None):
    """ Attach ipv6 nd raguard policy to target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to attach ipv6 nd raguard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("ipv6 nd raguard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to attach ipv6 nd raguard policya"
        )


def ipv6_nd_raguard_detach_policy(device, policy, interface=None, vlan=None):
    """ Detach ipv6 nd raguard policy from target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to detach ipv6 nd raguard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("no ipv6 nd raguard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to detach ipv6 nd raguard policy"
        )


def ipv6_source_guard_attach_policy(device, policy, interface=None, vlan=None):
    """ Attach ipv6 source-guard policy to target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to attach ipv6 source-guard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("ipv6 source-guard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to attach ipv6 source-guard policy"
        )


def ipv6_source_guard_detach_policy(device, policy, interface=None, vlan=None):
    """ Detach ipv6 source-guard policy from target
        Args:
            device ('obj'): device object
            policy ('str'): policy name
            interface ('str', optional): interface name. Defaults to None
            vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to detach ipv6 source-guard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("no ipv6 source-guard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to detach ipv6 source-guard policy"
        )


def enable_service_internal(device):
    """ Enable service internal
        Args:
            device ('obj'): device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to enable service internal
    """

    try:
        device.configure("service internal")
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to enable service internal"
        )


def disable_service_internal(device):
    """ Disable service internal
        Args:
            device ('obj'): device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to disable service internal
    """

    try:
        device.configure("no service internal")
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to disable service internal"
        )


def device_tracking_unit_test(device, options=None):
    """ Run device-tracking unit tests
        Args:
            device ('obj'): device object
            options ('list'): list of policy configuration options:
                dictionary contains any of the following keys:
                    association ('dict', optional):
                        vlan ('int'):                         vlan id
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        mac_address ('str')                   48-bit hardware address
                        command ('str')                       command to execute
                    bt_add ('dict', optional):
                        vlan ('int'):                         vlan id
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        # configs ('dict', optional):
                        network_address ('str'):              IPv4/v6 address or IPv6 prefix
                        mac_address ('str'):                  48-bit hardware address
                        data_glean('bool', optional):
                        pref ('dict', optional):
                            level ('int'):                    preference level
                            incomplete('bool'):               if True, set incomplete state
                            origin ('int'):                   set origin
                            iterate ('int', optional):        number of iterations
                    bt_mac ('dict', optional):
                        vlan ('int'):                         vlan id
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        # configs ('dict', optional):
                        mac_address ('str'):                  48-bit hardware address
                        canip ('str', optional):              candidate IP address
                        wired ('boot', optional):             If true, wired connection
                    bulk_sync ('bool'):                       if true, bulk sync to DS
                    check_reach ('dict', optional):
                        network_address ('str'):              IPv6 address
                        vlan ('int'):                         vlan id
                    clear ('dict', optional):
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        vlans ('list', optional):             list of vlan ids
                    disable_cli_sync ('bool'):                if true, disable CLI sync
                    dna ('dict', optional):
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        policy ('str', optional):             policy name
                        priority ('int', optional):           policy priority
                        vlan ('int', optional)
                    evpn_dt ('int'):                          vlanid - de/attach DT policy from evpn
                    evpn_flood_suppr ('dict', optional):
                        vlan: ('int'):                        vlan id
                        dhcp_floop_suppr ('bool')             enable/disable flooping suppress from evpn
                    evpn_gateway_add ('dict', optional):
                        vlan ('int'):                         vlan id
                        network_address ('str'):              IPv4/v6 address or IPv6 prefix
                        mac_address ('str'):                  48-bit hardware address
                    evpn_remote_bt_add ('dict', optional):
                        vlan ('int'):                         vlan id
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        network_address ('str'):              IPv4/v6 address or IPv6 prefix
                        mac_address ('str'):                  48-bit hardware address
                        pref_level ('int'):                   preference level
                    fabric ('dict', optional):
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        mac_address('str'):                   48-bit hardware address
                    fault ('dict', optional):
                        code: ('int'):                        fault code
                        mac_address ('str'):                  48-bit hardware address
                        bdid ('int'):                         bridge-domain id
                        interface ('str'):                    interface name
                        num ('str'):                          interface number
                        transaction_id ('int'):               DHCP transation id
                        client_address ('str'):               Client IP address
                        server_address ('str'):               Server IP address
                    flood_suppr ('int'):                      vlan id, de/attach flooding suppress policy
                    ha_sync_msg ('dict', optional):
                        msg_type ('str'):                     HA message type
                        action ('str'):                       enable or disable message type
                    ip_dhcp_snooping ('int'):                 vlan id, de/attach shared policy from ip dhcp snooping
                    lisp_dt ('dict', optional):
                        vlan ('int'):                         vlan id
                        pref_level ('int'):                   preference level
                        cache_guard ('int'):                  cache guard
                    notify ('dict', optional):
                        delete ('dict', optional):
                            network_address ('str'):          IP address
                            check ('str'):                    type of check
                        register ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                    pgm ('dict', optional):
                        target ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                        peer ('dict', optional):
                            network_address ('str'):          IP address
                            interface ('str'):                interface
                            num ('str'):                      interface num
                        vlan ('int', optional):               vlan id
                    profile ('dict', optional):
                        target ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                        vlan ('int', optional):               vlan id
                    reapply_filters ('dict', optional):
                        target ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                        vlan ('int', optional):               vlan id
                    replace_policy ('dict', optional):
                        target ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                        vlan ('dict', optional):
                            id ('int'):                       vlan id
                            old_policy ('str'):               old policy name
                            new_policy ('str'):               new policy name
                    transport ('str'):                        authentication key (Hex string)
                    upgm ('dict', optional):
                        target ('dict', optional):
                            interface ('str'):                interface name
                            num ('str'):                      interface number
                        vlan ('int', optional):               vlan id
                ex.)
                    [
                        {
                            "association": {
                                "vlan": 39,
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "mac_address": "1234.5678.90AB",
                                "command": "new"
                            },
                            "bt_add": {
                                "vlan": 39,
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "network_address": "10.10.10.10",
                                "mac_address": "1234.5678.90AB",
                                "pref": {
                                    "level": 2,
                                    "incomplete": True,
                                    "origin": 4,
                                    "iterate": 2,
                                },
                            },
                            "bt_mac": {
                                "vlan": 39,
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "mac_address": "1234.5678.90AB",
                                "wired": True,
                            },
                            "bulk_sync": True,
                            "check_reach": {
                                "network_address": "FE80::6AF3:3E56:FE0B:BEE9",
                                "vlan": 39,
                            },
                            "clear": {
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "vlans": [1, 2, 3, 4, 5],
                            },
                            "disable_cli_sync": True,
                            "dna": {
                                "policy": "test",
                                "priority": 255,
                                "vlan": 39,
                            },
                            "evpn_dt": 39,
                            "evpn_flood_suppr": {
                                "vlan": 39,
                                "dhcp_floop_suppr": True,
                            },
                            "evpn_gateway_add": {
                                "vlan": 39,
                                "network_address": "10.10.10.10",
                                "mac_address": "1234.5678.90AB",
                            },
                            "evpn_remote_bt_add": {
                                "vlan": 39,
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "network_address": "10.10.10.10",
                                "mac_address": "1234.5678.90AB",
                                "pref_level": 255,
                            },
                            "fabric": {
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "mac_address": "1234.5678.90AB",
                            },
                            "fault":{
                                "code": 12,
                                "mac_address": "1234.5678.90AB",
                                "bdid": 4094,
                                "interface": "TwentyFiveGigE",
                                "num": "1/0/42",
                                "transaction_id": 10000,
                                "client_address": "10.10.10.10",
                                "server_address": "20.20.20.20",
                            },
                            "flood_suppr": 39,
                            "ha_sync_msg": {
                                "msg_type": "bt-entry",
                                "action": "disable",
                            },
                            "ip_dhcp_snooping": 39,
                            "lisp_dt": {
                                "vlan": 39,
                                "pref_level": 0,
                                "cache_guard": 3,
                            },
                            "notify": {
                                "delete": {
                                    "network_address": "10.10.10.10",
                                    "check": "quick_check",
                                },
                            },
                            "pgm": {
                                "vlan": 39,
                            },
                            "profile": {
                                "vlan": 39,
                            },
                            "reapply_filters":{
                                "vlan": 39,
                            },
                            "replace_policy": {
                                "vlan": {
                                    "id": 39,
                                    "old_policy": "policy_old",
                                    "new_policy": "policy_new",
                                },
                            },
                            "transport": "ffff",
                            "upgm": {
                                "target": {
                                    "interface": "TwentyFiveGigE",
                                    "num": "1/0/42",
                                },
                            },
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to perform device-tracking unit-test
    """

    config = []
    prefix = "device-tracking unit-test"

    if options:
        for option in options:
            params = option.get("association", None)
            if params:
                suffix = "association vlan {vlan} interface {interface} {num} {mac} command {cmd}" \
                         .format(vlan=params["vlan"], interface=params["interface"],
                                 num=params["num"], mac=params["mac_address"], cmd=params["command"])
                config.append("{prefix} {suffix}".format(prefix=prefix, suffix=suffix))

            params = option.get("bt_add", None)
            if params:
                suffix = "bt-add vlan {vlan} interface {interface} {num} {ip} {mac}" \
                         .format(vlan=params["vlan"], interface=params["interface"],
                                 num=params["num"], ip=params["network_address"],
                                 mac=params["mac_address"])

                if "data_glean" in params:
                    config.append("{prefix} {suffix} data-glean".format(prefix=prefix, suffix=suffix))
                if "pref" in params:
                    pref_dict = params["pref"]
                    incomplete = iterate = origin = level = ""

                    if "incomplete" in pref_dict:
                        if pref_dict["incomplete"] is True:
                            incomplete = "incomplete "
                    if "origin" in pref_dict:
                        origin = "origin {origin}".format(origin=pref_dict["origin"])
                    if "level" in pref_dict:
                        level = "preflevel {level}".format(level=pref_dict["level"])
                    if "iterate" in pref_dict:
                        iterate = " iterate {num}".format(num=pref_dict["iterate"])

                    config.append("{prefix} {suffix} {level} {incomplete}" \
                                  "{origin}{iterate}"
                                  .format(prefix=prefix, suffix=suffix, level=level,
                                          incomplete=incomplete, origin=origin,
                                          iterate=iterate))

            params = option.get("bt_mac", None)
            if params:
                suffix = "bt-mac vlan {vlan} interface {interface} {num} {mac}" \
                         .format(vlan=params["vlan"], interface=params["interface"],
                                 num=params["num"], mac=params["mac_address"])

                if "canip" in params:
                    config.append("{prefix} {suffix} canip {canip}"
                                  .format(prefix=prefix, suffix=suffix, canip=params["canip"]))
                if "wired" in params:
                    config.append("{prefix} {suffix} wired".format(prefix=prefix, suffix=suffix))

            params = option.get("bulk_sync", None)
            if params:
                config.append("{prefix} bulk-sync".format(prefix=prefix))

            params = option.get("check_reach", None)
            if params:
                config.append("{prefix} check-reach vlan {vlan} {ip}" \
                              .format(prefix=prefix, vlan=params["vlan"],
                                      ip=params["network_address"]))

            params = option.get("clear", None)
            if params:
                vlans = " ".join(map(str, (params["vlans"])))
                config.append("{prefix} clear neighbors binding interface {interface} {num} " \
                              "vlanlist {vlans}" \
                              .format(prefix=prefix, interface=params["interface"],
                                      num=params["num"], vlans=vlans))

            params = option.get("disable_cli_sync", None)
            if params:
                config.append("{prefix} disable-cli-sync".format(prefix=prefix))

            params = option.get("dna", None)
            if params:
                target = policy = priority = ""
                if "vlan" in params:
                    target = "vlan {vlan}".format(vlan=params["vlan"])
                else:
                    target = "interface {interface} {num}".format(interface=params["interface"],
                                                                  num = params["num"])

                if params.get("policy", None):
                    policy = "policy {policy} ".format(policy=params["policy"])
                if params.get("priority", None):
                    priority = "priority {priority}".format(priority=params["priority"])

                if target:
                    suffix = "dna {target} {policy}{priority}" \
                             .format(target=target, policy=policy, priority=priority)
                    suffix = suffix.strip()
                    config.append("{prefix} {suffix}".format(prefix=prefix, suffix=suffix))

            params = option.get("evpn_dt", None)
            if params:
                config.append("{prefix} evpn-dt vlan {vlan}" \
                              .format(prefix=prefix, vlan=params))

            params = option.get("evpn_flood_suppr", None)
            if params:
                dhcp_flood_suppr = ""
                if "dhcp_flood_suppr" in params:
                    dhcp_flood_suppr = "dhcp_flood_suppr"

                suffix = "evpn-flood-suppr vlan {vlan} {dhcp}" \
                         .format(vlan=params["vlan"], dhcp=dhcp_flood_suppr)
                suffix = suffix.strip()
                config.append("{prefix} {suffix}".format(prefix=prefix, suffix=suffix))

            params = option.get("evpn_gateway_add", None)
            if params:
                config.append("{prefix} evpn-gateway-add vlan {vlan} {ip} {mac}" \
                              .format(prefix=prefix, vlan=params["vlan"],
                                      ip=params["network_address"], mac=params["mac_address"]))

            params = option.get("evpn_remote_bt_add", None)
            if params:
                config.append("{prefix} evpn-remote-bt-add vlan {vlan} interface {interface} " \
                              "{num} {ip} {mac} preflevel {pref_level}" \
                              .format(prefix=prefix, vlan=params["vlan"],
                                      interface=params["interface"], num=params["num"],
                                      ip=params["network_address"], mac=params["mac_address"],
                                      pref_level=params["pref_level"]))

            params = option.get("fabric", None)
            if params:
                config.append("{prefix} fabric interface {interface} {num} {mac}" \
                              .format(prefix=prefix, interface=params["interface"],
                                      num=params["num"], mac=params["mac_address"]))

            params = option.get("fault", None)
            if params:
                config.append("{prefix} fault dhcp {code} {mac} bdid {bdid} interface " \
                              "{interface} {num} {trans_id} {client} {server}" \
                              .format(prefix=prefix, code=params["code"], mac=params["mac_address"],
                                      bdid=params["bdid"], interface=params["interface"],
                                      num=params["num"], trans_id=params["transaction_id"],
                                      client=params["client_address"],
                                      server=params["server_address"]))

            params = option.get("flood_suppr", None)
            if params:
                config.append("{prefix} flood-suppr dhcp-flood-suppr vlan {vlan}"
                              .format(prefix=prefix, vlan=option["flood_suppr"]))


            params = option.get("ha_sync_msg", None)
            if params:
                config.append("{prefix} ha-sync-msg msg-type {type} action {action}" \
                              .format(prefix=prefix, type=params["msg_type"],
                                      action=params["action"]))

            params = option.get("ip_dhcp_snooping", None)
            if params:
                config.append("{prefix} ip-dhcp-snooping vlan {vlan}"
                              .format(prefix=prefix, vlan=option["ip_dhcp_snooping"]))

            params = option.get("lisp_dt", None)
            if params:
                pref_level = params.get("pref_level", 0)
                cache_guard = params.get("pref_level", 0)
                config.append("{prefix} lisp-dt vlan {vlan} pref {pref_level} cache guard {guard}" \
                              .format(prefix=prefix, vlan=params["vlan"], pref_level=pref_level,
                                      guard=cache_guard))

            params = option.get("notify", None)
            if params:
                if "delete" in params:
                    delete_dict = params["delete"]
                    config.append("{prefix} notify delete {ip} {check}" \
                                  .format(prefix=prefix, ip=delete_dict["network_address"],
                                          check=delete_dict["check"]))
                if "register" in params:
                    register_dict = params["register"]
                    config.append("{prefix} notify register {interface} {num}" \
                                  .format(prefix=prefix, interface=register_dict["interface"],
                                          num=register_dict["num"]))

            params = option.get("pgm", None)
            if params:
                if "vlan" in params:
                    config.append("{prefix} pgm vlan {vlan}".format(prefix=prefix,
                                                                    vlan=params["vlan"]))
                elif "interface" in params:
                    target_dict = params["interface"]
                    config.append("{prefix} pgm interface {interface} {num}" \
                                  .format(prefix=prefix, interface=target_dict["interface"],
                                          num=target_dict["num"]))
                elif "peer" in params:
                    peer_dict = params["peer"]
                    config.append("{prefix} pgm peer {ip} interface {interface} {num}" \
                                  .format(prefix=prefix, ip=peer_dict["network_address"],
                                          interface=peer_dict["interface"], num=peer_dict["num"]))

            params = option.get("profile", None)
            if params:
                if "target" in params:
                    target_dict = params["target"]
                    config.append("{prefix} profile interface {interface} {num}" \
                                  .format(prefix=prefix, interface=target_dict["interface"],
                                          num=target_dict["num"]))
                if "vlan" in params:
                    config.append("{prefix} profile vlan {vlan}" \
                                  .format(prefix=prefix, vlan=params["vlan"]))

            params = option.get("reapply_filters", None)
            if params:
                if "target" in params:
                    target_dict = params["target"]
                    config.append("{prefix} reapply-filters interface {interface} {num}" \
                                  .format(prefix=prefix, interface=target_dict["interface"],
                                          num=target_dict["num"]))
                if "vlan" in params:
                    config.append("{prefix} reapply-filters vlan {vlan}" \
                                  .format(prefix=prefix, vlan=params["vlan"]))

            params = option.get("replace_policy", None)
            if params:
                if "target" in params:
                    target_dict = params["target"]
                    config.append("{prefix} replace-policy interface {interface} {num} old " \
                                  "{old_policy} new {new_policy}" \
                                  .format(prefix=prefix, interface=target_dict["interface"],
                                          num=target_dict["num"],
                                          old_policy=target_dict["old_policy"],
                                          new_policy=target_dict["new_policy"]))
                if "vlan" in params:
                    vlan_dict = params["vlan"]
                    config.append("{prefix} replace-policy vlan {vlan} old " \
                                  "{old_policy} new {new_policy}" \
                                  .format(prefix=prefix, vlan=vlan_dict["id"],
                                          old_policy=vlan_dict["old_policy"],
                                          new_policy=vlan_dict["new_policy"]))

            params = option.get("transport", None)
            if params:
                config.append("{prefix} transport {auth_key}" \
                              .format(prefix=prefix, auth_key=option["transport"]))

            params = option.get("upgm", None)
            if params:
                if "target" in params:
                    target_dict = params["target"]
                    config.append("{prefix} upgm interface {interface} {num}" \
                                  .format(prefix=prefix, interface=target_dict["interface"],
                                          num=target_dict["num"]))
                if "vlan" in params:
                    config.append("{prefix} upgm vlan {vlan}" \
                                  .format(prefix=prefix, vlan=params["vlan"]))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to perform device-tracking unit-test"
        )


def configure_device_tracking_binding(device, vlan, address, interface, mac, tracking="default",
                                      reachable_lifetime=None, retry_interval=None):
    """Adds static entry to binding table
    Args:
        device ('obj'): device object
        vlan ('str'): vlan id
        address ('str'): ip address (v4 or v6)
        interface ('str'): interface for entry - Eg. TWE 1/0/1
        mac ('str'): entry's mac address
        tracking ('str', optional): Set the tracking for the device - Eg. "enable", "disable", or "default" . Defaults to "default.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to add static entry
    """
    cmd = f"device-tracking binding vlan {vlan} {address} interface {interface} {mac} tracking {tracking}"

    if retry_interval is not None:
        cmd = f'{cmd} retry-interval {retry_interval}'

    if reachable_lifetime is not None:
        cmd = f'{cmd} reachable-lifetime {reachable_lifetime}'

    try:
        device.configure(cmd)
    except SubCommandFailure:
        log.warning("Failed to add static entry")
        raise


def unconfigure_device_tracking_binding(device, vlan, address, interface, mac, tracking="default"):
    """Removes static entry to binding table
    Args:
        device ('obj'): device object
        vlan ('str'): vlan id
        address ('str'): ip address (v4 or v6)
        interface ('str'): interface for entry - Eg. TWE 1/0/1
        mac ('str'): entry's mac address
        tracking ('str', optional): Set the tracking for the device - Eg. "enable", "disable", or "default" . Defaults to "default.
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to add static entry
    """
    cmd = "no device-tracking binding vlan {vlan} {address} interface {interface} {mac} tracking {tracking}"
    cmd = cmd.format(vlan=vlan, address=address, interface=interface, mac=mac, tracking=tracking)

    try:
        device.configure(cmd)
    except SubCommandFailure:
        log.warning("Failed to remove static entry")
        raise


def configure_device_tracking_binding_options(device, reachable_lifetime=None, stale_lifetime=None,
                                              down_lifetime=None, max_entries=None, mac_limit=None,
                                              port_limit=None, vlan_limit=None, logging=False):
    """ Configures device-tracking binding options
        Args:
            device ('obj'): device object
            reachable_lifetime ('str', optional): Default max time in REACHABLE without activity - can be 1-86400 or "infinite". Defaults to None
            stale_lifetime ('str', optional): Default max time in STALE without activity - can be 1-86400 or "infinite". Defaults to None
            down_lifetime ('str', optional): Default max time in DOWN without activity - can be 1-86400 or "infinite". Defaults to None
            max_entries ('int', optional): Max number of entries - can be 1-1000000. Defaults to None
            mac_limit ('int', optional): Max number of mac entries - can be 1-1000000. Defaults to None
            port_limit ('int', optional): Max number of port entries - can be 1-1000000. Defaults to None
            vlan_limit ('int', optional): Max number of vlan entries - can be 1-2000000. Defaults to None
            logging ('bool', optional): Enable syslog logging of binding table events. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure device-tracking binding
    """

    config = []
    debug_dict = {
        "reachable-lifetime": reachable_lifetime,
        "stale-lifetime": stale_lifetime,
        "down-lifetime": down_lifetime,
        "max-entries": max_entries,
        "mac-limit": mac_limit,
        "port-limit": port_limit,
        "vlan-limit": vlan_limit
    }

    if logging:
        config.append("device-tracking binding logging")

    # The CLI accepts max-entries limits in the order of vlan->port->mac,
    # otherwise the options will not be set as intended
    if max_entries:
        limit = "max-entries {max_entries} ".format(max_entries=max_entries)
        if vlan_limit:
            limit += "vlan-limit {} ".format(vlan_limit)
        if port_limit:
            limit += "port-limit {} ".format(port_limit)
        if mac_limit:
            limit += "mac-limit {} ".format(mac_limit)
        config.append("device-tracking binding {limit}".format(limit=limit))

    # The CLI accepts lifetime timers in the order of reachable->stale->down,
    # otherwise the options will not be set as intended
    if any([reachable_lifetime, stale_lifetime, down_lifetime]):
        lifetime = ""
        if reachable_lifetime:
            lifetime += "reachable-lifetime {} ".format(reachable_lifetime)
        if stale_lifetime:
            lifetime += "stale-lifetime {} ".format(stale_lifetime)
        if down_lifetime:
            lifetime += "down-lifetime {} ".format(down_lifetime)
        config.append("device-tracking binding {lifetime}".format(lifetime=lifetime))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure device-tracking binding with parameters: {params} " \
            .format(params=debug_dict)
        )


def unconfigure_device_tracking_binding_options(device, reachable_lifetime=False, stale_lifetime=False,
                                              down_lifetime=False, max_entries=False, logging=False):
    """ Unconfigures device-tracking binding options
        Args:
            device ('obj'): device object
            reachable_lifetime ('bool', optional): Flag to unconfigure reachable-lifetime. Defaults to False
            stale_lifetime ('bool', optional): Flag to unconfigure stale-lifetime. Defaults to False
            down_lifetime ('bool', optional): Flag to unconfigure down-lifetime. Defaults to False
            max_entries ('bool', optional): Flag to unconfigure max-entries lifetime. Defaults to False
            logging ('bool', optional): Disable syslog logging of binding table events. Defaults to False
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to unconfigure device-tracking binding
    """

    config = []
    prefix_dict = {
        "reachable-lifetime": reachable_lifetime,
        "stale-lifetime": stale_lifetime,
        "down-lifetime": down_lifetime,
        "max-entries": max_entries,
        "logging": logging
    }

    for key, value in prefix_dict.items():
        if value:
            config.append("no device-tracking binding {key}".format(key=key))

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to unconfigure device-tracking binding with parameters: {params}" \
            .format(params=prefix_dict)
        )


def configure_ipv6_destination_guard_attach_policy(device, policy, interface=None, vlan=None):
    """ Attach ipv6 destination-guard policy
    Args:
        device ('obj'): device object
        policy ('str'): policy name
        interface ('str', optional): interface name. Defaults to None
        vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None.
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to attach ipv6 destination-guard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("ipv6 destination-guard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        log.warning("Failed to attach ipv6 destination-guard policy")
        raise


def configure_ipv6_destination_guard_detach_policy(device, policy, interface=None, vlan=None):
    """ Detach ipv6 destination-guard policy
    Args:
        device ('obj'): device object
        policy ('str'): policy name
        interface ('str', optional): interface name. Defaults to None
        vlan ('str', optional): vlan id list - Eg. "1-10,15". Defaults to None.
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to detach ipv6 destination-guard policy
    """
    if interface is None and vlan is None:
        raise ValueError("There is no specified target to attach policy." \
                         "Ensure there is either an interface or a vlan as input")

    config = []
    if interface:
        config.append("interface {interface}".format(interface=interface))
    elif vlan:
        config.append("vlan config {vlan}".format(vlan=vlan))

    config.append("no ipv6 destination-guard attach-policy {policy}".format(policy=policy))

    try:
        device.configure(config)
    except SubCommandFailure:
        log.warning("Failed to deattach ipv6 destination-guard policy")
        raise


def configure_ipv6_destination_guard_policy(device, policy_name, enforcement=None):
    """ Configure ipv6 destination-guard policy
    Args:
        device ("obj"): The device to configure the policy on
        policy_name ("str"): the name of the policy
        enforcement ("str", optional): The enforcement policy to set - Eg. "always" or "stressed". Defaults to None.
    Raises:
        SubCommandFailure: Failed to configure ipv6 destination-guard policy {policy_name}
    """
    config_cmds = []
    config_cmds.append("ipv6 destination-guard policy {policy_name}".format(policy_name=policy_name))
    if enforcement:
        config_cmds.append("enforcement {enforcement}".format(enforcement=enforcement))

    try:
        device.configure(config_cmds)
    except SubCommandFailure:
        log.warning("Failed to configure ipv6 destination-guard policy {policy_name}"
            .format(policy_name=policy_name))
        raise


def unconfigure_ipv6_destination_guard_policy(device, policy_name):
    """ Unconfigure ipv6 destination_guard policy
    Args:
        device ("obj"): the device to unconfigure the policy on
        policy_name ("str"): The name of the policy

    Raises:
        SubCommandFailure: Failed to unconfigure ipv6 destination-guard {policy_name}
    """
    try:
        device.configure([
            "ipv6 destination-guard policy {policy_name}".format(policy_name=policy_name),
            "no enforcement"
        ])
    except SubCommandFailure:
        log.warning("Failed to unconfigure ipv6 destination-guard {policy_name}"
            .format(policy_name=policy_name))
        raise


def configure_device_tracking_tracking(device, auto_source=None, retry_interval=None):
    """ Configure device-tracking tracking

    Args:
        device ("obj"): The device to configure
        auto_source ("str", optional): The configuration for auto_source - either override or failback address. Defaults to None.
        retry_interval ("str", optional): Device-tracking retry-interval in seconds. Defaults to None.

    Raises:
        SubCommandFailure: Failed to configure device-tracking tracking
    """
    config_cmds = []
    if auto_source:
        if auto_source != "override":
            config_cmds.append("device-tracking tracking auto-source fallback {fallback_addr}".format(fallback_addr=auto_source))
        else:
            config_cmds.append("device-tracking tracking auto-source override")
    if retry_interval:
        config_cmds.append("device-tracking tracking retry-interval {retry_interval}".format(retry_interval=retry_interval))

    try:
        device.configure(config_cmds)
    except SubCommandFailure:
        log.warning("Failed to configure device-tracking tracking")
        raise

def unconfigure_device_tracking_tracking(device, auto_source=False, retry_interval=False):
    """ Unconfigure device-tracking tracking

    Args:
        device ("obj"): The device to configure
        auto_source ("bool", optional): The configuration for auto_source - either override or failback address. Defaults to False.
        retry_interval ("bool", optional): Device-tracking retry-interval in seconds. Defaults to False.

    Raises:
        SubCommandFailure: Failed to unconfigure device-tracking tracking
    """
    config_cmds = []

    cmd = "no device-tracking tracking"
    if auto_source:
        config_cmds.append(f"{cmd} auto-source")
    if retry_interval:
        config_cmds.append(f"{cmd} retry-interval")

    if not auto_source and not retry_interval:
        config_cmds.append(f"{cmd}")

    try:
        device.configure(config_cmds)
    except SubCommandFailure:
        log.warning("Failed to unconfigure device-tracking tracking")
        raise

def clear_device_tracking_messages(device):
    """ Clear device-tracking database
        Args:
            device ('obj'): device object
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to execute clear device-tracking messages
    """
    try:
        device.execute('clear device-tracking messages')
    except SubCommandFailure:
        log.warning("Failed to clear device-tracking messages")

def clear_device_tracking_database(device, options=None):
    """ Clear device-tracking database
        Args:
            device ('obj'): device object
            options ('list'): list of policy configuration options to be removed or reset:
                dictionary contains following keys:
                    address ('dict', optional):
                        address ('str'): IPv4 address or "all"
                        target ('dict', optional):
                            force ('bool', optional): Force to clear all (mac) entries
                            interface ('str', optional): interface
                            policy ('str', optional): policy name
                            vlanid ('str', optional): vlanid
                    force ('bool', optional): Force to clear all (mac) entries
                    interface ('str', optional):
                        target ('str'): interface
                        force ('bool', optional): Force to clear all (mac) entries
                        vlanid ('str', optional): vlanid
                    mac ('str', optional):
                        address ('str'): 48-bit hardware address
                        target ('dict', optional):
                            force ('bool', optional): Force to clear all (mac) entries
                            interface ('str', optional): interface
                            policy ('str', optional): policy name
                            vlanid ('str', optional): vlanid
                    policy ('str', optional): policy name
                    prefix ('bool', optional)
                        address ('str'): IPv6 address (X:X:X:X::X/<0-128>) or "all"
                        target ('dict', optional):
                            force ('bool', optional): Force to clear all (mac) entries
                            interface ('str', optional): interface
                            policy ('str', optional): policy name
                            vlanid ('str', optional): vlanid
                    vlanid ('str', optional): vlan id
                ex.)
                    [
                        {
                            "force": True,
                            "mac": {
                                "address": "dead.beef.0001"
                                "target":
                                    "force": True
                                    "interface": "gigabitEthernet0/0"
                                    "policy": "test"
                                    "vlanid": 10
                            }
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed to remove ipv6 source-guard policy configurations
    """

    config = []
    prefix = "clear device-tracking database"
    nested_options_list = [
        "address",
        "mac",
        "prefix",
    ]

    if options is None:
        config.append(prefix)
    else:
        for option in options:
            if option.get("force", None):
                config.append("{prefix} force".format(prefix=prefix))
            if option.get("policy", None):
                config.append("{prefix} policy {policy}".format(prefix=prefix, policy=option['policy']))
            if option.get("vlanid", None):
                config.append("{prefix} vlanid {vlanid}".format(prefix=prefix, vlanid=option['vlanid']))
            if option.get("interface", None):
                interface_dict = option["interface"]
                if interface_dict.get("interface", None):
                    target = interface_dict["interface"]
                    suffix = ""
                    if interface_dict.get("force", None):
                        suffix = "force"
                    elif interface_dict.get("vlanid", None):
                        suffix = "vlanid {vlanid}".format(vlanid=interface_dict["vlanid"])

                    config.append("{prefix} interface {interface} {suffix}".format(prefix=prefix,
                                                                                interface=target,
                                                                                suffix=suffix))

            for nested_option in nested_options_list:
                if option.get(nested_option, None):
                    address_dict = option[nested_option]
                    if address_dict.get("address", None):
                        address = address_dict["address"]
                        opt = "{key} {value}".format(key=nested_option, value=address)
                        suffix = ""

                        if address_dict.get("target", None):
                            target_dict = address_dict["target"]
                            if target_dict.get("force", None):
                                suffix = "force"
                            elif target_dict.get("interface", None):
                                suffix = "interface {interface}".format(interface=target_dict["interface"])
                            elif target_dict.get("policy", None):
                                suffix = "policy {policy}".format(policy=target_dict["policy"])
                            elif target_dict.get("vlanid", None):
                                suffix = "vlanid {vlanid}".format(vlanid=target_dict["vlanid"])

                        config.append("{prefix} {opt} {suffix}".format(prefix=prefix, opt=opt, suffix=suffix))

    try:
        device.execute(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to clear device-tracking database"
        )


def clear_device_tracking_counters(device, interface=None, vlan=None, bdi=None):
    """ Clear device-tracking counters
    Args:
        device ('obj'): device object
        interface ('str', optional): interface name. Defaults to None
        vlan ('str', optional): vlan id. Defaults to None.
        bdi ('str', optional): bdi id. Defaults to None.
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to clear device-tracking counters
    """

    config = "clear device-tracking counters"

    if interface:
        config += " interface {interface}".format(interface=interface)
    elif vlan:
        config += " vlan {vlan}".format(vlan=vlan)
    elif bdi:
        config += " bdi {bdi}".format(bdi=bdi)

    try:
        device.execute(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to clear device-tracking counters"
        )

def configure_ipv6_nd_raguard_on_interface(device, interface):
    """ configure ipv6 nd raguard on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure ipv6 nd raguard on interface
    """
    config = [f"interface {interface}",
               "ipv6 nd raguard"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to remove ipv6 nd raguard from interface"
        )

def unconfigure_ipv6_nd_raguard_on_interface(device, interface):
    """ Unconfigure ipv6 nd raguard on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to remove ipv6 nd raguard from interface
    """
    config = [f"interface {interface}",
               "no ipv6 nd raguard"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to remove ipv6 nd raguard from interface"
        )

def configure_device_tracking_on_interface(device, interface):
    """ Configure device-tracking on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure device-tracking on interface
    """
    config = [f"interface {interface}",
               "device-tracking"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to configure device-tracking on interface"
        )

def unconfigure_device_tracking_on_interface(device, interface):
    """ Unconfigure device-tracking on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to remove device-tracking from interface
    """
    config = [f"interface {interface}",
               "no device-tracking"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to remove device-tracking from interface"
        )

def configure_ipv6_dhcp_guard_on_interface(device, interface):
    """ Configure ipv6 dhcp guard on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure ipv6 dhcp guard on interface
    """
    config = [f"interface {interface}",
               "ipv6 dhcp guard"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to configure ipv6 dhcp guard on interface"
        )

def unconfigure_ipv6_dhcp_guard_on_interface(device, interface):
    """ Unconfigure ipv6 dhcp guard on interface
    Args:
        device ('obj'): device object
        interface ('str'): interface name
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to remove ipv6 dhcp guard from interface
    """
    config = [f"interface {interface}",
               "no ipv6 dhcp guard"]
    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failure to remove ipv6 dhcp guard from interface"
        )

def configure_interface_template_with_default_ipv6_nd_raguard_policy(device, template_name, vlan=None):
    """ configure interface template with default ipv6 nd raguard policy
    Args:
        device ('obj'): device object
        template_name ('str'): template_name name,
        vlan ('str', optional): vlan id
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure default ipv6 nd raguard policy on template
    """
    config = [f'template {template_name}']

    cmd = 'ipv6 nd raguard'
    if vlan:
        cmd = f'{cmd} vlan {vlan}'

    config.append(cmd)

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure default ipv6 nd raguard policy on template"
        )

def configure_interface_template_with_default_device_tracking_policy(device, template_name, vlan=None):
    """ configure interface template with default device-tracking policy
    Args:
        device ('obj'): device object
        template_name ('str'): template_name name,
        vlan ('str', optional): vlan id
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure default device-tracking policy on template
    """
    config = [f'template {template_name}']

    cmd = 'device-tracking'
    if vlan:
        cmd = f'{cmd} vlan {vlan}'

    config.append(cmd)

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure default device-tracking policy on template"
        )

def configure_interface_template_with_default_ipv6_dhcp_guard_policy(device, template_name, vlan=None):
    """ configure interface template with default ipv6 dhcp guard policy
    Args:
        device ('obj'): device object
        template_name ('str'): template_name name,
        vlan ('str', optional): vlan id
    Returns:
        None
    Raises:
         SubCommandFailure: Failed to configure default ipv6 dhcp guard policy on template
    """
    config = [f'template {template_name}']

    cmd = 'ipv6 dhcp guard'
    if vlan:
        cmd = f'{cmd} vlan {vlan}'

    config.append(cmd)

    try:
        device.configure(config)
    except SubCommandFailure:
        raise SubCommandFailure(
            "Failed to configure default ipv6 dhcp guard policy on template"
        )

def configure_device_tracking_policy_reachable(device, policy, tracking, time=None):
    """ Device tracking configuration
        Args:
            device ('obj'): Device object
            policy ('str'): Policy name
            tracking ('str'): tracking is enable or disable
            time ('str', Optional) : Reachable life time value 1-86400-seconds or infinite
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    configs = []
    configs.append("device-tracking policy {policy}".format(policy=policy))
    if tracking=="enable" and time:
        configs.append("tracking enable reachable-lifetime {time}".format(time=time))
    elif tracking=="disable" and time:
        configs.append("tracking disable stale-lifetime {time}".format(time=time))
    elif tracking and time is None:
        configs.append("tracking {tracking}".format(tracking=tracking))

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure device policy on {device}. Error:\n{error}"
            .format(device=device, error=e))

def configure_device_tracking_binding_globally(device, vlan, address, interface):
    """Adds static entry to binding table globally
    Args:
        device ('obj'): device object
        vlan ('str'): vlan id
        address ('str'): ip address (v4 or v6)
        interface ('str'): interface for entry - Eg. TWE 1/0/1
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to add static entry globally
    """
    cmd = f"device-tracking binding vlan {vlan} {address} interface {interface}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure static entry globally on {device}. Error:\n{error}"
            .format(device=device, error=e))

def unconfigure_device_tracking_binding_globally(device, vlan, address, interface):
    """Removes static entry to binding table globally
    Args:
        device ('obj'): device object
        vlan ('str'): vlan id
        address ('str'): ip address (v4 or v6)
        interface ('str'): interface for entry - Eg. TWE 1/0/1
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to add static entry
    """
    cmd = f"no device-tracking binding vlan {vlan} {address} interface {interface}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure static entry globally on {device}. Error:\n{error}"
            .format(device=device, error=e))

def configure_vlan_config_device_tracking(device, vlan, policy=None, priority=None):
    """ Configure Device tracking on vlan
        Args:
            device ('obj'): Device object
            vlan ('str'): vlan number 1-4094
            policy ('str', optional): policy name for device-tracking
            priority ('str', optional): priority value, 0: lowest, 255 highest, 128 default
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring device tracking on vlan {device.name}")
    config = [f"vlan configuration {vlan}"]
    if policy:
        config.append(f"device-tracking attach-policy {policy}")
    elif priority:
        config.append(f"device-tracking priority {priority}")
    else:
        config.append("device-tracking")
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Could not configure device-tracking on vlan. Error:\n{e}')
