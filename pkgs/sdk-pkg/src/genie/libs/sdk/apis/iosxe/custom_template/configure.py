import logging
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def configure_sdm_prefer_custom_template(device, attribute):
    """ Configure SDM Prefer Custom Template
        Args:
            device ('obj'): device to use
            attribute ('str'): sdm prefer custom template value (Ex : commit, vlan)

        Returns:
            None
        Raises:
            SubCommandFailure: Failed to configure SDM Prefer Custom Template
    """
    log.info(
        "Configuring SDM Prefer Custom Template with attribute={}".format(attribute)
    )

    try:
        device.configure(["sdm prefer custom {}".format(attribute),])

    except SubCommandFailure:
        raise SubCommandFailure(
            "Could not configure sdm prefer custom {attribute}".format(attribute=attribute))