# Running config
from genie.libs.sdk.apis.iosxe.running_config.get import (
    get_running_config,
)


def is_eem_applet_configured(device, applet_name):
    """ Verify if EEM applet is configured in running config

        Args:
            device ('obj') : Device object
            applet_name ('str') : Applet name
        Returns:
            True
            False
        Raises:
            None
    """

    keyword = "event manager applet {name}".format(name=applet_name)

    try:

        running_config = get_running_config(
            device=device, keyword=keyword
        )
    except Exception:
        return False

    return True
