
__all__ = (
    'Rip',
)

from genie.utils.cisco_collections import typedset

from genie.decorator import managedattribute
from genie.conf.base import DeviceFeature, LinkFeature, InterfaceFeature
import genie.conf.base.attributes
from genie.conf.base.attributes import SubAttributes, SubAttributesDict, AttributesHelper

from genie.libs.conf.base import Routing
from genie.libs.conf.address_family import AddressFamily, AddressFamilySubAttributes
from genie.libs.conf.vrf import Vrf, VrfSubAttributes


class Rip(Routing, DeviceFeature, LinkFeature, InterfaceFeature):
    """Rip class

    `Rip` inherits `Feature' class. The class defines all rip related
    information and functionalities.

    Args:


    Returns:
            a `Rip` object

    """

    # When adding a rip instance to a link, all the interfaces in this link
    # needs to be told about the rip object.
    # this syntax means : all interfaces
    register_name = {}
    register_name['interfaces'] = 'rip'

    instance_id = managedattribute(
        name='instance_id',
        read_only=True,  # mandatory
        doc='RIP Instance ID')

    shutdown = managedattribute(
        name='shutdown',
        default=None,
        type=(None, managedattribute.test_istype(bool)))

    address_families = managedattribute(
        name='address_families',
        finit=typedset(AddressFamily, {AddressFamily.ipv4_unicast}).copy,
        type=typedset(AddressFamily)._from_iterable)

    # AddressFamilyAttributes

    distance = managedattribute(
        name='distance',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    maximum_paths = managedattribute(
        name='maximum_paths',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    default_metric = managedattribute(
        name='default_metric',
        default=None,
        type=(None, managedattribute.test_istype(int)))

    redistribute_lisp_rmap = managedattribute(
        name='redistribute_lisp_rmap',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    redistribute_direct_rmap = managedattribute(
        name='redistribute_direct_rmap',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    redistribute_static_rmap = managedattribute(
        name='redistribute_static_rmap',
        default=None,
        type=(None, managedattribute.test_istype(str)))

    @property
    def vrfs(self):
        return \
            self.force_vrfs | \
            {intf.vrf for intf in self.interfaces}

    force_vrfs = managedattribute(
        name='force_vrfs',
        read_only=True,
        finit=set,
        gettype=frozenset)
    # XXXJST TODO force_vrfs needs to also be accessible per-device. Being read_only, that can't happen

    def add_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.add(vrf)

    def remove_force_vrf(self, vrf):
        assert vrf is None or isinstance(vrf, Vrf)
        self.force_vrfs  # init!
        self._force_vrfs.remove(vrf)

    class DeviceAttributes(genie.conf.base.attributes.DeviceSubAttributes):
        """DeviceAttributes class

        `DeviceAttributes` contains attributes and functionalities
        that are specific for a device.

        Args:
            kwargs (`dict`) : assign attributes to this object while
                              creating it.

        Returns:
            a `DeviceAttributes` object
        """

        enabled_feature = managedattribute(
            name='enabled_feature',
            default=False,
            type=managedattribute.test_istype(bool),
            doc='''Argument to control 'feature rip' CLI''')

        address_families = managedattribute(
            name='address_families',
            type=typedset(AddressFamily)._from_iterable)

        @address_families.defaulter
        def address_families(self):
            return frozenset(self.parent.address_families)

        @property
        def vrfs(self):
            return \
                self.force_vrfs | \
                {intf.vrf for intf in self.interfaces}

        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        class VrfAttributes(VrfSubAttributes):
            """ VrfAttributes class

            `VrfAttributes` inherits from `SubAttributes' class.
             It contains all vrf related attributes and
             functionalities. Class contains some powers to access
             its parent attributes.

            Args:
                kwargs (`dict`) : gives the user ability to assign some or all
                                  address family attributes while creating the
                                  object.

            """

            def __init__(self, **kwargs):
                super().__init__(**kwargs)

            address_families = managedattribute(
                name='address_families',
                type=typedset(AddressFamily)._from_iterable)

            @address_families.defaulter
            def address_families(self):
                return frozenset(self.parent.address_families)

            class AddressFamilyAttributes(AddressFamilySubAttributes):
                """ AddressFamilyAttributes class

                `AddressFamilyAttributes` inherits from `SubAttributes' class.
                 It contains all address family related attributes and
                 functionalities. Class contains some powers to access
                 its parent attributes.

                Args:
                    kwargs (`dict`) : gives the user ability to assign some or all
                                      address family attributes while creating the
                                      object.

                Class variables:

                    allowed_keys (`List`): list of all allowed 'keys' the object can
                                      access.

                """

                allowed_keys = (
                    AddressFamily.ipv4_unicast,
                    AddressFamily.ipv6_unicast,
                )

            address_family_attr = managedattribute(
                name='address_family_attr',
                read_only=True,
                doc=AddressFamilyAttributes.__doc__)

            @address_family_attr.initter
            def address_family_attr(self):
                return SubAttributesDict(self.AddressFamilyAttributes, parent=self)

        vrf_attr = managedattribute(
            name='vrf_attr',
            read_only=True,
            doc=VrfAttributes.__doc__)

        @vrf_attr.initter
        def vrf_attr(self):
            return SubAttributesDict(self.VrfAttributes, parent=self)

    device_attr = managedattribute(
        name='device_attr',
        read_only=True,
        doc=DeviceAttributes.__doc__)

    @device_attr.initter
    def device_attr(self):
        return SubAttributesDict(self.DeviceAttributes, parent=self)

    def __init__(self, instance_id, **kwargs):
        '''Rip Base class'''
        self._instance_id = int(instance_id)
        super().__init__(**kwargs)

    def build_config(self, devices=None, apply=True, attributes=None, **kwargs):
        """method to build the configuration based on attributes

        Api to build the configuration of an Rip object.
        This configuration depends of the configurable attributes of
        this object.

        If Apply is set to True, then it will apply on the device(s)
        If it is set to False, then it will return a dictionary.

        If any kwargs are passed, then the configuration that is built
        will use those kwargs given, and not the object attributes. This
        is useful for modifying the configuration, without re-applying
        everything.


        Args:
            apply (`bool`): If True will apply the configuration on the device
                            and if False will return the configuration in a
                            dictionary
            kwargs (`dict`): If there is kwargs, then it will use those
                             attributes to configure the feature. Otherwise
                             will use the object attributes

        Return:
            `str`
        """
        attributes = AttributesHelper(self, attributes)

        # Get devices if none were passed
        if devices is None:
            devices = self.devices

        # For each device, loop over device_attr
        cfgs = {}
        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices):
            cfgs[key] = sub.build_config(apply=False, attributes=attributes2, **kwargs)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            # Return configuration
            return cfgs

    def build_unconfig(self, devices=None, apply=True, attributes=None, **kwargs):
        """method to build the unconfiguration based on attributes

        Api to build the unconfiguration of an Rip object.
        This configuration depends of the configurable attributes of
        this object.

        If Apply is set to True, then it will apply on the device(s)
        If it is set to False, then it will return a dictionary.

        If any kwargs are passed, then the configuration that is built
        will use those kwargs given, and not the object attributes. This
        is useful for modifying the configuration, without re-applying
        everything.


        Args:
            apply (`bool`): If True will apply the configuration on the device
                            and if False will return the configuration in a
                            dictionary
            kwargs (`dict`): If there is kwargs, then it will use those
                             attributes to configure the feature. Otherwise
                             will use the object attributes

        Return:
            `str`
        """
        attributes = AttributesHelper(self, attributes)

        # Get devices if none were passed
        if devices is None:
            devices = self.devices

        # For each device, loop over device_attr
        cfgs = {}
        for key, sub, attributes2 in attributes.mapping_items('device_attr', keys=devices):
            cfgs[key] = sub.build_unconfig(apply=False, attributes=attributes2, **kwargs)

        if apply:
            self.testbed.config_on_devices(cfgs, fail_invalid=True)
        else:
            # Return configuration
            return cfgs
