'''IOSXE execute functions for platform'''

# Python
import logging

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