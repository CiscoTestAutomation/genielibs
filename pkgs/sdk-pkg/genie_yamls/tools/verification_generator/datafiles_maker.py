import os
import sys
import yaml
import shutil
import logging
import inspect
import argparse
import importlib
from ats.log.utils import banner
from collections import OrderedDict
from pathlib import Path

from genie.metaparser import MetaParser
from genie.metaparser.util import merge_dict

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
log = logging.getLogger(__name__)

EXCLUDE_PARSERS = ['ShowDir', 'ShowBgpPolicyStatistics', 'ShowBgpVrfAllNeighborsRoutes',
                   'ShowBgpPolicyStatisticsNeighbor', 'ShowBgpVrfAllNeighborsAdvertisedRoutes',
                   'ShowBgpVrfAllNeighborsReceivedRoutes', 'ShowShowBgpVrfAllNeighborsRoutes',
                   'ShowIpOspfVrfAll', 'ShowIpOspfNeighborsDetailVrfAll', 'ShowIpOspfInterfaceVrfAll',
                   'ShowIpOspfDatabase', 'ShowIpRipNeighborVrfAll', 'ShowIpRipStatistics', 'ShowIpRipVrfAll',
                   'ShowIpRipInterfaceVrfAll', 'ShowIpRipRouteVrfAll', 'ShowIpRpf', 'ShowIpv6Rpf',
                   'ShowIpv6RipInterfaceVrfAll', 'ShowIpv6RipNeighborVrfAll', 'ShowIpv6RipStatistics',
                   'ShowIpv6RipVrfAll', 'ShowRunRip', 'ShowSystemInternalSysmgrServiceName',
                   'ShowIpIgmpSsmMapping', 'ShowIpv6MldSsmMap', 'ShowPimRp', 'ShowPimNeighbor',
                   'ShowIpOspf', 'ShowBgpAllNeighborsAdvertisedRoutes', 'ShowRunningConfigInterface',
                   'ShowBgpAllNeighborsPolicy', 'ShowBgpAllNeighborsReceivedRoutes',
                   'ShowBgpAllNeighborsRoutes', 'ShowBgpInstanceNeighborsAdvertisedRoutes',
                   'ShowBgpInstanceNeighborsReceivedRoutes', 'ShowBgpInstanceNeighborsRoutes',
                   'ShowL2VpnXconnectMp2mpDetail', 'ShowL2vpnForwardingProtectionMainInterface',
                   'ShowL2vpnForwardingBridgeDomainMacAddress', 'ShowOspfVrfAllInclusiveLinksParser',
                   'ShowOspfVrfAllInclusiveDatabaseParser', 'ShowIpOspfDatabaseDetailParser',
                   'ShowIpOspfDatabaseParser', 'ShowIpOspfLinksParser', 'ShowBgpSessions', 'ShowEvpnEvi',
                   'ShowEvpnEviDetail', 'ShowL2VpnXconnectSummary', 'ShowL2VpnXconnectBrief',
                   'ShowL2VpnXconnectDetail', 'ShowL2VpnBridgeDomain', 'ShowL2VpnBridgeDomainBrief',
                   'ShowL2VpnBridgeDomainDetail', 'ShowL2VpnBridgeDomainSummary', 'ShowEvpnEthernetSegment',
                   'ShowIpRouteWord', 'ShowIpv6RouteWord', 'ShowInterfacesCounters','ShowPowerInlineInterface',
                   'ShowProcessesCpuSorted','ShowVlanOld', 'ShowIpMsdpPolicyStatisticsSaPolicyIn',
                   'ShowIpMsdpPolicyStatisticsSaPolicyInOut', 'ShowIpMsdpPolicyStatisticsSaPolicyOut',
                   'ShowBgpL2vpnEvpnWord', 'ShowL2routeEvpnMacEvi', 'ShowMacAddressTableVni',
                   'ShowIpInterfaceBriefPipeIp', 'ShowLispExtranet', 'ShowBgpPolicyStatisticsParser']

