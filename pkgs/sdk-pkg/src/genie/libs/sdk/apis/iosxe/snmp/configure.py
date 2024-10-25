"""Common configure functions for snmp"""

import logging
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)

def configure_snmp(device,community_string, access_type):
    """ Configures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            access_type ('str') : type of Access
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("snmp-server community {community_string} {access_type}".format(
            community_string=community_string,access_type=access_type))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp. Error:\n{error}".format(error=e))

def unconfigure_snmp(device,community_string):
    """ Unconfigures the snmp on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp on device {device}".format(device=device))

    try:
        device.configure("no snmp-server community {community_string}".format(community_string=community_string))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not unconfigure snmp. Error:\n{error}".format(error=e))

def configure_snmp_server_view(device, mib_view, family_name, state = 'excluded'):
    """ Configures the snmp server view on device
        Args:
            device ('obj'): device to use
            mib_view ('str'): Name of the view
            family_name ('str'): MIB view family name
            state ('str'): mib family excluded|included
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmpserver view on device {device}")

    try:
        device.configure(f"snmp-server view {mib_view} {family_name} {state}")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp server view. Error:\n{str(error)}"
        )

def unconfigure_snmp_server_view(device, mib_view, family_name, state = 'excluded'):
    """ Unconfigures the snmp server view on device
        Args:
            device ('obj'): device to use
            mib_view ('str'): Name of the view
            family_name ('str'): MIB view family name
            state ('str'): mib family excluded|included
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp server view on device {device}")

    try:
        device.configure(f"no snmp-server view {mib_view} {family_name} {state}")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp server view. Error:\n{str(error)}"
        )

def configure_snmp_server_group(device,
                                group_name,
                                version,
                                auth_type,
                                mode = None,
                                acl_name = None,
                                view_name = None,
                                acl_type = None,
                                context_name = None,
                                match_type = None,
                                notify_name = None):
    """ Configures the snmp server group on device
        Args:
            device ('obj'): device to use
            group_name ('str'): name of the group
            version ('str'): v1,v2c,v3
            auth_type ('str'): auth, noauth, priv
            mode ('str'): write or read mode
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
            context_name ('str'): context name
            match_type ('str'): exact or prefix
            notify_name ('str'): notify view name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cli = f"snmp-server group {group_name} {version}"

    if auth_type is not None:
        cli = cli+' '+auth_type
    if match_type is not None:
        cli = cli+' match '+match_type
    if mode is not None and (mode == 'write'):
        cli = cli+' write '+view_name
    if mode is not None and (mode == 'read'):
        cli = cli+' read '+view_name
    if notify_name is not None:
        cli = cli+' notify '+notify_name
    if acl_name is not None:
        if acl_type is not None:
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access '+acl_name
    if context_name is not None:
        cli = cli+' context '+context_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp server group. Error:\n{str(error)}"
        )

def unconfigure_snmp_server_group(device,
                                group_name,
                                version,
                                auth_type,
                                mode = None,
                                acl_name = None,
                                view_name = None,
                                acl_type = None,
                                context_name = None,
                                match_type = None,
                                notify_name = None):
    """ unconfigures the snmp server group on device
        Args:
            device ('obj'): device to use
            group_name ('str'): name of the group
            version ('str'): v1,v2c,v3
            auth_type ('str'): auth, noauth, priv
            mode ('str'): write or read mode
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
            context_name ('str'): context name
            match_type ('str'): exact or prefix
            notify_name ('str'): notify view name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cli = f"no snmp-server group {group_name} {version}"

    if auth_type is not None:
        cli = cli+' '+auth_type
    if match_type is not None:
        cli = cli+' match '+match_type
    if mode is not None and (mode == 'write'):
        cli = cli+' write '+view_name
    if mode is not None and (mode == 'read'):
        cli = cli+' read '+view_name
    if notify_name is not None:
        cli = cli+' notify '+notify_name
    if acl_name is not None:
        if acl_type is not None:
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access '+acl_name
    if context_name is not None:
        cli = cli+' context '+context_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp server group. Error:\n{str(error)}"
        )

