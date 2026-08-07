--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* clean/stages
    * Modified ConfigureManagement stage
        * Added PING_ATTEMPTS = 3

* clean
    * Modified Connect recovery result handling
        * Report the Connect stage as PASSX when device recovery succeeds and pyATS Clean continues.
    * Modified recovery_processor
        * Preserve the triggering clean stage result when device recovery reports its own result.
        * Keep recovery results visible without rolling them up into the clean stage result.
        * Record clean termination as an explicit clean-flow result when non-Connect recovery succeeds.
    * Modified recovery_processor
        * Report successful device recovery as PASSED instead of FAILED when clean is terminated.
    * Modified DeleteFiles clean stage
        * Increased default delete timeout from 500 to 3600 seconds.
        * Added timeout to stage schema.

* ioxe/stages
    * Added a new pattern to detect device reload

* iosxe
    * InstallImage
        * Continued reload handling when install add activate commit reports SUCCESS before the execute service times out during auto-reload.
        * Made install log collection best-effort when image installation fails so diagnostic collection errors do not mask the original install failure.
    * Modified break boot recovery
        * Update Unicon current_state when the break-boot dialog matches a state prompt such as rommon.
    * Updated InstallImage clean stage
        * Detect C9350 quick reload messages that include "reload fru action requested", "Reload Command", or "Reload Firmware Command".
        * Added unittest coverage for C9350 quick reload dialog matching.
    * Modified the InstallImage stage to use create_empty_file API
    * Updated InstallImage clean stage
        * Continue reload handling when the install dialog detects a success marker even if execute returns empty output.
        * Fail the install step when execute returns empty output without a success marker.
    * Updated InstallImage clean stage
        * Updated required space conversion from KB to bytes before calling free_up_disk_space
    * Modified Reload clean stage
        * Preserved reload service arguments when retrying reload with manual boot command.
    * Modified Reload clean stage
        * Honor grub_boot_image during the manual boot fallback so GRUB based platforms (e.g. cat9kv) boot the requested menu entry instead of sending an invalid 'boot <image>' command at the bootloader prompt
    * Modified the SD-WAN Connect clean stage
        * Accepted ``logout: false`` while preserving the connection for later clean stages.
        * Rejected ``logout: true`` because SD-WAN clean requires the connection to remain active.


