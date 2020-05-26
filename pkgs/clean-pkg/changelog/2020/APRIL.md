April 2020
==========

April 28
--------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.4         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* Common OS Clean
    * Added infrastructure for Genie Clean
    * Added stage: connect
    * Added stage: ping_server
    * Added stage: copy_to_linux
    * Added stage: copy_to_device
    * Added stage: write_erase
    * Added stage: reload
    * Added stage: apply_configuration
    * Added stage: verify_running_image
    * Added stage: delete_backup_from_device
    * Added stage: backup_file_on_device
    * Added stage: delete_files_from_server
    * Support for handling image passthrough between stages

* NXOS Clean
    * Added stage: change_boot_variable
    * Added stage: tftp_boot
    * Support for NXOS N7K platform
    * Support for NXOS N9K hardware platform
    * Support for NXOS N9K titanium platform
    * Added unittests for NXOS platform

* IOSXE
    * Added stage: change_boot_variable
    * Added stage: tftp_boot
    * Support for IOSXE ASR1K
    * Support for IOSXE CSR1000v
    * Support for IOSXE Cat9K
    * Added unittests for IOSXE platform

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

N/A
