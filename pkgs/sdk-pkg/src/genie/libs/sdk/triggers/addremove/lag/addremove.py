'''Implementation for routing addremove triggers'''

# import genie.libs
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove


class TriggerAddRemoveTrunkEtherchannelLacp(TriggerAddRemove):
    pass

class TriggerAddRemoveAccessEtherchannelPagp(TriggerAddRemoveTrunkEtherchannelLacp):
    pass

class TriggerAddRemoveL3EtherchannelPagp(TriggerAddRemoveTrunkEtherchannelLacp):
    pass