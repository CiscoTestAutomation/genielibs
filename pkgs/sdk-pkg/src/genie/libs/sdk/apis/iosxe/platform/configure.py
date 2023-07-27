'''IOSXE execute functions for platform'''

# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

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


def unconfigure_ip_local_pool(device,name):
    """ ip local pool
        Args:
            device ('obj'): Device object
            name ('str') : pool name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no ip local pool {name}'
    try:
        device.configure(cmd)
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


def configure_bba_group(device,name,vt_number, service_profile_name=None):
    """ bba-group
        Args:
            device (`obj`): Device object
            name (`str`): bba-group name
            vt_number (`str`): virtual-template interface number
            service_profile_name('str', optional): service profile name
        Returns:
            None
        Raises:
            SubCommandFailure:Could not config bba-group on device
    """

    cli = []
    cli.append(f"bba-group pppoe {name}")
    cli.append(f"virtual-template {vt_number}")
    if service_profile_name:
        cli.append(f"service profile {service_profile_name}")
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

def configure_no_boot_system_switch_all(device):
    """ no boot system switch all
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    try:
        device.configure('no boot system switch all')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config no boot system on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_boot_system_switch_all_flash(device, image):
    """ boot system switch all flash
        Args:
            device ('obj'): Device object
            image ('str'): Image name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"boot system switch all flash:{image}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not config boot system on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_diagonistics_monitor_switch(device, switch_num, test_name, time, millisec, days):
    """ diagonistics monitor switch
        Args:
            device ('obj'): Device object
            switch_num('int'): switch number
            test_name('str'): diagnostic_test_name
            time('str'): time in hh:mm:ss
            millisec('int'): milli seconds
            days('int'): test_days
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"diagnostic monitor interval switch {switch_num} test {test_name} {time} {millisec} {days}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure diagnostic monitor interval switch {device}"
                .format(device=device, e=e)
        )

def unconfigure_diagonistics_monitor_switch(device, switch_num, test_name, time, millisec, days):
    """ diagonistics monitor switch
        Args:
            device ('obj'): Device object
            switch_num('int'): switch number
            test_name('str'): diagnostic_test_name
            time('str'): time in hh:mm:ss
            millisec('int'): milli seconds
            days('int'): test_days
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"no diagnostic monitor interval switch {switch_num} test {test_name} {time} {millisec} {days}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not Unconfigure diagnostic monitor interval switch  {device}"
                .format(device=device, e=e)
        )

def configure_ipxe_timeout(device, timeout, switch_number):
    """ Configure ipxe timeout for switch
        Args:
            device ('obj'): Device object
            timeout ('int'): timeout value
            switch_number ('int'): switch number
        Raises:
            SubCommandFailure
    """

    cmd = f'boot ipxe timeout {timeout} switch {switch_number}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipxe timeout on device {device}. Error:\n{e}"
            )

def configure_ipxe_forever(device, switch_number):
    """ Configure ipxe forever for switch
        Args:
            device ('obj'): Device object
            switch_number ('int'): switch number
        Raises:
            SubCommandFailure
    """

    cmd = f'boot ipxe forever switch {switch_number}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipxe forever on device {device}. Error:\n{e}"
            )

def hw_module_beacon_slot_on_off(device, slot, operation):
    """ ON/OFF beacon slot
        Args:
            device ('obj'): Device object
            slot('int'): Switch number
            operation('str'): ON/OFF

    """

    cmd = "hw-module beacon slot {} {}".format(slot, operation)
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure('Failed to switch {} the beacon slot :'.format(operation))

def stack_ports_enable_disable(device, switch_num, stack_port, operation):
    """ Enable/Disable the stack port
        Args:
            device (`obj`): Device object
            switch_num ('int'): Switch number
            stack_port ('int'): Stack port number
            operation('str'): Enable/Disable
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to continue\?\[y\/n\]\?\s\[yes\]',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )

    cmd = f'switch {switch_num} stack port {stack_port} {operation}'
    try:
        device.execute(cmd,reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure('Failed to {} stack port {} on switch{} :'.format(operation,stack_port,switch_num))

def configure_archive_logging(device):
    """ Configure archive logging enable for switch
        Args:
            device ('obj'): Device object
        Raises:
            SubCommandFailure
    """

    cmd = [
        "archive",
        "log config",
        "logging enable",
        "hidekeys",
        "notify syslog"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive logging enable on device {device}. Error:\n{e}"
            )

def unconfigure_archive_logging(device):
    """ Unconfigure archive logging enable for switch
        Args:
            device ('obj'): Device object
        Raises:
            SubCommandFailure
    """

    cmd = 'no archive'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure ipxe forever on device {device}. Error:\n{e}"
            )

def configure_switch_provision(device,switch_number,model):
    """ Configure switch provision for switch
        Args:
            device ('obj'): Device object
            switch_number('int'): switch number
            model ('str'): switch model
        Raises:
            SubCommandFailure
    """

    cmd = f'switch {switch_number} provision {model}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure switch provision on device {device}. Error:\n{e}"
            )

def unconfigure_switch_provision(device,switch_number):
    """ Unconfigure switch provision for switch
        Args:
            device ('obj'): Device object
            switch_number('int'): switch number
        Raises:
            SubCommandFailure
    """

    cmd = f'no switch {switch_number} provision'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure switch provision on device {device}. Error:\n{e}"
            )

def configure_interface_macro(device,interface,macro_name):
    """ Apply macro on a interface for switch
        Args:
            device ('obj'): Device object
            interface('str'):interface to configure
            ex.)
                interface = 'tenGigabitEthernet0/4/0'
            macro_name ('str'): macro name
        Raises:
            SubCommandFailure
    """

    cmd =[]
    cmd.append("interface {}".format(interface))
    cmd.append("macro apply {}".format(macro_name))
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to apply macro on a interface on device {device}. Error:\n{e}"
            )

def configure_service_timestamps(device, msg_type="", timestamp_type="", datetime_subcmd="" ):
    """ Configure service timestamps for switch
        Args:
            device ('obj'): Device object
            msg_type ('str'): timestamp message type log/debug
            timestamp_type ('str'): timestap type
            ex:)
                datetime  Timestamp with date and time
                uptime    Timestamp with system uptime
            datetime_subcmd ('str'): timestamp type for datetime

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if msg_type:
        if timestamp_type:
            if timestamp_type.lower() == "uptime":
                cmd.append(f'service timestamps {msg_type} uptime')
            if timestamp_type.lower() == "datetime":
                if datetime_subcmd:
                    cmd.append(f'service timestamps {msg_type} datetime {datetime_subcmd}')
                else:
                    cmd.append(f'service timestamps {msg_type} datetime')
        else:
            cmd.append(f'service timestamps {msg_type}')
    else:
        cmd.append('service timestamps')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to Configure service timestamps on {device}. Error:\n{e}"
            )

def unconfigure_service_timestamps(device, msg_type=""):
    """ Unconfigure service timestamps for switch
        Args:
            device ('obj'): Device object
            msg_type ('str'): timestamp message type log/debug

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if msg_type:
        cmd.append(f'no service timestamps {msg_type}')
    else:
        cmd.append('no service timestamps')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure service timestamps on {device}. Error:\n{e}"
            )

def copy_startup_config_to_flash_memory(device, timeout):
    """ Copying startup config to flash memory

        Args:
            device (`obj`): Device object
            timeout (`str`): timeout in seconds

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r".*Destination filename.*",
                action="sendline()",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    cmd = "copy startup-config flash:startup_config_backup"
    try:
        device.execute(cmd,reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not copy saved configuration on {device}. Error:\n{e}")

def copy_startup_config_to_tftp(device, host, file, timeout=30):
    """ Copy startup configuration to tftp location

        Args:
            device ('obj'): Device object to modify configuration
            host ('str'): tftp host ip address
            file('str'): configuration file path and file name
            ex:)
                /tftpboot/startup_config
            timeout('int', Optional): timeout in seconds for configuration file load to device(Default is 30 seconds)

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("copy startup configuration to tftp")
    dialog = Dialog([
        Statement(pattern=r'.*Address or name of remote host.*',
            action='sendline()',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*Destination filename',
            action='sendline()',
            loop_continue=True,
            continue_timer=False)
        ])

    cmd = f"copy startup-config tftp://{host}/{file}"
    try:
        device.execute(cmd,reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not copy startup configuration on tftp. Error:\n{e}")

def copy_running_config_to_tftp(device, host, file, timeout=30):
    """ Copy running configuration to tftp location

        Args:
            device ('obj'): Device object to modify configuration
            host ('str'): tftp host ip address
            file('str'): configuration file path and file name
            ex:)
                /tftpboot/running_config
            timeout('int', Optional): timeout in seconds for configuration file load to device(Default is 30 seconds)

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    log.debug("copy running configuration to tftp")
    dialog = Dialog([
        Statement(pattern=r'.*Address or name of remote host.*',
            action='sendline()',
            loop_continue=True,
            continue_timer=False),
        Statement(pattern=r'.*Destination filename',
            action='sendline()',
            loop_continue=True,
            continue_timer=False)
        ])

    cmd = f"copy running-config tftp://{host}/{file}"
    try:
        device.execute(cmd,reply=dialog, timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not copy running configuration on tftp. Error:\n{e}")

def configure_macro_auto_sticky(device):
    """ Configure macro auto sticky on this device

    Args:
        device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = 'macro auto sticky'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure macro auto sticky on this device. Error:\n{e}")

def unconfigure_macro_auto_sticky(device):
    """ Unconfigure macro auto sticky on this device

    Args:
        device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = 'no macro auto sticky'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure macro auto sticky on this device. Error:\n{e}")

def configure_device_classifier(device, dc_option="", dc_option_name=""):
    """ Configure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'): device classifier option
        ex:)
            condition    Define device classifier condition
            device-type  Define device type
        dc_option_name ('str'): Name of device classifier type
        ex:)
            WORD  Condition name
            WORD  Device type name

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if dc_option:
        cmd = f'device classifier {dc_option} {dc_option_name}'
    else:
        cmd = 'device classifier'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure classifier on this device. Error:\n{e}")

def unconfigure_device_classifier(device, dc_option="", dc_option_name=""):
    """ Unconfigure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'): device classifier option
        ex:)
            condition    Define device classifier condition
            device-type  Define device type
        dc_option_name ('str'): Name of device classifier type
        ex:)
            WORD  Condition name
            WORD  Device type name

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if dc_option:
        cmd = f'no device classifier {dc_option} {dc_option_name}'
    else:
        cmd = 'no device classifier'

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure classifier on this device. Error:\n{e}")


def configure_virtual_service_vnic_gateway_guest_ip_address(device, interface_id, ip, ip_mask, virtual_service, guest_ip):
    """ configure virtual service vnic gateway guest ip address

    Args:
        device ('obj'): device to use
        interface_id ('str'): The interface id
        ip ('str'): ip address
        ip_mask ('str'): ip mask
        virtual_service ('str'): The virtual service
        guest_ip ('str'): the guest ip address

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface_id}",
        f"ip address {ip} {ip_mask}",
        "no shut",
        f"virtual-service {virtual_service}",
        f"vnic gateway {interface_id}",
        f"guest ip address {guest_ip}",
        "exit",
        "activate"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure no system ignore startupconfig switch all on this device. Error:\n{e}")


