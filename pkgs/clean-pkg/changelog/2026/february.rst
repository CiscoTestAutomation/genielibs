--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean-pkg
    * 3.14 changed fnmatch.translate() to emit \z instead of \Z, so hardcoded regex strings differ and tests fail.
    * iosxe
        * Update the rommon_boot stage to support golden_image to boot the device.
        * cat9k
            * Removed RommonBoot stage as it is same as generic iosxe RommonBoot stage.
    * iosxe/cat9k
        * Fixed rommon_boot pcall race condition for HA/stack devices.

* iosxe/cat9k
    * stackwise_virtual
        * Updated the expected output of the show stackwise-virtual link command to reflect the changes in the link and protocol status values for the ports in the SVL configuration.
        * updated the logic to check the SVL link status on all sub connections

* clean-pkg/stages
    * cat9k/stackwise_virtual
        * Skip power cycle the device if no recovery is provided and reload device instead.
    * iosxe
        * Updated install image logic to skip the "Check for previous uncommitted install operation" step when the show install active returns no output.
    * Increased ping timeout from 30 to 120 seconds to prevent intermittent timeout failures due to delays in pinging gateway.

* iosxe/cat9k/stackwise_virtual
    * Removed wait time after device recovery boot in stackwise virtual configuration stage as it is not needed and is causing unnecessary delay in the clean execution.

* clean/stages/connect
    * Added logic for transitioning from shell state to enable mode in the device during connect stage.

* nxos
    * Updated logic to check for system and kickstart images when verifying boot variable
        * Now considers the current running image when determining if the boot variable is set correctly.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Fix the logic of verify_ignore_startup_configuration api in clean stages.
    * Updated the error pattern to include invalid command detected during execution of install image command.

* clean-pkg
    * Update the rommon_boot stage to re-use the api device_rommon_boot.


