# Genie
from genie.ops.base import Base


class Interface(Base):
    exclude = ['in_discards',
               'in_octets',
               'in_pkts',
               'last_clear',
               'out_octets',
               'out_pkts',
               'in_rate',
               'out_rate',
               'in_errors',
               'in_crc_errors',
               'in_rate_pkts',
               'out_rate_pkts',
               'in_broadcast_pkts',
               'out_broadcast_pkts',
               'in_multicast_pkts',
               'out_multicast_pkts',
               'in_unicast_pkts',
               'out_unicast_pkts',
               'last_change',
               'mac_address',
               'phys_address',
               '((t|T)unnel.*)',
               '(Null.*)',
               'chars_out',
               'chars_in',
               'pkts_out',
               'pkts_in',
               'mgmt0']