def configure_snmp_mib_bulkstat(device, object_name, oid, schema_name, poll_interval, snmp_interface, transfer_name, transfer_number, url, retry_number, retain_number):
    """ configure snmp mib bulkstat
    Args:
        device ('obj'): device to use
        object_name ('str'): The name of the object
        oid ('str'): object name to be added
        schema_name ('str'): The name of the schema
        poll_interval ('int'): The poll interval value
        snmp_interface ('str'): The snmp interface
        transfer_name ('str'): bulkstat transfer name
        transfer_number ('int'): bulkstat transfer number
        url ('str'): url primary
        retry_number ('int'): The retry nymber
        retain_number ('int'): The retain number

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"snmp mib bulkstat object-list {object_name}",
        f"add {oid}",
        "exit",
        f"snmp mib bulkstat schema {schema_name}",
        f"object-list {object_name}",
        f"poll-interval {poll_interval}",
        f"instance wild interface {snmp_interface}",
        "exit",
        f"snmp mib bulkstat transfer {transfer_name}",
        f"schema {schema_name}",
        "format schemaASCII",
        f"transfer-interval {transfer_number}",
        f"url primary {url}",
        f"retry {retry_number}",
        f"retain {retain_number}",
        "enable"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp mib bulkstat on this device. Error:\n{e}")


def configure_bulkstat_profile(device, name):
    """ configure bulkstat profile
    Args:
        device ('obj'): device to use
        name ('str') : profile name to be added
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"bulkstat profile {name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure bulkstat profile on this device. Error:\n{e}")

def unconfigure_bulkstat_profile(device, name):
    """ unconfigure bulkstat profile
    Args:
        device ('obj'): device to use
        name ('str') : profile name to be removed

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"no bulkstat profile {name}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure bulkstat profile on this device. Error:\n{e}")
    try:
        device.configure('no system ignore startupconfig switch all')
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure system ignore startupconfig switch all on this device. Error:\n{e}")

def configure_hw_switch_switch_logging_onboard_voltage(device, switch_number):
    """ configures hw-switch switch <#> logging onboard voltage
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"hw-switch switch {switch_number} logging onboard voltage"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure hw-switch switch {switch_number} logging onboard voltage on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def unconfigure_hw_switch_switch_logging_onboard_voltage(device, switch_number):
    """ unconfigures hw-switch switch <#> logging onboard voltage
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"no hw-switch switch {switch_number} logging onboard voltage"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure hw-switch switch {switch_number} logging onboard voltage on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )


def configure_hw_switch_switch_logging_onboard_environment(device, switch_number):
    """ configures hw-switch switch <#> logging onboard environment
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"hw-switch switch {switch_number} logging onboard environment"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure hw-switch switch {switch_number} logging onboard environment on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def unconfigure_hw_switch_switch_logging_onboard_environment(device, switch_number):
    """ unconfigures hw-switch switch <#> logging onboard environment
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"no hw-switch switch {switch_number} logging onboard environment"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure hw-switch switch {switch_number} logging onboard environment on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def configure_hw_switch_switch_logging_onboard_temperature(device, switch_number):
    """ configures hw-switch switch <#> logging onboard temperature
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"hw-switch switch {switch_number} logging onboard temperature"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure hw-switch switch {switch_number} logging onboard temperature on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def unconfigure_hw_switch_switch_logging_onboard_temperature(device, switch_number):
    """ unconfigures hw-switch switch <#> logging onboard temperature
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    cmd = f"no hw-switch switch {switch_number} logging onboard temperature"

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to unconfigure hw-switch switch {switch_number} logging onboard temperature on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def configure_clear_logging_onboard_switch_temperature(device, switch_number):
    """ unconfigures clear  logging  onboard  switch  temperature
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Clear logging.*",
                action="sendline(y)",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    cmd = "clear  logging  onboard  switch {switch_number} temperature".format(switch_number=switch_number)
    try:
        device.execute(cmd,reply=dialog)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure clear  logging  onboard  switch {switch_number} temperature on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def configure_clear_logging_onboard_switch_voltage(device, switch_number):
    """ unconfigures clear  logging  onboard  switch  voltage
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Clear logging.*",
                action="sendline(y)",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    cmd = "clear  logging  onboard  switch {switch_number} voltage".format(switch_number=switch_number)
    try:
        device.execute(cmd,reply=dialog)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure clear  logging  onboard  switch {switch_number} voltage on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )


def configure_clear_logging_onboard_switch_environment(device, switch_number):
    """ unconfigures clear  logging  onboard  switch  Environment
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number to configure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*Clear logging.*",
                action="sendline(y)",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    cmd = "clear  logging  onboard  switch {switch_number} environment".format(switch_number=switch_number)
    try:
        device.execute(cmd,reply=dialog)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure clear  logging  onboard  switch {switch_number} environment on the device {dev}. Error:\n{error}".format(
                dev=device.name,
                switch_number=switch_number,
                error=e,
            )
        )

def configure_system_ignore_startupconfig_switch_all(device, switch=True, switch_number=None):
    """ Configures the system ignore startup configuration on the switch
        Example: system ignore startupconfig switch all

        Args:
            device('obj'): device to configure on
            switch('boolean', optional): True for 9300 device, False for 9400 or above
            switch_number('int', optional): switch member number need to be configured

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    if switch==True and switch_number==None:
        log.info(f"Configuring system ignore startup config on {device.name}")
        config = 'system ignore startupconfig switch all'
    elif switch==True and switch_number:
        log.info(f"Configuring system ignore startup config on switch {switch_number} on {device.name}")
        config = f'system ignore startupconfig switch {switch_number}'
    else:
        log.info(f"Configuring system ignore startup config on {device.name}")
        config = 'system ignore startupconfig'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not configure system ignore startup configuration on device {device.name}. Error:\n{e}")

def unconfigure_system_ignore_startupconfig_switch_all(device, switch=True, switch_number=None):
    """ Unconfigures the system ignore startup configuration on the switch
        Example: no system ignore startupconfig switch all

        Args:
            device('obj'): device to configure on
            switch('boolean', optional): True for 9300 device, False for 9400 or above
            switch_number('int', optional): switch member number need to be configured

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    if switch==True and switch_number==None:
        log.info(f"Unconfiguring system ignore startup config on {device.name}")
        config = 'no system ignore startupconfig switch all'
    elif switch== True and switch_number:
        log.info(f"Unconfiguring system ignore startup config on switch {switch_number} on {device.name}")
        config = f'no system ignore startupconfig switch {switch_number}'
    else:
        log.info(f"Unconfiguring system ignore startup config on {device.name}")
        config = 'no system ignore startupconfig'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not unconfigure system ignore startup configuration on device {device.name}. Error:\n{e}")

def configure_boot_system_switch_all_flash(device, destination):
    """ Configures the boot variable on all switches in the stack
        Example : boot system switch all flash:ctest.bin

        Args:
            device ('obj'): device to use
            destination('str'): destination (e.g. test.bin)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring boot system variable on flash on {device.name}")
    output = device.execute("show switch")
    if "Invalid input" not in output:
        configs = f"boot system switch all flash:{destination}"
    else:
        configs = f"boot system flash:{destination}"
    try:
        device.configure(configs)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Failed to configure boot system variable on device {device.name}. Error:\n{e}")

def unconfigure_boot_system(device):
    """ Unconfigures the boot variable from the system
        Example : no boot system

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring boot system variable on {device.name}")
    config = "no boot system"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Failed to unconfigure boot system variable on device {device.name}. Error:\n{e}")

def configure_system_disable_password_recovery_switch_all(device, switch=True, switch_number=None):
    """ Disables password recovery on the switch
        Example: system disable password recovery switch all

        Args:
            device('obj'): device to configure on
            switch('boolean', optional): True for 9300 device, False for 9400 or above
            switch_number('int', optional): switch member number need to be configured

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    if switch==True and switch_number==None:
        log.info(f"Disable password recovery switch all on {device.name}")
        config = 'system disable password recovery switch all'
    elif switch==True and switch_number:
        log.info(f"Disable password recovery switch {switch_number} on {device.name}")
        config = f'system disable password recovery switch {switch_number}'
    else:
        log.info(f"Disable password recovery on {device.name}")
        config = 'system disable password recovery'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not disable password recovery switch all on device {device.name}. Error:\n{e}")

def unconfigure_system_disable_password_recovery_switch_all(device, switch=True, switch_number=None):
    """ Enables password recovery on the switch
        Example: no system disable password recovery switch all

        Args:
            device('obj'): device to configure on
            switch('boolean', optional): True for 9300 device, False for 9400 or above
            switch_number('int', optional): switch member number need to be configured
        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    if switch==True and switch_number==None:
        log.info(f"Enables password recovery switch all on {device.name}")
        config = 'no system disable password recovery switch all'
    elif switch==True and switch_number:
        log.info(f"Enable password recovery switch {switch_number} on {device.name}")
        config = f'no system disable password recovery switch {switch_number}'
    else:
        log.info(f"Enable password recovery on {device.name}")
        config = 'no system disable password recovery'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not enable password recovery switch all on device {device.name}. Error:\n{e}")

def configure_snmp_server_contact(device, name):
    """ Configures contact for snmp-server
        Example : snmp-server contact Testname

        Args:
            device ('obj'): device to use
            name ('str'): identification of the contact person

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config = f"snmp-server contact {name}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure contact {name} on the device {device.name}. Error:\n{e}")

def unconfigure_snmp_server_contact(device):
    """ Unconfigures contact for snmp-server
        Example: no snmp-server contact

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    config = "no snmp-server contact"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure snmp-server contact on the device {device.name}. Error:\n{e}")

def configure_snmp_server_location(device, location):
    """ Configures snmp-server location
        Example : snmp-server location Regression Test Lab

        Args:
            device ('obj'): device to use
            location ('str'): system location information (e.g. Cisco Kanata, Regression Test Lab)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring snmp-server location on {device.name}")
    config = f"snmp-server location {location}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp-server location on device {device.name}. Error:\n{e}")

def unconfigure_snmp_server_location(device):
    """ Unconfigures snmp-server location
        Example : no snmp-server location

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring snmp-server location on {device.name}")
    config = "no snmp-server location"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure snmp-server location on device {device.name}. Error:\n{e}")

