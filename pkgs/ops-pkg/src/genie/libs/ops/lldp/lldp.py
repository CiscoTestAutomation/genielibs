# Genie
from genie.ops.base import Base


class Lldp(Base):
    exclude = ['frame_in',
                'frame_out',
                'tlv_discard',
                'tlv_unknown',
                'frame_discard']