def configure_snmp_server_trap(device, intf=None, host_name=None, trap_type=None, version=None,
                               user_name=None, config_type=None, engine_id=None):
    """ Configures the snmp traps or informs on device
        Args:
            device ('obj'): device to use
            intf ('str',optional): trap source interface
            host_name ('str',optional): hostname/ip address of snmp-server
            trap_type ('str',optional): Traps or informs
            version ('str',optional): v1,v2c,v3
            user_name ('str',optional): Name of the user
            config_type ('str',optional): snmp trap type i.e config,link up down
            engine_id ('str',optional): remote engine id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if intf and host_name and trap_type and version and user_name and config_type:
        cli = f"snmp-server trap-source {intf}\n"
        cli += "snmp-server enable traps\n"
        cli += f"snmp-server host {host_name} {trap_type} version {version} priv {user_name} {config_type}\n"
        if trap_type == 'informs':
            cli += f"snmp-server engineID remote {host_name} {engine_id}"
    elif trap_type:
        cli = f"snmp-server enable traps {trap_type}"
    else:
        cli = f"snmp-server enable traps"

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure trap/inform config \
                on snmp-server. Error:\n{str(error)}")

def unconfigure_snmp_server_trap(device,  intf=None, host_name=None, trap_type=None, version=None,
                               user_name=None, config_type=None, engine_id=None):
    """ Unconfigures the snmp traps or informs on device
        Args:
            device ('obj'): device to use
            intf ('str',optional): trap source interface
            host_name ('str',optional): hostname/ip address of snmp-server
            trap_type ('str',optional): Traps or informs
            version ('str',optional): v1,v2c,v3
            user_name ('str',optional): Name of the user
            config_type ('str',optional): snmp trap type i.e config,link up down
            engine_id ('str',optional): remote engine id
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if intf and host_name and trap_type and version and user_name and config_type:
        cli = f"no snmp-server trap-source {intf}\n"
        cli += "no snmp-server enable traps\n"
        cli += f"no snmp-server host {host_name} {trap_type} version {version} priv {user_name} {config_type}\n"
        if trap_type == 'informs':
            cli += f"no snmp-server engineID remote {host_name} {engine_id}"
    elif trap_type:
        cli = f"no snmp-server enable traps {trap_type}"
    else:
        cli = f"no snmp-server enable traps"

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure trap or inform config \
                on snmp-server. Error:\n{str(error)}")