EXCLUDE_DEVICES = ['Verify_BgpOpenconfigYang_yang',
                   'Verify_BgpProcessVrfAll_yang',
                   'Verify_BgpVrfAllNeighbors_yang_vrf_default',
                   'Verify_BgpInstanceNeighborsDetail_yang_vrf_type_all',
                   'Verify_BgpInstanceNeighborsDetail_yang_vrf_type_vrf_af_type_ipv4_unicast',
                   'Verify_BgpInstanceNeighborsDetail_yang_vrf_type_vrf_af_type_ipv6_unicast',
                   'Verify_BgpInstanceProcessDetail_yang_vrf_type_all',
                   'Verify_BgpInstanceProcessDetail_yang_vrf_type_vrf_af_type_ipv4_unicast',
                   'Verify_BgpInstanceProcessDetail_yang_vrf_type_vrf_af_type_ipv6_unicast',
                   'Verify_EthernetTags_yang',
                   'Verify_BgpPolicyStatisticsParser_xml',
                   'Verify_IpInterfaceBrief_yang', 'Verify_StandbyAll_yang',
                   'Verify_IpInterfaceBriefPipeVlan_yang',
                   'Verify_NveInterface']

CONTEXTS = ['cli', 'yang', 'xml', 'rest']
OSES = ['iosxe', 'ios', 'iosxr', 'nxos', 'junos']
YAMLS = os.path.join(os.environ['VIRTUAL_ENV'], 'genie_yamls')

