# Genie
from genie.ops.base import Base


class Msdp(Base):
    exclude = ['statistics',
               'elapsed_time',
               'up_time',
               'expire']