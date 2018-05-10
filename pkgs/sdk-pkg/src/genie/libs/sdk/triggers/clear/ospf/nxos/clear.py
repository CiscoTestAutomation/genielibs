'''NXOS implementation for ospf clear triggers'''


from ..clear import TriggerClearIpOspfNeighborVrfAll,\
                    TriggerRestartOspf

class TriggerClearIpOspfNeighborVrfAll(TriggerClearIpOspfNeighborVrfAll):
    """Reset all Ospf neighbor connections using CLI command "clear ip ospf neighbor * vrf all"."""

    __description__ = """Reset all Ospf neighbor connections using CLI command "clear ip ospf neighbor * vrf all".

           trigger_datafile:
               Mandatory:
                   timeout:
                       max_time (`int`): Maximum wait time for the trigger,
                                       in second. Default: 180
                       interval (`int`): Wait time between iterations when looping is needed,
                                       in second. Default: 15
               Optional:
                   tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                        restored to the reference rate,
                                        in second. Default: 60
                   tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                      in second. Default: 10

           steps:
               1. Learn Ospf ops object and store the neighbor(s)
                  if has any, otherwise, SKIP the trigger
               2. Reset all the neighbors with command "clear ip ospf neighbor * vrf all"
               3. Learn Ospf Ops again, verify the last state change of neighbor(s) is reset,
                  and verify it is the same as the Ops in step 1 except the uptime
        """
    clear_cmd = ['clear ip ospf neighbor * vrf all']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'

class TriggerRestartOspf(TriggerRestartOspf):
    """Restart Ospf instances using command "clear ospf <instance>"."""

    __description__ = """Restart Ospf instance(s) using CLI command "restart ospf <instance>".

              trigger_datafile:
                  Mandatory:
                      timeout:
                          max_time (`int`): Maximum wait time for the trigger,
                                          in second. Default: 180
                          interval (`int`): Wait time between iterations when looping is needed,
                                          in second. Default: 15
                  Optional:
                      tgn_timeout (`int`): Maximum wait time for all traffic threads to be
                                           restored to the reference rate,
                                           in second. Default: 60
                      tgn_delay (`int`): Wait time between each poll to verify if traffic is resumed,
                                         in second. Default: 10

              steps:
                  1. Learn Ospf ops object and store the all neighbors
                     if has any, otherwise, SKIP the trigger
                  2. Restart Ospf instance(s) with command "restart ospf <instance>"
                  3. Learn Ospf Ops again and verify it is the same as the Ops in step 1
                     except the last state change
           """
    clear_cmd = ['restart ospf (?P<instance>.*)']

    # Operator representing the relation between uptime and
    # waiting time for waiting, for the device to be steady
    sign='<'