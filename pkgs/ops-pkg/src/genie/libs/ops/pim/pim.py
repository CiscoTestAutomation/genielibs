# Genie
from genie.ops.base import Base


class Pim(Base):
    exclude = ['expiration',
               'hello_expiration',
               'hello_interval',
               'up_time',
               'bsr_next_bootstrap',
               'expires',
               'rp_candidate_next_advertisement',
               'genid',
               'df_address',
               'gen_id',
               'incoming_interface',
               'rpf_neighbor',
               'dr_address',
               'neighbors']