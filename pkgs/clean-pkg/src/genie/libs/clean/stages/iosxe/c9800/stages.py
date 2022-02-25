"""IOSXE C9800 specific clean stages"""

# Python
import logging

# Genie
from genie.libs import clean
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from unicon.core.errors import SubCommandFailure, TimeoutError

# Logger
log = logging.getLogger(__name__)

# MetaParser
from genie.metaparser.util.schemaengine import Optional

class VerifyApMode(BaseStage):
    """ This stage verifies the mode of a given access point.

    Stage Schema
    ------------
    verify_accesspoint_mode:

        access_points(list):mode of a given access_point
        ap_mode(str,optional):mode of accesspoint (i.e: local or flexmode)

    Examples:
        verify_accesspoint_mode:
            access_point:
                - "AP188B.4500.44C8"
            ap_mode:"local"
    """

    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10
    AP_MODE = "local"

    # ============
    # Stage Schema
    # ============
    schema = {
        'access_points': list,
        Optional('ap_mode'): str,

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_accesspoint_mode'
    ]

    def verify_accesspoint_mode(self, device, steps, access_points, ap_mode=AP_MODE, max_time=MAX_TIME,
                                check_interval=CHECK_INTERVAL):
        for ap_name in access_points:
            with steps.start("Checking mode for accesspoint {}".format(ap_name)) as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    # Fetch ap mode from get_ap_mode api
                    try:
                        ap_mode_fetch = device.api.get_ap_mode(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find access point mode",from_exception=e)

                    # Verify if the mode for the given accesspoint
                    if ap_mode_fetch == "":
                        log.warning('Access point {} has not yet registered'.format(ap_name))
                        timeout.sleep()                        
                    elif ap_mode_fetch.lower() == ap_mode.lower():
                        step.passed('Access point {} has registered with {} mode'.format(ap_name, ap_mode))
                    else:
                        step.failed('The access point {} could not register with the given ap mode'.\
                                format(ap_name))
                else:
                    step.failed("Accesspoints failed to register to the controller")


class VerifyApAssociation(BaseStage):
    """ This stage verifies the given access point has configured.

    Stage Schema
    ------------
    verify_accesspoint_association:

        access_points(list):access_point to be verified if present

    Examples:
        verify_accesspoint_association:
            access_points:
                - "AP188B.4500.44C8"            
    """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 600
    CHECK_INTERVAL = 10

    # ============
    # Stage Schema
    # ============
    schema = {
        'access_points': list,

    }
    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_accesspoint_association'
    ]

    def verify_accesspoint_association(self, device, steps, access_points, max_time=MAX_TIME,
                                       check_interval=CHECK_INTERVAL):
        for ap_name in access_points:
            with steps.start("Checking association for accesspoint {}".format(ap_name)) as step:
                timeout = Timeout(max_time, check_interval)
                while timeout.iterate():
                    # Fetch ap state from get_ap_state api
                    try:
                        ap_state = device.api.get_ap_state(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find access point state",from_exception=e)
                    # Fetch ap country from get_ap_country api
                    try:
                        ap_country = device.api.get_ap_country(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find country name",from_exception=e)

                    # Verify if the given accesspoint is configured
                    if ap_state.lower() == "registered" and ap_country != "":
                        step.passed('Access point {} has registered successfully with country as {}'.\
                                format(ap_name, ap_country))
                    else:
                        log.warning('Access point {} has not yet registered'.format(ap_name))
                        timeout.sleep()
                else:
                    step.failed("Accesspoints failed to register to the controller")

