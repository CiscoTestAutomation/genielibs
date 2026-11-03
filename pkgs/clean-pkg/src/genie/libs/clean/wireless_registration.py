"""Coordinate wireless WLC/AP registration through Kleenex KIPC.

This module defines the shared protocol adapter used by the C9800 WLC and AP
Clean workers. The WLC worker publishes readiness, observes AP progress, and
records registration evidence. Each AP worker waits for WLC readiness,
publishes completion of its CAPWAP configuration, and waits for terminal
registration confirmation.

The adapter uses the following KIPC namespace:

    protocol/wireless/wlc/readiness
        WLC readiness state. The WLC worker publishes ``ready`` after it is
        ready to receive AP progress, or ``failed`` when its coordination
        stage cannot continue. This record is terminal and is published with
        ``if_unset`` so readiness cannot be changed after publication.
    protocol/wireless/ap/{ap_id}/status
        Per-AP configuration and registration state. The AP worker publishes
        ``configured`` after completing CAPWAP configuration. The WLC worker
        publishes terminal ``confirmed`` or ``failed`` after checking WLC
        registration evidence. The configured record is protected with
        ``if_unset``; the terminal WLC result prevents later updates.
    protocol/wireless/ap/{ap_id}/diagnostics
        Bounded diagnostic evidence for an unresolved or failed AP. The WLC
        worker owns this record and publishes it as terminal with ``if_unset``
        so the first diagnostic snapshot is retained.
    participant/{coordinator}/lifecycle
        Coordinator lifecycle state used to fail peers promptly. A
        ``completed`` worker finished normally; ``exited`` means the worker
        ended before publishing the expected coordination result and is
        treated as a terminal failure by waiting peers.

AP participants are keyed by ``ap_id``. The radio MAC is learned by the AP
worker and published with its configured state; it is not part of the
dyntopo coordination contract. ``snapshot_group()`` returns all records below
``protocol/wireless/`` for WLC polling, while ``snapshot_ap(ap_id)`` returns
the current status record for one validated AP.
"""

from genie.libs.sdk.apis.iosxe.cat9k.c9800.platform.get import (
    normalize_ap_radio_mac as normalize_radio_mac,
)


WLC_READINESS = "protocol/wireless/wlc/readiness"


