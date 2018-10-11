'''
NXOS Genie Conf using CLI for prefix-list.
'''

# Python
import warnings
from abc import ABC

# Genie
from genie.conf.base.config import CliConfig
from genie.conf.base.cli import CliConfigBuilder
from genie.conf.base.attributes import UnsupportedAttributeWarning,\
                                       AttributesHelper


class PrefixList(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, devices=None, apply=True, attributes=None,
                         unconfig=False, **kwargs):
            assert not apply
            attributes = AttributesHelper(self, attributes)
            configurations = CliConfigBuilder(unconfig=unconfig)

            # loop over all prefixes
            for sub, attributes2 in attributes.mapping_values(
                    'prefix_attr', keys=self.prefix_attr.keys(), sort=True):
                configurations.append_block(sub.build_config(apply=False,
                    attributes=attributes2, unconfig=unconfig, **kwargs))

            return CliConfig(device=self.device, unconfig=unconfig,
                             cli_config=configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            return self.build_config(apply=apply, attributes=attributes,
                                     unconfig=True, **kwargs)

        class PrefixAttributes(ABC):

            def build_config(self, apply=True, attributes=None,
                             unconfig=False, **kwargs):
                assert not apply
                attributes = AttributesHelper(self, attributes)
                configurations = CliConfigBuilder(unconfig=unconfig)

                # loop over all maxlength_range
                for sub, attributes2 in attributes.mapping_values(
                        'maxlength_range_attr', sort=True,
                        keys=self.maxlength_range_attr.keys()):
                    configurations.append_block(sub.build_config(apply=False,
                        attributes=attributes2, unconfig=unconfig, **kwargs))

                return str(configurations)

            def build_unconfig(self, apply=True, attributes=None, **kwargs):
                return self.build_config(apply=apply, attributes=attributes,
                                         unconfig=True, **kwargs)

            class MaxLengthRangeAttributes(ABC):

                def build_config(self, apply=True, attributes=None,
                                 unconfig=False, **kwargs):
                    assert not apply
                    attributes = AttributesHelper(self, attributes)
                    configurations = CliConfigBuilder(unconfig=unconfig)

                    # <protocol> prefix-list <prefix_set_name> permit <prefix> [ge length | le length]
                    if attributes.value('protocol'):
                        ip = attributes.value('protocol').value
                        cfg_str = '{}'.format(ip) if ip == 'ipv6' else 'ip'
                    else:
                        return str(configurations)

                    # prefix-list <prefix_set_name>
                    cfg_str += ' prefix-list {}'.format(self.name)

                    # prefix <prefix> 
                    cfg_str += ' permit {prefix}'.format(prefix=self.prefix)

                    if not attributes.value('maxlength_range_attr'):
                        configurations.append_line(cfg_str)
                        return str(configurations)

                    # get range edge value from the maxlength_range
                    [min_val, max_val] = self.maxlength_range.split('..')
                    min_val = int(min_val)
                    max_val = int(max_val)

                    # get mask of prefix to compare
                    mask = int(self.prefix.split('/')[1])

                    # compare with range edge values
                    if mask == min_val:
                        if min_val < max_val:
                            cfg_str += ' le {}'.format(max_val)
                    elif mask < min_val:
                        if max_val == 32 or max_val == 128:
                            cfg_str += ' ge {}'.format(min_val)
                        else:
                            cfg_str += ' ge {a} le {b}'.format(a=min_val, b=max_val)


                    configurations.append_line(cfg_str)

                    return str(configurations)

                def build_unconfig(self, apply=True, attributes=None, **kwargs):
                    return self.build_config(apply=apply, attributes=attributes,
                                             unconfig=True, **kwargs)

