'''Implementation for routing addremove triggers'''

# import genie.libs
from genie.libs.sdk.triggers.addremove.addremove import TriggerAddRemove


class TriggerAddRemoveIpv4StaticRoutes(TriggerAddRemove):
    pass


class TriggerAddRemoveIpv6StaticRoutes(TriggerAddRemoveIpv4StaticRoutes):
    pass