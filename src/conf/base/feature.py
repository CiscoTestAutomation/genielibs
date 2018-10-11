__all__ = (
    'DeviceFeature',
    'LinkFeature',
    'InterfaceFeature',
    'consolidate_feature_args',
)

from genie.conf.base import DeviceFeature, LinkFeature, InterfaceFeature

def consolidate_feature_args(feature, devices=None, interfaces=None, links=None):
    '''Consolidate feature arguments.

    Example::

        devices, interfaces, links = consolidate_feature_args(
            feature_obj, devices=devices, links=links)

    Returns:
        3-`tuple` of `set` of devices, interfaces, and links
    '''

    if devices is None and interfaces is None and links is None:
        # No parameters specified, use defaults from feature.
        devices = feature.devices if isinstance(feature, DeviceFeature) else ()
        interfaces = feature.interfaces if isinstance(feature, InterfaceFeature) else ()
        links = feature.links if isinstance(feature, LinkFeature) else ()
    else:
        # Some parameters specified, just replace None values
        devices = devices or ()
        interfaces = interfaces or ()
        links = links or ()

    # Convert all to sets
    devices = set(devices)
    interfaces = set(interfaces)
    links = set(links)

    # Expand links into interfaces and then into devices
    interfaces.update(*(link.interfaces for link in links))
    devices.update(interface.device for interface in interfaces)

    return devices, interfaces, links

