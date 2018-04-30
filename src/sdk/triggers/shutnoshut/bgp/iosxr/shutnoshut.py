'''IOSXR implementation for shutnoshut triggers'''

# import python
import logging

# import ats
from ats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import \
                       TriggerShutNoShut as CommonShutNoShut

log = logging.getLogger(__name__)


# Inherit sections only for IOSXR
class TriggerShutNoShut(CommonShutNoShut):
    '''Trigger class for ShutNoShut action'''

    @aetest.test
    def shut(self, uut, method, abstract, steps):
        '''Send configuration to shut

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # shut BGP process
        try:
            uut.execute("process shutdown bgp")
        except Exception as e:
            self.failed('Failed to shut the feature', from_exception=e)

    @aetest.test
    def unshut(self, uut, method, abstract, steps):
        '''restart process bpm, cause bgp cannot be started from sysmgr.
           This is workaround for known xr bgp bugs, should use 'process start bgp'
            when bug fixes

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''

        # unshut BGP process
        # workaround: shut bpm instead of bgp cause bgp cannot be started from sysmgr.
        # known bug: CSCtr26693
        try:
            uut.execute("process restart bpm")
        except Exception as e:
            self.failed('Failed to shut the feature', from_exception=e)

# Trigger required data settings
# Which key to exclude for BGP Ops comparison
bgp_exclude = ['maker', 'bgp_session_transport', 'route_refresh',
               'bgp_negotiated_capabilities', 'notifications', 'capability',
               'keepalives', 'total', 'total_bytes', 'up_time', 'last_reset',
               'bgp_negotiated_keepalive_timers', 'updates', 'opens', 'totals',
               'bgp_table_version', 'holdtime', 'keepalive_interval']


class TriggerShutNoShutBgp(TriggerShutNoShut):
    """Shut BGP protocol by shutdown the dynamically learned BGP process,
    then unshut it by restart bpm. """
    
    __description__ = """Shut BGP protocol by shutdown the dynamically learned BGP process,
    then unshut it by restart bpm. 

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Do "process shutdown bgp"
        3. Verify the state of BGP instance(s) is "KILLED"
        4. Do "process restart bpm"
        5. Learn BGP Ops again and verify it is the same as the Ops in step 1

    """

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.bgp.bgp.Bgp':{
                                          'requirements':[['info', 'instance', '(?P<instance>.*)',
                                                           '(?P<instance_info>.*)']],
                                        'kwargs':{'attributes':['info']},
                                        'exclude': bgp_exclude}},
                      verify_ops={'ops.bgp.bgp.Bgp':{
                                    'requirements': [['info', 'instance', '(?P<instance>.*)',
                                                      'protocol_state', 'KILLED'],
                                                     ['info', 'instance', '(?P<instance>.*)',
                                                      '(.*)']],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':'all'})
