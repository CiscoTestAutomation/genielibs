--------------------------------------------------------------------------------
                                      Fix                                       
--------------------------------------------------------------------------------

* stages
    * Update configure management to check for status of management interface to be up and fail the stage if it is not.

* clean-pkg/stages
    * iosxe
        * Updated the reset configuration to process the config in chunks
    * iosxe
        * Added a separate section to handle the unconfigure ignore startup config
        * Added logic to check status of previous install commit and perform commit if wasn't committed
    * cat9k
        * Added a separate section to handle the unconfigure ignore startup config

* clean/stages
    * Updated DeleteFilesFromServer to automatically access the hostname if not provided explicitly in either DeleteFilesFromServer or CopyToLinux stages.

* stages/iosxe
    * connect
        * Updated logout step to handle login prompts.
    * connect
        * Updated logout step to handle ssh connection issues after logout.

* clean-pkg
    * Refactor plugin loading from pkg_resources.iter_entry_points to importlib.metadata.entry_points

* iosxe
    * Fixed issue in `copy_to_device` where `origin['files']` would raise an error if there were no files.
    * InstallImage stage
        * Added new dialog to handle different platform reload patterns

* os/iosxe
    * Modified reset configuration
        * add platform console virtual to platform console virtual in Replace dictionaryå


--------------------------------------------------------------------------------
                                      New                                       
--------------------------------------------------------------------------------

* stages/clean/iosxe
    * Modified the Rommon Boot stage.

* os/iosxe
    * Modified connect
        * Added logout logic.
    * Modified InstallRemoveInactive
        * Updated loop_continue to True.