def configure_hw_switch_logging_onboard(device, switch):
    """ Configures OBFL on the specified switch
        Example : hw-switch switch 1 logging onboard

        Args:
            device ('obj'): device to use
            switch ('int'): switch number (Range 1-16)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring OBFL on switch {switch} on {device.name}")
    config = f"hw-switch switch {switch} logging onboard"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure OBFL on switch {switch} on device {device.name}. Error:\n{e}")

def unconfigure_hw_switch_logging_onboard(device, switch):
    """ Unconfigures OBFL on the specified switch
        Example : no hw-switch switch 1 logging onboard

        Args:
            device ('obj'): device to use
            switch ('int'): switch number (Range 1-16)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring OBFL on switch {switch} on {device.name}")
    config = f"no hw-switch switch {switch} logging onboard"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure OBFL on switch {switch} on device {device.name}. Error:\n{e}")

def configure_ip_tftp_blocksize(device, size):
    """ Specifies the size of TFTP blocks
        Example : ip tftp blocksize 2000

        Args:
            device ('obj'): device to use
            size ('int'): block size value ranging from 512 to 8192 bytes

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring tftp blocksize {size} on {device.name}")
    config = f"ip tftp blocksize {size}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure tftp blocksize {size} on device {device.name}. Error:\n{e}")

def unconfigure_ip_tftp_blocksize(device):
    """ Resets the TFTP blocksize to default
        Example : no ip tftp blocksize

        Args:
            device ('obj'): device to use

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring tftp blocksize on {device.name}")
    config = "no ip tftp blocksize"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure tftp blocksize on device {device.name}. Error:\n{e}")

def configure_enable_http_server(device):
    """Configure ip http server
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("ip http server")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to enable http server "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully enabled http server for {}".format(device.name))

def configure_set_clock_calendar(device):
    """Configure clock calendar-valid
    Args:
        device (obj): Device object
    Returns:
            None
    Raises:
            SubCommandFailure
    """

    try:
        device.configure("clock calendar-valid")

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to set valid clock calendar "
            "on device {device} "
            "Error: {e}".format(
                device=device.name,
                e=str(e)
            )
        ) from e

    else:
        log.info("Successfully set clock calendar for {}".format(device.name))

def configure_clock_timezone(device, timezone_name, hours_offset, minutes_offset):
    """ Configure Clock Timezone
        Args:
            device ('obj'): Device object
            timezone_name('str'): name of time zone
            hours_offset('int'): Hours offset from UTC
            minutes_offset('int'): Minutes offset from UTC
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"clock timezone {timezone_name} {hours_offset} {minutes_offset}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure clock timezone on {device}"
                .format(device=device, e=e)
        )

def configure_virtual_service(device, name):
    """ Configures virtual-service name
        Example : virtual-service UTD

        Args:
            device ('obj'): device to use
            name ('str'): Virtual service name (up to 63 characters)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring virtual-service {name} on {device.name}")
    config = f"virtual-service {name}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure virtual-service {name} on device {device.name}. Error:\n{e}")

def unconfigure_virtual_service(device, name):
    """ Unconfigures virtual-service name
        Example : no virtual-service UTD

        Args:
            device ('obj'): device to use
            name ('str'): Virtual service name (up to 63 characters)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring virtual-service {name} on {device.name}")
    config = f"no virtual-service {name}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure virtual-service {name} on device {device.name}. Error:\n{e}")

def unconfigure_virtual_service_activate(device, name):
    """ Deactivates virtual-service
        Example : virtual-service UTD
                  no activate

        Args:
            device ('obj'): device to use
            name ('str'): Virtual service name (up to 63 characters)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Deactivating virtual-service {name} on {device.name}")
    config = [
        f'virtual-service {name}',
        f'no activate'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to deactivates virtual-service {name} on device {device.name}. Error:\n{e}")

def configure_interface_VirtualPortGroup(device, number):
    """ Configures interface VirtualPortGroup
        Example : interface VirtualPortGroup 1

        Args:
            device ('obj'): device to use
            number ('int'): VirtualPortGroup interface number (Range: 0-31)

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring interface VirtualPortGroup {number} on {device.name}")
    config = f'interface VirtualPortGroup {number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure interface VirtualPortGroup {number} on device {device.name}. Error:\n{e}")

def unconfigure_interface_VirtualPortGroup(device, number):
    """ Unconfigures interface VirtualPortGroup
        Example : no interface VirtualPortGroup 1

        Args:
            device ('obj'): device to use
            name ('str'): name of the interface

        Returns:
            None

        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring VirtualPortGroup interface {number} on {device.name}")
    config = f'no interface VirtualPortGroup {number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure interface VirtualPortGroup {number} on device {device.name}. Error:\n{e}")

def configure_source_template(device, template_name, source_template):
    """ Configure source template

    Args:
        device ('obj'): device to use
        template_name ('str'): Select a template to configure
        source_template ('str'): Template name to source configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'template {template_name}')
    cmd.append(f'source template {source_template}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure source template on this device. Error:\n{e}")

def unconfigure_source_template_global(device, template_name, source_template):
    """ unconfigure source template

    Args:
        device ('obj'): device to use
        template_name ('str'): Select a template to configure
        source_template ('str'): Template name to source configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'template {template_name}')
    cmd.append(f'no source template {source_template}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure source template on this device. Error:\n{e}")


def unconfigure_global_source_template(device, source_template):
    """ unconfigure source template globally

    Args:
        device ('obj'): device to use
        source_template ('str'): Template name to source configs
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no source template {source_template}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure source template on this device. Error:\n{e}")


def configure_commands_to_template(device, template_name, cmd_to_add):
    """ Configure commands to a template

    Args:
        device ('obj'): device to use
        template_name ('str'): Select a template to configure
        cmd_to_add ('str'): Template configuration commands
        ex:)
            aaa              Authentication, Authorization and Accounting.
            access-session   Access Session specific Interface Configuration Commands
            authentication   Auth Manager Interface Configuration Commands
            carrier-delay    Specify delay for interface transitions
            cts              Configure Cisco Trusted Security
            default          Set a command to its defaults
            description      Interface specific description
            device-tracking  Device tracking commands on the interface
            dialer           Dial-on-demand routing (DDR) commands
            dialer-group     Assign interface to dialer-list
            dot1x            Interface Config Commands for IEEE 802.1X
            ethernet         Ethernet service
            exit             Exit from template configuration mode
            hold-queue       Set hold queue depth
            ip               IP template config
            ip               Interface Internet Protocol config commands
            ipv6             IPv6 interface commands
            keepalive        Enable keepalive
            load-interval    Specify interval for load calculation for an interface
            loopdetect       Configure loopdetect feature setting
            mab              MAC Authentication Bypass Interface Config Commands
            negate           Negate the following commands on a template
            no               Negate a command or set its defaults
            peer             Peer parameters for point to point interfaces
            ppp              Point-to-Point Protocol
            remark           template description comment
            service-policy   Configure CPL Service Policy
            source           Get config from another source
            spanning-tree    Spanning Tree Subsystem
            storm-control    storm configuration
            subscriber       Subscriber inactivity timeout value.
            switchport       Set switching mode characteristics
            trust            Set trust value for the interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'template {template_name}')
    cmd.append(f'{cmd_to_add}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure commands to a template on this device. Error:\n{e}")

def unconfigure_commands_from_template(device, template_name, cmd_to_add):
    """ Unconfigure commands from a template

    Args:
        device ('obj'): device to use
        template_name ('str'): Select a template to configure
        cmd_to_add ('str'): Template configuration commands
        ex:)
            aaa              Authentication, Authorization and Accounting.
            access-session   Access Session specific Interface Configuration Commands
            authentication   Auth Manager Interface Configuration Commands
            carrier-delay    Specify delay for interface transitions
            cts              Configure Cisco Trusted Security
            default          Set a command to its defaults
            description      Interface specific description
            device-tracking  Device tracking commands on the interface
            dialer           Dial-on-demand routing (DDR) commands
            dialer-group     Assign interface to dialer-list
            dot1x            Interface Config Commands for IEEE 802.1X
            ethernet         Ethernet service
            exit             Exit from template configuration mode
            hold-queue       Set hold queue depth
            ip               IP template config
            ip               Interface Internet Protocol config commands
            ipv6             IPv6 interface commands
            keepalive        Enable keepalive
            load-interval    Specify interval for load calculation for an interface
            loopdetect       Configure loopdetect feature setting
            mab              MAC Authentication Bypass Interface Config Commands
            negate           Negate the following commands on a template
            no               Negate a command or set its defaults
            peer             Peer parameters for point to point interfaces
            ppp              Point-to-Point Protocol
            remark           template description comment
            service-policy   Configure CPL Service Policy
            source           Get config from another source
            spanning-tree    Spanning Tree Subsystem
            storm-control    storm configuration
            subscriber       Subscriber inactivity timeout value.
            switchport       Set switching mode characteristics
            trust            Set trust value for the interface
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append(f'template {template_name}')
    cmd.append(f'no {cmd_to_add}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure commands from a template on this device. Error:\n{e}")

def request_platform_software_package_clean(device, switch_detail, clean_option, file_path):
    """ Perform request platform software package clean switch
        Args:
            device ('obj'): Device object
            switch_detail ('str'): Switch id, or 'all' for all switches
            clean_option ('str'): clean option file/pattern
            file_path ('str'):  file path
        Returns:
                None
        Raises:
                SubCommandFailure
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to proceed\? \[y\/n\]',
                action='sendline(Y)',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    cmd = f'request platform software package clean switch {switch_detail} {clean_option} {file_path}'
    try:
        device.execute(cmd,reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to perform request platform software package clean switch on the device. Error:\n{e}")

def configure_macro_global_apply(device, macro_name):
    """
        Configure macro global apply on device
        cli: macro global apply
        Args:
            device ('obj'): Device object
            macro_name ('str'): macro name
        Raises:
            SubCommandFailure
        Returns:
            None
    Returns:
        None
    """
    cmd = f"macro global apply {macro_name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure macro global on device {device}. Error:\n{e}"
            )

def configure_stack_power_switch(device, switch_number):
    """ Configures stack-power switch
        Example : stack-power switch 1

        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring stack-power switch {switch_number} on {device.name}")
    config = f'stack-power switch {switch_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stack-power switch on device {device.name}. Error:\n{e}")

def configure_stack_power_stack(device, powerstack_name):
    """ Configures stack-power stack
        Example : stack-power stack test

        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring stack-power stack {powerstack_name} on {device.name}")
    config = f'stack-power stack {powerstack_name}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stack-power stack on device {device.name}. Error:\n{e}")

def unconfigure_stack_power_stack(device, powerstack_name):
    """ Unconfigures stack-power stack
        Example : no stack-power stack test

        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring stack-power stack {powerstack_name} on {device.name}")
    config = f'no stack-power stack {powerstack_name}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure stack-power stack on device {device.name}. Error:\n{e}")

def configure_stack_power_mode_redundant(device, powerstack_name, strict=None):
    """ Configures redundant mode on stack-power stack
        Example : mode redundant / mode redundant strict

        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
            strict ('str'): Strict mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring redundant mode on stack-power stack on {device.name}")
    config = [f'stack-power stack {powerstack_name}']
    if strict is None:
        config.append ('mode redundant')
    else:
        config.append ('mode redundant strict')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure redundant mode on device {device.name}. Error:\n{e}")

def unconfigure_stack_power_mode_redundant(device, powerstack_name, strict=None):
    """ Unconfigures redundant mode on stack-power stack
        Example : no mode redundant / no mode redundant strict

        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
            strict ('str'): Strict mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring redundant mode on {device.name}")
    config = [f'stack-power stack {powerstack_name}']
    if strict is None:
        config.append ('no mode redundant')
    else:
        config.append ('no mode redundant strict')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure redundant mode on device {device.name}. Error:\n{e}")

def configure_stack_power_default_mode(device, powerstack_name):
    """ Configures default mode on stack-power stack
        Example : default mode

        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring default mode on stack-power stack on {device.name}")
    config = [
        f'stack-power stack {powerstack_name}',
        'default mode'
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure default mode on device {device.name}. Error:\n{e}")

def clear_macro_auto_confgis(device, interface=""):

    """ Clear macro auto configuration on device
        Args:
            device (`obj`): Device object
            interface (`str`): Interface name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    if interface:
        cmd = f"clear macro auto configuration interface {interface}"
    else:
        cmd = "clear macro auto configuration all"
    try:
        return device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to clear macro auto configuration on device. Error:\n{e}")

def configure_software_auto_upgrade(device, auto_upgrade_option, src_url=""):
    """ Configure software auto upgrade on a device
        Args:
            device (`obj`): Device object
            auto_upgrade_option (`str`): auto upgrade options
                ex:)
                    disable  Disable the auto upgrade installation feature
                    enable  Enable the auto upgrade installation feature
                    source  Configure software auto upgrade source parameters
            src_url('str',optional) : Location of the software to install during auto upgrades
                ex:)
                    bootflash:   Software URL
                    flash-1:     Software URL
                    flash-2:     Software URL
                    flash-3:     Software URL
                    flash:       Software URL
                    ftp:         Software URL
                    http:        Software URL
                    https:       Software URL
                    sftp:        Software URL
                    stby-flash:  Software URL
                    tftp:        Software URL
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if auto_upgrade_option == "source":
        cmd.append(f'software auto-upgrade source url {src_url}')
    elif auto_upgrade_option == "disable":
        cmd.append(f'no software auto-upgrade disable')
    elif auto_upgrade_option == "enable":
        cmd.append(f'software auto-upgrade enable')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to Configure software auto upgrade on device. Error:\n{e}")

def unconfigure_software_auto_upgrade(device, auto_upgrade_option, src_url=""):
    """ Unconfigure software auto upgrade on a device
        Args:
            device (`obj`): Device object
            auto_upgrade_option (`str`): auto upgrade options
                ex:)
                    enable  Enable the auto upgrade installation feature
                    source  Configure software auto upgrade source parameters
            src_url('str',optional) : Location of the software to install during auto upgrades
                ex:)
                    bootflash:   Software URL
                    flash-1:     Software URL
                    flash-2:     Software URL
                    flash-3:     Software URL
                    flash:       Software URL
                    ftp:         Software URL
                    http:        Software URL
                    https:       Software URL
                    sftp:        Software URL
                    stby-flash:  Software URL
                    tftp:        Software URL
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if auto_upgrade_option == "source":
        cmd.append(f'no software auto-upgrade source url {src_url}')
    elif auto_upgrade_option == "enable":
        cmd.append(f'no software auto-upgrade enable')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure software auto upgrade on device. Error:\n{e}")

