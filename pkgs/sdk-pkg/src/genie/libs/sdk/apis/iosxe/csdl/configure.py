'''IOSXE execute functions for csdl'''

# Python
import logging
import time

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def unconfigure_service_private_config_encryption(device):
    """ 
        no service private-config-encryption
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    cmd = [f"no service private-config-encryption"]

    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unconfigure encryption on device {device}. Error:\n{e}")

# service private-config-encryption
def configure_service_private_config_encryption(device):
    """ 
        service private-config-encryption
        Args:
            device ('obj'): Device object
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        device.configure([f'service private-config-encryption'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure encryption on device {device}. Error:\n{e}")
    
#  snmp_server_engine_id_local
def snmp_server_engine_id_local(device, engine_id):
    """ 
        snmp-server engineID local
        Args:
            device ('obj'): Device object
            engine_id('str') : engineID
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        device.configure([f'snmp-server engineID local {engine_id}'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure snmp-server on device {device}. Error:\n{e}")

#  cry key generate rsa encryption mod {mod} label {label}
def cry_key_generate_rsa_encryption(device, mod, label):
    """ 
        cry key generate rsa encryption
        Args:
            device ('obj'): Device object
            mod('str') : mod , (512-4096) 
            label('str') : label -- name for keys
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        device.configure([f'cry key generate rsa encryption mod {mod} label {label}'])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to generate rsa on device {device}. Error:\n{e}")    

# no hw-module switch <num> usbflash1-password
def unconfigure_hw_module_switch_number_usbflash(device, switch_number):

    """ unconfigure_hw_module_switch_num_usbflash
        Args:
            device ('obj'): device to use
            switch_number ('str'): switch number
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        cmd = [f"no hw-module switch {switch_number} usbflash1-password"]
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to unset hw-module on device {device}. Error:\n{e}")    

# hw-module switch <num> usbflash1-password
def configure_hw_module_switch_number_usbflash(device, switch_number,password):

    """ configure_hw_module_switch_num_usbflash
        Args:
            device ('obj'): device to use
            switch_number ('str'): switch number
            password ('str'): password(atleast 8 character long)
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        cmd = [f"hw-module switch {switch_number} usbflash1-password {password}"]
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure hw-module on device {device}. Error:\n{e}")

# device-sensor filter-list lldp list
def configure_device_sensor_filter_list_lldp(device):

    """ configure device-sensor filter-list lldp list  
        Args:
            device ('obj'): device to  be used    
        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    try:
        device.configure([
            "device-sensor filter-list lldp list system-name","device-sensor filter-list lldp list system-description","device-sensor filter-list lldp list system-capabilities"
        ])
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Failed to configure device-sensor on device {device}. Error:\n{e}")
def hw_module_switch_num_usbflash_security_password(device, switch_number, action, pwd):
   
    """  configure hw-module switch <switch_number> usbflash1 security enable or diasble password
            Args:
            device ('obj'): device to use
            switch_number ('str'): switch number
            action ('str') : enable or disable
            pwd ('str') : password

        Returns:
            None
        Raises:
            SubCommandFailure exception
    """
    cmd = [f"hw-module switch {switch_number} usbflash1 security {action} password {pwd}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not {action} hw-module on device {device}. Error:\n{e}")



