"""IOS XE PKI certificate storage APIs used by clean stages."""

import fnmatch
import logging
import re

from unicon.core.errors import SubCommandFailure

log = logging.getLogger(__name__)

DEFAULT_CERTIFICATE_PATTERNS = ("IOS-Self-Sig#*.cer",)
CERTIFICATE_DIRECTORY_TIMEOUT = 300
_FILE_REFERENCE_RE = re.compile(
    r"(?P<location>[A-Za-z0-9_-]+:)(?P<filename>[^\s/]+)"
)
_USAGE_RE = re.compile(r"(?P<total>[\d,]+)\s+bytes\s+total\s+\((?P<free>[\d,]+)\s+bytes\s+free\)", re.IGNORECASE)
_DELETE_ERROR_RE = re.compile(
    r"^%Error deleting .+? \((?P<reason>.+)\)$", re.IGNORECASE | re.MULTILINE)


def _normalise_locations(locations):
    """Return filesystem locations in IOS XE ``location:`` format."""
    if locations is None:
        return ["nvram:"]
    if isinstance(locations, str):
        locations = [locations]
    if isinstance(locations, dict):
        values = []
        for entries in locations.values():
            values.extend(entries if isinstance(entries, list) else [entries])
        locations = values
    return [location if location.endswith(":") else "{}:".format(location)
            for location in locations]


def _matching_files(output, patterns):
    """Return filenames from IOS XE directory output matching patterns."""
    files = []
    for line in output.splitlines():
        fields = line.split()
        if len(fields) < 4 or not fields[0].isdigit() or not fields[1].startswith(("-", "d")):
            continue
        filename = fields[-1]
        if any(fnmatch.fnmatchcase(filename, pattern) for pattern in patterns):
            files.append(filename)
    return files


def _file_references(output, patterns):
    """Return certificate paths in configuration output matching patterns."""
    references = []
    for match in _FILE_REFERENCE_RE.finditer(output):
        filename = match.group("filename")
        if any(fnmatch.fnmatchcase(filename, pattern) for pattern in patterns):
            references.append("{}{}".format(match.group("location"), filename))
    return references


def _reference_include_expression(patterns):
    """Build the IOS pipe expression from the non-wildcard pattern prefix."""
    prefixes = [re.split(r"[*?[]", pattern, maxsplit=1)[0] for pattern in patterns]
    return "|".join(prefix for prefix in prefixes if prefix)


def get_certificate_storage_locations(device):
    """Return certificate storage locations for a standalone IOS XE device."""
    return {"active": ["nvram:"]}


def get_certificate_references(device, patterns=DEFAULT_CERTIFICATE_PATTERNS):
    """Return matching certificate files referenced by running and startup config."""
    patterns = tuple(patterns or DEFAULT_CERTIFICATE_PATTERNS)
    references = {}
    include_expression = _reference_include_expression(patterns)
    for name, command in (("running_config", "show running-config"),
                          ("startup_config", "show startup-config")):
        try:
            if include_expression:
                command = "{} | include {}".format(command, include_expression)
            output = device.execute(command)
        except Exception as error:
            raise SubCommandFailure("Failed to retrieve {} certificate references: {}".format(name, error))
        references[name] = _file_references(output, patterns)
    return references


def get_certificate_files(device, locations=None, patterns=DEFAULT_CERTIFICATE_PATTERNS):
    """Return matching certificate files by filesystem location."""
    patterns = tuple(patterns or DEFAULT_CERTIFICATE_PATTERNS)
    include_expression = _reference_include_expression(patterns)
    files = {}
    for location in _normalise_locations(locations):
        command = "dir {}".format(location)
        if include_expression:
            command = "{} | include {}|bytes".format(
                command, include_expression)
        try:
            output = device.execute(
                command,
                timeout=CERTIFICATE_DIRECTORY_TIMEOUT,
            )
        except Exception as error:
            raise SubCommandFailure("Failed to list certificate storage {}: {}".format(location, error))
        files[location] = ["{}{}".format(location, filename) for filename in _matching_files(output, patterns)]
    return files


def delete_certificate_files(device, files):
    """Delete the explicitly supplied certificate files and return deletions by location."""
    deleted = {}
    for location, paths in files.items():
        deleted[location] = []
        for path in paths:
            if not path.startswith(location):
                path = "{}{}".format(location, path)
            try:
                output = device.execute("delete /force {}".format(path))
            except Exception as error:
                raise SubCommandFailure("Failed to delete certificate file {}: {}".format(path, error))
            error_match = _DELETE_ERROR_RE.search(
                output if isinstance(output, str) else "")
            if error_match:
                reason = error_match.group("reason")
                if "no such file or directory" in reason.lower():
                    log.info("Certificate file %s is already absent", path)
                    continue
                raise SubCommandFailure(
                    "Failed to delete certificate file {}: {}".format(
                        path, reason))
            deleted[location].append(path)
    return deleted


def verify_certificate_references(device, references):
    """Return whether every explicitly referenced certificate file still exists."""
    expected = set()
    for paths in references.values():
        expected.update(paths)
    if not expected:
        return True
    found = set()
    locations = {}
    for path in expected:
        location, filename = path.split(":", 1)
        locations.setdefault("{}:".format(location), []).append(filename)
    for location, filenames in locations.items():
        inventory = get_certificate_files(device, [location], filenames)
        found.update(inventory[location])
    missing = expected - found
    if missing:
        log.error("Referenced certificate files are missing: %s", sorted(missing))
        return False
    return True


def get_certificate_storage_usage(device, locations=None):
    """Return total, free, and used bytes for certificate storage locations."""
    usage = {}
    for location in _normalise_locations(locations):
        try:
            output = device.execute("dir {} | include bytes".format(location))
        except Exception as error:
            raise SubCommandFailure("Failed to get certificate storage usage for {}: {}".format(location, error))
        match = _USAGE_RE.search(output)
        if not match:
            raise SubCommandFailure("Could not determine total and free bytes for {}".format(location))
        total = int(match.group("total").replace(",", ""))
        free = int(match.group("free").replace(",", ""))
        usage[location] = {"total": total, "free": free, "used": total - free}
    return usage
