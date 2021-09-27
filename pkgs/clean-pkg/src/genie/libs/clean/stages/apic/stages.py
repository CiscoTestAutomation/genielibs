""" NXOS ACI Specific Clean Stages """

import os
import logging
import time

from genie.metaparser.util.schemaengine import Optional
from genie.utils.timeout import Timeout
from genie.libs.clean import BaseStage
from genie.libs.clean.utils import (
    find_clean_variable,
    verify_num_images_provided,
    remove_string_from_image)
from genie.libs.sdk.apis.nxos.aci.firmware.get import (
    get_firmware_version_from_image_name as nxos_aci_get_firmware_version_from_image_name)
from genie.libs.sdk.apis.apic.firmware.get import (
    get_firmware_version_from_image_name as apic_get_firmware_version_from_image_name)

from pyats.utils.fileutils import FileUtils

from unicon.eal.dialogs import Statement, Dialog


log = logging.getLogger(__name__)


class FabricUpgrade(BaseStage):
    """This stage upgrades (or downgrades) the firmware version for APIC
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

    # =================
    # Argument Defaults
    # =================
    CONTROLLER_IMAGE = None
    SWITCH_IMAGE = None
    SWITCH_GROUP_NAME = 'switches'
    CLEAR_SWITCH_GROUP = True
    SLEEP_AFTER_DELETE = 5
    SWITCH_GROUP_NODES = None
    TIMEOUTS = {
        'firmware_repository_add': 300,
        'controller_upgrade': 1800,
        'controller_reconnect': 900,
        'controller_upgrade_after_reconnect': 300,
        'switch_upgrade': 2700,
        'stabilize_switch_group_config': 120
    }

    error_patterns = [
        r".*Command execution failed.*"
    ]

    # ============
    # Stage Schema
    # ============
    schema = {
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
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'check_fabric_versions',
        'update_firmware_repository',
        'install_firmware'
    ]

    def check_fabric_versions(self, steps, device, controller_image=CONTROLLER_IMAGE,
                              switch_image=SWITCH_IMAGE,
                              switch_group_nodes=SWITCH_GROUP_NODES):
        with steps.start('Checking fabric versions') as step:
            if not device.connected:
                device.connect()
            version_info = device.parse('show version')
            try:
                controller_version = version_info['pod'][1]['node'][1]['version']
            except KeyError:
                log.debug('Could not get info from show version', exc_info=True)
                controller_version = 'unknown'

            if controller_image:
                with step.start("Checking controller image version") as substep:
                    controller_image_version = device.api.get_firmware_version_from_image_name(controller_image[0])

                    if controller_version == controller_image_version:
                        log.debug('Controller upgrade not needed, skipping')
                        self.upgrade_controller = False
                        upgrade_msg = ''
                    else:
                        self.upgrade_controller = True
                        upgrade_msg = ', upgrade needed'

                    log.info('Controller {} version: {}, controller image version: {}{}'.format(
                        device.name,
                        controller_version,
                        controller_image_version,
                        upgrade_msg))

            if switch_image and switch_group_nodes:
                switches_to_upgrade = []
                with step.start("Checking switch image versions") as substep:
                    for node in switch_group_nodes:
                        if node not in device.testbed.devices:
                            substep.failed("The node '{dev}' that was provided, does not "
                                           "exist in the testbed yaml".format(dev=node))

                        node_device = device.testbed.devices[node]
                        node_image_version = node_device.api.get_firmware_version_from_image_name(switch_image[0])
                        log.debug('Switch {} image: {}, version {}'.format(
                            node_device.name,
                            switch_image[0],
                            node_image_version))

                        try:
                            switch_version = version_info['pod'][1]['node'][int(node_device.custom.get('node_id'))]['version']
                        except KeyError:
                            log.debug('Could not get info from show version', exc_info=True)
                            switch_version = 'unknown'

                        if switch_version == node_image_version:
                            log.debug('Switch {} upgrade not needed, skipping'.format(node))
                            upgrade_msg = ''
                        else:
                            switches_to_upgrade.append(node)
                            upgrade_msg = ', upgrade needed'

                        log.info('Switch {} version: {}, image version: {}{}'.format(
                            node_device.name, switch_version, node_image_version, upgrade_msg))

            switch_group_nodes = switches_to_upgrade
            if switch_group_nodes:
                log.info('Switches to upgrade: {}'.format(switch_group_nodes))
            else:
                log.info('No switches to upgrade')

            if not self.upgrade_controller and not switch_group_nodes:
                return

    def update_firmware_repository(self, steps, device,
                                   sleep_after_delete=SLEEP_AFTER_DELETE,
                                   controller_image=CONTROLLER_IMAGE,
                                   switch_image=SWITCH_IMAGE,
                                   timeouts=None):

        # Because dict is mutable
        if timeouts is None:
            timeouts = {}

        # Update the default values with the user provided
        timeouts = self.TIMEOUTS.update(timeouts)

        with steps.start("Updating firmware repository") as step:

            with step.start("Clearing firmware repository") as substep:
                result = device.api.execute_clear_firmware_repository(
                    sleep_after_delete=sleep_after_delete)

                if not result:
                    substep.failed("Images still exist in the firmware repository")

            if controller_image and self.upgrade_controller:
                with step.start("Adding controller-image to the firmware repository") as substep:
                    controller_image = controller_image[0]

                    device.execute('firmware repository add {}'.format(controller_image),
                                   timeout=timeouts['firmware_repository_add'],
                                   error_pattern=self.error_patterns)

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
                                   error_pattern=self.error_patterns)

                    images = device.api.get_firmware_repository_images_by_polling(
                        image_type='switch',
                        max_time=timeouts['firmware_repository_add'])

                    if not images:
                        substep.failed("Firmware did not exist in the repository "
                                       "after timeout was reached")

                    switch_image = images[0]

                    substep.passed("Found newly added switch firmware '{}'"
                                   .format(switch_image))

    def install_firmware(self, steps, device, controller_image=CONTROLLER_IMAGE,
                         timeouts=None, switch_image=SWITCH_IMAGE,
                         switch_group_nodes=SWITCH_GROUP_NODES,
                         switch_group_name=SWITCH_GROUP_NAME,
                         clear_switch_group=CLEAR_SWITCH_GROUP):

        # Because dict is mutable
        if timeouts is None:
            timeouts = {}

        # Update the default values with the user provided
        timeouts = self.TIMEOUTS.update(timeouts)

        with steps.start("Installing new firmware") as step:

            if controller_image and self.upgrade_controller:
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


class FabricClean(BaseStage):
    """This stage will clean APIC controllers.

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

    # =================
    # Argument Defaults
    # =================
    CLEANING_TIMEOUT = 90
    RELOAD_TIMEOUT = 800
    SLEEP_AFTER_RELOAD = 60

    # ============
    # Stage Schema
    # ============
    schema = {
        Optional("cleaning_timeout"): int,
        Optional("reload_timeout"): int,
        Optional("sleep_after_reload"): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'fabric_clean',
        'reload'
    ]

    def fabric_clean(self, steps, device, cleaning_timeout=CLEANING_TIMEOUT):

        with steps.start("Cleaning the device") as step:
            result = device.api.execute_clean_controller_fabric(
                max_time=cleaning_timeout)

            if not result:
                step.failed("Failed to clean the device")
            else:
                step.passed("Successfully cleaned the device")

    def reload(self, steps, device, reload_timeout=RELOAD_TIMEOUT,
               sleep_after_reload=SLEEP_AFTER_RELOAD):

        with steps.start("Reloading '{dev}'".format(dev=device.name)) as step:

            reload_dialog = Dialog([
                Statement(
                    pattern=r".*This command will restart this device\, Proceed\? \[y\/N\].*",
                    action='sendline(y)'
                )
            ])

            device.sendline('acidiag reboot')
            reload_dialog.process(device.spawn)

            timeout = Timeout(reload_timeout, 60)
            while timeout.iterate():
                timeout.sleep()
                device.destroy()

                try:
                    device.connect(learn_hostname=True)
                except Exception:
                    log.info("{dev} is not reloaded".format(dev=device.hostname))
                else:
                    log.info("Sleeping for '{}' seconds for '{}' to stabilize."
                             .format(sleep_after_reload, device.name))
                    time.sleep(sleep_after_reload)

                    step.passed("{dev} has successfully reloaded".format(dev=device.hostname))

            step.failed("{dev} failed to reboot".format(dev=device.hostname))


