# Genie
from genie.ops.base import Base


class Lag(Base):
    exclude = ['age',
                'lacp_in_pkts',
                'lacp_out_pkts']