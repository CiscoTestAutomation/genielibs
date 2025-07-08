'''IOSXE execute functions for IIOT platform'''

# Python
import re
import logging
import time

# pyATS
from pyats.async_ import pcall
from pyats.utils.fileutils import FileUtils

# Genie
from genie.utils import Dq
from genie.harness.utils import connect_device
from genie.utils.timeout import Timeout
from genie.metaparser.util.exceptions import SchemaEmptyParserError

# Unicon
from unicon.eal.dialogs import Statement, Dialog
from unicon.core.errors import StateMachineError,SubCommandFailure

# Logger
log = logging.getLogger(__name__)

def execute_set_config_register():
    '''Set config register to load image in boot variable        
    '''

    log.info("Config register configuration not supported on IOT platforms")


def execute_locate_switch(device, seconds, switch_number=None, switch_type=None):
    """ Execute locate switch
        Args:
            device ('obj'): Device object
            switch_number ('int'): Switch number
            seconds ('str'): Time in seconds
            switch_type ('str'): Switch type(active/standby)
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    if switch_number:
        cmd = f"locate-switch {switch_number} {seconds}"
    elif switch_type:
        cmd = f"locate-switch {switch_type} {seconds}"
    else:
        cmd = f"locate-switch {seconds}"
    
    try:
        device.execute(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute locate switch on {device.name}. Error:\n{e}"
        )
    

def execute_reload_verify(device, prompt_wait_time=10, timeout=600):
    """ Execute reload verify
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = "reload /verify"
    try:
        device.reload(reload_command=cmd, prompt_recovery=True, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute reload verify on {device.name}. Error:\n{e}"
        )


