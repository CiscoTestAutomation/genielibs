""" NXOS ACI Specific Clean Stages """

import os
import json
import logging
import time

from genie.libs.clean.utils import clean_schema
from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout

from pyats import aetest

from unicon.eal.dialogs import Statement, Dialog

log = logging.getLogger(__name__)

@clean_schema({
    Optional('controller_image'): list,
    Optional('switch_image'): list,
    Optional('switch_group_name'): str,
    Optional('clear_switch_group'): bool,
    Optional('sleep_after_delete'): int,
    Optional('switch_group_nodes'): list,
    Optional('timeouts'): {
        Optional('firmware_repository_add'): int,
        Optional('controller_upgrade'): int,
        Optional('controller_reconnect'): int,
        Optional('switch_upgrade'): int,
        Optional('controller_upgrade_after_reconnect'): int,
        Optional('switch_upgrade'): int,
        Optional('stabilize_switch_group_config'): int,
    }
})
@aetest.test
def fabric_upgrade(section, steps, device, controller_image=None, switch_image=None,
                   switch_group_name='switches', clear_switch_group=True,
                   sleep_after_delete=5, switch_group_nodes=None, timeouts=None):
    """ This stage upgrades (or downgrades) the firmware version for APIC
    devices. This includes the controller-group and the switch-group.

    Stage Schema
    ------------
    fabric_upgrade:

        controller_image (list, optional): Contains the controller image.
            Defaults to None.

        switch_image (list, optional): Contains the switch image. Defaults to
            None.

        switch_group_name (str, optional): The name of the switch-group to
            create. Defaults to switches.

        clear_switch_group (bool, optional): Whether or not to clear the
            switch-group configuration before configuring it. Defaults to True.

        sleep_after_delete (int, optional): How long in seconds to sleep after
            clearing the firmware repository. Defaults to 5.

        switch_group_nodes (list, optional): Contains the Nodes which will
            be added to the switch_group_name. Defaults to None.

        timeouts (dict, optional):

            firmware_repository_add (int, optional): Max time in seconds allowed
                for adding images to the firmware repository. Defaults to
                300 (5 mins).

            controller_upgrade (int, optional): Max time in seconds allowed for
                upgrading the controller. Defaults to 1800 (30 mins).

            controller_reconnect (int, optional): Max time in seconds allowed
                for reconnecting to the controller during upgrade. This may
                occur if there is only one controller. Defaults to 900 (15 mins).

            controller_upgrade_after_reconnect (int, optional): Max time in
                seconds allowed for completing the controller upgrade after
                reconnecting. Defaults to 300 (5 mins).

            switch_upgrade (int, optional): Max time in seconds allowed for
                upgrading switches. Defaults to 2700 (45 mins).

            stabilize_switch_group_config (int, optional): Time to sleep after
                configuring the switch-group. Defaults to 120 (2 mins).

    Example
    -------
    fabric_upgrade:
        switch_group_name: my_switches
        switch_group_nodes: [switch1, switch2]
    """

    # Setup default timeouts
    if timeouts is None:
        timeouts = {}
    timeouts.setdefault('firmware_repository_add', 300) # 5 minutes
    timeouts.setdefault('controller_upgrade', 1800) # 30 minutes
    timeouts.setdefault('controller_reconnect', 900) # 15 minutes
    timeouts.setdefault('controller_upgrade_after_reconnect', 300) # 5 minutes
    timeouts.setdefault('switch_upgrade', 2700) # 45 minutes
    timeouts.setdefault('stabilize_switch_group_config', 120) # 2 minutes

    error_patterns = [
        r".*Command execution failed.*"
    ]

    with steps.start("Updating firmware repository") as step:

        with step.start("Clearing firmware repository") as substep:
            result = device.api.execute_clear_firmware_repository(
                sleep_after_delete=sleep_after_delete)

            if not result:
                substep.failed("Images still exist in the firmware repository")

        if controller_image:
            with step.start("Adding controller-image to the firmware repository") as substep:
                controller_image = controller_image[0]

                device.execute('firmware repository add {}'.format(controller_image),
                               timeout=timeouts['firmware_repository_add'],
                               error_pattern=error_patterns)

                images = device.api.get_firmware_repository_images_by_polling(
                    image_type='controller',
                    max_time=timeouts['firmware_repository_add'])

                if not images:
                    substep.failed("Firmware did not exist in the repository "
                                   "after timeout was reached")

                controller_image = images[0]

                substep.passed("Found newly added controller firmware '{}'"
                               .format(controller_image))

        if switch_image:
            with step.start("Adding switch-image to the firmware repository") as substep:
                switch_image = switch_image[0]

                device.execute('firmware repository add {}'.format(switch_image),
                               timeout=timeouts['firmware_repository_add'],
                               error_pattern=error_patterns)

                images = device.api.get_firmware_repository_images_by_polling(
                    image_type='switch',
                    max_time=timeouts['firmware_repository_add'])

                if not images:
                    substep.failed("Firmware did not exist in the repository "
                                   "after timeout was reached")

                switch_image = images[0]

                substep.passed("Found newly added switch firmware '{}'"
                               .format(switch_image))

    with steps.start("Installing new firmware") as step:

        if controller_image:
            with step.start("Installing '{}' firmware onto the controller-group"
                            .format(controller_image)) as substep:

                result = device.api.execute_install_controller_group_firmware(
                    controller_image=controller_image,
                    controller_upgrade_max_time=timeouts['controller_upgrade'],
                    controller_reconnect_max_time=timeouts['controller_reconnect'],
                    controller_upgrade_after_reconnect_max_time=timeouts['controller_upgrade_after_reconnect']
                )

                if not result:
                    substep.failed("Controller firmware install failed.")

        if switch_image and switch_group_nodes and switch_group_name:

            step_msg = "Installing '{firmware}' firmware onto the switch-group " \
                       "'{switch_group}'".format(firmware=switch_image,
                                                 switch_group=switch_group_name)

            with step.start(step_msg) as substep:

                # Get switch node ids from testbed datafile, convert them into a string
                # separated by commas
                switch_nodes = []
                for node in switch_group_nodes:
                    if node not in device.testbed.devices:
                        substep.failed("The node '{dev}' that was provided, does not "
                                       "exist in the testbed yaml".format(dev=node))

                    node = device.testbed.devices[node]
                    node_id = node.custom.get('node_id')
                    if not node_id:
                        substep.failed("The node '{dev}' that was provided, does not "
                                       "have a '{dev}.custom.node_id' attribute."
                                       .format(dev=node))

                    switch_nodes.append(str(node_id))
                switch_nodes = ','.join(switch_nodes)

                # Do the install and verify
                result = device.api.execute_install_switch_group_firmware(
                    switch_image=switch_image,
                    switch_node_ids=switch_nodes,
                    switch_group_name=switch_group_name,
                    clear_switch_group=clear_switch_group,
                    switch_upgrade_max_time=timeouts['switch_upgrade'],
                    stabilize_switch_group_config_sleep=timeouts['stabilize_switch_group_config'],
                    controller_reconnect_max_time=timeouts['controller_reconnect'],
                )

                if not result:
                    substep.failed("Switch-group firmware install failed.")

