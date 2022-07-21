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