class CreateVerificationDataFiles(object):
    def __init__(self):
        # No idea
        # Make sure we got a virtual_env
        assert 'VIRTUAL_ENV' in os.environ
        self.parsers = {}

    def find_all_parsers(self):
        # User should have pypi/genieparser location to use the the
        # verification_generator
        # Can't access parsers under projects in the new structured design
        path = ['pypi', 'genieparser', 'src', 'genie', 'libs', 'parser']
        root_dir = os.path.join(os.environ['VIRTUAL_ENV'],
                                'pypi',
                                'genieparser')

        for dirname, subdir, files in os.walk(root_dir):
            # dirName is how we categorize them - Right now only support os
            log.debug('Directory: {dirname}'.format(dirname=dirname))

            # For each file
            for file in files:
                # Safe assumption ?
                # Check class within, if no Schema in name, assume its a parser
                filename = Path(file)
                dirname = os.path.basename(dirname)
                if not filename.suffix == '.py' or\
                   filename.name == '__init__.py' or\
                   dirname not in OSES or\
                   dirname == 'tests' or\
                   dirname in path:
                    continue

                log.debug('File: {file}'.format(file=file))
                pythonpath = '{p}.{d}.{f}'.format(p='.'.join(path),
                                                  d=dirname,
                                                  f=filename.stem)
                module = importlib.import_module(pythonpath)
                for name, obj in inspect.getmembers(module):

                    # skip internal attributes
                    # ------------------------
                    # assuming anything starting with _, including __
                    if name.startswith('_'):
                        continue
                    # skip non-class items
                    # --------------------
                    if not inspect.isclass(obj):
                        continue

                    # Only get the parsers

                    if not issubclass(obj, MetaParser):
                        continue

                    if obj is MetaParser:
                        continue

                    # Assumption!
                    if 'schema' in name.lower():
                        continue

                    if name in EXCLUDE_PARSERS:
                        continue

                    # Rest is good
                    if dirname not in self.parsers:
                        self.parsers[dirname] = {}
                    if filename.stem not in self.parsers[dirname]:
                        self.parsers[dirname][filename.stem] = []

                    self.parsers[dirname][filename.stem].append(obj)

    def create_yaml_files(self, datafile):
        # Load existing Yaml file (If any)
        # Load main verifications datafiles
        #main_file = OrderedDict()
        main_file = {}
        nxos_file = {'extends': '%ENV{VIRTUAL_ENV}/genie_yamls/verification_datafile.yaml'}
        iosxe_file = {'extends': '%ENV{VIRTUAL_ENV}/genie_yamls/verification_datafile.yaml'}
        ios_file = {'extends': '%ENV{VIRTUAL_ENV}/genie_yamls/verification_datafile.yaml'}
        iosxr_file = {'extends': '%ENV{VIRTUAL_ENV}/genie_yamls/verification_datafile.yaml'}
        junos_file = {'extends': '%ENV{VIRTUAL_ENV}/genie_yamls/verification_datafile.yaml'}
        nxos = []
        iosxe = []
        ios = []
        iosxr = []
        junos = []        
        ios = []
        # Load the file
        with open(datafile, 'r') as f:
            parser_yaml = yaml.safe_load(f)

        main_yaml = os.path.join(YAMLS, 'verification_datafile.yaml')
        with open(main_yaml, 'r') as f:
            content = yaml.safe_load(f)

        nxos_yaml = os.path.join(YAMLS, 'nxos', 'verification_datafile_nxos.yaml')
        with open(nxos_yaml, 'r') as f:
            nxos_content = yaml.safe_load(f)

        iosxe_yaml = os.path.join(YAMLS, 'iosxe', 'verification_datafile_iosxe.yaml')
        with open(iosxe_yaml, 'r') as f:
            iosxe_content = yaml.safe_load(f)

        ios_yaml = os.path.join(YAMLS, 'ios', 'verification_datafile_ios.yaml')
        with open(ios_yaml, 'r') as f:
            ios_content = yaml.safe_load(f)

        iosxr_yaml = os.path.join(YAMLS, 'iosxr', 'verification_datafile_xr.yaml')
        with open(iosxr_yaml, 'r') as f:
            iosxr_content = yaml.safe_load(f)

        junos_yaml = os.path.join(YAMLS, 'junos', 'verification_datafile_junos.yaml')
        with open(junos_yaml, 'r') as f:
            junos_content = yaml.safe_load(f)

        # All parser should be in this verification datafile
        for osx in self.parsers:
            if osx == 'nxos':
                os_yaml = nxos_content
                os_file = nxos_file
                triggers = nxos
            elif osx == 'iosxe':
                os_yaml = iosxe_content
                os_file = iosxe_file
                triggers = iosxe
            elif osx == 'ios':
                os_yaml = ios_content
                os_file = ios_file
                triggers = ios
            elif osx == 'iosxr':
                os_yaml = iosxr_content
                os_file = iosxr_file
                triggers = iosxr
            elif osx == 'junos':
                os_yaml = junos_content
                os_file = junos_file
                triggers = junos

            for file in self.parsers[osx]:
                for parser in self.parsers[osx][file]:
                    # Check which context exists
                    for context in CONTEXTS:
                        if not hasattr(parser, context):
                            continue

                        parser_name = parser.__name__
                        # Verification name
                        verification_name = 'Verify_{p}'.format(p=parser_name.replace('Show', ''))
                        if context != 'cli':
                            verification_name = '{v}_{c}'.format(v=verification_name, c=context)

                        values = []
                        if parser_name in parser_yaml:

                            # initial index number
                            index_num = None
                            # For all of the combination, add it
                            # Make the lists ready to go
                            for key, items in sorted(parser_yaml[parser_name].items(), reverse=True):

                                if isinstance(items, dict):
                                    if key not in parser.__module__:
                                        continue
                                    for ky, val in sorted(items.items(), reverse=True):
                                        count = 0
                                        if ky == 'zos':
                                            try:
                                                index_num = val.index(osx)
                                            except:
                                                values.append(None)
                                                break
                                            continue

                                        if index_num is not None:
                                            val = val[index_num]

                                        for item in val:
                                            if item == '' or item is None:
                                                count += 1
                                                continue
                                            try:
                                                values[count].extend([ky, val[count]])
                                            except IndexError:
                                                values.append([ky, val[count]])
                                            count += 1

                                else:
                                    count = 0
                                    if key == 'zos':
                                        try:
                                            index_num = items.index(osx)
                                        except:
                                            values.append(None)
                                            break
                                        continue

                                    if index_num is not None:
                                        items = items[index_num]

                                    for item in items:
                                        if item == '' or item is None:
                                            count += 1
                                            continue
                                        try:
                                            values[count].extend([key, items[count]])
                                        except IndexError:
                                            values.append([key, items[count]])
                                        count += 1
                        else:
                            values.append(None)

                        for value in values:

                            if value is not None:
                                veri_name = '{v}_{e}'.format(v=verification_name,
                                                             e='_'.join(value).replace(' ', '_'))
                            else:
                                veri_name = verification_name

                            main_file[veri_name] = {}
                            main_file[veri_name]['source'] = {'class':'genie.harness.base.Template'}
                            main_file[veri_name]['context'] = context
                            main_file[veri_name]['cmd'] = {}
                            main_file[veri_name]['cmd']['pkg'] = 'genie.libs.parser'
                            main_file[veri_name]['cmd']['class'] = '{f}.{p}'.format(f=file, p=parser.__name__)

                            os_file[veri_name] = {}
                            if veri_name not in EXCLUDE_DEVICES:
                                os_file[veri_name]['devices'] = ['uut']

                            if value is not None:
                                for i in range(0,len(value),2):
                                    if value[i+1] != 'default':
                                        if 'parameters' not in os_file[veri_name]:
                                            os_file[veri_name]['parameters'] = {}
                                        os_file[veri_name]['parameters'][value[i]] = value[i+1]

                            if veri_name in content:
                                # Good already exists
                                # Do not copy source and cmd
                                # But keep the rest
                                try:
                                    del content[veri_name]['source']
                                except:
                                    pass
                                try:
                                    del content[veri_name]['cmd']
                                except:
                                    pass
                                merge_dict(main_file[veri_name], content[veri_name])

                            if veri_name in os_yaml:
                                merge_dict(os_file[veri_name], os_yaml[veri_name])
                            triggers.append(veri_name)

        # Create the files
        with open('verification_datafile.yaml', 'w') as f:
            yaml.dump(main_file, f, default_flow_style=False)

        self.clean_up('nxos')
        with open('nxos/verification_datafile_nxos.yaml', 'w') as f:
            yaml.dump(nxos_file, f, default_flow_style=False)

        self.clean_up('iosxe')
        with open('iosxe/verification_datafile_iosxe.yaml', 'w') as f:
            yaml.dump(iosxe_file, f, default_flow_style=False)

        self.clean_up('ios')
        with open('ios/verification_datafile_ios.yaml', 'w') as f:
            yaml.dump(ios_file, f, default_flow_style=False)

        self.clean_up('iosxr')
        with open('iosxr/verification_datafile_xr.yaml', 'w') as f:
            yaml.dump(iosxr_file, f, default_flow_style=False)

        self.clean_up('junos')
        with open('junos/verification_datafile_junos.yaml', 'w') as f:
            yaml.dump(junos_file, f, default_flow_style=False)

        log.info(banner('nxos'))
        log.info('\n'.join(nxos))

        log.info(banner('iosxe'))
        log.info('\n'.join(iosxe))

        log.info(banner('ios'))
        log.info('\n'.join(ios))

        log.info(banner('iosxr'))
        log.info('\n'.join(iosxr))

        log.info(banner('junos'))
        log.info('\n'.join(junos))
        
        return main_file

    def clean_up(self, dir):
        if os.path.isdir(dir):
            shutil.rmtree(dir)
        os.makedirs(dir)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-datafile',
                        metavar='FILE',
                        type=str,
                        default=None,
                        help='File containing parser information')
    custom_args = parser.parse_known_args()[0]

    cv = CreateVerificationDataFiles()
    cv.find_all_parsers()
    mail_file = cv.create_yaml_files(custom_args.datafile)