class NodeRegistration(BaseStage):
    """This stage registers nodes on APIC using REST API.

Stage Schema
------------
node_registration:

    nodes (list): Nodes to register on APIC

    rest_alias (str, optional): Connection alias for REST connection.
        Defaults to 'rest'.

    verify_max_time (int, optional): Max time in seconds to verify node registration.
        Defaults to 480.

    verify_interval (int, optional): How often in seconds to attempt verify node
        registration. Defaults to 30.

Example
-------
node_registration:
    nodes: [Spine1, Spine2]
    rest_alias: cli
"""

    # =================
    # Argument Defaults
    # =================
    REST_ALIAS = 'rest'
    VERIFY_MAX_TIME = 480
    VERIFY_INTERVAL = 30

    # ============
    # Stage Schema
    # ============
    schema = {
        "nodes": list,
        Optional("rest_alias"): str,
        Optional("verify_max_time"): int,
        Optional("verify_interval"): int
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'register_nodes',
        'verify_nodes'
    ]

    def register_nodes(self, steps, device, nodes, rest_alias=REST_ALIAS):

        with steps.start("Registering nodes") as step:
            # Register each node
            result = device.api.execute_register_nodes(
                nodes=nodes, rest_alias=rest_alias)

            if not result:
                step.failed("Node registration failed")
            else:
                step.passed("Node registration completed")

    def verify_nodes(self, steps, device, nodes, verify_max_time=VERIFY_MAX_TIME,
                     verify_interval=VERIFY_INTERVAL):

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


