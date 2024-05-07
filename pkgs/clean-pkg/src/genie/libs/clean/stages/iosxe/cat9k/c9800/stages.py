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

# Errors
from genie.metaparser.util.exceptions import SchemaMissingKeyError, SchemaUnsupportedKeyError


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
                        step.failed("Failed to find access point mode", from_exception=e)

                    # Verify if the mode for the given accesspoint
                    if ap_mode_fetch == "":
                        log.warning('Access point {} has not yet registered'.format(ap_name))
                        timeout.sleep()
                    elif ap_mode_fetch.lower() == ap_mode.lower():
                        step.passed('Access point {} has registered with {} mode'.format(ap_name, ap_mode))
                    else:
                        step.failed('The access point {} could not register with the given ap mode'. \
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
                        step.failed("Failed to find access point state", from_exception=e)
                    # Fetch ap country from get_ap_country api
                    try:
                        ap_country = device.api.get_ap_country(ap_name)
                    except (AttributeError, SubCommandFailure) as e:
                        step.failed("Failed to find country name", from_exception=e)

                    # Verify if the given accesspoint is configured
                    if ap_state.lower() == "registered" and ap_country != "":
                        step.passed('Access point {} has registered successfully with country as {}'. \
                                    format(ap_name, ap_country))
                    else:
                        log.warning('Access point {} has not yet registered'.format(ap_name))
                        timeout.sleep()
                else:
                    step.failed("Accesspoints failed to register to the controller")


class ConfigureRrmDcaChannel(BaseStage):
    """ This stage removes the specified channels from the controller.

    Stage Schema
    ------------
    configure_rrm_dca_channel:
        N/A

    """
    # =================
    # Argument Defaults
    # =================
    CHANNEL_LIST = ["52", "56", "60", "64", "100", "104", "108", "112", "116", "120", "124", "128", "132", "136", "140",
                    "144"]

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('channel_list'): list
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'configure_rrm_dca_channel',
        'verify_rrm_dcs_channels_removed'
    ]

    def configure_rrm_dca_channel(self, device, steps, channel_list=CHANNEL_LIST):

        command_list = []
        command_str = "ap dot11 5ghz rrm channel dca remove "

        for ch in channel_list:
            command_list.append(command_str + ch)
        with steps.start("Removing dca channel for {}".format(device.name)) as step:

            try:
                device.configure("wireless rf-network {}".format(device.name))

                for command in command_list:
                    device.configure(command)
                device.configure("ap dot11 5ghz rrm group-mode auto")
            except Exception as e:
                step.failed("Failed during removing rrm dca channel", from_exception=e)

    def verify_rrm_dcs_channels_removed(self, device, steps, channel_list=CHANNEL_LIST):

        with steps.start("Verifying channels have been removed") as step:
            if device.api.verify_unused_channel(channel_list):
                step.passed("Unused channels have deleted successfully")
            else:
                step.failed("All un used channels have not deleted")


class VerifyInstallationMode(BaseStage):
    """ This stage verifies the configured installation mode.

    Stage Schema
    ------------
    verify_installation_mode:
        verify_installation_mode(str):installation_mode to be verified if present

    Examples:
        verify_installation_mode:
            installation_mode: "INSTALL"
    """
    # =================
    # Argument Defaults
    # =================
    INSTALLATION_MODE = "INSTALL"

    # ============
    # Stage Schema
    # ============
    schema = {
        'installation_mode': str,

    }
    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_installation_mode'
    ]

    def verify_installation_mode(self, device, steps, installation_mode=INSTALLATION_MODE):
        with steps.start("Checking installation mode for {}".format(device.name)) as step:
            # Fetch installation mode from get_installation_mode api
            try:
                installation_mode_fetch = device.api.get_installation_mode()
            except Exception as e:
                step.failed("Failed to find installation mode", from_exception=e)
            # Verify if the installation mode for the given device
            if installation_mode_fetch.lower() != installation_mode.lower():
                step.failed("Actual mode {} is different than the expected mode {}". \
                            format(installation_mode_fetch, installation_mode))


