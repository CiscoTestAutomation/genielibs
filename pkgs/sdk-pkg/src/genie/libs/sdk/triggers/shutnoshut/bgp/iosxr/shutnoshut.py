'''IOSXR implementation for shutnoshut triggers'''

# import python
import logging

# import pyats
from pyats import aetest

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.shutnoshut.shutnoshut import \
                       TriggerShutNoShut as CommonShutNoShut

from pyats.utils.objects import NotExists

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
        with steps.start("Shut Bgp process") as step:
          try:
              uut.execute("process shutdown bgp")
          except Exception as e:
              step.failed('Failed to shut the feature', from_exception=e)

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
        with steps.start("UnShut Bgp process") as step:
          try:
              uut.execute("process restart bpm")
          except Exception as e:
              step.failed('Failed to shut the feature', from_exception=e)

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

    trigger_datafile:
        Mandatory:
            timeout:
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
        Optional:
            tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                 restored to the reference rate,
                                 in second. Default: 60
            tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                               in second. Default: 10
            timeout_recovery:
                Buffer recovery timeout make sure devices are recovered at the end
                of the trigger execution. Used when previous timeouts have been exhausted.

                max_time (`int`): Maximum wait time for the last step of the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
            static:
                 The keys below are dynamically learnt by default.
                 However, they can also be set to a custom value when provided in the trigger datafile.

                 instance: `str`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn BGP Ops object and store the BGP instance(s)
           if has any, otherwise, SKIP the trigger
        2. Do "process shutdown bgp"
        3. Verify the protocol state in BGP instance(s) is "KILLED"
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
                                    'requirements': [['info', 'instance', '(?P<instance>.*)', 'protocol_state', 'KILLED'],
                                                    ['info', 'instance', '(?P<instance>.*)', NotExists('vrf')]],
                                    'kwargs':{'attributes':['info']},
                                    'exclude': bgp_exclude}},
                      num_values={'instance':'all'})
