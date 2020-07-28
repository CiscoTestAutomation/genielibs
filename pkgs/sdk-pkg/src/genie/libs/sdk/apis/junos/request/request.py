"""Common request functions"""

# Python
import logging

# Unicon
from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

def request_chassis_routing_engine_master_switch(device):
    """Run request chassis routing-engine master switch

    Args:
        device (obj): Device object
    """

    try:
        device.execute('request chassis routing-engine master switch no-confirm')
    except SubCommandFailure as e:
        log.info("Sub command failure: {e}(e)".format(e))
        raise
    except Exception as e:
        log.info("General failure: {e}(e)".format(e))
        raise

def request_routing_engine_login_other_routing_engine(device):
    """Run request routing-engine login other-routing-engine

    Args:
        device (obj): Device object
    """

    try:
        device.execute('request routing-engine login other-routing-engine')
    except SubCommandFailure as e:
        log.info("Sub command failure: {e}(e)".format(e))
        raise
    except Exception as e:
        log.info("General failure: {e}(e)".format(e))
        raise


