June 2020
==========

July 6
--------

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.clean``    |  20.6         |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
N/A

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------
* Fix tftp copy_to_linux and copy_to_device issue

* Common OS:
	* Fix tftp copy_to_linux and copy_to_device issue

* NXOS:
	* Updated n7k, n9k, n9kv image_handler to also handle image list

* IOSXE:
	* Fix change_boot_variable step1 'delete previous boot variables'
        get 'next_reload_boot_variable' instead of 'current_boot_variable'
