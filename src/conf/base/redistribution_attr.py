__all__ = (
    'Redistribution',
)

from genie.decorator import managedattribute

from .routing import Routing


def _defer_route_policy_type(value):
    # Avoid the cyclic dependency by deferring the route_policy type
    # transformations
    from genie.libs.conf.route_policy import RoutePolicy
    transforms = (
        None,
        managedattribute.test_isinstance(RoutePolicy))
    # Cache for speed
    Redistribution.route_policy = Redistribution.route_policy.copy(
        type=transforms)
    return managedattribute._transform(value, transforms)


class Redistribution(object):

    protocol = managedattribute(
        name='protocol',
        type=(
            managedattribute.test_in((
                'connected',
                'subscriber',
            )),
            managedattribute.test_isinstance(Routing)))

    metric = managedattribute(
        name='metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    route_policy = managedattribute(
        name='route_policy',
        default=None,
        type=_defer_route_policy_type)

    def __init__(self, protocol, **kwargs):

        if not kwargs and isinstance(protocol, Redistribution):
            # copy constructor
            kwargs = vars(protocol)
        else:
            self.protocol = protocol

        for k, v in kwargs.items():
            setattr(self, k, v)

