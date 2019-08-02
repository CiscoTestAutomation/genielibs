# Genie
from genie.ops.base import Base


class Msdp(Base):
    exclude = ['statistics',
               'elapsed_time',
               'up_time',
               'expire',
               'sa_message',
               'last_message_received',
               'total',
               'keepalive']