class WirelessAPRegistration(object):
    """Adapt generic KIPC state to the WLC/AP registration protocol."""

    def __init__(self, context, expected_aps=None):
        """Create a registration adapter for one KIPC context.

        Args:
            context: Injected KIPC context for the coordination group.
            expected_aps: AP aliases or AP metadata mappings.

        Raises:
            ValueError: If no KIPC context or an invalid AP definition is
                provided.
        """
        if context is None:
            raise ValueError("Wireless registration requires a KIPC context")
        self.kipc = context
        self.expected_aps = self._normalize_expected_aps(expected_aps)

    @staticmethod
    def _normalize_expected_aps(expected_aps):
        """Normalize AP aliases or mappings into participant metadata.

        Args:
            expected_aps (list or dict): AP aliases or AP identity mappings.

        Returns:
            dict: AP metadata keyed by participant identifier.

        Raises:
            ValueError: If the input shape or AP identity is invalid.
        """
        if expected_aps is None:
            return {}
        if isinstance(expected_aps, dict):
            values = expected_aps.items()
        elif isinstance(expected_aps, list):
            values = []
            for item in expected_aps:
                if isinstance(item, str):
                    values.append((item, {"ap_id": item, "ap_name": item}))
                elif isinstance(item, dict):
                    ap_id = item.get("ap_id") or item.get("id")
                    if not ap_id:
                        raise ValueError("Each expected AP needs an ap_id")
                    values.append((ap_id, item))
                else:
                    raise ValueError("Invalid expected AP definition")
        else:
            raise ValueError("expected_aps must be a list or mapping")

        normalized = {}
        for ap_id, value in values:
            if not isinstance(value, dict):
                value = {"ap_name": value}
            entry = dict(value)
            entry["ap_id"] = ap_id
            if entry.get("radio_mac"):
                entry["radio_mac"] = normalize_radio_mac(entry["radio_mac"])
            entry.setdefault("ap_name", ap_id)
            normalized[ap_id] = entry
        return normalized

    @staticmethod
    def _ap_path(ap_id):
        return "protocol/wireless/ap/{}/status".format(ap_id)

    @staticmethod
    def _diagnostics_path(ap_id):
        return "protocol/wireless/ap/{}/diagnostics".format(ap_id)

    def _wlc_lifecycle_path(self):
        return "participant/{}/lifecycle".format(self.kipc.coordinator)

    def _validate_ap(self, ap_id, ap_name=None, radio_mac=None):
        """Validate and optionally learn one AP's radio identity.

        Args:
            ap_id (str): AP participant identifier.
            ap_name (str, optional): AP name reported by the worker.
            radio_mac (str, optional): AP radio MAC learned by the worker.

        Returns:
            str or None: Normalized radio MAC when available.

        Raises:
            ValueError: If the participant is unknown or identity conflicts.
        """
        expected = self.expected_aps.get(ap_id)
        if expected is None:
            raise ValueError("Unknown AP participant: {}".format(ap_id))
        # AP names are consistency evidence only. The radio MAC is learned by
        # the AP worker and becomes the stable registration identity.
        if radio_mac is not None:
            normalized = normalize_radio_mac(radio_mac)
            if expected.get("radio_mac") and expected["radio_mac"] != normalized:
                raise ValueError("AP radio MAC does not match expected identity")
            expected["radio_mac"] = normalized
            return normalized
        return expected.get("radio_mac")

    def signal_wlc_ready(self, evidence=None):
        """Publish terminal WLC readiness for the coordination group.

        Args:
            evidence (dict, optional): Readiness evidence.

        Returns:
            bool: Whether the readiness record was published.
        """
        return self.kipc.publish(
            WLC_READINESS,
            {"status": "ready", "evidence": evidence},
            terminal=True,
            if_unset=True,
        )

    def signal_wlc_failed(self, reason, evidence=None):
        """Publish terminal WLC failure for the coordination group.

        Args:
            reason (str): Failure reason.
            evidence (dict, optional): Failure evidence.

        Returns:
            bool: Whether the failure record was published.
        """
        return self.kipc.publish(
            WLC_READINESS,
            {"status": "failed", "reason": reason, "evidence": evidence},
            terminal=True,
            if_unset=True,
        )

    def wait_for_wlc_ready(self, timeout):
        """Wait for WLC readiness or coordinator termination.

        Args:
            timeout (float): Maximum wait in seconds.

        Returns:
            dict: Readiness, failure, cancellation, or timeout payload.
        """
        def terminal(value):
            value = value or {}
            if value.get("status") in {"ready", "failed"}:
                return True
            # Treat coordinator exit as terminal failure so peers do not wait
            # for the full readiness timeout after the WLC worker dies.
            lifecycle = self.kipc.read(self._wlc_lifecycle_path()) or {}
            return lifecycle.get("status") == "exited"

        result = self.kipc.wait_for(
            WLC_READINESS,
            terminal,
            timeout,
        )
        if result["status"] != "matched":
            return result
        lifecycle = self.kipc.read(self._wlc_lifecycle_path()) or {}
        if lifecycle.get("status") == "exited":
            return {
                "status": "failed",
                "reason": "WLC worker exited before readiness",
                "evidence": lifecycle,
            }
        return result["value"]

    def signal_ap_configured(self, ap_id, ap_name, radio_mac):
        """Publish AP CAPWAP configuration completion.

        Args:
            ap_id (str): AP participant identifier.
            ap_name (str): AP name reported by the AP worker.
            radio_mac (str): Radio MAC learned from the AP device.

        Returns:
            bool: Whether the configured state was published.
        """
        # Configuration and registration are separate states: configured lets
        # the WLC begin evidence collection before final confirmation.
        normalized = self._validate_ap(ap_id, ap_name, radio_mac)
        return self.kipc.publish(
            self._ap_path(ap_id),
            {
                "status": "configured",
                "ap_name": ap_name,
                "radio_mac": normalized,
            },
            if_unset=True,
        )

    def wait_for_ap_configured(self, ap_id, timeout):
        """Wait for one AP to report configuration or failure.

        Args:
            ap_id (str): AP participant identifier.
            timeout (float): Maximum wait in seconds.

        Returns:
            dict: AP configured, failed, cancelled, or timeout payload.
        """
        self._validate_ap(ap_id)
        result = self.kipc.wait_for(
            self._ap_path(ap_id),
            lambda value: (value or {}).get("status") in {"configured", "failed"},
            timeout,
        )
        if result["status"] != "matched":
            return result
        return result["value"]

    def signal_registration_confirmed(self, ap_id, evidence):
        """Publish terminal AP registration confirmation.

        Args:
            ap_id (str): AP participant identifier.
            evidence (dict): Independent WLC registration evidence.

        Returns:
            bool: Whether confirmation was published.
        """
        self._validate_ap(
            ap_id,
            None,
            evidence.get("radio_mac"),
        )
        return self.kipc.publish(
            self._ap_path(ap_id),
            dict(evidence, status="confirmed"),
            terminal=True,
        )

    def signal_registration_failed(self, ap_id, reason, evidence=None):
        """Publish terminal AP registration failure.

        Args:
            ap_id (str): AP participant identifier.
            reason (str): Failure reason.
            evidence (dict, optional): Failure evidence.

        Returns:
            bool: Whether failure was published.
        """
        self._validate_ap(ap_id)
        return self.kipc.publish(
            self._ap_path(ap_id),
            {"status": "failed", "reason": reason, "evidence": evidence},
            terminal=True,
        )

    def signal_registration_diagnostics(self, ap_id, evidence):
        """Publish bounded terminal diagnostics for one AP.

        Args:
            ap_id (str): AP participant identifier.
            evidence (dict): Diagnostic payload.

        Returns:
            bool: Whether diagnostics were published.
        """
        self._validate_ap(ap_id)
        return self.kipc.publish(
            self._diagnostics_path(ap_id),
            evidence,
            terminal=True,
            if_unset=True,
        )

    def wait_for_registration(self, ap_id, timeout):
        """Wait for terminal AP registration or WLC termination.

        Args:
            ap_id (str): AP participant identifier.
            timeout (float): Maximum wait in seconds.

        Returns:
            dict: Confirmation, failure, cancellation, or timeout payload.
        """
        self._validate_ap(ap_id)

        def terminal(value):
            value = value or {}
            if value.get("status") in {"confirmed", "failed"}:
                return True
            lifecycle = self.kipc.read(self._wlc_lifecycle_path()) or {}
            return lifecycle.get("status") == "exited"

        result = self.kipc.wait_for(self._ap_path(ap_id), terminal, timeout)
        if result["status"] != "matched":
            return result
        lifecycle = self.kipc.read(self._wlc_lifecycle_path()) or {}
        if lifecycle.get("status") == "exited":
            return {
                "status": "failed",
                "reason": "WLC worker exited before confirmation",
                "evidence": lifecycle,
            }
        return result["value"]

    def is_registration_confirmed(self, ap_id):
        """Return whether an AP has terminal confirmation.

        Args:
            ap_id (str): AP participant identifier.

        Returns:
            bool: True when confirmation is present.
        """
        value = self.kipc.read(self._ap_path(ap_id)) or {}
        return value.get("status") == "confirmed"

    def is_registration_failed(self, ap_id):
        """Return whether an AP has terminal failure.

        Args:
            ap_id (str): AP participant identifier.

        Returns:
            bool: True when failure is present.
        """
        value = self.kipc.read(self._ap_path(ap_id)) or {}
        return value.get("status") == "failed"

    def snapshot_group(self):
        """Return all wireless protocol records.

        Returns:
            dict: Wireless KIPC payloads keyed by opaque path.
        """
        return self.kipc.snapshot("protocol/wireless/")

    def snapshot_ap(self, ap_id):
        """Return one AP's current registration payload.

        Args:
            ap_id (str): AP participant identifier.

        Returns:
            dict: AP status payload.
        """
        self._validate_ap(ap_id)
        return self.kipc.read(self._ap_path(ap_id), {})
