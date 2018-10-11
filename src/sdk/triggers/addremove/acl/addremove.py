'''Implementation for routing addremove triggers'''

# import genie.libs
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove


class TriggerAddRemoveEthernetMacAcl(TriggerAddRemove):
    pass

class TriggerAddRemoveEthernetIpAclPermit(TriggerAddRemove):
    pass

class TriggerAddRemoveEthernetIpAclDeny(TriggerAddRemove):
    pass

class TriggerAddRemoveVlanIpAclPermit(TriggerAddRemove):
    pass
