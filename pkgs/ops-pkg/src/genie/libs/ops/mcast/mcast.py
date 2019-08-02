# Genie
from genie.ops.base import Base


class Mcast(Base):
    exclude = ['expire',
               'uptime',
               'flags',
               'incoming_interface_list']