"""Common configure functions for control-plane"""
# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)


def configure_control_plane_control_plane_policy(device, config):

    """ Configure control plane policy

        Args:
            device ('obj'): Device object
            config('list'): List of commands to configure
                ex.)
                    [
                        {
                            'policy_name': 'Control_Plane_In',
                            'remove': False
                        },
                        {
                            'policy_name': 'Control_Plane_In',
                            'remove': True
                        }
                    ]
        Returns:
            None
        Raises:
            SubCommandFailure: Failed configuring control plane policy

    """

    conf = []
    conf.append("control-plane\n")
    for c in config:
        if "remove" in c:
            conf.append(
                "no service-policy input {}\n".format(c["policy_name"])
            )
        else:
            conf.append("service-policy input {}\n".format(c["policy_name"]))
    try:
        device.configure("".join(conf))
    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure control plane policy on device {device}".format(
                device=device.name
            )
        )