class CopyToDevice(BaseStage):
    """This stage will copy an image to a device from a networked location.

Stage Schema
------------
copy_to_device:

    origin:
        files (list): Image files location on the server.

        hostname (str): Hostname or address of the server.

    destination:

        directory (str): Location on the device to copy images.

    protocol (str): Protocol used for copy operation.

    verify_num_images (bool, optional): Verify number of images provided by
        user for clean is correct. Defaults to True.

    expected_num_images (int, optional): Number of images expected to be
        provided by user for clean. Defaults to 1.

    vrf (str, optional): Vrf used to copy. Defaults to an empty string.

    timeout (int, optional): Copy operation timeout in seconds. Defaults to 300.

    compact (bool, optional): Compact copy mode if supported by the device.
        Defaults to False.

    protected_files (list, optional): File patterns that should not be deleted.
        Defaults to None.

    overwrite (bool, optional): Overwrite the file if a file with the same
        name already exists. Defaults to False.

    skip_deletion (bool, optional): Do not delete any files even if there isn't
        any space on device. Defaults to False.

    copy_attempts (int, optional): Number of times to attempt copying image
        files. Defaults to 1 (no retry).

    copy_attempts_sleep (int, optional): Number of seconds to sleep between
        copy_attempts. Defaults to 30.

    check_file_stability (bool, optional): Verifies that the file size is not
        changing. This ensures the image is not actively being copied.
        Defaults to False.

    stability_check_tries (int, optional): Max number of checks that can be
        done when checking file stability. Defaults to 3.

    stability_check_delay (int, optional): Delay between tries when checking
        file stability in seconds. Defaults to 2.

    min_free_space_percent (int, optional) : Percentage of total disk space
        that must be free. If specified the percentage is not free then the
        stage will attempt to delete unprotected files to reach the minimum
        percentage. Defaults to None.

    use_kstack (bool, optional): Use faster version of copy with limited options.
        Defaults to False.

Example
-------
copy_to_device:
    origin:
        hostname: server-1
        files:
            - /home/cisco/asr1k.bin
    destination:
        directory: harddisk:/
    protocol: sftp
    timeout: 300
"""

    # =================
    # Argument Defaults
    # =================
    VERIFY_NUM_IMAGES = True
    EXPECTED_NUM_IMAGES = 1
    VRF = ''
    TIMEOUT = 300
    COMPACT = False
    USE_KSTACK = False
    PROTECTED_FILES = None
    OVERWRITE = False
    SKIP_DELETION = False
    COPY_ATTEMPTS = 1
    COPY_ATTEMPTS_SLEEP = 30
    CHECK_FILE_STABILITY = False
    STABILITY_CHECK_TRIES = 3
    STABILITY_CHECK_DELAY = 2
    MIN_FREE_SPACE_PERCENT = None

    # ============
    # Stage Schema
    # ============
    schema = {
        'origin': {
            Optional('files'): list,
            'hostname': str
        },
        'destination': {
            'directory': str,
            Optional('standby_directory'): str,
        },
        'protocol': str,
        Optional('verify_num_images'): bool,
        Optional('expected_num_images'): int,
        Optional('vrf'): str,
        Optional('timeout'): int,
        Optional('compact'): bool,
        Optional('use_kstack'): bool,
        Optional('protected_files'): list,
        Optional('overwrite'): bool,
        Optional('skip_deletion'): bool,
        Optional('copy_attempts'): int,
        Optional('copy_attempts_sleep'): int,
        Optional('check_file_stability'): bool,
        Optional('stability_check_tries'): int,
        Optional('stability_check_delay'): int,
        Optional('min_free_space_percent'): int,
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'copy_to_device'
    ]

    def copy_to_device(self, steps, device, origin, destination, protocol,
                       verify_num_images=VERIFY_NUM_IMAGES,
                       expected_num_images=EXPECTED_NUM_IMAGES,
                       vrf=VRF,
                       timeout=TIMEOUT,
                       compact=COMPACT,
                       use_kstack=USE_KSTACK,
                       protected_files=PROTECTED_FILES,
                       overwrite=OVERWRITE,
                       skip_deletion=SKIP_DELETION,
                       copy_attempts=COPY_ATTEMPTS,
                       copy_attempts_sleep=COPY_ATTEMPTS_SLEEP,
                       check_file_stability=CHECK_FILE_STABILITY,
                       stability_check_tries=STABILITY_CHECK_TRIES,
                       stability_check_delay=STABILITY_CHECK_DELAY,
                       min_free_space_percent=MIN_FREE_SPACE_PERCENT,
                       **kwargs):
        switch_image = None
        controller_image = None

        # ['aci-apic-dk9.5.1.2e.iso', 'aci-n9000-dk9.15.1.2e.bin']
        with steps.start('Checking image file versions') as step:
            controller_image_version = 'unknown'
            switch_image_version = 'unknown'
            image_files = origin.get('files')
            for fn in image_files:
                if 'apic' in fn:
                    controller_image = fn
                    controller_image_version = apic_get_firmware_version_from_image_name(device, controller_image)
                elif 'n9000' in fn:
                    switch_image = fn
                    switch_image_version = nxos_aci_get_firmware_version_from_image_name(device, switch_image)

            log.info(f'Controller image version: {controller_image_version}')
            log.info(f'Switch image version: {switch_image_version}')

        with steps.start('Checking fabric versions') as step:
            if not device.connected:
                device.connect()
            version_info = device.parse('show version')
            try:
                controller_version = version_info['pod'][1]['node'][1]['version']
            except KeyError:
                log.debug('Could not get info from show version', exc_info=True)
                controller_version = 'unknown'

            if controller_image_version:
                with step.start("Checking controller image version") as substep:
                    if controller_version == controller_image_version:
                        upgrade_msg = ', skipping upgrade'
                        image_files.remove(controller_image)
                    else:
                        upgrade_msg = ', upgrade needed'

                    log.info('Controller {} version: {}, controller image version: {}{}'.format(
                        device.name,
                        controller_version,
                        controller_image_version,
                        upgrade_msg))

            download_switch_image = False
            with step.start("Checking switch image versions") as substep:
                for node_idx in version_info['pod'][1]['node']:
                    if node_idx > 100:
                        node_version = version_info['pod'][1]['node'][node_idx]['version']
                        if node_version != switch_image_version:
                            log.info('Switch {}, version {}, upgrade needed'.format(node_idx, node_version))
                            download_switch_image = True
                            break
                        else:
                            log.info('Switch {}, version {}'.format(node_idx, node_version))

            if download_switch_image is False and switch_image in image_files:
                image_files.remove(switch_image)

        if image_files:
            log.info(f'Images to download: {image_files}')

        log.info("Section steps:\n1- Verify correct number of images provided"
                 "\n2- Get filesize of image files on remote server"
                 "\n3- Check if image files already exist on device"
                 "\n4- (Optional) Verify stability of image files"
                 "\n5- Verify free space on device else delete unprotected files"
                 "\n6- Copy image files to device"
                 "\n7- Verify copied image files are present on device")

        # list of destination directories
        destinations = []

        # Get args
        server = origin['hostname']

        # Establish FileUtils session for all FileUtils operations
        file_utils = FileUtils(testbed=device.testbed)

        string_to_remove = file_utils.get_server_block(server).get('path', '')
        image_files = remove_string_from_image(images=origin['files'],
                                               string=string_to_remove)

        # Set active node destination directory
        destination_act = destination['directory']

        # Set standby node destination directory
        if 'standby_directory' in destination:
            destination_stby = destination['standby_directory']
            destinations = [destination_stby, destination_act]
        else:
            destination_stby = None
            destinations = [destination_act]

        # Check remote server info present in testbed YAML
        if not file_utils.get_server_block(server):
            self.failed(
                "Server '{}' was provided in the clean yaml file but "
                "doesn't exist in the testbed file.\n".format(server))

        # Check image files provided
        if verify_num_images:
            # Verify correct number of images provided
            with steps.start("Verify correct number of images provided") as step:
                if not verify_num_images_provided(
                        image_list=image_files,
                        expected_images=expected_num_images):
                    step.failed(
                        "Incorrect number of images provided. Please "
                        "provide {} expected image(s) under destination"
                        ".path in clean yaml file.\n".format(expected_num_images))
                else:
                    step.passed("Correct number of images provided")

        # Loop over all image files provided by user
        for index, file in enumerate(image_files):
            # Init
            files_to_copy = {}
            unknown_size = False

            # Get filesize of image files on remote server
            with steps.start("Get filesize of '{}' on remote server '{}'".\
                             format(file, server)) as step:
                try:
                    file_size = device.api.get_file_size_from_server(
                        server=file_utils.get_hostname(server),
                        path=file,
                        protocol=protocol,
                        timeout=timeout,
                        fu_session=file_utils)
                except FileNotFoundError:
                    step.failed(
                        "Can not find file {} on server {}. Terminating clean".
                        format(file, server))
                except Exception as e:
                    log.warning(str(e))
                    # Something went wrong, set file_size to -1
                    file_size = -1
                    unknown_size = True
                    err_msg = "\nUnable to get filesize for file '{}' on "\
                              "remote server {}".format(file, server)
                    if overwrite:
                        err_msg += " - will copy file to device"
                    step.passx(err_msg)
                else:
                    step.passed("Verified filesize of file '{}' to be "
                                "{} bytes".format(file, file_size))
            for dest in destinations:

                # Execute 'dir' before copying image files
                dir_before = device.execute('ls -l {}'.format(dest))

                # Check if file with same name and size exists on device
                dest_file_path = os.path.join(dest, os.path.basename(file))
                image_mapping = self.history[
                    'CopyToDevice'].parameters.setdefault('image_mapping', {})
                image_mapping.update({origin['files'][index]: dest_file_path})
                with steps.start("Check if file '{}' exists on device {} {}".\
                                format(dest_file_path, device.name, dest)) as step:
                    # Check if file exists
                    try:
                        exist = device.api.verify_file_exists(
                            file=dest_file_path,
                            size=file_size,
                            dir_output=dir_before)
                    except Exception as e:
                        exist = False
                        log.warning("Unable to check if image '{}' exists on device {} {}."
                                    "Error: {}".format(dest_file_path,
                                                       device.name,
                                                       dest,
                                                       str(e)))

                    if (not exist) or (exist and overwrite):
                        # Update list of files to copy
                        file_copy_info = {
                            file: {
                                'size': file_size,
                                'dest_path': dest_file_path,
                                'exist': exist
                            }
                        }
                        files_to_copy.update(file_copy_info)
                        # Print message to user
                        step.passed("Proceeding with copying image {} to device {}".\
                                    format(dest_file_path, device.name))
                    else:
                        step.passed(
                            "Image '{}' already exists on device {} {}, "
                            "skipping copy".format(file, device.name, dest))

                # Check if any file copy is in progress
                if check_file_stability:
                    for file in files_to_copy:
                        with steps.start("Verify stability of file '{}'".\
                                         format(file)) as step:
                            # Check file stability
                            try:
                                stable = device.api.verify_file_size_stable_on_server(
                                    file=file,
                                    server=file_utils.get_hostname(server),
                                    protocol=protocol,
                                    fu_session=file_utils,
                                    delay=stability_check_delay,
                                    max_tries=stability_check_tries)

                                if not stable:
                                    step.failed(
                                        "The size of file '{}' on server is not "
                                        "stable\n".format(file), )
                                else:
                                    step.passed(
                                        "Size of file '{}' is stable".format(file))
                            except NotImplementedError:
                                # cannot check using tftp
                                step.passx(
                                    "Unable to check file stability over {protocol}"
                                    .format(protocol=protocol))
                            except Exception as e:
                                log.error(str(e))
                                step.failed(
                                    "Error while verifying file stability on "
                                    "server\n")

                # Verify available space on the device is sufficient for image copy, delete
                # unprotected files if needed, copy file to the device
                # unless overwrite: False
                if files_to_copy:
                    with steps.start(
                            "Verify sufficient free space on device '{}' '{}' or delete"
                            " unprotected files".format(device.name,
                                                        dest)) as step:

                        if unknown_size:
                            total_size = -1
                            log.warning("Amount of space required cannot be confirmed, "
                                        "copying the files on the device '{}' '{}' may fail".
                                        format(device.name, dest))

                        if not protected_files:
                            protected_files = [r'^.+$(?<!\.bin)(?<!\.iso)']

                        # Try to free up disk space if skip_deletion is not set to True
                        if not skip_deletion:
                            # TODO: add golden images, config to protected files once we have golden section
                            golden_config = find_clean_variable(
                                self, 'golden_config')
                            golden_image = find_clean_variable(
                                self, 'golden_image')

                            if golden_config:
                                protected_files.extend(golden_config)
                            if golden_image:
                                protected_files.extend(golden_image)

                            # Only calculate size of file being copied
                            total_size = sum(0 if file_data['exist']
                                             else file_data['size'] for
                                             file_data in files_to_copy.values())

                            try:
                                free_space = device.api.free_up_disk_space(
                                    destination=dest,
                                    required_size=total_size,
                                    skip_deletion=skip_deletion,
                                    protected_files=protected_files,
                                    min_free_space_percent=min_free_space_percent)
                                if not free_space:
                                    step.failed("Unable to create enough space for "
                                                "image on device {} {}".
                                                format(device.name, dest))
                                else:
                                    step.passed(
                                        "Device {} {} has sufficient space to "
                                        "copy images".format(device.name, dest))
                            except Exception as e:
                                log.error(str(e))
                                step.failed("Error while creating free space for "
                                            "image on device {} {}".
                                            format(device.name, dest))

                # Copy the file to the devices
                for file, file_data in files_to_copy.items():
                    with steps.start("Copying image file {} to device {} {}".\
                                     format(file, device.name, dest)) as step:

                        # Copy file unless overwrite is False
                        if not overwrite and file_data['exist']:
                            step.skipped(
                                "File with the same name size exists on "
                                "the device {} {}, skipped copying".format(
                                    device.name, dest))

                        for i in range(1, copy_attempts + 1):
                            try:
                                device.api.\
                                    copy_to_device(protocol=protocol,
                                                   server=file_utils.get_hostname(server),
                                                   remote_path=file,
                                                   local_path=file_data['dest_path'],
                                                   vrf=vrf,
                                                   timeout=timeout,
                                                   compact=compact,
                                                   use_kstack=use_kstack,
                                                   **kwargs)
                            except Exception as e:
                                # if user wants to retry
                                if i < copy_attempts:
                                    log.warning(
                                        "Could not copy file '{file}' to '{d}', {e}\n"
                                        "attempt #{iteration}".format(
                                            file=file,
                                            d=device.name,
                                            e=e,
                                            iteration=i + 1))
                                    log.info("Sleeping for {} seconds before retrying"
                                             .format(copy_attempts_sleep))
                                    time.sleep(copy_attempts_sleep)
                                else:
                                    substep.failed("Could not copy '{file}' to '{d}'\n{e}"\
                                                   .format(file=file, d=device.name, e=e))
                            else:
                                log.info(
                                    "File {} has been copied to {} on device {}"
                                    " successfully".format(file, dest,
                                                           device.name))
                                break
                        # Save the file copied path and size info for future use
                        history = self.history['CopyToDevice'].parameters.\
                                            setdefault('files_copied', {})
                        history.update({file: file_data})

                with steps.start("Verify images successfully copied") as step:
                    # If nothing copied don't need to verify, skip
                    if 'files_copied' not in self.history[
                            'CopyToDevice'].parameters:
                        step.skipped(
                            "Image files were not copied for {} {} in previous steps, "
                            "skipping verification steps".format(device.name, dest))

                    # Execute 'dir' after copying image files
                    dir_after = device.execute('dir {}'.format(dest))

                    for name, image_data in self.history['CopyToDevice'].\
                                                    parameters['files_copied'].items():
                        with step.start("Verify image '{}' copied to {} on device {}".\
                                        format(image_data['dest_path'], dest, device.name)) as substep:
                            # if size is -1 it means it failed to get the size
                            if image_data['size'] != -1:
                                if not device.api.verify_file_exists(
                                        file=image_data['dest_path'],
                                        size=image_data['size'],
                                        dir_output=dir_after):
                                    substep.failed("Size of image file copied to device {} is "
                                                   "not the same as remote server filesize".\
                                                   format(device.name))
                                else:
                                    substep.passed("Size of image file copied to device {} is "
                                                   "the same as image filesize on remote server".\
                                                   format(device.name))
                            else:
                                substep.skipped(
                                    "Image file has been copied to device {} correctly"
                                    " but cannot verify file size".format(device.name))

        self.passed("Copy to device completed")