def configure_snmp_server_user(device,
                               user_name,
                               group_name,
                               version,
                               auth_type = None,
                               auth_algorithm = None,
                               auth_password = None,
                               priv_method = None,
                               aes_algorithm = None,
                               aes_password = None,
                               des_algorithm = None,
                               des_password = None,
                               priv_password = None,
                               acl_type = None,
                               acl_name = None):
    """ Configure the snmp user on device
        Args:
            device ('obj'): device to use
            user_name ('str'): Name of the user
            group_name ('str'): Group to which the user belongs
            version ('str'): v1,v2c,v3
            auth ('str'): authentication parameters for the user
            auth_type ('str'): md5, sha
            auth_algorithm ('str'): 256,192,128
            auth_password ('str'): authentication password for user
            priv_method ('str'): 3des,aes,des
            aes_algorithm ('str'): 128,192,256
            aes_password ('str'): privacy password for user
            des_algorithm ('str'): 128,192,256
            des_password ('str'): privacy password for user
            priv_password ('str'): privacy password for user
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cli = f"snmp-server user {user_name} {group_name} {version}"

    if auth_type and auth_password:
        cli += f" auth {auth_type}"
        if auth_algorithm:
            cli += f" {auth_algorithm}"
        cli += f" {auth_password}"

    if priv_method  is not None:
        if(priv_method == 'aes'):
            if aes_algorithm is not None and aes_password is not None:
                cli = f"{cli} priv {priv_method} {aes_algorithm} {aes_password}"
        elif(priv_method == 'des'):
            if des_algorithm is not None and des_password is not None:
                cli = f"{cli} priv {priv_method} {des_algorithm} {des_password}"

    if acl_name is not None:
        if (acl_type == 'ipv6'):
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access'+acl_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure snmp user. Error:\n{error}"
        )


def unconfigure_snmp_server_user(device,
                               user_name,
                               group_name,
                               version,
                               auth_type = None,
                               auth_algorithm = None,
                               auth_password = None,
                               priv_method = None,
                               aes_algorithm = None,
                               aes_password = None,
                               priv_password = None,
                               acl_type = None,
                               acl_name = None):
    """ Unconfigures the snmp user on device
        Args:
            device ('obj'): device to use
            user_name ('str'): Name of the user
            group_name ('str'): Group to which the user belongs
            version ('str'): v1,v2c,v3
            auth ('str'): authentication parameters for the user
            auth_type ('str'): md5, sha
            auth_algorithm ('str'): 256,192,128
            auth_password ('str'): authentication password for user
            priv_method ('str'): 3des,aes,des
            aes_algorithm ('str'): 128,192,256
            aes_password ('str'): privacy password for user
            priv_password ('str'): privacy password for user
            acl_name ('str'): name of the Standerd acl, acl list name, ipv6 named acl
            acl_type ('str'): specify IPv6 Named Access-List
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cli = f"no snmp-server user {user_name} {group_name} {version}"

    if auth_type is not None:
        cli = cli+' auth '+auth_type+' '+auth_algorithm+' '+auth_password

    if priv_method  is not None:
        if(priv_method == 'aes'):
            cli = cli+' priv '+priv_method+' '+aes_algorithm+' '+aes_password

    if acl_name is not None:
        if (acl_type == 'ipv6'):
            cli = cli+' access ipv6 '+acl_name+' '+acl_name
        else:
            cli = cli+' access'+acl_name

    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure snmp user. Error:\n{error}"
        )

def configure_snmp_host_version(device,host_name,vrf_id,version_id,community_string, udp_port = 0):
    """ Configures the snmp-server host 172.21.226.240 vrf Mgmt-vrf version 2c public on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            host_name ('str'): Host name
            vrf_id ('str') : vrf(Mgmt-vrf) is special connection,usually we have it in mgmt-interface for management port.
            version_id('str') : Snmp Version
            udp_port('int', optional) :  udp_port should be passed when enabling traps. The value can also be checked in snmp.server.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp host version on device {device}".format(device=device))

    if  udp_port == 0:
        cmd = f"snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string}"
    else:
        cmd = f"snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp host version. Error:\n{error}".format(error=e))


def unconfigure_snmp_host_version(device,host_name,vrf_id,version_id,community_string, udp_port = 0):
    """ UnConfigures the snmp-server host 172.21.226.240 vrf Mgmt-vrf version 2c public on device
        Args:
            device ('obj'): device to use
            community_string ('str'): community_string
            host_name ('str'): Host name
            vrf_id ('str') : vrf(Mgmt-vrf) is special connection,usually we have it in mgmt-interface for management port.
            version_id('str') : Snmp Version
            udp_port('int', optional) :  udp_port should be passed when enabling traps. The value can also be checked in snmp.server.
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug("Configuring snmp host version on device {device}".format(device=device))

    if  udp_port == 0:
        cmd = f"no snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string}"
    else:
        cmd = f"no snmp-server host {host_name} vrf {vrf_id} version {version_id} {community_string} udp-port {udp_port}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure snmp host version. Error:\n{error}".format(error=e))

