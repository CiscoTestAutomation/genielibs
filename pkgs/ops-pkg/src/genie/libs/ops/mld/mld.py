# Genie
from genie.ops.base import Base


class Mld(Base):
    exclude = ['expire',
               'up_time',
               'last_reporter',
               'querier']