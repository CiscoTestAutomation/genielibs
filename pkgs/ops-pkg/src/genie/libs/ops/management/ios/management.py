"""
Platform Genie Ops Object for IOSXE.
"""

import logging

from genie.libs.ops.management.iosxe.management import Management as IosxeManagement

logger = logging.getLogger(__name__)


class Management(IosxeManagement):
    ...