def configure_debug_snmp_packets(device):
    """ enable snmp debugs on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp debugs on device {device}")

    try:
        device.execute("debug snmp packets")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not configure debugs on device. Error:\n{error}"
        )

def unconfigure_debug_snmp_packets(device):
    """ enable snmp debugs on device
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp debugs on device {device}")

    try:
        device.execute("undebug snmp packets")
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not unconfigure debugs on device. Error:\n{error}"
        )

def configure_snmp_server_enable_traps_power_ethernet_group(device, number, ip, snmp_v, name=None, rw='rw'):
    """ Configure snmp-server enable traps power-ethernet group
        Args:
            device ('obj'): Device object
            number ('str'): The group number
            ip ('str') : ip address
            snmp_v ('str'): snmpv1/v2c community string or snmpv3 user name
            name ('str'): snmp community string
            rw ('str'): read-write/read-only

        Returns:
                None
        Raises:
                SubCommandFailure
    """
    config = [
        f'snmp-server enable traps power-ethernet group {number}',
        f'snmp-server host {ip} {snmp_v}',
        'snmp-server enable traps power-ethernet police',
        f'snmp-server community {name} {rw}',
        'snmp-server manager'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp-server enable traps power-ethernet group on the device. Error:\n{e}")

def configure_snmp_server_manager(device):
    """
        Configures the snmp-server manager
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring snmp manager on {device}")
    try:
        device.configure("snmp-server manager")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure snmp-server manager . Error:\n{e}")

def unconfigure_snmp_server_manager(device):
    """
        Unconfigures the snmp-server manager
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp manager on {device}")
    try:
        device.configure("no snmp-server manager")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure snmp-server manager . Error:\n{e}")


def configure_logging_snmp_trap(device, sev_type):
    """
        Configures the snmp-trap logging
        Args:
            device ('obj'): device to use
            sev_type('sev_type): trap-sev or trap_type
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Configuring logging snmp-trap on {device}")
    try:
        device.configure(f"logging snmp-trap {sev_type}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging snmp-trap . Error:\n{e}")


def unconfigure_logging_snmp_trap(device, sev_type):
    """
        Configures the snmp-trap logging
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring logging snmp-trap on {device}")
    try:
        device.configure(f"no logging snmp-trap {sev_type}")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure logging snmp-trap . Error:\n{e}")


def unconfigure_snmp_server_engineid(device):
    """
        Unconfigures the snmp server engineID
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Unconfiguring snmp server engineID on {device}")
    try:
        device.configure("no snmp-server engineID local")

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure snmp server engineID . Error:\n{e}")


def enable_ietf_standard_snmp_link_traps(device):
    """
        Enable ietf standard snmp link traps
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Enable ietf standard snmp link traps {device}")
    try:
        device.configure("snmp-server trap link ietf")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not enable ietf standard snmp link traps . Error:\n{e}")


def disable_ietf_standard_snmp_link_traps(device):
    """
        Disable ietf standard snmp link traps
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.debug(f"Disable ietf standard snmp link traps on {device}")
    try:
        device.configure(f"no snmp-server trap link ietf")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not disable ietf standard snmp link traps . Error:\n{e}")

def configure_snmp_server_host_trap(device, host_name=None, trap_type=None):
    """ Configures the snmp traps or informs on device
        Args:
            device ('obj'): device to use
            host_name ('str', optional): WORD     IP/IPV6 address of SNMP notification host
                                         http://<Hostname or A.B.C.D>[:<port number>][/<uri>]  HTTP address of XML notification host
            trap_type ('str', optional): entity Allow SNMP entity traps
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f"snmp-server host {host_name} traps public {trap_type}")
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure host on snmp-server. Error:\n{str(error)}")

