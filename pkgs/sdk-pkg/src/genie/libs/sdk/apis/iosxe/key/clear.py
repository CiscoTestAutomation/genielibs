import time
from unicon.eal.dialogs import Statement, Dialog
import logging 

logger = logging.getLogger(__name__)

# Unicon
from unicon.core.errors import SubCommandFailure

# Genie
from genie.metaparser.util.exceptions import SchemaEmptyParserError

def crypto_key_zeroize(device, 
                       key_type='',
                       key_label='',
                       timeout=30):

    ''' 
        Zeroize crypto keys
        Args:
            device ('obj'): Device object
            key_type ('str', optional): Type of key to be zeroized
            key_label ('str',optional): Name of the keypair that needs to be zeroized
            timeout('int', optional): timeout for exec command execution, default is 30

        Returns:
            None
        Raises:
            SubCommandFailure
    """
    '''

    logger.info("Zeroizing crypto keys")

    crypto_config = []

    if not key_type:
        crypto_config = (f"crypto key zeroize")
    else: 
        if not key_label:
            crypto_config = (f"crypto key zeroize {key_type}")
        else:
            crypto_config = (f"crypto key zeroize {key_type} {key_label}")
   
    try:    
        device.execute(crypto_config,  
            timeout=timeout)
    
    except SubCommandFailure as e:
        raise SubCommandFailure(
            "Could not zeroize crypto keys on {device}. Error:\n{error}"
                .format(device=device, error=e)
        )
