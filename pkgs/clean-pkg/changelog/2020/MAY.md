May 2020
========

May 26
------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.5         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------

* IOSXR Clean:
    * Added stage: tftp_boot
    * Added stage: load_pies
    * Added stage: change_boot_variable
    * Support for IOSXR ASR9K PX platform

* IOSXE Clean:
    * Redesign stage: tftp_boot


--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

* Common OS Clean:
    * Bugfix for unique_file_name propagation with image passthrough


* IOSXE Clean:
    * Added argument 'recovery_password' for stage: tftp_boot
    * Bugfix for cat9k change_boot_variable
    * Bugfix for disabling powercycle for CSR1000v virtual platform
    * Bugfix for post reload module status check for 'Ready' state

* NXOS Clean:
    * Bugfix for post reload module status check for 'Ready' state
