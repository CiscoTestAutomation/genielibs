# Python
import logging
import re
import time

# Unicon
from unicon.core.errors import SubCommandFailure

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def export_packet_capture(device, server_config, timeout=60):
    """Export the packet capture to device
        Args:
            device (`obj`): Device object
            server_config dict has following attributes
                cap_name (str): capture name
                filetype (`str`): Filetype(flash)
                file_name (`str`): pcap file name
            timeout : timeout value
        Returns:
            True on successful export and copy
            False on not successful export or copy
        Raises:
            pyATS Results
    """
    logger.info('''Export the capture to {p}
                '''.format(p=server_config["file_name"]))
    try:
        output = device.execute('''monitor capture {0} export location {1}:{2}
                '''.format(server_config["cap_name"],
                           server_config["filetype"],
                           server_config["file_name"]), timeout=timeout)
        time.sleep(30)
        if "Export Started Successfully" or "Export completed" in output:
            logger.info("Export to device success")
            return True
        else:
            logger.info("Export to device not successful")
            return False
    except Exception as e:
        logger.info("Error {e} while exporting monitor capture".format(e=e))
        return False