class ConfigureApTxPower(BaseStage):
    """ This stage verifies the configured Tx power.

    Stage Schema
    ------------
    configure_ap_tx_power:
        configure_ap_tx_power(str): tx power to be verified

    Examples:
        configure_ap_tx_power:
            tx_power: 
                - "1"
                - "2"
    """
    # =================
    # Argument Defaults
    # =================
    TX_POWER = "1"
    ASSIGNMENT_MODE = "AUTO"

    # ============
    # Stage Schema
    # ============
    schema = {
        'access_points': list,
        'tx_power': str,

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'configure_ap_tx_power',
        'verify_ap_tx_power_configure'
    ]

    def configure_ap_tx_power(self, device, steps, access_points, tx_power=TX_POWER):

        for ap_name in access_points:

            with steps.start("Checking the tx power for {}".format(device.name)) as step:
                # Fetch ap_model from get_ap_model api
                try:
                    ap_model = device.api.get_ap_model(ap_name)
                    device.api.execute_ap_tx_power_commands(ap_name, ap_model, tx_power)
                except (AttributeError, SubCommandFailure) as e:
                    step.failed("Failed to find access point model", from_exception=e)

                device.configure("ap dot11 5ghz rrm txpower {}".format(tx_power))
                device.configure("ap dot11 24ghz rrm txpower {}".format(tx_power))

    def verify_ap_tx_power_configure(self, device, steps, access_points, tx_power=TX_POWER,
                                     assignment_mode=ASSIGNMENT_MODE):
        for ap_name in access_points:
            with steps.start("Verifying Assignment mode and TX power are configured properly") as step:
                if device.api.verify_assignment_mode(assignment_mode):
                    if device.api.verify_tx_power(ap_name, tx_power):
                        step.passed("Assignment mode and TX power are configured properly")
                    else:
                        step.failed("TX power {} is not configured".format(tx_power))
                else:
                    step.failed("Given assignment mode " + assignment_mode + " is not configured")


class VerifyHaState(BaseStage):
    """ This stage verifies the if HA pair has formed successfully

        Stage Schema
        ------------
        verify_ha_state:

        Examples:
            verify_ha_state:
        """

    # =================
    # Argument Defaults
    # =================
    TIMEOUT = 900
    RETRY_INTERVAL = 30

    # ============
    # Stage Schema
    # ============
    schema = {
            Optional('timeout'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_show_redundancy_states',
        'verify_show_chassis'
    ]

    def verify_show_redundancy_states(self, device, steps, timeout=TIMEOUT, interval=RETRY_INTERVAL):
        with steps.start("Checking the HA pairing in show redundancy states for {}".format(device)) as step:
            retry_timeout = Timeout(timeout, interval)
            while retry_timeout.iterate():
                # Verify show redundancy states for HA pairing
                try:
                    show_redundancy = device.parse("show redundancy states")
                    if show_redundancy.get("peer_state") and "STANDBY HOT" in show_redundancy.get("peer_state"):
                        step.passed('Device is in STANDBY HOT state')
                    elif show_redundancy.get("peer_state") and "STANDBY HOT" not in show_redundancy.get("peer_state"):
                        log.warning('Device is not in STANDBY HOT state yet')
                        retry_timeout.sleep()
                    elif show_redundancy.get("peer_state") is None:
                        log.warning('Standby Device has not yet registered')
                        retry_timeout.sleep()
                except (SchemaUnsupportedKeyError, SubCommandFailure, SchemaMissingKeyError) as e:
                    step.failed("Failed to parse show redundancy states", from_exception=e)
            step.failed("Device never formed the HA Instance after timeout of {}. Hence failed".format(timeout))

    def verify_show_chassis(self, device, steps, timeout=TIMEOUT, interval=RETRY_INTERVAL):
        with steps.start("Checking the HA pairing in show chassis for {}".format(device)) as step:
            retry_timeout = Timeout(timeout, interval)
            while retry_timeout.iterate():
                show_chassis = device.parse("show chassis")
                for chassis_details in show_chassis.get("chassis_index").values():
                    if chassis_details.get("role") == "Standby" and chassis_details.get("current_state") == "Ready":
                        step.passed("Device has formed HA and Standby chassis is ready")
                    elif chassis_details.get("role") == "Standby" and chassis_details.get(
                            "current_state") != "Ready":
                        log.warning("Device has formed HA but Standby chassis is not ready. Hence waiting...")
                        retry_timeout.sleep()
                    elif chassis_details.get("role") == "Active":
                        continue
            step.failed("Device never formed the HA Instance after timeout of {}. Hence failed".format(timeout))
