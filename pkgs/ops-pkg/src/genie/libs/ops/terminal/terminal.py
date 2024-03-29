# Genie
from genie.ops.base import Base
from genie.metaparser.util.schemaengine import Optional, ListOf

schema = {
    "line": str,
    "location": str,
    "type": str,
    "length": int,
    "width": int,
    Optional("baud_rate"):{
        "tx": int,
        "rx": int
    },
    Optional("parity"): str,
    Optional("stopbits"): int,
    Optional("databits"): int,
    Optional("status"): ListOf(str),
    Optional("input_transport"): ListOf(str),
    Optional("output_transport"): ListOf(str)
}

class Terminal(Base):
    exclude = []
