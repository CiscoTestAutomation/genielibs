from genie.ops.base import Context
from genie.libs.ops.ospf.iosxe.ospf import Ospf as b_ospf
from genie.libs.parser.iosxe import show_ospf

class Ospf(b_ospf):
    '''Ospf Ops Object'''

    # To keep short names
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_manager[show_ospf.ShowIpOspf] = Context.yang
        # Rest use cli as their info cannot be retrieve via yang at the moment
