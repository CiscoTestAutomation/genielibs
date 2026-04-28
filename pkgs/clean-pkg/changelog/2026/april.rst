--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages
    * Updated ApplyConfiguration stage to pass timeout to show running-config and show startup-config commands to prevent timeout
    * Update Connect stage to use parameters.internal for correct result_rollup handling
    * Updated ConfigureInterfaces to disable switchport before configuring ipv4/ipv6 address on interfaces that default to L2 mode

* clean-pkg
    * InstallImage stage
        * Added validation check for empty output after install command execution
        * If the install command returns no output, log an error and fail the step.
    * stages/CopyToDevice
        * Use the actual destination path from the history, if the file was renamed during copying, we are checking for the correct file on the device.

* stages/iosxe
    * Update Connect stage to use parameters.internal and disable result_rollup on all steps when recovery is enabled

* iosxe
    * InstallImage stage
        * Fixed unnecessary two-time 'dir' command parsing.
        * Moved 'packages.conf' creation to use `touch_file` API.
        * Removed duplicate ignore-startup-config verification from `verify_boot_variable`.
    * ConfigureManagement stage
        * Added detailed log messages for interface status verification failures.
    * CopyToDevice stage
        * Merged 'get filesize' local & remote steps into one.

* iosxe/ie3k
    * InstallImage stage
        * Removed duplicate `install_image` function logic already present in IOS-XE.
        * Added `configure_no_boot_manual` to order.
    * RommonBoot stage
        * Complete revamp with correct logic.

* clean/stages/copy_to_device
    * Modified the copy_to_device stage to verify sufficient free space on device even if image files already exist on the device.


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* clean/apply_configuration
    * Added skip_if_no_config option to skip apply configuration if no configuration is provided.

* stages/configure_management
    * Added check for master key security configuration and configure master key if missing.

* linux
    * Added image handler to linux.
    * Added api to execute configuration lines on linux devices, as linux does not have a configure method.

* stages/configure_interfaces
    * Added api to apply configuration lines to device.

* iosxe/ie3k
    * Added WriteErase stage.

* iosxe/ie9k
    * Added RommonBoot stage.
    * Added InstallImage stage.
    * Added WriteErase stage.


