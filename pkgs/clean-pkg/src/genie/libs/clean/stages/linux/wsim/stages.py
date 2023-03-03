"""Linux WSIM specific clean stages"""

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
from genie.metaparser.util.schemaengine import Optional, Required, Any, Or

class Connect(BaseStage):
    """This stage connects to the device that is being cleaned.
Stage Schema
------------
connect:
    via (str, optional): Which connection to use from the testbed file. Uses the
        default connection if not specified.
    timeout (int, optional): The timeout for the connection to complete in seconds.
        Defaults to 200.
    retry_timeout (int, optional): Overall timeout for retry mechanism in seconds.
        Defaults to 0 which means no retry.
    retry_interval (int, optional): Interval for retry mechanism in seconds. Defaults
        to 0 which means no retry.
Example
-------
connect:
    timeout: 60
"""

    # =================
    # Argument Defaults
    # =================
    VIA = None
    TIMEOUT = 200
    RETRY_TIMEOUT = 0
    RETRY_INTERVAL = 0

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('via', description="Which connection to use from the testbed file. Uses the default connection if not specified."): str,
        Optional('timeout', description=f"The timeout for the connection to complete in seconds. Defaults to {TIMEOUT}.", default=TIMEOUT): Or(str, int),
        Optional('retry_timeout', description=f"Overall timeout for retry mechanism in seconds. Defaults to {RETRY_TIMEOUT} which means no retry.", default=RETRY_TIMEOUT): Or(str, int, float),
        Optional('retry_interval', description=f"Interval for retry mechanism in seconds. Defaults to {RETRY_INTERVAL} which means no retry.", default=RETRY_INTERVAL): Or(str, int, float),
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'connect'
    ]

    def connect(self, steps, device, via=VIA, timeout=TIMEOUT,
                retry_timeout=RETRY_TIMEOUT, retry_interval=RETRY_INTERVAL):


        with steps.start("Connecting to the device:%s" % device.name) as step:

            log.info('Checking connection to device:%s' % device.name)

            # Create a timeout that will loop
            retry_timeout = Timeout(float(retry_timeout), float(retry_interval))
            retry_timeout.one_more_time = True
            # Without this we see 'Performing the last attempt' even if retry
            # is not being used.
            retry_timeout.disable_log = True

            while retry_timeout.iterate():
                retry_timeout.disable_log = False

                device.instantiate(connection_timeout=timeout,
                                   learn_hostname=True,
                                   prompt_recovery=True,
                                   via=via)

                try:
                    device.connect()
                except Exception:
                    log.error("Connection to the device failed", exc_info=True)
                    device.destroy_all()
                    # Loop
                else:
                    step.passed("Successfully connected".format(device.name))
                    # Don't loop

                retry_timeout.sleep()

            step.failed("Could not connect.")


class ApplyGlobalConfiguration(BaseStage):
    """This stage apply configuration on the device with user provided data
Stage Schema
------------
apply_global_configuration:
    ctrl_type(str): Type of the controller in which wsim will simulate the Aps/Clients.
    ctrl_ip(str): Management IP of the controller
    ctrl_username(str): username of the controller
    ctrl_password(str): password of the controller
    ap_name(str): Base Ap name
    ap_version(str,optional): Version of the AP
    ap_vlan(str): Vlan of the AP
    ap_freq(str,optional): Ap radio 2.4Ghz/5GHz
    ap_base_mac(str): Base mac address of the AP
    client_base_mac(str): Client base mac address

Example
-------
apply_global_configuration:
    ctrl_type: 'EWLC'
    ctrl_ip: '9.2.45.15'
    ctrl_username: 'welcome'
    ctrl_password: 'welcome'
    ap_name: 'wsim-AP'
    ap_model: '9117'
    ap_vlan: '46'
    ap_ip: '9.2.45.15' #give the controller mgmt IP
    ap_base_mac: '00:e5:64:00:00:00'
    client_base_mac: '00:00:e5:64:00:00'
"""

    # =================
    # Argument Defaults
    # =================
    CTRL_TYPE = None
    CTRL_IP = None
    CTRL_USERNAME = None
    CTRL_PASSWORD = None
    AP_NAME = None
    AP_MODEL = None
    AP_VLAN = None
    AP_FREQ = '2.4GHz'
    AP_BASE_MAC = None
    CLIENT_BASE_MAC=None

    # ============
    # Stage Schema
    # ============
    schema = {
        'ctrl_type': str,
        'ctrl_ip': str,
        'ctrl_username': str,
        'ctrl_password': str,
        'ap_name': str,
        'ap_model': str,
        'ap_vlan': str,
        'ap_ip': str,
        'ap_freq': str,
        'ap_base_mac': str,
        'client_base_mac': str,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'apply_global_configuration'
    ]

    def apply_global_configuration(self, steps, device,
                                   ctrl_type=CTRL_TYPE,
                                   ctrl_ip=CTRL_IP,
                                   ctrl_username=CTRL_USERNAME,
                                   ctrl_password=CTRL_PASSWORD,
                                   ap_name=AP_NAME,
                                   ap_model=AP_MODEL,
                                   ap_freq=AP_FREQ,
                                   ap_vlan=AP_VLAN,
                                   ap_base_mac=AP_BASE_MAC,

                                   client_base_mac=CLIENT_BASE_MAC,):
        log.info("Section steps:\n1- Apply controller configuration to the wsim"
                 "\n2- Apply ap configuration to the wsim"
                 "\n3- Apply client configuration to the wsim")

        with steps.start("Apply controller configuration to the wsim {}". \
                                 format(device.name)) as step:
            try:

                device.api.configure_controller_details(ctrl_type=ctrl_type,
                                                        ctrl_ip=ctrl_ip,
                                                        ctrl_username=ctrl_username,
                                                        ctrl_password=ctrl_password,)
            except Exception as e:
                step.failed("Failed to apply controller configs on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully applied controller configs on wsim "
                            "{}".format(device.name))

        with steps.start("Apply ap configuration to the wsim {}". \
                                 format(device.name)) as step:
            try:
                device.api.configure_ap_details(ap_name=ap_name,
                                                ap_model=ap_model,
                                                ap_freq=ap_freq,
                                                ap_vlan=ap_vlan,
                                                ap_ip=ctrl_ip,
                                                ap_base_mac=ap_base_mac,)
            except Exception as e:
                step.failed("Failed to apply ap configs on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully applied ap configs on wsim "
                            "{}".format(device.name))

        with steps.start("Apply client configuration to the wsim {}". \
                                 format(device.name)) as step:
            try:
                device.api.configure_client_details(client_base_mac=client_base_mac,)
            except Exception as e:
                step.failed("Failed to apply client configs on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully applied client configs on wsim "
                            "{}".format(device.name))

