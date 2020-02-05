'''Implementation for vlan modify triggers'''
import re
import logging


log = logging.getLogger(__name__)

# Genie Libs
from genie.libs.sdk.libs.utils.mapping import Mapping
from genie.libs.sdk.triggers.modify.modify import TriggerModify
from pyats import aetest

# Which key to exclude for VXLAN Ops comparison
vlan_exclude = ['maker', 'uptime']


class TriggerModifyVlanVnsegment(TriggerModify):
    """Modify and revert the vnsegemnt for dynamically learned vlan(s)."""

    __description__ = """Modify and revert the vnsegemnt for dynamically learned vlan(s).

    trigger_datafile:
        Mandatory:
            timeout: 
                max_time (`int`): Maximum wait time for the trigger,
                                in second. Default: 180
                interval (`int`): Wait time between iteration when looping is needed,
                                in second. Default: 15
                method (`str`): Method to recover the device configuration,
                              Support methods:
                                'checkpoint': Rollback the configuration by
                                              checkpoint (nxos),
                                              archive file (iosxe),
                                              load the saved running-config file on disk (iosxr)
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

                vlan: `str`
                vn_segment: `int`

                (e.g) interface: '(?P<interface>Ethernet1*)' (Regex supported)
                      OR
                      interface: 'Ethernet1/1/1' (Specific value)

    steps:
        1. Learn Vlan Ops object and store the vlan which is active and has vnsegment.
            SKIP the trigger if there is no VLAN(s) found
        2. Save the current device configurations through "method" which user uses
        3. Modify the vnsegment of the learned VLAN from step 1 with VLAN Conf object
        4. Verify the vnsegment of the learned VLAN  from step 3
           changes to the modified value in step 3,
        5. Recover the device configurations to the one in step 2
        6. Learn VLAN Ops again and verify it is the same as the Ops in step 1

    """

    VN_SEGMENT = 1111

    @aetest.test
    def modify_configuration(self, uut, abstract, steps):
        '''Modify configuration on the uut device

           Args:
               uut (`obj`): Device object.
               abstract (`obj`): Abstract object.
               steps (`step obj`): aetest step object

           Returns:
               None

           Raises:
               pyATS Results
        '''
        # Flap vlan for config change to take effect
        cmd = "vlan (?P<vlan>.*)\n" \
              " no vn-segment\n" \
              " vn-segment {}\n".format(self.VN_SEGMENT)
        x = re.findall(r'\S+|\n', cmd)
        req = self.mapping._path_population([x], uut)
        req_str = []
        for item in req[0]:
            req_str.append(str(item))

        cmd = ' '.join(req_str)
        try:
            uut.configure(cmd)
        except Exception as e:
            self.failed('Failed to modify the configuration', from_exception=e)

    # Mapping of Information between Ops and Conf
    # Also permit to dictates which key to verify
    mapping = Mapping(requirements={'ops.vlan.vlan.Vlan':{
                                          'requirements':[['info', 'vlans', '(?P<vlan>.*)', 'state', 'active'],
                                                          ['info', 'vlans', '(?P<vlan>.*)', 'vn_segment_id', '(?P<vn_segment>^(?!1111).*)$']],
                                          'kwargs':{'attributes':['info[vlans][(.*)][vn_segment_id]',
                                                                  'info[vlans][(.*)][state]']},
                                          'all_keys':True,
                                          'exclude': vlan_exclude}},
                      config_info={'conf.vlan.Vlan':{
                                     'requirements':[['device_attr', '{uut}', 'vlan_attr', '(?P<vlan>.*)',\
                                                      'vn_segment_id', VN_SEGMENT]],
                                     'verify_conf':False,
                                     'kwargs':{}}},
                      verify_ops={'ops.vlan.vlan.Vlan':{
                                    'requirements':[['info','vlans','(?P<vlan>.*)','state','active'],
                                                    ['info','vlans','(?P<vlan>.*)','vn_segment_id',VN_SEGMENT]],
                                    'kwargs':{'attributes':['info[vlans][(.*)][vn_segment_id]',
                                                            'info[vlans][(.*)][state]']},
                                    'exclude': vlan_exclude}},
                      num_values={'vlan': 1})



