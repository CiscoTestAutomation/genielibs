"""Common verify functions for crypto session"""
import logging
import time

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

log = logging.getLogger(__name__)

def verify_crypto_session_svti(device, tunnel_no, state, repeat = 60):
    """Verify the crypto session state
        Args:
            device('obj'): Device name
            tunnel_no('str'): The name of the tunnel
            state('str'): expected state of the session
        Returns:
            result (`bool`): Verified result            
    """
    count = 1
    matchobj = False
    while not matchobj:
        try:
            crypto_status = device.parse("show crypto session")
            log.info(crypto_status)
            if crypto_status['interface'][tunnel_no]['session_status'] == state:
                matchobj = True
        except Exception as excep:
            log.info(f'Exception- str(type({excep})), str({excep})')

        if count == repeat:
            log.info("Return false")
            return False
        else:
            count += 1

        if not matchobj:
            log.info("Wait for 5 sec")
            time.sleep(5)
        else:
            return True