class ApplyConfiguration(BaseStage):
    """This stage executes the REST API against the device.

Stage schema
------------
apply_configuration:

    method (str, optional): the REST API method to call (get/put/post/delete).
        Defaults to 'post'.

    rest_alias (str, optional): the connection alias for the REST
        connection. Defaults to 'rest'.

    rest_via (str, optional): the connection name from the topology.
        Defaults to 'rest'.

    kwargs (dict, optional): the keyword arguments to pass to the REST API call.
        Defaults to None.

Example
-------
apply_configuration:
    method: get
    kwargs:
        dn: api/class/topSystem.json
"""

    # =================
    # Argument Defaults
    # =================
    METHOD = 'post'
    REST_ALIAS = 'rest'
    REST_VIA = 'rest'
    KWARGS = None

    # ============
    # Stage Schema
    # ============
    schema = {
        "method": str,
        Optional("rest_alias"): str,
        Optional("rest_via"): str,
        Optional("kwargs"): dict
    }

    # ==============================
    # Execution order of Stage steps
    # ==============================
    exec_order = [
        'apply_configuration'
    ]

    def apply_configuration(self, steps, device, method=METHOD,
                            rest_alias=REST_ALIAS,
                            rest_via=REST_VIA,
                            kwargs=KWARGS):

        if kwargs is None:
            kwargs = {}

        with steps.start("Executing REST call {} via {}".format(method, rest_via)) as step:
            try:
                device.connect(via=rest_via, alias=rest_alias)
                rest_api = getattr(device, rest_alias)
                getattr(rest_api, method)(**kwargs)
            except Exception as e:
                step.failed('Failed to execute REST API', from_exception=e)