def power_supply_on_off(device, switch_number, ps_slot, operation):
    """ Perform on/off on power supply slot of a switch
        Args:
            device (`obj`): Device object
            switch_number ('int'): Switch number
            ps_slot ('str'): power supply slot
            operation('str'): on/off
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'power supply {switch_number} slot {ps_slot} {operation}'
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to {operation} power supply {ps_slot} on switch{switch_number} . Error:\n{e}')

def configure_archive_default(device, archive_option, archive_subcmd=""):
    """ Configure archive default for switch
        Args:
            device ('obj'): Device object
            archive_option ('str'): archive options
            ex:)
                log           Logging commands
                maximum       maximum number of backup copies
                path          path for backups
                rollback      Rollback parameters
                time-period   Period of time in minutes to automatically archive the running-config
                write-memory  Enable automatic backup generation during write memory
            archive_subcmd('str'): if archive_option is rollback
            ex:)
                filter  Rollback filter parameter
                retry   Rollback retry parameters
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    if archive_option.lower() == "log":
        cmd.append("default log config")
    elif archive_option.lower() == 'rollback':
        if archive_subcmd.lower() == "filter":
            cmd.append("default rollback filter adaptive")
        elif archive_subcmd.lower() == "retry":
            cmd.append("default rollback retry timeout")
    else:
        cmd.append(f'default {archive_option}')

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive default on device {device}. Error:\n{e}")

def configure_archive_path(device, backup_path):
    """ Configure archive path for switch
        Args:
            device ('obj'): Device object
            backup_path ('str'): path for backup
            ex:)
                bootflash:  Write archive on bootflash: file system
                crashinfo:  Write archive on crashinfo: file system
                flash:      Write archive on flash: file system
                ftp:        Write archive on ftp: file system
                http:       Write archive on http: file system
                https:      Write archive on https: file system
                rcp:        Write archive on rcp: file system
                scp:        Write archive on scp: file system
                sftp:       Write archive on sftp: file system
                tftp:       Write archive on tftp: file system
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append(f'path {backup_path}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive path on device {device}. Error:\n{e}")

def unconfigure_archive_path(device):
    """ Unconfigure archive path for switch
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append('no path')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure archive path on device {device}. Error:\n{e}")

def configure_archive_maximum(device, max_value):
    """ Configure archive maximum for switch
        Args:
            device ('obj'): Device object
            max_value ('int'): maximum number of backup copies
            ex:)
                <1-14>  maximum number of backup copies
        Returns:
            output
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append(f'maximum {max_value}')
    try:

        exec_out = device.configure(cmd)
        return exec_out
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive maximum on device {device}. Error:\n{e}")

def unconfigure_archive_maximum(device):
    """ Unconfigure archive maximum for switch
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append("no maximum")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive maximum on device {device}. Error:\n{e}")

def configure_archive_rollback(device, rollback_option, timeout=1):
    """ Configure archive rollback for switch
        Args:
            device ('obj'): Device object
            rollback_option ('str'): if archive_option is rollback
            ex:)
                filter  Rollback filter parameter
                retry   Rollback retry parameters
            timeout ('int', optional): Timeout value in seconds(default is 1 second)
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    if rollback_option.lower() == "filter":
        cmd.append("rollback filter adaptive")
    elif rollback_option.lower() == "retry":
        cmd.append(f'rollback retry timeout {timeout}')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive rollback on device {device}. Error:\n{e}")

def unconfigure_archive_rollback(device, rollback_option):
    """ Unconfigure archive rollback for switch
        Args:
            device ('obj'): Device object
            rollback_option ('str'): if archive_option is rollback
            ex:)
                filter  Rollback filter parameter
                retry   Rollback retry parameters
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    if rollback_option.lower() == "filter":
        cmd.append("no rollback filter adaptive")
    elif rollback_option.lower() == "retry":
        cmd.append("no rollback retry timeout")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure archive rollback on device {device}. Error:\n{e}")

def configure_archive_time_period(device, time_period):
    """ Configure archive time-period for switch
        Args:
            device ('obj'): Device object
            time_period ('int'): Number of minutes to wait between archive creation
            ex:)
                <1-525600>  Number of minutes to wait between archive creation

        Returns:
            result
        Raises:
            SubCommandFailure
    """

    cmd = [
            "archive",
            f"time-period {time_period}",
    ]
    try:
        exec_out = device.configure(cmd)
        return exec_out
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive time-period on device {device}. Error:\n{e}")

def unconfigure_archive_time_period(device):
    """ Unconfigure archive time-period for switch
        Args:
            device ('obj'): Device object

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append('no time-period')
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure archive time-period on device {device}. Error:\n{e}")

def configure_archive_write_memory(device):
    """ Configure archive write memory for switch
        Args:
            device ('obj'): Device object

        Returns:
            output
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append('write-memory')
    try:
        exec_out = device.configure(cmd)
        return exec_out
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure archive write memory on device {device}. Error:\n{e}")

def unconfigure_archive_write_memory(device):
    """ Unconfigure archive write memory for switch
        Args:
            device ('obj'): Device object

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd.append("archive")
    cmd.append('no write-memory')
    try:
       device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure archive write memory on device {device}. Error:\n{e}")

def unconfigure_router_bgp(device, number):
    """ Unconfigures router bgp number
        Example : no router bgp 1

        Args:
            device ('obj'): device to use
            number ('int'): Autonomous system number (Range: 1-4294967295)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring router BGP {number} on {device.name}")
    config = f'no router bgp {number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure router bgp on device {device.name}. Error:\n{e}")

def unconfigure_udld_aggressive(device):
    """ Unconfigures udld aggressive
        Example : no udld aggressive

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring udld aggressive on {device.name}")
    config = 'no udld aggressive'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure udld aggressive on device {device.name}. Error:\n{e}")

def unconfigure_udld_message_time(device):
    """ Unconfigures udld message time
        Example : no udld message time

        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring udld message time on {device.name}")
    config = 'no udld message time'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure udld message time on device {device.name}. Error:\n{e}")

def unconfigure_router_ospf(device, process_id):
    """ Unconfigures router ospf process
        Example : no router ospf 1

        Args:
            device ('obj'): device to use
            process_id ('int'): process ID (Range: 1-65535)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring router ospf {process_id} on {device.name}")
    config = f'no router ospf {process_id}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure router ospf {process_id} on device {device.name}. Error:\n{e}")

def unconfigure_interface_port_channel(device, number):
    """ Unconfigures interface port-channel number
        Example : no interface port-channel 1
        Args:
            device ('obj'): device to use
            number ('int'): Port-channel interface number (Range: 1-126)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring interface port-channel {number} on {device.name}")
    config = f'no interface port-channel {number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure interface port-channel on device {device.name}. Error:\n{e}")

def configure_udld_aggressive(device):
    """ Configures udld aggressive
        Example : udld aggressive
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring udld aggressive on {device.name}")
    config = 'udld aggressive'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure udld aggressive on device {device.name}. Error:\n{e}")

def configure_udld_message_time(device, time):
    """ Configures udld message time
        Example : udld message time 30
        Args:
            device ('obj'): device to use
            time ('int'): Time in seconds between sending of messages in steady state
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring udld message time on {device.name}")
    config = f'udld message time {time}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure message time on device {device.name}. Error:\n{e}")

