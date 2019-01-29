| Module                  | Version       |
| ------------------------|:-------------:|
| ``genie.libs.sdk``      |   v3.1.9      |

--------------------------------------------------------------------------------
                               Features
--------------------------------------------------------------------------------
* Libs
    * Generic
        * Update the class UpdateLearntDatabase to not execute commands when
          there are no previous verifications/pts
        * Create libs.utils.triggeractions.verify_ops_or_logic to support check
          Or logic for triggers mapping requirements in verify_ops

--------------------------------------------------------------------------------
                               TRIGGERS
--------------------------------------------------------------------------------
* NXOS
    * Update TriggerReloadActiveRp to have one active|ok|standby LC