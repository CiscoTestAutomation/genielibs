# Genie
from genie.ops.base import Base


class Nd(Base):
    exclude = ['neighbor_state', 'age']