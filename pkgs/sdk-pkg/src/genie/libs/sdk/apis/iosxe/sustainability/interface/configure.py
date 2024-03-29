'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_smartpower_interface_level (device, interface, level):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        level('int'): level (Range 0-10)
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    level = int(level)
    if not 0 <= level <= 10:
        raise SubCommandFailure(
            f"The level value provided for {device} is outside the range of <0-10>"
        )
    cmd = f"interface {interface} ; smartpower level {level}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower level {device}. Error:\n{e}"
        )

def unconfigure_smartpower_interface_level (device, interface, level):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        level('int'): level (Range 0-10)
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    level = int(level)
    if not 0 <= level <= 10:
        raise SubCommandFailure(
            f"The level value provided for {device} is outside the range of <0-10>"
        )
    cmd = f"interface {interface} ; no smartpower level {level}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower level {device}. Error:\n{e}"
        )
    
def configure_smartpower_interface_name (device, interface, name):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        name('str'): name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"interface {interface} ; smartpower name {name}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower name {device}. Error:\n{e}"
        )

def unconfigure_smartpower_interface_name (device, interface, name):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        name('str'): name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"interface {interface} ; no smartpower name {name}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower name {device}. Error:\n{e}"
        )

def configure_smartpower_interface_role (device, interface, role):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        role('str'): role
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"interface {interface} ; smartpower role {role}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower role {device}. Error:\n{e}"
        )

def unconfigure_smartpower_interface_role (device, interface, role):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        role('str'): role
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"interface {interface} ; no smartpower role {role}" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower role {device}. Error:\n{e}"
        )

def configure_smartpower_interface_domain_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"interface {interface} ; default smartpower domain" # ; works as a command seperator
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower domain {device}. Error:\n{e}"
        )
