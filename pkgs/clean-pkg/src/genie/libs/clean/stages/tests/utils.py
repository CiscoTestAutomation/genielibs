from unittest.mock import Mock


from genie.conf.base import Device

# Since this class doesnt inherit from 'unittest.Testcase'
# these tests wont run by themselves.
class CommonStageTests:

    def test_exec_order(self):
        exec_order = set(self.cls.exec_order)
        cls_attributes = set(dir(self.cls))

        self.assertTrue(exec_order.issubset(cls_attributes),
                        "The following methods are defined in 'exec_order' "
                        "but do not exist within the class: "
                        "{}".format(exec_order - cls_attributes))


def create_test_device(name, os, platform=None):
    """This function does boilerplate work of creating a device for unittests.

    - Sets the device os and platform
    - Sets the device abstraction order
    - Modifies device attributes to simulate being connected
    - Mocks the configure method

    Arguments:
        name (str): The name of the new device.
        os (str): The os of the new device.
        platform (str, optional): The platform of the new device.

    returns:
        device (obj): That is ready to be used to unittests.
    """

    if platform:
        device = Device(name, os=os, platform=platform)
    else:
        device = Device(name, os=os)

    device.custom.abstraction = {'order': ['os', 'platform']}

    # This enables calling parsers without explicitly passing output.
    device.is_connected = Mock(return_value=True)
    setattr(device, 'cli', device)

    device.configure = Mock()

    return device
