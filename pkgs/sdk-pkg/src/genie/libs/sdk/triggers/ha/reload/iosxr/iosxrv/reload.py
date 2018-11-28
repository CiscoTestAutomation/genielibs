'''IOSXRv implementation for Reload triggers'''

# import python
import logging

# import ats
from ats import aetest
from ats.utils.objects import R

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from ..reload import TriggerReload as CommonReload

log = logging.getLogger(__name__)

# Trigger required data settings
# Which key to exclude for Platform Ops comparison
platform_exclude = ['maker', 'total_free_bytes', 'rp_uptime']


class TriggerReload(CommonReload):

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.platform.platform.Platform':{
                                        'requirements': [\
                                            ['slot', 'rp', '(?P<rp>.*)',
                                              'state', 'IOS XR RUN'],
                                            ['slot', 'lc', '(?P<lc>.*)',
                                              'state', '(?P<state>IOS XR RUN|OK)'],
                                          ],
                                        'all_keys': True,
                                        'exclude': platform_exclude}},
                      verify_ops={'ops.platform.platform.Platform':{
                                      'requirements': [\
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'state', 'IOS XR RUN'],
                                          ['slot', 'rp', '(?P<rp>.*)',
                                           'redundancy_state', '(Active|Standby)'],
                                          ['slot', 'lc', '(?P<lc>.*)',
                                           'state', '(IOS XR RUN|OK)']],
                                    'exclude': platform_exclude}},
                      num_values={'rp': 'all', 'lc': 'all'})

