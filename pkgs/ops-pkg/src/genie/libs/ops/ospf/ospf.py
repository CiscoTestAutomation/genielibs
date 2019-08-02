# Genie
from genie.ops.base import Base


class Ospf(Base):
    exclude = ['age',
               'uptime',
               'last_change',
               'cksum',
               'seq',
               'dead_timer',
               'hello_timer',
               'checksum',
               'seq_num',
               'statistics',
               'lsas',
               'last_state_change',
               'bdr_ip_addr',
               'dr_ip_addr',
               'state',
               'bdr_router_id',
               'dr_router_id',
               'area_scope_lsa_cksum_sum']