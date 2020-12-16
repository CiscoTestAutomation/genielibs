''' NXOS N3K: specific recovery functions'''
# Python
import logging

# Genie
from genie.libs.clean.recovery.nxos.n9k.recovery import recovery_worker as n9k_recovery_worker
from genie.libs.clean.recovery.nxos.n9k.recovery import golden_recovery as n9k_golden_recovery
from genie.libs.clean.recovery.nxos.n9k.recovery import tftp_recovery_worker as n9k_tftp_recovery_worker
from genie.libs.clean.recovery.nxos.n9k.recovery import tftp_recover_from_rommon as n9k_tftp_recover_from_rommon

# Logger
log = logging.getLogger(__name__)

def recovery_worker(*args, **kwargs):
    n9k_recovery_worker(*args, **kwargs)

def golden_recovery(*args, **kwargs):
    n9k_golden_recovery(*args, **kwargs)

def tftp_recovery_worker(*args, **kwargs):
    n9k_tftp_recovery_worker(*args, **kwargs)

def tftp_recover_from_rommon(*args, **kwargs):
    n9k_tftp_recover_from_rommon(*args, **kwargs)

