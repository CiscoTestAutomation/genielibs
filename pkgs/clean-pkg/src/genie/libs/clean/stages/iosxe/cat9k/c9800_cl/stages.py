'''
IOSXE specific clean stages
'''

# Python
import logging

# Genie
from genie.libs.clean import BaseStage
from genie.metaparser.util.schemaengine import Optional, Any, Or

# Unicon
from unicon.core.errors import SubCommandFailure

# Logger
log = logging.getLogger(__name__)


class ApplySelfSignedCert(BaseStage):
    """ This stage configures the self-signed-certificate for the given trustpoint.

    Stage Schema
    ------------
    apply_self_signed_cert:

        key_size (int, optional): Key size to be configured. Default is 2048

        signature_algorithm (str, optional): Algorithm to be applied. Default is sha256

        encryption_type (int, optional): Encryption type to be configured. Default is 0

        password (str): Password to be configured for the trustpoint.

        timeout (int, optional): Execute timeout in seconds. Defaults to 300.

    Examples:
        apply_self_signed_cert:
            key_size:2048
            signature_algorithm:sha256
            encryption_type:0
            password:cisco123
            timeout: 150
    """

    # =================
    # Argument Defaults
    # =================
    KEY_SIZE = 2048
    SIGNATURE_ALGORITHM = "sha256"
    ENCRYPTION_TYPE = 0
    TIMEOUT = 300
    MAX_TIME=300
    CHECK_INTERVAL=30

    # ============
    # Stage Schema
    # ============
    schema = {
        'password': str,
        Optional('key_size'): int,
        Optional('signature_algorithm'): str,
        Optional('encryption_type'): int,
        Optional('timeout'): int,

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'configure_ssc_trustpoint',
        'verify_configured_trustpoint'
    ]

    def configure_ssc_trustpoint(self, device, steps, password, key_size=KEY_SIZE,
                                 signature_algorithm=SIGNATURE_ALGORITHM,
                                 encryption_type=ENCRYPTION_TYPE, timeout=TIMEOUT):

        # Configuring the self-signed certificate on the device
        with steps.start("Configuring the self-signed certificate on {}".format(device.name)) as step:
            try:
                device.api.enable_http_server()
                device.api.set_clock_calendar()

                # passing the arguments to configure the SSC
                device.api.execute_self_signed_certificate_command(key_size=key_size,
                                                                   signature_algorithm=signature_algorithm,
                                                                   encryption_type=encryption_type, password=password,
                                                                   timeout=timeout)

            except (AttributeError, SubCommandFailure) as e:
                step.failed("Failed to configure the self-signed certificate", from_exception=e)

    def verify_configured_trustpoint(self, device, steps, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):
        # the trustpoint name will always be in the following format of '<dev name>_WLC_TP' as it comes from the device
        trustpoint_name = device.hostname + "_WLC_TP"

        with steps.start("Verify the self-signed certificate is configured")as step:
            # verifying if the trustpoint is configured properly
            result_1 = device.api.verify_wireless_management_trustpoint_name(
                trustpoint_name=trustpoint_name,
                max_time=max_time,
                check_interval=check_interval)

            result_2 = device.api.verify_pki_trustpoint_state(trustpoint_name=trustpoint_name, max_time=max_time,
                                                              check_interval=check_interval)

            if not result_1 or not result_2:
                step.failed(
                    "Management trustpoint {} is configured incorrectly".format(trustpoint_name))
