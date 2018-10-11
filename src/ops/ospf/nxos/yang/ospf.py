from genie.ops.base import Context
from genie.libs.ops.ospf.nxos.ospf import Ospf as b_ospf
from genie.libs.parser.nxos import show_ospf

class Ospf(b_ospf):
    '''Ospf Ops Object'''

    # To keep short names
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context_manager[show_ospf.ShowIpOspfVrfAll] = Context.yang
        self.context_manager[show_ospf.ShowIpOspfInterfaceVrfAll] = Context.yang
        self.context_manager[show_ospf.ShowIpOspfDatabase] = Context.yang
        self.context_manager[show_ospf.ShowIpOspfNeighborsDetailVrfAll] = Context.yang
