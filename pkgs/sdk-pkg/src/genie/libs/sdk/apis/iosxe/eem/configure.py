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