@clean_schema({
    Optional("cleaning_timeout"): int,
    Optional("reload_timeout"): int,
    Optional("sleep_after_reload"): int,
})
@aetest.test
def fabric_clean(section, steps, device, cleaning_timeout=90, reload_timeout=800,
                 sleep_after_reload=60):
    """ This stage will clean APIC controllers.

    The stage will execute 'acidiag touch clean' and then reload the controller.

    Stage Schema
    ------------
    fabric_clean:

        cleaning_timeout (int, optional): Max time for cleaning scripts to execute.
            Defaults to 90.

        reload_timeout (int, optional): Max time for reload. Defaults to 800.

        sleep_after_reload (int, optional): Time in seconds to sleep after the
            device completes reloading. Defaults to 60.

    Example
    -------
    fabric_clean:
        cleaning_timeout: 90
    """

    with steps.start("Cleaning the device") as step:
        result = device.api.execute_clean_controller_fabric(
            max_time=cleaning_timeout)

        if not result:
            step.failed("Failed to clean the device")
        else:
            step.passed("Successfully cleaned the device")

    with steps.start("Reloading '{dev}'".format(dev=device.name)):

        reload_dialog = Dialog([
            Statement(
                pattern=r".*This command will restart this device\, Proceed\? \[y\/N\].*",
                action='sendline(y)'
            )
        ])

        device.sendline('acidiag reboot')
        reload_dialog.process(device.spawn)

    with steps.start("Waiting for {dev} to reload".format(dev=device.hostname)) as step:
        timeout = Timeout(reload_timeout, 60)
        while timeout.iterate():
            timeout.sleep()
            device.destroy()

            try:
                device.connect(learn_hostname=True)
            except Exception:
                log.info("{dev} is not reloaded".format(dev=device.hostname))
            else:
                step.passed("{dev} has successfully reloaded".format(dev=device.hostname))

        step.failed("{dev} failed to reboot".format(dev=device.hostname))

    log.info("Sleeping for '{}' seconds for '{}' to stabilize."
             .format(sleep_after_reload, device.name))

    time.sleep(sleep_after_reload)

@clean_schema({
    "nodes": list,
    Optional("rest_alias"): str,
    Optional("verify_max_time"): int,
    Optional("verify_interval"): int
})
@aetest.test
def node_registration(section, steps, device, nodes, rest_alias='rest',
                      verify_max_time=480, verify_interval=30):
    """ This stage registers nodes on APIC using REST API.

    Stage Schema
    ------------
    node_registration:

        nodes (list): Nodes to register on APIC

        rest_alias (str, optional): Connection alias for REST connection.
            Defaults to 'rest'.

        verify_max_time (int, optional): Max time to verify node registration.
            Defaults to 480.

        verify_interval (int, optional): How often to attempt verify node registration.
            Defaults to 30.

    Example
    -------
    node_registration:
        nodes: [Spine1, Spine2]
        rest_alias: cli
    """

    with steps.start("Registering nodes") as step:
        # Register each node
        result = device.api.execute_register_nodes(
            nodes=nodes, rest_alias=rest_alias)

        if not result:
            step.failed("Node registration failed")
        else:
            step.passed("Node registration completed")

    with steps.start("Verifying all nodes are registered and active") as step:

        node_ids = []
        for node in nodes:
            if node not in device.testbed.devices:
                step.failed("The node '{dev}' that was provided, does not "
                            "exist in the testbed yaml".format(dev=node))

            node = device.testbed.devices[node]
            node_ids.append(int(node.custom['node_id']))

        if not device.api.verify_aci_registered_nodes_in_state(
            node_ids=node_ids,
            state='active',
            max_time=verify_max_time,
            check_interval=verify_interval
        ):
            step.failed("Not all nodes are registered and active")

        step.passed("All nodes are registered and active")

