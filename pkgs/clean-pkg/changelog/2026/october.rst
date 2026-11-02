--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* cheetah/ap
    * Added the ``ConfigureManagement`` clean stage.

* generic clean stages
    * Added optional endpoint diagnostics to ``ping_server``. On its first failed ping, the stage calls the Genie SDK collector to log Cisco and configured Linux VM state before retrying. Diagnostic failures do not change the ping result.

* clean/stages/cheetah/ap and clean/stages/iosxe/cat9k/c9800
    * Added coordinated C9800 WLC/AP registration with readiness tracking, registration verification, failure diagnostics, and parallel AP registration.

* clean/stages/iosxe
    * Added an optional ``shell`` boolean to the CopyToDevice stage schema and forwarded it to the SDK ``copy_to_device`` API to select the IOS XE shell-based FileUtils transfer path. Defaults to False to preserve the existing transfer behavior.


--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Modified SetControllerMode clean stage to publish the verified post-Clean device platform for parent-process testbed reconstruction.
    * Preserved the connection ``via`` selected by the Clean connect stage across controller-mode reconnects.
    * Keep the SD-WAN recovery worker compatible with SDK dispatchers that do not pass the console start command, and preserve the original Clean stage failure when device recovery cannot restore the device. Prevent an already-destroyed Unicon connection from blocking the console-speed recovery retry, and prevent disconnected-device verification errors from masking the original recovery result.
    * Updated InstallImage clean stage to commit activated and uncommitted images only once when ``show install active`` reports multiple locations, such as a dual-RP device.
    * Fixed ROMMON TFTP boot with wrapped Clean image/file metadata. Boot retries now keep the provider-selected TFTP image and recovery options.
    * Reject invalid or ambiguous ROMMON TFTP image metadata before boot.
    * Modified the IOS XE SD-WAN Connect stage to preserve an existing connection and fail when connection recovery is unsuccessful.
    * Added regression tests for the updated connection behavior.
    * Modified SetControllerMode to preserve or accept the connection ``via`` used for internal reconnects when a device has multiple connections.

* image handling
    * Standardized image paths after platform validation without changing supported image roles or multi-file package and SMU collections.
    * Reject terminal control characters and surrounding whitespace in image paths.

* clean/stages
    * When an IOS XE install reports ISSU in progress or an already added package, inspect the ISSU and install state. Clear only a known stale TFTP ISSU leftover (failed or aborted ISSU) without SMUs with the existing API, save the configuration, and retry the install. Wait for the command prompt on recoverable failure footers and preserve the install error if state diagnostics fail.

* clean/stages/iosxe
    * Skip the post-reload ``install commit`` when the install command already includes ``commit``.


--------------------------------------------------------------------------------
                                    Changed                                     
--------------------------------------------------------------------------------

* clean/stages/cheetah/ap and clean/stages/iosxe/cat9k/c9800
    * PrimeAp discovers the target controller and resolves WLC aliases during verification.


