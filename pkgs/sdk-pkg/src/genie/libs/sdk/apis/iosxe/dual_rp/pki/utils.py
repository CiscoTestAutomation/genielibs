"""HA-aware IOS XE PKI certificate storage APIs."""

from genie.libs.sdk.apis.iosxe.pki import utils as generic
from genie.libs.sdk.apis.iosxe.stack.pki import utils as stack


def get_certificate_storage_locations(device):
    """Return local NVRAM for every connected HA processor."""
    return stack.get_certificate_storage_locations(device)


def get_certificate_references(
        device, patterns=generic.DEFAULT_CERTIFICATE_PATTERNS):
    """Return certificate references from the active HA connection."""
    return stack.get_certificate_references(device, patterns)


def get_certificate_files(
        device, locations=None,
        patterns=generic.DEFAULT_CERTIFICATE_PATTERNS):
    """Return matching certificate files for the selected HA connections."""
    return stack.get_certificate_files(device, locations, patterns)


def delete_certificate_files(device, files):
    """Delete explicitly supplied certificate files on HA connections."""
    return stack.delete_certificate_files(device, files)


def verify_certificate_references(device, references):
    """Verify referenced certificates exist on every HA connection."""
    return stack.verify_certificate_references(device, references)


def get_certificate_storage_usage(device, locations=None):
    """Return local certificate storage usage for each HA connection."""
    return stack.get_certificate_storage_usage(device, locations)


__all__ = [
    "delete_certificate_files",
    "get_certificate_files",
    "get_certificate_references",
    "get_certificate_storage_locations",
    "get_certificate_storage_usage",
    "verify_certificate_references",
]
