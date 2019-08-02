# Genie
from genie.ops.base import Base


class Ntp(Base):
    exclude = ['root_delay',
               'delay',
               'root_dispersion',
               'receive_time']