def unconfigure_interface_vlan(device, vlan_id):
    """ Unconfigures interface vlan id
        Example : no interface vlan 1
        Args:
            device ('obj'): device to use
            vlan_id ('int'): Vlan interface number (Range: 1-4093)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring interface vlan {vlan_id} on {device.name}")
    config = f'no interface vlan {vlan_id}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure interface vlan {vlan_id} on device {device.name}. Error:\n{e}")

def configure_udld_port_aggressive(device, interface_name):
    """ Configures udld port aggressive on an interface
        Example: udld port aggressive

        Args:
            device ('obj'): device to use
            interface_name ('str'): name of the interface (eg: gig1/0/1)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configure udld port aggressive on {device.name}")
    cmd = [
            f"interface {interface_name}",
            "udld port aggressive"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure udld port aggressive on {device.name}. Error:\n{e}")

def configure_event_manager_applet_event_none(device, applet_name):
    """ Configures event none to specific event manager applet
        Example: event manager applet test
                event none

        Args:
            device ('obj'): device to use
            applet_name ('str'): Name of the Event Manager applet
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring event none on event manager applet on {device.name}")
    config = [
        f"event manager applet {applet_name}",
        "event none"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure event none on event manager applet {applet_name}. Error:\n{e}"
        )

def configure_action_syslog_msg(device, applet_name, action_label, msg):
    """ Configures action syslog message on event manager applet
        Example: action 0.5 syslog msg "------ High memory usage detected ----"

        Args:
            device ('obj'): device to use
            applet_name ('str'): Name of the Event Manager applet
            action_label ('str'): Action label (eg. 0.5, 5.0)
            msg ('str'): Syslog message
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring action syslog message on event manager applet on {device.name}")
    config = [
        f"event manager applet {applet_name}",
        f"action {action_label} syslog msg {msg}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure action syslog message on event manager applet. Error:\n{e}"
        )

def configure_action_string(device, applet_name, action_label, action_string):
    """ Configures action {action_string} on event manager applet
        Example: action 5.1 force-switchover

        Args:
            device ('obj'): device to use
            applet_name ('str'): Name of the Event Manager applet
            action_label ('str'): Action label (eg. 5.1, 5.2)
            action_string ('str'): Action string (Eg. force-switchover)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring action force-switchover on event manager applet on {device.name}")
    config = [
        f"event manager applet {applet_name}",
        f"action {action_label} {action_string}"
    ]
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure action {action_string} on event manager applet. Error:\n{e}"
        )

def configure_stack_power_switch(device, switch_number):
    """ Configures stack-power switch
        Example : stack-power switch 1

        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring stack-power switch {switch_number} on {device.name}")
    config = f'stack-power switch {switch_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stack-power switch on device {device.name}. Error:\n{e}")

def configure_service_template(device, template_name):
    """ Configure service-template
        Args:
            device (`obj`): Device object
            template_name ('str'): template name
    """
    cmd = f'service-template {template_name}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed configure service-template on this device. Error:\n{e}')

def configure_policy_map_control(device, subscriber, class_number, action_number, template_name, match_type=None, action=None):
    """ Configures policy-map type control
        Example : policy-map type control subscriber BUILTIN_AUTOCONF_POLICY
                event identity-update match-first
                1 class always do-all
                1 activate interface-template DMP_INTERFACE_TEMPLATE

        Args:
            device ('obj'): device to use
            subscriber ('str'): name of identity policy-map
            class_number ('int'): class number (Range: 1-254)
            action_number ('int'): action number (Range 1-254)
            template_name ('str'): name of an interface template
            match_type ('str'): match classes to evaluate (Eg. match-all, match-first)
            action ('str'): execute action (Eg. do-all, do-until-failure, do-until-success)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r'.*Do you want to continue\?\s\[yes\].*',
                action='sendline()',
                loop_continue=True,
                continue_timer=False
            )
        ]
    )
    log.info(f"Configuring policy-map type control on {device.name}")
    config = [f'policy-map type control subscriber {subscriber}']
    if match_type:
        config.append(f'event identity-update {match_type}')
    else:
        config.append('event identity-update')
    if action:
        config.append(f'{class_number} class always {action}')
    else:
        config.append(f'{class_number} class always')
    config.append(f'{action_number} activate interface-template {template_name}')
    try:
        device.configure(config, reply=dialog)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure policy-map type control on device {device.name}. Error:\n{e}")

def configure_port_channel_persistent(device, channel_group_num):
    """ Configures port-channel persistent
        Args:
            device ('obj'): device to use
            channel_group_num ('int'):  Channel group number
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = f'port-channel {channel_group_num} persistent '
    try:
        device.execute(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(
          f"Failed to uConfigures port-channel persistent on device {device.name}. Error:\n{e}")

def unconfigure_license_smart_reservation(device):
    """ Unconfigure license smart reservation

    Args:
        device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'no license smart reservation'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure license smart reservation on this device. Error:\n{e}")

def configure_license_smart_transport_off(device):
    """ Configure license smart transport off

    Args:
        device ('obj'): device to use
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'license smart transport off'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure license smart transport off on this device. Error:\n{e}")

def configure_ip_domain_timeout(device, value):
    """ Configure ip domain timeout

    Args:
        device ('obj'): device to use
        value ('int'): timeout value
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip domain timeout {value}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip domain timeout on this device. Error:\n{e}")

def configure_platform_shell(device):
    """ Configure platform shell

    Args:
        device ('obj'): device to use
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'platform shell'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure platform shell on this device. Error:\n{e}")

def configure_ip_http_authentication_local(device):
    """ Configure ip http authentication local

    Args:
        device ('obj'): device to use
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip http authentication local'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip http authentication local on this device. Error:\n{e}")


def configure_ip_domain_name(device, name):
    """ Configure ip domain name
    Args:
        device ('obj'): device to use
        name ('str'): domain name
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip domain name {name}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip domain name on this device. Error:\n{e}")


def configure_ip_domain_name_vrf_mgmt_vrf(device, name):
    """ Configure ip domain name vrf mgmt-vrf
    Args:
        device ('obj'): device to use
        name ('str'): domain name
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip domain name vrf mgmt-vrf {name}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip domain name vrf mgmt-vrf on this device. Error:\n{e}")


def configure_ip_name_server_vrf(device, name, ip):
    """ Configure ip name-server vrf
    Args:
        device ('obj'): device to use
        name ('str'): domain name
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip name-server vrf {name} {ip}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip name-server vrf on this device. Error:\n{e}")

def configure_ip_http_client_source_interface_vlan_domain_lookup(device, vlan_id):
    """ Configure ip http client source-interface vlan domain lookup
    Args:
        device ('obj'): device to use
        vlan_id ('str'): vlan id
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
        f'ip http client source-interface vlan {vlan_id}',
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip http client source-interface vlan domain lookup on this device. Error:\n{e}")

def unconfigure_service_internal(device):
    """ Unonfigure service imternal
    Args:
        device ('obj'): device to use
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"no service internal"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure service imternal on this device. Error:\n{e}")

def configure_ip_http_client_source_interface_vlan_domain_lookup_name_server_vrf_mgmt_vrf(device, interface_id):
    """ Configure ip http client source-interface vlan domain lookup
    Args:
        device ('obj'): device to use
        interface_id ('str'): interface id
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = [
        'no ip name-server vrf mgmt-vrf',
        f'interface {interface_id}'
    ]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip http client source-interface vlan domain lookup on this device. Error:\n{e}")

def configure_ip_http_client_source_interface(device, interface_name, interface_id):
    """ Configure ip http client source-interface
    Args:
        device ('obj'): device to use
        interface_id ('str'): vlan id
        Returns
            None
        Raises:
            SubCommandFailure
    """

    cmd = f'ip http client source-interface {interface_name} {interface_id}',

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip http client source-interface on this device. Error:\n{e}")

def configure_service_performance(device):
    """ Configures service performance on device
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring service performance on device")
    cmd = 'service performance'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure service performance on {device}. Error:\n{error}"
                .format(device=device, error=e))
def unconfigure_service_performance(device):
    """ Unconfigures service performance on device
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring service performance on device")
    cmd = 'no service performance'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure service performance on {device}. Error:\n{error}"
                .format(device=device, error=e))
def configure_key_config_key_password_encrypt(device, password):
    """ Configure key config-key password encrypt on device
        Args:
            device ('obj'): Device object
            password('str'): password, The config-key
                Minimum 8 characters not beginning with
                IOS special character(! # ;)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring key config-key password encrypt on device")
    cmd = [f'key config-key password encrypt {password}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure key config-key password encrypt on {device}. Error:\n{error}"
                .format(device=device, error=e))
def unconfigure_key_config_key_password_encrypt(device, password):
    """ Unconfigures key config-key password encrypt on device
        Args:
            device (`obj`): Device object
            password('str'): password, The config-key
                Minimum 8 characters not beginning with
                IOS special character(! # ;)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring no key config-key password encrypt on device")
    cmd = [f'no key config-key password encrypt {password}']

    dialog = Dialog([
        Statement(pattern=r"Continue with master key deletion \? \[yes\/no\]\:\s*$",
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False)
        ])
    try:
        device.configure(cmd,reply=dialog)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure no key config-key password encrypt on {device}. Error:\n{error}"
                .format(device=device, error=e))


def unconfigure_event_manager_applet(device, event):
    """ Unonfigures event manager applet
        Args:
            device ('obj'): device to use
            event ('str'): event manager applet name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no event manager applet {event}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure event manager applet on device {device.name}. Error:\n{e}")

def configure_event_manager_applet(device, event):
    """ Configures event manager applet
        Args:
            device ('obj'): device to use
            event ('str'): event manager applet name
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"event manager applet {event}",
        "event none"
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure event manager applet on device {device.name}. Error:\n{e}")

def configure_power_inline_auto_max(device, interface, time):
    """ Configures power inline auto max
        Args:
            device ('obj'): device to use
            interface ('obj'): interface name
            time ('str'): <4000-60000>  milli-watt
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"interface {interface}",
        f"power inline auto max {time}",
    ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure power inline auto max on device {device.name}. Error:\n{e}")

def configure_switch_provision_model(device, switch_number, model):
    """ Configures switch provision
        Args:
            device ('obj'): device to use
            switch_number ('int'): switch number
            model ('str'): provision model
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"switch {switch_number} provision {model}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure switch provision on device {device.name}. Error:\n{e}")

def configure_snmp_server_manager(device):
    """ Configures snmp-server manager
        Args:
            device ('obj'): device to use
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"snmp-server manager"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure snmp-server manager on device {device.name}. Error:\n{e}")

def configure_service_performance(device):
    """ Configures service performance on device
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring service performance on device")
    cmd = 'service performance'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure service performance on {device}. Error:\n{error}"
                .format(device=device, error=e))
def unconfigure_service_performance(device):
    """ Unconfigures service performance on device
        Args:
            device (`obj`): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Unconfiguring service performance on device")
    cmd = 'no service performance'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure service performance on {device}. Error:\n{error}"
                .format(device=device, error=e))
