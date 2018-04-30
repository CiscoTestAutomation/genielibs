''' 
OSPF Genie Conf Object Implementation for IOSXE:
    - StubRouter multi-line configuration implementation for IOSXE - CLI
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import AttributesHelper


class StubRouter(ABC):

    def build_config(self, apply=True, attributes=None, unconfig=False,
                         **kwargs):
        assert not kwargs, kwargs
        attributes = AttributesHelper(self, attributes)
        configurations = CliConfigBuilder(unconfig=unconfig)

        # router ospf 1
        #   max-metric router-lsa external-lsa include-stub summary-lsa
        #   max-metric router-lsa external-lsa include-stub summary-lsa on-startup 50
        if attributes.value('stub_router_always') or \
            attributes.value('stub_router_on_startup'):
            
            # max-metric router-lsa
            sr_str = 'max-metric router-lsa'

            # + external-lsa
            if attributes.value('stub_router_external_lsa'):
                sr_str += ' external-lsa'

            # + include-stub
            if attributes.value('stub_router_include_stub'):
                sr_str += ' include-stub'

            # + summary-lsa
            if attributes.value('stub_router_summary_lsa'):
                sr_str += ' summary-lsa'

            # + on-startup {stub_router_on_startup}
            if attributes.value('stub_router_on_startup'):
                sr_str += ' on-startup {stub_router_on_startup}'

            configurations.append_line(attributes.format(sr_str))

        return str(configurations)

    def build_unconfig(self, apply=True, attributes=None, **kwargs):
        return self.build_config(apply=apply, attributes=attributes,
                                 unconfig=True, **kwargs)