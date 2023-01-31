'''
cheetah AP specific clean stages
'''

# Python
import logging
import time

# Genie
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.metaparser.util.exceptions import InvalidCommandError


# Unicon
from unicon.core.errors import SubCommandFailure, ConnectionError, StateMachineError, TimeoutError

# Logger
log = logging.getLogger(__name__)


class PrimeAp(BaseStage):
    """This stage primes accesspoint to desired controller

    Stage Schema
    ------------
    prime_ap:

        controller_name (str):Name of the controller where AP needs to join.

        controller_ip_address (str): IPv4/Ipv6 address of controller where AP needs to join.

        max_time (int, optional): Maximum time for which this clean stage will try to associate Ap to controller .
                                    Defaults to 900

        check_interval (int, optional): Interval for retry mechanism in seconds. Defaults to 30

        sleep_time (int, optional): Interval for sleeping mechanism in seconds after priming AP to controller.
                                    Defaults to 30


    Example
    -------
    prime_ap:
        controller_name: "ewlc-5"
        controller_ip_address: "9.4.62.41"
"""
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 900
    CHECK_INTERVAL = 30
    SLEEP_TIME=30

    # ============
    # Stage Schema
    # ============
    schema = {
        'controller_name': str,
        'controller_ip_address': str,
        Optional('max_time'): int,
        Optional('check_interval'): int,
        Optional('sleep_time'): int,

    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'prime_ap_to_controller',
        'verify_primed_ap',
    ]

    def prime_ap_to_controller(self, device, steps, controller_name, controller_ip_address,  max_time=MAX_TIME,
                               check_interval=CHECK_INTERVAL, sleep_time=SLEEP_TIME):
        with steps.start("Priming the AP-{} to Controller-{}".format(device.name, controller_name)) as step:
            if not device.api.execute_prime_ap(controller_ip_address=controller_ip_address, controller_name=controller_name):
                step.failed("Failed to prime the AP")
            # sleep is needed since AP takes time to figure out reachability whether to reload or not
            time.sleep(sleep_time)
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                try:
                    if not device.is_connected():
                        device.connect()
                    if device.api.get_operation_state() == "IMAGE":
                        timeout.sleep()
                    else:
                        break
                except (SubCommandFailure, StateMachineError, ConnectionError, InvalidCommandError):
                    device.disconnect()
                    timeout.sleep()
            else:
                step.failed("Failed to login to device after priming the AP")

    def verify_primed_ap(self, device, steps, controller_name, controller_ip_address,  max_time=MAX_TIME, check_interval=CHECK_INTERVAL):

        with steps.start("Validate if the AP has joined the intended controller")as step:
            # verifying if the AP has joined right controller
            try:
                result_1 = device.api.verify_operation_state(operation_state="UP",max_time=max_time,
                                                             check_interval=check_interval)

                result_2 = device.api.verify_controller_name(controller_name=controller_name,
                                                             max_time=max_time, check_interval=check_interval)

                result_3 = device.api.verify_controller_ip(controller_ip_address=controller_ip_address,
                                                           max_time=max_time, check_interval=check_interval)

                if not result_1 or not result_2 or not result_3:
                    step.failed("AP {} has not joined right controller".format(device.name))
            except (SubCommandFailure, TimeoutError) as e:
                step.failed("Failed due to exception",from_exception=e)


class EraseApConfiguration(BaseStage):
    """This stage erases the AP configuration

       Stage Schema
       ------------
       erase_ap_configuration:
           login_credentials_alias (str): Alias of login credentials to use after write erase which will be mentioned in TB yaml

           max_time (int, optional): Maximum time for which this clean stage will try to associate Ap to controller.
               Defaults to 900

           check_interval (int, optional): Interval for retry mechanism in seconds. Defaults to 30


       Example
       -------
       erase_ap_configuration:
            login_credentials_alias: "erase"
            max_time: "600"
   """
    # =================
    # Argument Defaults
    # =================
    MAX_TIME = 900
    CHECK_INTERVAL = 30

    # ============
    # Stage Schema
    # ============
    schema = {
        "login_credentials_alias": str,
        Optional('max_time'): int,
        Optional('check_interval'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'erase_configs',
    ]

    def erase_configs(self, device, steps, login_credentials_alias, max_time=MAX_TIME, check_interval=CHECK_INTERVAL):
        with steps.start("Erasing the AP-{}".format(device.name)) as step:
            if not device.api.execute_erase_ap():
                step.failed("Failed to erase the AP")
            time.sleep(300)
            timeout = Timeout(max_time, check_interval)
            while timeout.iterate():
                try:
                    if not device.is_connected():
                        device.destroy()
                        device.connect(login_creds=login_credentials_alias)
                    device.execute("show version")
                    break
                except (SubCommandFailure, StateMachineError, ConnectionError, InvalidCommandError):
                    device.disconnect()
                    timeout.sleep()
            else:
                step.failed("Failed to login to device after erasing the AP configs")
