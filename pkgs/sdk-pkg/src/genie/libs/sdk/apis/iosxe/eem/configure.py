import jinja2

# Unicon
from unicon.core.errors import SubCommandFailure

# Eem
from genie.libs.sdk.apis.iosxe.eem.verify import is_eem_applet_configured


# Jinja2
from jinja2.exceptions import TemplateNotFound


def remove_eem_applet(device, applet_name):
    """ Remove EEM applet from running config

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
        Raises:
            SubCommandFailure
        Returns:
            None
    """

    if is_eem_applet_configured(device=device, applet_name=applet_name):

        try:
            device.configure(
                "no event manager applet {name}".format(name=applet_name)
            )
        except Exception:
            raise SubCommandFailure(
                "Could not remove EEM applet {name} from device "
                "{dev} configuration".format(name=applet_name, dev=device.name)
            )


def configure_eem_applet_watchdog_time(device,applet_name,watchdog_time):
    """ Configure EEM applet watchdog time

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
            watchdog_time('int') : watchdog time in seconds
        Raises:
            SubCommandFailure
        Returns:
            None
    """
    cmd = [f"event manager applet {applet_name}",f"event timer watchdog time {watchdog_time}"]

    try:
        device.configure(cmd)
    except Exception:
        raise SubCommandFailure(
                "could not configure EEM applet watchdog time"
        )

def configure_eem_action_cli_command(device,applet_name,action_label,cli_command):
    """ Configure EEM applet watchdog time

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
            action_label('str') : action label
            cli_command ('str') : cli command
        Raises:
            SubCommandFailure
        Returns:
            None
    """
    cmd = [f"event manager applet {applet_name}",f"action {action_label} cli command \"{cli_command}\""]

    try:
        device.configure(cmd)
    except Exception:
        raise SubCommandFailure(
                "could not configure EEM applet cli command"
        )
        

def configure_eem_action_syslog_msg(device,applet_name,action_label,syslog_msg):
    """ Configure EEM applet watchdog time

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
            action_label('str') : action label
            syslog_msg('str') : syslog msg
        Raises:
            SubCommandFailure
        Returns:
            None
    """
    cmd = [f"event manager applet {applet_name}",f"action {action_label} syslog msg \"{syslog_msg}\""]

    try:
        device.configure(cmd)
    except Exception:
        raise SubCommandFailure(
                "could not configure EEM applet syslog message"
        )

def configure_eem_action_wait(device,applet_name,action_label,wait_time):
    """ Configure EEM applet watchdog time

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
            action_label('str') : action label
            wait_time('str') : wait time
        Raises:
            SubCommandFailure
        Returns:
            None
    """
    cmd = [f"event manager applet {applet_name}",f"action {action_label} wait {wait_time}"]

    try:
        device.configure(cmd)
    except Exception:
        raise SubCommandFailure(
                "could not configure EEM applet wait time"
        )


def configure_eem_action_info_type_routername(device,applet_name,action_label):
    """ Configure EEM applet watchdog time

        Args:
            device ('obj'): Device object
            applet_name ('str'): Applet name
            action_label('str') : action label
        Raises:
            SubCommandFailure
        Returns:
            None
    """
    cmd = [f"event manager applet {applet_name}",f"action {action_label} info type routername"]

    try:
        device.configure(cmd)
    except Exception:
        raise SubCommandFailure(
                "could not configure EEM applet info type routername"
        )

        
