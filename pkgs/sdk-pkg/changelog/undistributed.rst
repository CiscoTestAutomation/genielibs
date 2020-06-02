* Please follow the template we introduced in NOVEMBER.md file.
* Every Trigger/verification need to be added under the corresponding feature.

| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |               |

--------------------------------------------------------------------------------
                                New
--------------------------------------------------------------------------------
* Processors:
    * Enhanced pre_execute_command and post_execute_command processors. Now both have an option to save show command outputs as file.

* Common API:
    * Added slugify to convert special characters such as backslash, dot and etc to underscore
    * Added verify_pcap_has_imcp_destination_unreachable and verify_pcap_has_imcpv6_destination_unreachable for verifying pcap files
    * Added repeat_command_save_output to Execute the command on the device and store the output to file

--------------------------------------------------------------------------------
                                Fix
--------------------------------------------------------------------------------

* Blitz:
    * Fixed the polling issue in blitz
    * Fixed run_genie_sdk action
