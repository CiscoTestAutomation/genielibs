''' 
BGP Genie Ops Object for IOSXR - YANG.
'''

# Genie
from genie.ops.base import Context
from genie.libs.ops.bgp.iosxr.bgp import Bgp as BgpOpsCli

# Parser
from genie.libs.parser.iosxr import show_bgp


class Bgp(BgpOpsCli):
    '''BGP Genie Ops Object'''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # ShowBgpInstanceProcessDetail
        self.context_manager[show_bgp.ShowBgpInstanceProcessDetail] = [Context.yang, Context.cli]

        # ShowBgpInstanceNeighborsDetail
        self.context_manager[show_bgp.ShowBgpInstanceNeighborsDetail] = [Context.yang, Context.cli]