def configure_key_config_key_password_encrypt(device, password):
    """ Configure key config-key password encrypt on device
        Args:
            device ('obj'): Device object
            password('str'): password, The config-key
                Minimum 8 characters not beginning with
                IOS special character(! # ;)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring key config-key password encrypt on device")
    cmd = [f'key config-key password encrypt {password}']
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure key config-key password encrypt on {device}. Error:\n{error}"
                .format(device=device, error=e))
def unconfigure_key_config_key_password_encrypt(device, password):
    """ Unconfigures key config-key password encrypt on device
        Args:
            device (`obj`): Device object
            password('str'): password, The config-key
                Minimum 8 characters not beginning with
                IOS special character(! # ;)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring no key config-key password encrypt on device")
    cmd = [f'no key config-key password encrypt {password}']

    dialog = Dialog([
        Statement(pattern=r"Continue with master key deletion \? \[yes\/no\]\:\s*$",
                  action='sendline(yes)',
                  loop_continue=True,
                  continue_timer=False)
        ])
    try:
        device.configure(cmd,reply=dialog)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure no key config-key password encrypt on {device}. Error:\n{error}"
                .format(device=device, error=e))
def configure_enable_secret_password(device, enable_secret):
    ''' Apply enable secret password for switch
        Args:
            device ('obj'): Device object
            enable_secret('str'): password
            ex.)
        Raises:
            SubCommandFailure
    '''
    cmd = [f"enable secret password  {enable_secret}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to apply enable secrate password on device {device}. Error:\n{e}")

def configure_call_home_reporting(device, address="", proxy_server="", email="", port=-1):
    """ Configures call home reporting
        Example : default mode
        Args:
            device ('obj'): device to use
            address ('str'): call home reporting address
            proxy_server ('str'): http proxy server
            email ('str'): email address
            port ('int'): port number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if address == "anonymous":
        cmd = f"call-home reporting {address}"
        if proxy_server:
            cmd += f" http-proxy {proxy_server} port {port}"
    elif address == "contact-email-addr":
        cmd = f"call-home reporting {address} {email}"
    else:
        raise SubCommandFailure("Incorrect call-home reporting address type.")
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure call home reporting on device {device.name}. Error:\n{e}")

def unconfigure_enable_secret_password(device, enable_secret):
    ''' Apply enable secret password for switch
        Args:
            device ('obj'): Device object
            enable password('str'):password
            ex.)
        Raises:
            SubCommandFailure
    '''
    cmd = [f"no enable secret password  {enable_secret}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure secrate password on device {device}. Error:\n{e}")

def configure_line_vty(
    device, first_line_number, second_line_number=''):
    """ Configures line vty on switch

        Args:
            device ('obj'): device to use
            first_line_number('int'): first line number
            second_line_number ('int', optional): Second line number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring line vty number on {device.name}")
    config = f'line vty {first_line_number} {second_line_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure line vty on device {device.name}. Error:\n{e}")

def unconfigure_line_vty(
    device, first_line_number, second_line_number=''):
    """ unconfigures line vty  on switch
        Args:
            device ('obj'): device to use
            first_line_number ('int'): first line number
            second_line_number ('int'): Second line number
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unonfiguring line vty number stack on {device.name}")
    config = f'no line vty {first_line_number} {second_line_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure line vty on device {device.name}. Error:\n{e}")

def configure_diagnostic_monitor_switch(
    device, switch_number, test_name, failure_count=None):
    """ execute diagnostic start switch 1 test

        Args:
            device ('obj'): Device object
            test_id ('str'): Test ID list (e.g. 1,3-6) or Test Name or minimal  or complete
              Interface port number WORD    Port number list (e.g. 2,4-7)
            switch_number ('int'): Switch number on which diagnostic has to be performed
            test_name ('str'): Word , test name

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    if failure_count :
        cmd = f"diagnostic monitor threshold switch {switch_number} test {test_name} failure count {failure_count}"
    else:
        cmd = f"diagnostic monitor switch {switch_number} test {test_name}"

    try:
       device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic start switch {switch_number} test {test_name} on device. Error:\n{e}")

def unconfigure_diagnostic_monitor_switch(
    device, switch_number, test_name):
    """ execute diagnostic start switch 1 test

        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number on which diagnostic has to be performed
            test_name ('str'): Word , test name

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [f"no diagnostic monitor switch {switch_number} test {test_name}"]

    try:
       device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic monitor switch {switch_number} on device. Error:\n{e}")


def configure_diagnostic_schedule_switch(
    device, switch_number, time,
    day=None, month=None, day_number=None, year=None):
    """ execute diagnostic start switch 1 test

        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number on which diagnostic has to be performed
            time ('str'): time in hours and min  "hh:mm  Begin time"
            day ('str'): Day of the week
            day_number ('int'): day number of a month
            month ('str'): name of the month
            year ('int'): year number ,

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd = f"diagnostic schedule switch {switch_number} test all "

    if day and time :
        cmd += f"weekly {day} {time}"
    elif month and year and time:
        cmd += f"on {month} {day_number} {year} {time}"
    else:
        cmd += f"daily {time}"
    try:
       device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic schedule switch {switch_number} on device. Error:\n{e}")

def unconfigure_diagnostic_schedule_switch(
    device, switch_number,
    time, day=None, month=None,
    day_number=None, year=None):
    """ execute diagnostic start switch 1 test
        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number on which diagnostic has to be performed
            time ('str'): time in hours and min  "hh:mm  Begin time"
            day ('str'): Day of the week
            day_number ('int'): day number of a month
            month('str'): name of the month
            year ('int'): year number ,

        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = []
    cmd = f"no diagnostic schedule switch {switch_number} test all "

    if day and time :
        cmd += f"weekly {day} {time}"
    elif month and year and time:
        cmd += f"on {month} {day_number} {year} {time}"
    else :
        cmd += f"daily {time}"
    try:
       device.configure(cmd)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not execute diagnostic schedule switch {switch_number} on device. Error:\n{e}")


def configure_stack_power_switch_power_priority(
    device,
    switch_number,
    power_priority,
    power_priority_value=None,
    default=False
    ):
    """ configure_stack power switch <sw_num> power priority
        Example : stack-power switch 1 power priority low 15
        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
            power_priority('str'): power_priority (low/high/switch)
            power_priority_value ('int', optional): priority_values <1-27>. Default is None
            default ('bool', optional): default power priority. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = [f"stack-power switch {switch_number}"]
    if default:
        config.append(f"default power-priority {power_priority}")
    elif power_priority_value:
        config.append(f"power-priority {power_priority} {power_priority_value}")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure power priorities stack-power stack on device {device.name}. Error:\n{e}")

def unconfigure_stack_power_switch_power_priority(
    device,
    switch_number,
    power_priority
    ):
    """ unconfigure_stack power switch <sw_num> power priority low <priority_value>
        Example : stack-power switch 1 power priority low 15
        Args:
            device ('obj'): device to use
            stack_parameters ('str'): stack_parameters (stack/switch)
            switch_number ('int'): Switch number (1-16)
            power_priority('str'): power_priority (low/high/switch)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    config = [ 
        f"stack-power switch {switch_number}",
        f"no power-priority {power_priority}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure power priorities stack-power stack on device {device.name}. Error:\n{e}")


def configure_default_stack_power_switch_power_priority(
    device,
    stack_parameters,
    switch_number,
    power_priority,
    power_priority_value
    ):
    """ configure_default stack power switch <sw_num> power priority low/high/switch <priority_value>
        Example : stack-power switch 1 default power priority low 15
        Args:
            device ('obj'): device to use
            stack_parameters ('str'): stack_parameters (stack/switch)
            switch_number ('int'): Switch number (1-16)
            power_priority('str'): default power_priority (low/high/switch)
            power_priority_value ('int'): priority_values <1-27>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info('configure default stack-power switch power priority')

    config = [
        f"stack-power {stack_parameters} {switch_number}",
        f"default power-priority {power_priority} {power_priority_value}"]

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure default power priority on device {device.name}. Error:\n{e}")


def configure_stackpower_stack_switch_standalone(device, switch_number, stack_name=None, standalone=True):
    """ Configures stack and standalone on stack-power switch
        
        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
            stack_name ('str', optional): Power stack name - Up to 31 chars
            standalone ('bool', optional): standalone. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    config = [f'stack-power switch {switch_number}']
    if stack_name:
        config.append(f'stack {stack_name}')
    if standalone:
        config.append('standalone')
    else:
        config.append('no standalone')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stack power switch standalone on device {device.name}. Error:\n{e}")

def unconfigure_stackpower_stack_switch_standalone(device, switch_number, stack_name=None, standalone=True):
    """ Unconfigures stack and standalone on stack-power switch
        
        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
            stack_name ('str', optional): Power stack name - Up to 31 chars
            standalone ('bool', optional): standalone. Default is True
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    config = [f'stack-power switch {switch_number}']

    if stack_name:
        config.append(f'no stack {stack_name}')
    if standalone:
        config.append('standalone')
    else:
        config.append('no standalone')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure stack power switch standalone on device {device.name}. Error:\n{e}")


def configure_stack_power_switch_standalone(device,switch_number):
    """ configure standalone on stack power switch
        Example : standalone on stack power switch <sw_num>
        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("configuring standalone on stack-power switch")

    config = [ 
        f'stack-power switch {switch_number}',
        'standalone']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure standalone stack-power switch  on device {device.name}. Error:\n{e}")

def configure_stack_power_switch_no_standalone(device,switch_number):
    """ configure no standalone on stack power switch
        Example: no standalone on stack power switch <sw_num>
        Args:
            device ('obj'): device to use
            switch_number ('int'): Switch number (1-16)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring standalone on stack power switch")

    config = [
        f'stack-power switch {switch_number}',
        'no standalone']

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure no standalone stack-power switch on device {device.name}.Error:\n{e}")