def execute_reload_noverify(device, prompt_wait_time=10, timeout=600):
    """ Execute reload noverify
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = "reload /noverify"
    
    try:
        device.reload(reload_command=cmd, prompt_recovery=True, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute reload noverify on {device.name}. Error:\n{e}"
        )
    
    
def execute_factory_reset(device,
                          reset_all=False,
                          secure=False,
                          three_pass=False,
                          boot_vars=None,
                          config=None,
                          switch_number=None,
                          all_switches=False,
                          keep_licensing_info=False,
                          prompt_wait_time=10,
                          timeout=600,
                          boot_partition=None,
                          image=None,
                          password=None,
                          hostname=None,
                          enable_password=None,
                          enable_secret=None,
                          interface=None,
                          interface_ip=None,
                          interface_mask=None):
    """
    Execute factory reset on the device based on the given parameters.

    Args:
        device ('obj'): Device object
        reset_all ('bool'): Reset all configuration
        secure ('bool'): Secure reset
        three_pass ('bool'): Three-pass secure reset(5220.22-M 3-pass overwrite)
        boot_vars ('str'): Reset user added boot variables
        config ('str'): Reset configuration
        switch_number ('int'): Switch number to reset(1 or All)
        all_switches ('bool'): Reset all switches
        keep_licensing_info ('bool'): Keep licensing information
        prompt_wait_time ('int'): Time to wait before sending a prompt
        timeout ('int'): Timeout for the factory reset operation in seconds
        boot_partition ('str'): Boot partition(Eg: emgy0)
        image ('str'): Image to boot
        password ('str'): Password
        hostname ('str'): Hostname
        enable_password ('str'): Enable password
        enable_secret ('str'): Enable secret
        interface ('str'): Management interface name
        interface_ip ('str'): Interface IP address
        interface_mask ('str'): Interface subnet mask

    Returns:
        None
    Raises:
        SubCommandFailure
    """

    def slow_sendline(spawn):
        time.sleep(prompt_wait_time)
        spawn.sendline("")

    def send_password(spawn):
        time.sleep(1)
        spawn.sendline(password)

    def send_enable(spawn):
        spawn.sendline("enable")

    def send_boot(spawn):
        spawn.sendline(f"boot {boot_partition}:{image}")

    def send_hostname(spawn):
        spawn.sendline(f"hostname {hostname}")

    def send_enable_password(spawn):
        spawn.sendline(f"enable password {enable_password}")

    def send_enable_secret(spawn):
        spawn.sendline(f"enable secret {enable_secret}")

    def send_interface(spawn):
        spawn.sendline(f"{interface}")

    def send_interface_ip(spawn):
        spawn.sendline(f"{interface_ip}")

    def send_interface_mask(spawn):
        spawn.sendline(f"{interface_mask}")

    def send_select(spawn):
        spawn.sendline("0")

    cmd_reset = None
    pattern_fragment = None

    try:
        # Build correct reset command
        if reset_all and secure and three_pass:
            if all_switches:
                cmd_reset = "factory-reset switch all all secure 3-pass"
            elif switch_number is not None:
                cmd_reset = f"factory-reset switch {switch_number} all secure 3-pass"
            else:
                cmd_reset = "factory-reset all secure 3-pass"
            pattern_fragment = "securely reset all"

        elif reset_all and secure:
            cmd_reset = "factory-reset all secure"
            pattern_fragment = "securely reset all"

        elif reset_all:
            cmd_reset = "factory-reset all"
            pattern_fragment = "all operations"

        elif boot_vars is not None:
            cmd_reset = f"factory-reset boot-vars {boot_vars}"
            pattern_fragment = "boot variables"

        elif config is not None:
            cmd_reset = f"factory-reset config {config}"
            pattern_fragment = "configuration"

        elif keep_licensing_info:
            cmd_reset = "factory-reset keep-licensing-info"
            pattern_fragment = "licensing information"

        else:
            raise ValueError("Invalid combination of reset options")
        
        # Dialog to match the logs
        dialog = Dialog([
            Statement(
                pattern=r"Do you still want to proceed with the secure factory reset operation\? \[no\]:",
                action=lambda spawn: spawn.sendline("yes"),
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=fr"The factory reset operation is irreversible for {pattern_fragment}.*\[confirm\]",
                action=lambda spawn: spawn.sendline(""),
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"Are you sure you want to continue\? \[confirm\]",
                action=lambda spawn: spawn.sendline(""),
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"switch:\s*$",
                action=send_boot,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                # More specific pattern for "initial configuration dialog"
                pattern=r".*Would you like to enter the initial configuration dialog\? \[yes/no\]:\s*$",                
                action=lambda spawn: spawn.sendline("no"),
                loop_continue=False, # Set to False to move past this prompt once answered
                continue_timer=False,
            ),
            Statement(
                # More specific pattern for "basic management setup"
                pattern=r"Would you like to enter basic management setup\? \[yes/no\]:\s",
                action=lambda spawn: spawn.sendline("no"),
                loop_continue=False, # Set to False to move past this prompt once answered
                continue_timer=False
            ),
            Statement(
                pattern=r".*Enter host name \[.*\]: ",
                action=send_hostname,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"Enter enable secret:",
                action=send_enable_secret,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"Confirm enable secret:",
                action=send_enable_secret,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"Enter enable password:",
                action=send_enable_password,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"Enter virtual terminal password:",
                action=send_password,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"(?s)Enter interface name.*interface summary:",
                action=send_interface,
                loop_continue=True,
                continue_timer=True
            ),
            Statement(
                pattern=r"IP address for this interface \[.*\]:",
                action=send_interface_ip,
                loop_continue=True,
                continue_timer=True,
            ),
            Statement(
                pattern=r"IP address for this interface: ",
                action=send_interface_ip,  # Accept default
                loop_continue=False,
                continue_timer=False,
            ),
            Statement(
                pattern=r"Subnet mask for this interface \[.*\] :",
                action=send_interface_mask,  # Accept default
                loop_continue=False,
                continue_timer=False,
            ),
            Statement(
                pattern=r"Enter your selection \[2\]:",
                action=send_select, 
                loop_continue=False,
                continue_timer=False
            ),
            Statement(
                pattern=r"Press RETURN to get started!",
                action=slow_sendline,
                loop_continue=False,
                continue_timer=False
            ),
            Statement(
                pattern=r">",
                action=send_enable,
                loop_continue=False,
                continue_timer=False
            )
        ])
        
        device.execute(cmd_reset, reply=dialog, timeout=timeout)

    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute factory reset on {device.name}. Error:\n{e}"
        )

        
def execute_copy_verify(device, source, dest, timeout=300, file_name=None):
    """ Execute copy verify
        Args:
            device ('obj'): Device object
            source ('str'): Source file
            dest ('str'): Destination file
            timeout ('int'): Timeout for the copy operation in seconds. Default is 300s
            file_name ('str'): Optional. If provided, appends the file name to source and destination.
            Returns:
            None
        Raises:
            SubCommandFailure
    """
            
    dialog = Dialog([
        # Handle destination filename prompt
        Statement(
            pattern=r"Destination filename \[.*\]\?",
            action='sendline()',
            loop_continue=True,
            continue_timer=True
        ),
        # Handle overwrite confirmation prompt
        Statement(
            pattern=r"%Warning:.*existing with this name\s+Do you want to over write\? \[confirm\]",
            action='sendline()',
            loop_continue=True,
            continue_timer=True
        ),
     ])

    if file_name:
        source = f"{source}:{file_name}"
        dest = f"{dest}:{file_name}"

    cmd = f"copy /verify {source} {dest}"
    
    try:
        device.execute(cmd, reply=dialog, timeout=timeout, error_pattern=[r'%ERROR:.*Aborting copy.'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Error while executing {cmd} on {device.name}. Error:\n{e}"
        )

def execute_copy_noverify(device, source, dest, timeout=300, file_name=None):
    """ Execute copy noverify
        Args:
            device ('obj'): Device object
            source ('str'): Source file
            dest ('str'): Destination file
            timeout ('int'): Timeout for the copy operation in seconds. Default is 300s
            file_name ('str'): Optional. If provided, appends the file name to source and destination.
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    dialog = Dialog([
        # Handle destination filename prompt
        Statement(
            pattern=r"Destination filename \[.*\]\?",
            action='sendline()',
            loop_continue=True,
            continue_timer=True
        ),
        # Handle overwrite confirmation prompt
        Statement(
            pattern=r"%Warning:.*existing with this name\s+Do you want to over write\? \[confirm\]",
            action='sendline()',
            loop_continue=True,
            continue_timer=True
        ),
    ])

    if file_name:
        source = f"{source}:{file_name}"
        dest = f"{dest}:{file_name}"

    cmd = f"copy /noverify {source} {dest}"

    try:
        device.execute(cmd, reply=dialog, timeout=timeout)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to execute copy noverify on {device.name}. Error:\n{e}"
        )

