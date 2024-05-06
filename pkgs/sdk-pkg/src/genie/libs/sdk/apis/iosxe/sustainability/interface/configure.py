'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_smartpower_interface_endpoint_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower endpoint",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower endpoint {device}. Error:\n{e}")
    

def configure_smartpower_interface_importance_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower importance",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower importance {device}. Error:\n{e}")


def configure_smartpower_interface_keywords_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower keywords",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower keywords {device}. Error:\n{e}")


def configure_smartpower_interface_level_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower level",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower level {device}. Error:\n{e}"
        )


def configure_smartpower_interface_management_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower management",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower management {device}. Error:\n{e}")
    

def configure_smartpower_interface_name_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower name",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower name {device}. Error:\n{e}"
        )


# def configure_smartpower_interface_neighbor_default (device, interface):
#     """
#     Args:
#         device ('obj'): Device object
#         interface('str'): interface
#     Returns:
#         None
#     Raises:
#         SubCommandFailure
#     """
#     cmd = [f"interface {interface}",
#            "default smartpower neighbor",
#            ]
#     try:
#         device.configure(cmd)
#     except SubCommandFailure as e:
#         raise SubCommandFailure(f"Could not configure SmartPower neighbor {device}. Error:\n{e}")


def configure_smartpower_interface_role_default (device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        role('str'): role.
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "default smartpower role",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower role {device}. Error:\n{e}"
        )

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
    cmd = [f"interface {interface}",
           f"smartpower level {level}",
           ]
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
    cmd = [f"interface {interface}",
           f"no smartpower level {level}",
           ]
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
    cmd = [f"interface {interface}",
           f"smartpower name {name}",
           ]
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
    cmd = [f"interface {interface}",
           f"no smartpower name {name}",
           ]
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
    cmd = [f"interface {interface}",
           f"smartpower role {role}",
           ]
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
    cmd = [f"interface {interface}",
           f"no smartpower role {role}",
           ]
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
    cmd = [f"interface {interface}",
           "default smartpower domain",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower domain {device}. Error:\n{e}"
        )

def configure_smartpower_activitycheck(device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailuregit
    """
    cmd = [f"interface {interface}",
           "smartpower activitycheck"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower activitycheck {device}. Error:\n{e}"
        )

def unconfigure_smartpower_activitycheck(device, interface):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           "no smartpower activitycheck"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower activitycheck {device}. Error:\n{e}")

def configure_smartpower_interface_importance (device, interface, importance_value):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        importance_value('int'): importance value (Range 1-100)
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    importance_value = int(importance_value)
    if not 1 <= importance_value <= 100:
        raise ValueError(
            f"The importance value provided for {device} is outside the range of <1-100>"
        )
    cmd = [f"interface {interface}",
           f"smartpower importance {importance_value}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower importance {device}. Error:\n{e}"
        )

def unconfigure_smartpower_interface_importance (device, interface, importance_value):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        importance_value('int'): importance value (Range 1-100)
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    importance_value = int(importance_value)
    if not 1 <= importance_value <= 100:
        raise ValueError(
            f"The importance value provided for {device} is outside the range of <1-100>"
        )
    cmd = [f"interface {interface}",
           f"no smartpower importance {importance_value}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower importance {device}. Error:\n{e}"
        )

def configure_smartpower_interface_keywords (device, interface, keywords):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        keywords('str'): SmartPower keywords associated with this entity
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           f"smartpower keywords {keywords}",
           ]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower keywords {device}. Error:\n{e}"
        )

def unconfigure_smartpower_interface_keywords (device, interface, keywords):
    """
    Args:
        device ('obj'): Device object
        interface('str'): interface
        keywords('str'): SmartPower keywords associated with this entity
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = [f"interface {interface}",
           f"no smartpower keywords {keywords}"]
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower keywords {device}. Error:\n{e}"
        )