def unconfigure_snmp_server_enable_traps_power_ethernet_group(device, action_type_1, action_type_2, group_number):

    """unconfigure snmp server enable traps power ethernet group
       Args:
            device ('obj'): device object
            action_type_1 ('str'): logging or traps
            action_type_2 ('str'): group or police
            group_number ('int') : The group number (1-9)

       Return:
            None
       Raises:
            SubCommandFailure
    """
    config = [
        f'no snmp-server enable {action_type_1} power-ethernet {action_type_2} {group_number}'
    ]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f'Failed to unconfigure snmp server enable traps power ethernet group on {device.name}\n{e}'
        )


def configure_object_list_schema_transfer_for_bulkstat(device, type_, object_name=None, schema_name=None, transfer_name=None,
                                                       oid_value_list=None, poll_interval=None, snmp_interface=None,
                                                       format_=None, transfer_interval=None,
                                                       buffer_size=None, primary_url=None, enable=None, logging_on=None):
    """ Configure object list, schema and transfer for bulkstat
        Args:
            device ('obj'): device to use
            type_('str'): object-list  Configure an Object List
                          schema       Configure Schema definition
                          transfer     Configure Transfer Parameters
            object_name('str', optional): WORD  Name of object list, default value is None
            schema_name('str', optional): WORD  Name of the schema, default value is None
            transfer_name('str', optional): WORD  Name of bulk transfer, default value is None
            oid_value_list:('list', optional): WORD  Object name or OID list, default value is None
            poll_interval('int', optional): Periodicity for the polling of objects in this schema in
                                  Minutes. (Default value is 5 Mins), default value is None
            snmp_interface('str', optional): Specify instance as ifDescr, default value is None
            format_('str', optional): An ASCII format containing schema definitions, default value is None
            transfer_interval('int', optional): Periodicity for the transfer of bulk data in Minutes, default value is None
            buffer_size('int', optional): Bulkstat data file maximum size(Default size is 2048 bytes), default value is None
            primary_url('str', optional): WORD  URL of primary destination, default value is None
            enable('str', optional): Start Data Collection for this Configuration, default value is None
            logging_on('str', optional): Modify message logging facilities, default value is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """


    if type_ == "object-list":
        cli = [f"snmp mib bulkstat {type_} {object_name}"]
        for oid_value in oid_value_list:
            cli.append(f"add {oid_value}")

    elif type_ == "schema":
        cli =[f"snmp mib bulkstat {type_} {schema_name}",
        f"object-list {object_name}",
        f"poll-interval {poll_interval}",
        f"instance wild interface {snmp_interface}"]

    elif type_ == "transfer":
        cli =[f"snmp mib bulkstat {type_} {transfer_name}",
        f"schema {schema_name}",
        f"format {format_}",
        f"transfer-interval {transfer_interval}",
        f"buffer-size {buffer_size}",
        f"url primary {primary_url}",
        f"{enable}",
        f"{logging_on}"]
    try:
        device.configure(cli)
    except SubCommandFailure as error:
        raise SubCommandFailure(
            f"Could not  configure Object list Schema Transfer for Bulkstat. Error:\n{error}"
        )


def configure_snmp_server_host(device, host_ip, version, community_string):
    """ Configures the snmp-server host or informs on device
        Args:
            device ('obj'): device to use
            host_ip ('str'): WORD     IP address of the SNMP notification host
            community_string ('str'): Community string
            version ('str', optional): SNMP version
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"snmp-server host {host_ip} {version} {community_string}"
    try:
        device.configure(cmd)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not configure host on snmp-server. Error:\n{str(error)}")


def unconfigure_snmp_server_host(device, host_ip, version, community_string):
    """ Unconfigures the snmp-server host
        Args:
            device ('obj'): device to use
            host_ip ('str'): IP address of the SNMP notification host
            version ('str'): SNMP version
            community_string ('str'): Community string
        Returns:
           None
        Raises:
            SubCommandFailure
    """
    cmd = f"no snmp-server host {host_ip} {version} {community_string}"
    try:
        device.configure(cmd)
    except SubCommandFailure as error:
        raise SubCommandFailure(f"Could not unconfigure SNMP server host. Error:\n{str(error)}")

