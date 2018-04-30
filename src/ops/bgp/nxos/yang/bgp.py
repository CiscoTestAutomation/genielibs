''' 
BGP Genie Ops Object for NXOS - YANG.
'''

# Genie
from genie.ops.base import Context
from genie.libs.ops.bgp.nxos.bgp import Bgp as BgpOpsCli

# Parser
from genie.libs.parser.nxos import show_bgp


class Bgp(BgpOpsCli):
    '''BGP Genie Ops Object'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ShowBgpProcessVrfAll
        self.context_manager[show_bgp.ShowBgpProcessVrfAll] = [Context.yang, Context.cli]

        # ShowBgpVrfAllNeighbors
        self.context_manager[show_bgp.ShowBgpVrfAllNeighbors] = [Context.yang, Context.cli]