def configure_stack_power_mode_power_shared(device, powerstack_name, strict=None):
    """ Configures power_shared mode on stack-power stack
        Example : power-shared_ / power-shared-strict
        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
            strict ('str'): Strict mode
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring power_shared mode on stack-power stack on {device.name}")

    config = [f'stack-power stack {powerstack_name}']

    if strict is None:
        config.append ('mode power-shared')
    else:
        config.append ('mode power-shared strict')
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure power_shared mode on device {device.name}.Error:\n{e}")


def unconfigure_boot_system_switch_switchnumber(device, switch_num):
    ''' Delete the boot variables
        Args:
            device ('obj'): Device object
            switch_num ('int'): Switch number
    '''
    log.info("Removing boot system switch with switch number on {device}".format(device=device))

    cmd = f'no boot system switch {switch_num}'
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not remove boot system switch with switch number on {device}. Error:\n{e}")


def configure_boot_system_switch_switchnumber(device, switch_num, destination):
    ''' Configure Boot System Switch with Destination
        Args:
            device ('obj'): Device object
            switch_num ('int'): Switch number
            destination ('int'): Destination path
    '''
    log.info(f"Configuring boot system switch with switch number and destination on {device}")

    cmd = f'boot system switch {switch_num} {destination}'

    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Configuring boot system switch with switch number and destination on {device}. Error:\n{e}")


def restore_running_config_file(device, path, file, timeout=120):
    """ Restore config from local file
        Args:
            device ('obj'): Device object
            path ('str'): directory
            file ('str'): file name
            timeout ('int'): Timeout for applying config
        Returns:
            output
    """
    dialog = Dialog(
        [
            Statement(
                pattern=r".*\[(yes|no)\].*",
                action="sendline(y)",
                loop_continue=True,
                continue_timer=False,
            )
        ]
    )
    try:
        output = device.execute(
            "configure replace {path}{file}".format(path=path, file=file),
            reply=dialog,
            timeout=timeout
        )
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not replace saved configuration on device {device}\nError: {e}")
    return output

def configure_macro_auto_global_processing_on_interface(device, interface):
    """ Configure macro auto global processing on the device interface

    Args:
        device ('obj'): device to use
        interface (int): interface to configure
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure macro auto global processing
    """

    config = [f'interface {interface}',
              f'macro auto global processing']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure macro auto global processing on the device interface. Error:\n{e}")

def unconfigure_macro_auto_global_processing_on_interface(device, interface):
    """ unConfigure macro auto global processing on the device interface

    Args:
        device ('obj'): device to use
        interface (int): interface to configure
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure macro auto global processing
    """

    config = [f'interface {interface}',
              f'no macro auto global processing']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure macro auto global processing on the device interface. Error:\n{e}")

def configure_macro_auto_global_processing(device):
    """ Configure macro auto global processing on the device globally

    Args:
        device ('obj'): device to use
    Returns:
            None
    Raises:
            SubCommandFailure: Failed to configure macro auto global processing
    """

    config = f'macro auto global processing'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure macro auto global processing on the device. Error:\n{e}")

def unconfigure_macro_auto_global_processing(device):
    """ unConfigure macro auto global processing on the device globally

    Args:
        device ('obj'): device to use
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure macro auto global processing
    """

    config = f'no macro auto global processing'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure macro auto global processing on the device. Error:\n{e}")

def configure_process_cpu_threshold_type_rising_interval(device, utilization_level, rising_level, interval):
    """ Configures process cpu threshold type  rising interval
        Example : no process cpu threshold type {utilization_level} rising {rising_level} interval {interval}
        Args:
            device ('obj'): device to use
            utilization_level ('str'): interrupt/process/total cpu level utilization
            rising_level ('str'): default rising level(1-100)
            interval('str'):default interval (5-86400)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"process cpu threshold type {utilization_level} rising {rising_level} interval {interval}"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure process cpu threshold type  on the device {device.name}. Error:\n{e}")

def unconfigure_process_cpu_threshold_type_rising_interval(device, utilization_level, rising_level, interval):
    """ Unconfigures process cpu threshold type  rising interval
        Example : no process cpu threshold type {utilization_level} rising {rising_level} interval {interval}
        Args:
            device ('obj'): device to use
            utilization_level ('str'): interrupt/process/total cpu level utilization
            rising_level ('str'): default rising level(1-100)
            interval('str'):default interval (5-86400)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"no process cpu threshold type {utilization_level} rising {rising_level} interval {interval}"

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure process cpu threshold type  on the device {device.name}. Error:\n{e}")

def configure_process_cpu_statistics_limit_entry_percentage_size(device, entry_percentage, size):
    """ Configures process cpu  statistics limit entry-percentage size
        Example : process cpu  statistics limit entry-percentage <10> size <100>
        Args:
            device ('obj'): device to use
            entry percentage ('str'): default entry percentage (1-100)
            size('str'):default interval (5-86400)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"process cpu  statistics limit entry-percentage {entry_percentage} size {size}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure process cpu  statistics limit entry-percentage size on the device {device.name}. Error:\n{e}")

def unconfigure_process_cpu_statistics_limit_entry_percentage_size(device, entry_percentage, size):
    """ unconfigures process cpu  statistics limit entry-percentage size
        Example :no process cpu  statistics limit entry-percentage <10> size <100>
        Args:
            device ('obj'): device to use
            entry percentage ('str'): default entry percentage (1-100)
            size('str'):default interval (5-86400)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    config = f"no process cpu  statistics limit entry-percentage {entry_percentage} size {size}"
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure process cpu  statistics limit entry-percentage size on the device {device.name}. Error:\n{e}")

def copy_startup_config_from_flash(device, startup_config, timeout=60):
    """ Copying startup config from flash memory
        Args:
            device ('obj'): Device object
            startup_config('str'): Config to be copied from flash
            timeout ('str'): timeout in seconds
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    dialog = Dialog(
        [
            Statement(
                pattern=r".*Destination filename.*",
                action="sendline()",
                loop_continue=False,
                continue_timer=False,
            )
        ]
    )
    cmd = f"copy flash:{startup_config} startup"

    try:
        device.execute(cmd, reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not copy saved configuration on {device}. Error:\n{e}")

def configure_macro_auto_processing_on_interface(device, interface):
    """ Configure macro auto processing on the device on interface level

    Args:
        device ('obj'): device to use
        interface ('int'): interface to configure
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure macro auto processing
    """

    config = [f'interface {interface}',
              f'macro auto processing']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure macro auto processing on the device interface. Error:\n{e}")

def unconfigure_macro_auto_processing_on_interface(device, interface):
    """ Unconfigure macro auto processing on the device on interface level

    Args:
        device ('obj'): device to use
        interface ('int'): interface to configure
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to unconfigure macro auto processing
    """

    config = [f'interface {interface}',
              f'no macro auto processing']
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure macro auto processing on the device interface. Error:\n{e}")

def config_cns_agent_passwd(device, cnspasswd):
    """ configure cns agent password

        Args:
            device (`obj`): Device object
            cnspasswd (`str`): Cns agent password
        Return:
            None
        Raise:
            SubCommandFailure: Failed to configure cns agent password
    """

    try:
        device.configure("cns password {cnspasswd}".format(cnspasswd=cnspasswd))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure cns agent password, Error: {error}'.format(error=e)
        )
    
def configure_diagnostic_monitor_syslog(device):
    """ diagnostic monitor syslog
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.configure('diagnostic monitor syslog')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure diagnostic monitor syslog on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )


def unconfigure_diagnostic_monitor_syslog(device):
    """ no diagnostic monitor syslog
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    try:
        device.configure('no diagnostic monitor syslog')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not unconfigure diagnostic monitor syslog on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )


def unconfigure_device_classifier_command(
        device, dc_option="", dc_option_name="", dc_command="",
        dc_command_name=""
):
    """ Unconfigure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'):device classifier option
            ex:)
            condition   - Define device classifier condition
            device-type - Define device type
        dc_option_name ('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_command ('str'): Define device rule commands
            ex:)
            cdp      CDP related rules
            default  Set a command to its defaults
            dhcp     DHCP related rules
            exit     Exit from device-classifier condition configuration mode
            lldp     LLDP related rules
            no       Negate a command or set its defaults
        dc_command_name('str'): command names
            ex:)
            cdp tlv-type 1 value String 9300-24UX-2
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        'no device classifier',
        f'device classifier {dc_option} {dc_option_name}',
        f'{dc_command} {dc_command_name}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure classifier command on this device. Error:\n{e}")


def unconfigure_device_classifier_profile_command(
    device, dc_option="", dc_option_name="", dc_command= "",
    dc_command_name="", dc_profile_commands="", dc_option_type="",
    dc_profile_command_name=""
):
    """ Unconfigure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'): device classifier option
            ex:)
            condition    Define device classifier condition
            device-type  Define device type
        dc_option_name ('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_command ('str'): Define device rule commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        dc_command_name(str'): Command names
            ex:)
            CDP_RULE_TLV_1
        dc_profile_commands('str'): Given commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        dc_option_type('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_profile_command_name('str'): profile command and it's configuration
            ex:)
            no device classifier device-type CDP_TYPE_TLV_1
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        'no device classifier',
        f'device classifier {dc_option} {dc_option_name}',
        f'{dc_command} {dc_command_name}',
        f'{dc_profile_commands} {dc_option_type} {dc_profile_command_name}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure classifier command on this device. Error:\n{e}")


def configure_device_classifier_command(
        device, dc_option="", dc_option_name="", dc_command="",
        dc_command_name="", dc_profile_commands=""
):
    """ configure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'): device classifier option
            ex:)
            condition    Define device classifier condition
            device-type  Define device type
        dc_option_name ('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_command ('str'): Define device rule commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        dc_command_name('str'): command names
            ex:)
            cdp tlv-type 1 value String 9300-24UX-2
        dc_profile_commands('str'): Given commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f'device classifier {dc_option} {dc_option_name}',
        f'{dc_command} {dc_command_name}',f'{dc_profile_commands}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure classifier command on this device. Error:\n{e}")


def unconfigure_device_classifier_profile(
    device, dc_option, dc_option_name, dc_command, dc_command_name,
    dc_profile_commands, dc_option_type, dc_profile_command_name
):
    """ Unconfigure device classifier on this device

    Args:
        device ('obj'): device to use
        dc_option ('str'): device classifier option
            ex:)
            condition    Define device classifier condition
            device-type  Define device type
        dc_option_name ('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_command ('str'): Define device rule commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        dc_command_name(str'): Command names
            ex:)
            CDP_RULE_TLV_1
        dc_profile_commands('str'): Given commands
            ex:)
            Device classifier profile commands
            condition  Give condition name
            default    Set a command to its defaults
            exit       Exit from device-classifier dev-type configuration mode
            no         Negate a command or set its defaults
        dc_option_type('str'): Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        dc_profile_command_name('str'): profile command and it's configuration
            ex:)
            no device classifier device-type CDP_TYPE_TLV_1
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        'no device classifier',
        f'device classifier {dc_option} {dc_option_name}',
        f'{dc_command} {dc_command_name}',
        f'{dc_profile_commands} {dc_option_type} {dc_profile_command_name}']

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure classifier command on this device. Error:\n{e}")

def unconfigure_device_classifier_operator(device, dc_option="", dc_option_name="", operator_type=""):
    """ Unconfigure device classifier on this device
    Args:
        device ('obj'):  device to use
        dc_option ('str'):  device classifier option
            ex:)
            condition     Define device classifier condition
            device-type   Define device type
        dc_option_name ('str'):  Name of device classifier type
            ex:)
            WORD  Condition name
            WORD  Device type name
        operator_type('str'):  Name of the given operator name
            ex:)
            <operator-type(AND/OR)>
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if all((dc_option, dc_option_name, operator_type)):
        cmd = f'no device classifier {dc_option} {dc_option_name} op {operator_type}'
    else:
        cmd = 'no device classifier'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure classifier on this device. Error:\n{e}")

def configure_ip_source_binding(device, mac_address, vlan_id, ip_address, interface):
    """ Configure ip source binding
    Args:
        device ('obj'): device to use
        mac_address ('str'): binding MAC address
        vlan_id ('int'): binding VLAN number (1-4094)
        ip_address ('str'): binding IP address
        interface ('str'): interface name (eg: Gi1/0/13)
        Returns
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'ip source binding {mac_address} vlan {vlan_id} {ip_address} interface {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure ip source binding. Error:\n{e}")

