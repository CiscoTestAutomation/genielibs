--------------------------------------------------------------------------------
                                      Fix
--------------------------------------------------------------------------------

* clean
    * Modified the ``ConfigureManagement`` gateway verification to fail before pinging when no IPv4 or IPv6 management address is available.
    * Modified recovery_processor
        * Merge a failed device recovery result into the owning clean stage so the stage cannot remain passed while its recovery processor failed.
        * Preserve an existing stage result when it is worse than the recovery result.
    * Boot only IOS XE stack subconnections already in ROMMON with the configured golden or TFTP recovery image, then reconnect before clear-line or power-cycle recovery.
    * Improved recovery handling for HA devices with mixed enable and disable subconnections by avoiding unnecessary disconnects and reconnects.
    * Updated device recovery to clear the mapped terminal-server console lines instead of issuing ``clear line 0`` through the device management connection.
    * Improved recovery handling for stale or closed connections by avoiding commands on invalid sessions and preserving the original connection failure.

* recovery_image
    * Fixed remote recovery-image size checks to use the server protocol's FileUtils implementation instead of the device filesystem implementation.
    * Kept canonical recovery-image paths in clean data and resolves short-path aliases internally only when copying over the production HTTP(S) transport.
    * Added a disk-space check before recovery-image copies. When size verification is enabled, the stage deletes unprotected files as needed while preserving configured golden files and recovery-image targets that are not being replaced.

* clean/stages
    * Avoid a false ROMMON timeout when IOS XE reloads automatically after installing an image. The configured ``packages.conf`` boot variable is still used for the reload.
    * Increased the default IOS XE install_remove_inactive timeout from 180 to 300 seconds to allow package removal to complete on slower devices.
    * Boot the IOS XE installed image from the generated ``packages.conf`` during the install image reload.
    * Modified ``copy_to_device`` to automatically protect an existing target image when the copy operation is skipped, preventing later free-space cleanup from deleting an image required by subsequent clean stages.

* iosxe
    * Kept the controller-mode reload dialog active after the ``Press RETURN to get started!`` prompt so that authentication and the default-admin password change can complete before the final IOS XE prompt.
    * Added regression coverage for the controller-mode authentication flow and reload timeout propagation.
    * Restored the post-reconnect autoboot step in the ROMMON boot flow.

* iosxe/cat9k/c9800
    * Organized C9800 clean stages under the C9800 abstraction.
    * Retained the AP association stage and removed the unused AP mode, RRM DCA channel, installation mode, AP transmit power, HA state, AP fabric, access tunnel, and wireless process stages. Equivalent reusable APIs are available from the C9800 SDK package.

* iosxe/cat9k/c9800/c9800_cl
    * Organized C9800-CL clean stages under the C9800-CL submodel abstraction.
    * Updated the self-signed certificate stage to prefer the Clean YAML password, fall back to the device certificate credential password, and skip when neither is configured.


--------------------------------------------------------------------------------
                                      New
--------------------------------------------------------------------------------

* iosxe/cat9k/c9800
    * Added the ``configure_wireless_management`` Clean stage to configure WMI from explicit stage arguments or ``device.management.wireless`` and verify the trunk VLAN, SVI state and address, and wireless management binding.
    * Added unit coverage for testbed fallback, complete missing-value reporting, readiness verification, and C9800-CL stage abstraction.
    * Updated the stage to require only mode-dependent values and to verify configured IPv6 WMI addresses.
    * Updated the stage to verify every requested static IPv4 WMI address, including secondary addresses.
    * Updated wireless binding verification to use the ``show wireless interface summary`` Genie parser without polling.

* iosxe
    * Added the ``EraseCertificates`` clean stage.
        * Erases certificate files matching configurable filename patterns.
        * Preserves certificates referenced by running-config or startup-config by default and fails safely when a reference is already missing.
        * Reports deleted files and certificate storage usage before and after cleanup.

* clean
    * Added ``testbed_config`` to Genie Clean stage parameters so stages can emit serializable devices and topology for the parent pyATS Clean engine to merge into the effective testbed.


