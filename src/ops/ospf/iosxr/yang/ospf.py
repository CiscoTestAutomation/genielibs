from genie.ops.base import Context
from genie.libs.ops.ospf.iosxr.ospf import Ospf as b_ospf

class Ospf(b_ospf):
    '''Ospf Ops Object'''

    # To keep short names
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