def unconfigure_ip_source_binding(device, mac_address, vlan_id, ip_address, interface):
    """ unconfigure ip source binding
    Args:
        device ('obj'): device to use
        mac_address ('str'): binding MAC address
        vlan_id ('int'): binding VLAN number (1-4094)
        ip_address ('str'): binding IP address
        interface ('str'): interface name (eg: Gi1/0/13)
        Returns
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no ip source binding {mac_address} vlan {vlan_id} {ip_address} interface {interface}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure ip source binding. Error:\n{e}")


def configure_boot_manual_switch(device, switch_num):
    """ Configure boot manual switch
    Args:
        device ('obj'): device to use
        switch_num ('int'): Active switch number
        Returns
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'boot manual switch {switch_num}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure boot manual switch {switch_num}. Error:\n{e}")


def unconfigure_boot_manual_switch(device, switch_num):
    """ Unconfigure boot manual switch
    Args:
        device ('obj'): device to use
        switch_num ('int'): Active switch number
        Returns
            None
        Raises:
            SubCommandFailure
    """
    cmd = f'no boot manual switch {switch_num}'
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure boot manual switch {switch_num}. Error:\n{e}")


def configure_mdix_auto(device, interface):
    """ configure mdix auto
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Configuring the mdix auto on {device} {interface}")
    cmd = [f"interface {interface}",
           f"mdix auto"
           ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure mdix auto on {device} {interface}. Error:\n{e}"
        )


def unconfigure_mdix_auto(device, interface):
    """ Unconfigure mdix auto
        Args:
            device ('obj'): device to use
            interface ('str'): interface to configure
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info(f"Unconfiguring no mdix auto on {device} {interface}")
    cmd = [f"interface {interface}",
           f"no mdix auto"
           ]
    try:
        device.configure(cmd)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure mdix auto on {device} {interface}. Error:\n{e}"
        )


def unconfigure_enable_secret_level(device, level_num):
    ''' Remove enable secret level for switch
        Args:
            device ('obj'): Device object
            level_num('int'): level number
            ex.)
        Raises:
            SubCommandFailure
    '''
    cmd = f"no enable secret level {level_num}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure secrate level number on device {device}. Error:\n{e}")

def unconfigure_stack_power_switch(device, switch_number):
    """ un configures stack-power switch
        Example : no stack-power switch 1
        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number (1-16)
        Returns:
            None
        Raises: 
            SubCommandFailure
    """
    log.info(f"Un configuring stack-power switch {switch_number} on {device.name}")
    config = f'no stack-power switch {switch_number}'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure stack-power switch on device {device.name}. Error:\n{e}")


def unconfig_banner(device, banner_text):
    """ Unconfig Day banner

        Args:
            device (`obj`): Device object
            banner_text (`str`): Banner text
        Return:
            None
        Raise:
            SubCommandFailure: Failed to unconfigure Day banner
    """

    try:
        device.configure("no banner motd {banner_text}".format(banner_text=banner_text))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not unconfigure banner {banner_text}, Error: {error}'.format(
                banner_text=banner_text, error=e)
        )

def configure_logging_buffered_persistent_url(device, filesystem_name=None):
    """ Configure logging buffered, logging persistent url
    Args:
        device ('obj'): device to use
        filesystem_name ('str'): Filesystem name (bootflash:/crashinfo:/flash:/usbflash0:)
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    config = 'logging buffered\n'
    if filesystem_name:
        config += f'logging persistent url {filesystem_name}\n'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure logging buffered and logging persistent url. Error:\n{e}")


def configure_graceful_reload_interval(device, interval_val):
    """ configure graceful reload interval the XFSU device 
    
    Args:
        device ('obj'): device to use
        interface ('int'): graceful interval value
    Returns:
        None
    Raises:
        SubCommandFailure: Failed to configure graceful reload interval the XFSU device
    """

    config = f"graceful-reload interval {interval_val}"
    try:
        device.configure(config)

    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure graceful reload interval the XFSU device. Error:\n{e}")


def configure_diagnostic_bootup_level_minimal(device):
    """ diagonistics bootup level minimal
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """   
    try:
        device.configure('diagnostic bootup level minimal')
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not configure diagnostic bootup level minimum on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )

def configure_cos(device,priority_value):
    """ config COS setting on device
        Args:
            device ('obj'): Device object
            priority_value('int'):  Priority number
            ex:)
                <0-7>  priority value
        
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    log.info("Configuring 'COS setting' globally")

    configs = [f"l2protocol-tunnel cos {priority_value}"]

    try:
        device.configure(configs)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Failed to configure 'l2-protocol tunnel cos' globally"
            'Error:{e}'.format(e=e)
        )    

def unconfigure_snmp_mib_bulkstat(device, object_name, schema_name, transfer_name):
    
    """ unconfigure snmp mib bulkstat
    Args:
        device ('obj'): device to use
        object_name ('str'): The name of the object 
        schema_name ('str'): The name of the schema 
        transfer_name ('str'): bulkstat transfer name 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"bulkstat profile {transfer_name}",
        f"no enable",
        "exit",
        f"no snmp mib bulkstat object-list {object_name}",
        f"no snmp mib bulkstat schema {schema_name}",
        f"no snmp mib bulkstat transfer {transfer_name}",
 
        ]
        
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure snmp mib bulkstat on this device. Error:\n{e}")
        

def configure_stackpower_stack(device, powerstack_name, mode=None, strict=False):
    """ Configures power stack mode on stack-power stack
        
        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
            mode ('str', optional): Power stack mode. Default is None
            strict ('bool', optional): Strict mode. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = [f'stack-power stack {powerstack_name}']

    if mode:
        command = f'mode {mode}'
        if strict:
            command += ' strict'
        cmd.append(command)
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stackpower stack on device {device.name}. Error:\n{e}")


def unconfigure_stackpower_stack(device, powerstack_name):
    """ Configures power stack mode on stack-power stack
        
        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
        Returns:
            None
        Raises:
            SubCommandFailure
    """
      
    cmd = [f'no stack-power stack {powerstack_name}']

    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stackpower stack on device {device.name}. Error:\n{e}")

def unconfig_cns_agent_password(device, cns_password=None):
    """ un configure cns agent password
        Args:
            device ('obj'): Device object
            cns_password ('str', optional): Cns agent password. Default is None
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to un configure cns agent password
    """
    log.debug("un configure cns agent password")
    try:
        if cns_password:
            device.configure("no cns password {cns_password}".format(cns_password=cns_password))
        else:
            device.configure("no cns password")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure cns agent password. Error:\n{e}")


def configure_boot_system_image_file(device, image_path, switch_number=None):
    """ Configure boot system image file
        Args:
            device ('obj'): Device object
            image_path ('str'): full image path. Ex: flash:cat9k_17467.SSA.pkg
            switch_number ('str', optional): switch number or all. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    cmd = f"boot system{f' switch {switch_number}' if switch_number else ''} {image_path}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure boot system on {device}. Error:\n{e}")

def configure_banner(device, banner_text):
    """ Config Day banner
        Args:
            device (`obj`): Device object
            banner_text (`str`): Banner text
        Return:
            None
        Raise:
            SubCommandFailure: Failed configuring Day banner
    """

    try:
        device.configure("banner motd {banner_text}".format(banner_text=banner_text))
    except SubCommandFailure as e:
        raise SubCommandFailure(
            'Could not configure banner {banner_text}, Error: {error}'.format(
                banner_text=banner_text, error=e)
        )

def unconfigure_snmp_mib_bulkstat(device, object_name, schema_name, transfer_name):
    
    """ unconfigure snmp mib bulkstat
    Args:
        device ('obj'): device to use
        object_name ('str'): The name of the object 
        schema_name ('str'): The name of the schema 
        transfer_name ('str'): bulkstat transfer name 
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = [
        f"bulkstat profile {transfer_name}",
        f"no enable",
        "exit",
        f"no snmp mib bulkstat object-list {object_name}",
        f"no snmp mib bulkstat schema {schema_name}",
        f"no snmp mib bulkstat transfer {transfer_name}",
 
        ]
        
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to unconfigure snmp mib bulkstat on this device. Error:\n{e}")
        

def configure_stackpower_stack(device, powerstack_name, mode=None, strict=False):
    """ Configures power stack mode on stack-power stack
        
        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
            mode ('str', optional): Power stack mode. Default is None
            strict ('bool', optional): Strict mode. Default is False
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = [f'stack-power stack {powerstack_name}']

    if mode:
        command = f'mode {mode}'
        if strict:
            command += ' strict'
        cmd.append(command)
    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stackpower stack on device {device.name}. Error:\n{e}")


def unconfigure_stackpower_stack(device, powerstack_name):
    """ Configures power stack mode on stack-power stack
        
        Args:
            device ('obj'): device to use
            powerstack_name ('str'): Power stack name - Up to 31 chars
        Returns:
            None
        Raises:
            SubCommandFailure
    """
      
    cmd = [f'no stack-power stack {powerstack_name}']

    try:
        device.configure(cmd)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure stackpower stack on device {device.name}. Error:\n{e}")


def configure_graceful_reload(device, interval=5):
    """ Configure graceful-reload
        Args:
            device ('obj'): Device object
            interval('int', optional): <1-900>, Default is 5
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"graceful-reload interval {interval}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Failed to configure graceful-reload. Error:\n{e}")   

def unconfig_cns_agent_password(device, cns_password=None):
    """ un configure cns agent password
        Args:
            device ('obj'): Device object
            cns_password ('str', optional): Cns agent password. Default is None
        Returns:
            None
        Raise:
            SubCommandFailure: Failed to un configure cns agent password
    """
    log.debug("un configure cns agent password")
    try:
        if cns_password:
            device.configure("no cns password {cns_password}".format(cns_password=cns_password))
        else:
            device.configure("no cns password")
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not un configure cns agent password. Error:\n{e}")


def configure_boot_system_image_file(device, image_path, switch_number=None):
    """ Configure boot system image file
        Args:
            device ('obj'): Device object
            image_path ('str'): full image path. Ex: flash:cat9k_17467.SSA.pkg
            switch_number ('str', optional): switch number or all. Default is None
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"boot system{f' switch {switch_number}' if switch_number else ''} {image_path}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure boot system on {device}. Error:\n{e}")


def hw_module_beacon_RP_active_standby(device, supervisor, operation):
    """ ON/OFF beacon supervisor
        Args:
            device ('obj'): Device object
            supervisor('str'): active/standby
            operation('str'): ON/OFF
            
    """
    
    cmd = (f"hw-module beacon RP {supervisor} {operation}")
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f'Failed to turn {operation} the {supervisor} beacon slot. Error:\n{e}')
