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

def unconfigure_system_ignore_startupconfig_switch_all(device):
    """ Unconfigure system ignore startupconfig switch all
    Args:
        device ('obj'): device to use

        Returns:
            None
        Raises:
            SubCommandFailure
    """
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
                action="sendline()",
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
                action="sendline()",
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
                action="sendline()",
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

def configure_system_ignore_startupconfig_switch_all(device):
    """ Configures the system ignore startup configuration on the switch
        Example: system ignore startupconfig switch all
        
        Args:
            device('obj'): device to configure on

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Configuring system ignore startup config on {device.name}")
    config = 'system ignore startupconfig switch all'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not configure system ignore startup configuration on device {device.name}. Error:\n{e}")

def unconfigure_system_ignore_startupconfig_switch_all(device):
    """ Unconfigures the system ignore startup configuration on the switch
        Example: no system ignore startupconfig switch all
        
        Args:
            device('obj'): device to configure on

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """
    log.info(f"Unconfiguring system ignore startup config on {device.name}")
    config = 'no system ignore startupconfig switch all'
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

def configure_system_disable_password_recovery_switch_all(device):
    """ Disables password recovery on the switch
        Example: system disable password recovery switch all
        
        Args:
            device('obj'): device to configure on

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(f"Disable password recovery switch all on {device.name}")
    config = 'system disable password recovery switch all'
    try:
        device.configure(config)
    except SubCommandFailure as e:
        log.error(e)
        raise SubCommandFailure(f"Could not disable password recovery switch all on device {device.name}. Error:\n{e}")

def unconfigure_system_disable_password_recovery_switch_all(device):
    """ Enables password recovery on the switch
        Example: no system disable password recovery switch all
        
        Args:
            device('obj'): device to configure on

        Return:
            N/A

        Raises:
            SubCommandFailure: Failed executing command
    """

    log.info(f"Enables password recovery switch all on {device.name}")
    config = 'no system disable password recovery switch all'
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

def unconfigure_source_template(device, template_name, source_template):
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