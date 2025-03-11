import re

# Genie
from genie.ops.base import Base
from genie.metaparser.util.schemaengine import Any, ListOf


class Management(Base):

    schema = {
        "management": {
            "interface": str,
            "ipv4_address": Any(),
            "ipv4_gateway": Any(),
            "vrf": str,
            "routes": {
                "ipv4": {
                    Any(): {
                        "next_hop": str,
                        "outgoing_interface": str,
                        "source_protocol": str,
                    }
                }
            },
        }
    }