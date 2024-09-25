'''IOSXE execute functions for platform'''

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure
from unicon.eal.dialogs import Dialog, Statement

# Logger
log = logging.getLogger(__name__)

def configure_smartpower_domain(device, domain_name, security_level, password, protocol, port):
    """ SmartPower Domain
        Args:
            device ('obj'): Device object
            domain_name('str'): domain name
            security_level('str'): security level
            password('str'): password
            protocol('str'): protocol
            port('int'): port
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"smartpower domain {domain_name} security {security_level} {password} protocol {protocol} port {port}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower Domain {device}. Error:\n{e}"
        )

def unconfigure_smartpower_domain(device, domain_name, security_level, password, protocol, port):
    """ SmartPower Domain
        Args:
            device ('obj'): Device object
            domain_name('str'): domain name
            security_level('str'): security level
            password('str'): password
            protocol('str'): protocol
            port('int'): port
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    cmd = f"no smartpower domain {domain_name} security {security_level} {password} protocol {protocol} port {port}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower Domain {device}. Error:\n{e}"
        )


def configure_smartpower_importance(device, importance_value):
    """
    Args:
        device ('obj'): Device object
        importance_value('int'): importance value : Range <1-100>
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    importance_value = int(importance_value)
    if not 1 <= importance_value <= 100:
        raise SubCommandFailure(
            f"The importance value provided for {device} is outside the range of <1-100>"
        )
    cmd = f"smartpower importance {importance_value}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower Importance {device}. Error:\n{e}"
        )

def unconfigure_smartpower_importance(device, importance_value):
    """
    Args:
        device ('obj'): Device object
        importance_value('int'): importance value : Range <1-100>
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    importance_value = int(importance_value)
    if not 1 <= importance_value <= 100:
        raise SubCommandFailure(
            f"The importance value provided for {device} is outside the range of <1-100>"
        )
    cmd = f"no smartpower importance {importance_value}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not unconfigure SmartPower Importance {device}. Error:\n{e}"
        )


def configure_smartpower_name(device, name):
    """
    Args:
        device ('obj'): Device object
        name('str'): name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"smartpower name {name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower Name {device}. Error:\n{e}"
        )

def unconfigure_smartpower_name(device, name):
    """
    Args:
        device ('obj'): Device object
        name('str'): name
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no smartpower name {name}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure SmartPower Name {device}. Error:\n{e}"
        )

def configure_smartpower_role(device, role):
    """
    Args:
        device ('obj'): Device object
        role('str'): role
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"smartpower role {role}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower Role {device}. Error:\n{e}"
        )

def unconfigure_smartpower_role(device, role):
    """
    Args:
        device ('obj'): Device object
        role('str'): role
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no smartpower role {role}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure SmartPower Role {device}. Error:\n{e}"
        )



def configure_smartpower_keywords(device, keywords):
    """
    Args:
        device ('obj'): Device object
        keywords('str'): keywords
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"smartpower keywords {keywords}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower Keywords {device}. Error:\n{e}"
        )

def unconfigure_smartpower_keywords(device, keywords):
    """
    Args:
        device ('obj'): Device object
        keywords('str'): keywords
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no smartpower keywords {keywords}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure SmartPower Keywords {device}. Error:\n{e}"
        )


def configure_smartpower_level(device, level):
    """
    Args:
        device ('obj'): Device object
        level('int'): level : Range <0-10>
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    level = int(level)
    if not 0 <= level <= 10:
        raise SubCommandFailure(
            f"The level value provided for {device} is outside the range of <1-10>"
        )
    cmd = f"smartpower level {level}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower Level {device}. Error:\n{e}"
        )

def unconfigure_smartpower_level(device, level):
    """
    Args:
        device ('obj'): Device object
        level('int'): level : Range <0-10>
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    level = int(level)
    if not 0 <= level <= 10:
        raise SubCommandFailure(
            f"The level value provided for {device} is outside the range of <1-10>"
        )
    cmd = f"no smartpower level {level}"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure SmartPower Level {device}. Error:\n{e}"
        )


def configure_smartpower_domain_default (device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "default smartpower domain"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"could not configure SmartPower domain {device}. Error:\n{e}"
        )

def configure_smartpower_endpoint_default (device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "default smartpower endpoint"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower endpoint {device}. Error:\n{e}")


def configure_smartpower_importance_default (device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "default smartpower importance"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower importance {device}. Error:\n{e}")


def configure_smartpower_keywords_default (device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = "default smartpower keywords"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(f"Could not configure SmartPower keywords {device}. Error:\n{e}")

def configure_smartpower_level_default(device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"default smartpower level"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower level {device}. Error:\n{e}"
        )

def configure_smartpower_management_default(device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"default smartpower management"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower management {device}. Error:\n{e}"
        )

def configure_smartpower_name_default(device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"default smartpower name"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower name {device}. Error:\n{e}"
        )

def configure_smartpower_role_default(device):
    """
    Args:
        device ('obj'): Device object
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"default smartpower role"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure SmartPower role {device}. Error:\n{e}"
        )

def configure_ecomode_optics(device, switch_number):
    """
    Args:
        device ('obj'): Device object
        switch_number('int'): switch number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"hw-module switch {switch_number} ecomode optics"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure serdes shutdown {device}. Error:\n{e}"
        )

def unconfigure_ecomode_optics(device, switch_number):
    """
    Args:
        device ('obj'): Device object
        switch_number('int'): switch number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no hw-module switch {switch_number} ecomode optics"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure serdes shutdown {device}. Error:\n{e}"
        )

def configure_auto_off_optics(device, switch_number):
    """
    Args:
        device ('obj'): Device object
        switch_number('int'): switch number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"hw-module switch {switch_number} auto-off optics"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not configure serdes shutdown {device}. Error:\n{e}"
        )

def unconfigure_auto_off_optics(device, switch_number):
    """
    Args:
        device ('obj'): Device object
        switch_number('int'): switch number
    Returns:
        None
    Raises:
        SubCommandFailure
    """
    cmd = f"no hw-module switch {switch_number} auto-off optics"
    try:
        device.configure(cmd)
    except SubCommandFailure as e:
        raise SubCommandFailure(
            f"Could not unconfigure serdes shutdown {device}. Error:\n{e}"
        )






