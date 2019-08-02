# Genie
from genie.ops.base import Base


class Igmp(Base):

    exclude = ['expire', 'up_time']