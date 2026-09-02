--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* iosxe
    * Updated InstallImage clean stage
        * Added ``verify_install_space`` step to ensure free space of ``install_space_factor`` (default 1.25) times the image size before running ``install add``.
    * Modified clean template
        * Increased the default ``install_remove_inactive`` timeout from 180 to 300 seconds.
    * Updated InstallRemoveInactive clean stage
        * Fail the step when install remove inactive times out instead of reporting it as passed.
    * Updated InstallImage clean stage
        * Recognize IE3K insufficient-space and install-add failure output.
        * Avoid collecting install logs before recoverable space and ISSU retries so device configuration remains unchanged for the retry.
        * Fail the step when space retries are exhausted instead of falling through silently.
    * Updated InstallImage clean stage
        * Call ``device.api.collect_install_log(reconnect=True)`` so the connection/state-machine resynchronization required after an install timeout is handled by the API instead of the clean stage.
        * Preserve the original install error when diagnostic recovery or log collection also fails.
    * Modified SetControllerMode clean stage
        * Fixed SetControllerMode so IOS XE devices that stop at ``grub>`` during ``controller-mode disable`` recover and continue booting instead of timing out.

* iosxe ie3k, cat9k, cat3k
    * Updated InstallImage clean stage
        * Added ``verify_install_space`` to ``exec_order``.

* clean
    * Preserve failed and errored Connect stage results when device recovery is enabled, so an unsuccessful recovery cannot hide the triggering failure.
    * Modified recovery_processor
        * Added separate reachability and recovery steps to device recovery processor reporting.

* generic clean stages
    * Use the ApplyConfiguration max_time value as the command timeout when copying running-config to startup-config, preserving the separate configuration timeout.

* linux
    * Modified run_configure to handle True or False return values
    * Modified simulate_ap_container to handle True or False return values


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* iosxe
    * Added the generic ``RecoveryImage`` clean stage.
        * Resolves recovery images from paths supplied by clean configuration.
        * Supports fast, optional file-size verification with the boolean ``verify_size`` option and exact MD5 verification with ``verify_md5``.
        * Supports protocol-aware server ports and clear copy-operation output.
        * Accepts optional pre-resolved transfer paths while retaining the original filesystem paths for size or MD5 verification.
        * Skips safely when a shared clean template invokes the stage for a device without recovery-image inputs or a golden-image target.
        * Discovers protocol-matching file-transfer servers and ports, supports multiple images and verify-only operation, copies images to golden-image targets, verifies target presence and optional size or MD5, and updates device recovery data.
        * Supports recovery from devices that boot through ROMMON.

* clean
    * Retry a complete Clean workflow for a device when configured device recovery restores the device after a stage failure.
    * Keep the failed or errored attempt visible as superseded, record recovery as a separate passed processor result, and let the retry attempt determine the final Clean result.


