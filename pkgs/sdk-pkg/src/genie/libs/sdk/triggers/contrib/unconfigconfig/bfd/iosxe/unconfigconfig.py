import time
import logging
from pyats import aetest
from genie.harness.base import Trigger
from pprint import pprint as pp
from genie.harness.base import Trigger
import pdb
import re

log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.triggers.template.unconfigconfig import \
                       TriggerUnconfigConfig as UnconfigConfigTemplate

# Genie
from genie.harness.exceptions import GenieConfigReplaceWarning

from pyats.utils.objects import Not, NotExists

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.unconfigconfig.unconfigconfig import TriggerUnconfigConfig

class TriggerUnconfigConfigBfdTimer(Trigger):

    @aetest.setup
    def prerequisites(self, uut):
        '''checking for bfd configuration'''

        output = uut.parse('show bfd neighbors details')
        print(output)
       # pprint.pprint(output)
