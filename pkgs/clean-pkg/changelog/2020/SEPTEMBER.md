September 2020
==========

September 29
--------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.9         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* COM
    * Modified apply_configuration stage
        * to support reading a configuration from a file then applying it on the device

* IOSXR
    * Added install_iamge_and_packages stage

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* COM
    * Modified copy_to_device stage:
        * to support testbed.servers without credentials specified.
    * Modified copy_to_linux stage:
        * to skip verification for scp as scp does not support file listing.