'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def configure_no_boot_manual(device):
    """ no boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not remove boot manual config on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_boot_manual(device):
    """ boot manual
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('boot manual')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config boot manual on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_ip_local_pool(device,name,start,end):
    """ ip local pool
        Args:
            device (`obj`): Device object
            name ('str') : pool name
            start ('str') : pool start ip
            end ('str') : pool end ip
        
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure(f'ip local pool {name} {start} {end}')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure local pool on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )


def configure_dope_wrsp(device, asic, core, idx, hi_value, lo_value):
    """ Configures wrsp parameters in dope shell
        Args:
            device (`obj`): Device object
            asic ('int'): Asic number to be configured
            core ('int'): Core number to be configured
            idx ('int'): IDX number to be configured
            hi_value ('str'): WRSP Nfl High GlobalTime value
            lo_value ('str'): WRSP Nfl Low GlobalTime value

        Returns:
            None

        Raises:
            SubCommandFailure
    """

    try:
        with device.dope_shell() as shell:
            shell.execute([f'asic {asic}',
                    f'core {core}',
                    f'wrsp NflGlobalTime globalTimeHi idx {idx} value {hi_value}',
                    f'wrsp NflGlobalTime globalTimeLo idx {idx} value {lo_value}'
                    ])

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure wrsp parameters in dope shell in {device}. Error:\n{e}"
                        )


def configure_bba_group(device,name,vt_number):
    """ bba-group
        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cli = []
    cli.append(f"bba-group pppoe {name}")
    cli.append(f"virtual-template {vt_number}")
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config bba-group on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_bba_group(device,name,vt_number):
    """ bba-group
        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cli = []
    cli.append(f"no bba-group pppoe {name}")

    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfig bba-group on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_platform_qos_port_channel_aggregate(device,portchannel_number):

    """ platform qos port-channel-aggregate <portchannel_number>
        Args:
            device (`obj`): Device object
            portchannel_number ('str') : Port-channel number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"platform qos port-channel-aggregate {portchannel_number}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure platform qos port-channel-aggregate on \
            {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def unconfigure_platform_qos_port_channel_aggregate(device,portchannel_number):

    """ platform qos port-channel-aggregate <portchannel_number>
        Args:
            device (`obj`): Device object
            portchannel_number ('str') : Port-channel number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no platform qos port-channel-aggregate {portchannel_number}"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure platform qos port-channel-aggregate on \
            {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_call_admission(device, limit, cpu_limit, session_lifetime, per_session_charge):

    """Common funtion to configure call admission new model
        Args:
            device ('obj'): device to use
            limit('int'): call admission limit value 
            cpu_limit('int'):call admission cpu limit value
            session_lifetime('int'): call admission session lifetime value
            per_session_charge('int'): call admission per session charge value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("configuring call admission ")
    cli = [
        "call admission new-model",
        f"call admission limit {limit}",
        f"call admission cpu-limit {cpu_limit}",
        f"call admission pppoe {session_lifetime} {per_session_charge}",
        f"call admission vpdn {per_session_charge} {session_lifetime}"
    ]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not config call admission on {device}. Error:\n{e}")

def unconfigure_call_admission(device, limit, cpu_limit, session_lifetime, per_session_charge):

    """Common funtion to unconfigure call admission new model
        Args:
            device ('obj'): device to use
            limit('int'): call admission limit value
            cpu_limit('int'): call admission cpu limit value
            session_lifetime('int'): call admission session lifetime value
            per_session_charge('int'): call admission per session charge value
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("unconfiguring call admission")
    cli = [
        "no call admission new-model",
        f"no call admission limit {limit}",
        f"no call admission cpu-limit {cpu_limit}",
        f"no call admission pppoe {session_lifetime} {per_session_charge}",
        f"no call admission vpdn {per_session_charge} {session_lifetime}"
    ]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfig call admission on {device}. Error:\n{e}")

def configure_broadband_aaa(device, server_name, interval):

    """ Configure aaa configuration for broadband 
        Args:
            device (`obj`): Device object
            server_name (`str`): aaa group server name
            interval (`str`): Accounting time interval
        Return:
            None
        Raise:
            SubCommandFailure
    """

    cli = [
        f"aaa authentication ppp default group {server_name}",
        f"aaa authorization network default group {server_name}",
        f"aaa authorization subscriber-service default group {server_name}",
        f"aaa accounting network default start-stop group {server_name}",
        f"aaa accounting update periodic {interval}"
    ]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure aaa on {device}. Error:\n{e}")

def unconfigure_broadband_aaa(device, server_name, interval):

    """ Unconfigure aaa configuration for broadband 
        Args:
            device (`obj`): Device object
            server_name (`str`): aaa group server name
            interval (`str`): Accounting time interval
        Return:
            None
        Raise:
            SubCommandFailure
    """

    cli = [
        f"no aaa authentication ppp default group {server_name}",
        f"no aaa authorization network default group {server_name}",
        f"no aaa authorization subscriber-service default group {server_name}",
        f"no aaa accounting network default start-stop group {server_name}",
        f"no aaa accounting update periodic {interval}"
    ]
    try:
        device.configure(cli)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not unconfig aaa on {device}. Error:\n{e}")


