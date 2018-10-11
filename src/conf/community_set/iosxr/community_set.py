"""Implement IOS-XR (iosxr) Specific Configurations for CommunitySet objects.
"""

# Table of contents:
#     class CommunitySet:
#         class DeviceAttributes:
#             def build_config/build_unconfig:

from abc import ABC
import operator
import warnings

from genie.conf.base.attributes import UnsupportedAttributeWarning,\
    AttributesHelper
from genie.conf.base.cli import CliConfigBuilder


class UnsupportedSelectiveCommunitySetConfig(UserWarning):
    '''Warning class for Unsupported Selective CommunitySet Configuration.'''
    pass


class CommunitySet(ABC):

    class DeviceAttributes(ABC):

        def build_config(self, apply=True, attributes=None, **kwargs):
            '''IOS-XR CommunitySet configuration.

            Note:
                Selective configuration is not supported on IOS-XR; The whole
                community-set is always removed and re-configured.
            '''
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            if not attributes.iswildcard:
                warnings.warn(UnsupportedSelectiveCommunitySetConfig,
                              'IOS-XR does not support selective community-set'
                              ' configuration.')
                attributes = AttributesHelper(self)
            configurations = CliConfigBuilder()

            # First remove any existing to avoid CLI warnings
            if False:
                # Actually, a commit is needed to avoid the warning, so don't even bother!
                configurations.append_line(attributes.format(
                    'no community-set {name}', force=True))

            # iosxr: community-set <cs> (config-comm)
            with configurations.submode_context(
                    attributes.format('community-set {name}', force=True),
                    exit_cmd='end-set'):

                for icomm, community in enumerate(self.communities):
                    last = icomm == (len(self.communities) - 1)
                    # *                  Wildcard (any community or part thereof)                                                                                                                                                                                                                                 
                    # <0-65535>          16-bit half-community number                                                                                                                                                                                                                                             
                    # [                  Left bracket to begin range                                                                                                                                                                                                                                              
                    # accept-own         Accept-Own (BGP well-known community)                                                                                                                                                                                                                                    
                    # dfa-regex          DFA style regular expression                                                                                                                                                                                                                                             
                    # graceful-shutdown  Graceful Shutdown (BGP well-known community)                                                                                                                                                                                                                             
                    # internet           Internet (BGP well-known community)                                                                                                                                                                                                                                      
                    # ios-regex          Traditional IOS style regular expression                                                                                                                                                                                                                                 
                    # local-AS           Do not send outside local AS (BGP well-known community)                                                                                                                                                                                                                  
                    # no-advertise       Do not advertise to any peer (BGP well-known community)                                                                                                                                                                                                                  
                    # no-export          Do not export to next AS (BGP well-known community)                                                                                                                                                                                                                      
                    # private-as         Match within BGP private AS range [64512..65534]                                                                                                                                                                                                                         
                    configurations.append_line('{}{}'.format(
                        community,
                        '' if last else ','))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return str(configurations)

        def build_unconfig(self, apply=True, attributes=None, **kwargs):
            '''IOS-XR CommunitySet unconfiguration.

            Note:
                Selective unconfiguration is not supported on IOS-XR; The whole
                community-set is always removed.
            '''
            assert not kwargs, kwargs
            attributes = AttributesHelper(self, attributes)
            if not attributes.iswildcard:
                warnings.warn(UnsupportedSelectiveCommunitySetConfig,
                              'IOS-XR does not support selective community-set'
                              ' unconfiguration.')
                attributes = AttributesHelper(self)
            configurations = CliConfigBuilder()

            configurations.append_line(attributes.format(
                'no community-set {name}', force=True))

            if apply:
                if configurations:
                    self.device.configure(configurations, fail_invalid=True)
            else:
                return str(configurations)


