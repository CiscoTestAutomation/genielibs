# Genie
from genie.ops.base import Base


class Arp(Base):
    exclude = ['in_requests_pkts',
                'in_replies_pkts',
                'in_requests_pkts',
                'out_replies_pkts',
                'out_requests_pkts',
                'in_drops',
                'in_replies_pkts',
                'out_requests_pkts',
                'out_total']
