"""Utility type functions for Platform"""
from ...iosxe.platform.utils import write_erase_reload_device_without_reconfig \
    as iosxe_write_erase_reload_device_without_reconfig

def write_erase_reload_device_without_reconfig(
    device,
    via_console,
    reload_timeout,
    username=None,
    password=None,
    reload_creds=None,
    reload_hostname='Router',
    sleep_after_reload=15
):
    """Execute 'write erase' on device and reload without reconfiguring.

        Args:
            device(`obj`): Device object
            via_console(`str`): Via to use to reach the device console.
            reload_timeout(`int`): Maximum time to wait for reload to complete
            reload_creds(`str or list`): Creds to apply if reloading device asks
            sleep_after_reload (int, optional): Amount of time to sleep after reload.
                Defaults to 15 seconds.
    """
    return iosxe_write_erase_reload_device_without_reconfig(
        device=device,
        via_console=via_console,
        reload_timeout=reload_timeout,
        username=username,
        password=password,
        reload_creds=reload_creds,
        reload_hostname=reload_hostname,
        sleep_after_reload=sleep_after_reload)
