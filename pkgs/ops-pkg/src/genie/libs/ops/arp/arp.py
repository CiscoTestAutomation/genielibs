# Genie
from genie.ops.base import Base


class Arp(Base):
    exclude = ['in_requests_pkts']
