import logging
from unicon.core.errors import SubCommandFailure
from pyats.aetest.steps import Steps
from genie.conf.base import Interface

log = logging.getLogger(__name__)

def configure_controller_shutdown(device, interface, shutdown=True):
    """ Configures the shutdown/no shutdown for VDSL interface
        Args:
            device ('obj'): device to use
            interface ('str'): controller vdsl interface
            shutdown ('bool', optional) : true/false need to be send. default is false/Shutdown
        Returns:
            None
        Raises:
            SubCommandFailure
    """
    
    cmd = 'shutdown' if shutdown else 'no shutdown'
    log.debug(f"Configuring VDSL interface {cmd} on device {device}")

    try:
        device.configure(
            "Controller VDSL {interface}\n"
            "{cmd}".format(interface=interface,cmd=cmd))
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure controller VDSL shutdown/no shutdown. Error:\n{error}".format(error=e))

def configure_controller_vdsl(
        device,
        interface,
        description_str=None,
        op_mode_config=None,
        sra_config=None,
        bandwidth_set_config=None,
        firmware_config=None,
        training_config=None,
        modem_config=None,
        diagnostics_config=None,
    ):
    """ Configures the controller VDSL
        Args:
            device ('obj'): device to use
            interface ('str'): controller VDSL interface
            description_str ('str', optional): description of VDSL controller in string, default is none
            op_mode_config ('str', optional): Operating mode of VDSL in string, default is none
            sra_config ('str', optional) : sra config. default is none
            bandwidth_set_config ('str', optional): bandwidth-set config, Eg: bandwidth-set 11000 5000, default is none
            firmware_config ('str', optional): firmware filename(Eg: firmware phy filename bootflash:nim_vab_phy_fw_A38q_B39x3.pkg), default is none
            training_config ('str', optional): training log filename (Eg: training log filename bootflash:test.log), default is none
            modem_config ('str', optional): modem config, default is none
            diagnostics_config ('str', optional) : diagnostics DELT config. default is none
        Returns:
            None
        Raises:
            SubCommandFailure
    """

    config = [f"controller VDSL {interface}"]
    if description_str:
        config.append(f'{description_str}')
    
    if op_mode_config:
        config.append(f'{op_mode_config}')

    if sra_config:
        config.append(f'{sra_config}')

    if bandwidth_set_config:
        config.append(f'{bandwidth_set_config}')

    if firmware_config:
        config.append(f'{firmware_config}')

    if training_config:
        config.append(f'{training_config}')

    if modem_config:
        config.append(f'{modem_config}')

    if diagnostics_config:
        config.append(f'{diagnostics_config}')

    log.debug(f"Configuring VDSL controller on device {device}")

    try:
        device.configure(config)
    except SubCommandFailure as e:
        raise SubCommandFailure("Could not configure VDSL controller. Error:\n{error}".format(error=e))
