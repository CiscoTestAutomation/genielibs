# Genie
from genie.ops.base import Base


class Eigrp(Base):
    exclude = ['hold', 'uptime']