class RunConfigure(BaseStage):
    """This stage apply certs on controller.
Stage Schema
------------
run_configure:
    timeout(int,optional): 600
Example
-------
run_configure:
    timeout: 600
"""

    # =================
    # Argument Defaults
    # =================
    TIMEOUT=600

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('timeout'): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'run_configure'
    ]

    def run_configure(self, steps, device,timeout=TIMEOUT):

        with steps.start("Run the configurations on wsim") as step:
            try:
                device.api.run_wsim_config(timeout=timeout,)
            except Exception as e:
                step.failed("Failed to run the config on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully ran the configurations "
                            "{}".format(device.name))

class StartApContainers(BaseStage):
    """This stage starts the ap containers.
Stage Schema
------------
start_device_containers:

    ap_count(str,optional): Number of APs that Wsim will simulate
    client_count(str,optional): Number of Clients that Wsim will simulate
    timeout(int,optional): timeout for the command execution
    shell_access(bool,optional): True/False for client shell access

Example
-------
start_ap_containers:
    ap_count: '1'
    client_count: '1'
    timeout:600
    shell_access:True
"""

    # =================
    # Argument Defaults
    # =================
    AP_COUNT = '1'
    CLIENT_COUNT = '1'
    TIMEOUT=600
    SHELL_ACCESS=True

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional('timeout'): int,
        Optional('client_count'): str,
        Optional('ap_count'): str,
        Optional('shell_access'): bool
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'start_ap_containers'
    ]

    def start_ap_containers(self, steps, device,ap_count=AP_COUNT, client_count=CLIENT_COUNT, timeout=TIMEOUT):

        with steps.start("Configure the ap, client count in wsim {}". \
                                 format(device.name))  as step:
            try:
                device.api.configure_ap_client_count(ap_count=ap_count,
                                                     client_count=client_count,)
            except Exception as e:
                step.failed("Failed to configure ap, client count on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully applied ap, client configs on wsim "
                            "{}".format(device.name))

        with steps.start("Start the Ap containers") as step:
            try:
                device.api.simulate_ap_container(ap_count=ap_count,timeout=timeout,)
            except Exception as e:
                step.failed("Failed to start ap container on wsim "
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully started ap containers on wsim "
                            "{}".format(device.name))

class VerifyApRunState(BaseStage):
    """This stage starts the ap containers.
Stage Schema
------------
verify_ap_run_state:
    ap_count(str): Number of Aps that were being verified
    max_time(int,optional): 600
Example
-------
verify_ap_run_state:
    ap_count: '5'
    max_time: 600
"""

    # =================
    # Argument Defaults
    # =================
    AP_COUNT=None
    MAX_TIME=600

    # ============
    # Stage Schema
    # ============
    schema = {
        'ap_count': str,
        'max_time': int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'verify_ap_run_state'
    ]

    def verify_ap_run_state(self, steps, device,ap_count=AP_COUNT,max_time=MAX_TIME):

        with steps.start("Verify AP status as RUN") as step:
            try:
                device.api.verify_ap_associate(ap_count=ap_count,max_time=max_time)
            except Exception as e:
                step.failed("APs failed to move to RUN state"
                            "{}\n{}".format(device.name, str(e)))
            else:
                step.passed("Successfully started ap containers on wsim "
                            "{}".format(device.name))