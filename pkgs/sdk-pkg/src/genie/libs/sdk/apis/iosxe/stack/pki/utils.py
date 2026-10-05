"""Stack-aware IOS XE PKI certificate storage APIs."""

import logging

from genie.libs.sdk.apis.iosxe.pki import utils as generic


log = logging.getLogger(__name__)


def _connection_items(device):
    """Return stable labels and connections for the connected stack members."""
    connections = getattr(device, "subconnections", None) or []
    if not connections:
        log.warning(
            "No stack subconnections are available on %s; certificate cleanup "
            "will be limited to the current connection",
            getattr(device, "name", device),
        )
        return [("active", device)]

    items = []
    labels = set()
    for index, connection in enumerate(connections, 1):
        role = getattr(connection, "role", None)
        alias = getattr(connection, "alias", None)
        label = role if role in ("active", "standby") else alias
        if not isinstance(label, str) or not label or label in labels:
            label = alias if isinstance(alias, str) and alias not in labels else None
        if not label:
            label = "member_{}".format(index)
        labels.add(label)
        items.append((label, connection))
    return items


def _primary_connection(device):
    items = _connection_items(device)
    for label, connection in items:
        if label == "active":
            return connection
    return items[0][1]


def _locations_for_endpoint(locations, endpoint):
    if locations is None:
        return ["nvram:"]
    if isinstance(locations, dict):
        return locations.get(endpoint, [])
    return locations


def _flatten_values(mapping):
    return [value for values in mapping.values() for value in values]


def _files_by_location(paths):
    files = {}
    for path in paths:
        if ":" not in path:
            raise ValueError(
                "Certificate path must include a location: {}".format(path))
        location = "{}:".format(path.split(":", 1)[0])
        files.setdefault(location, []).append(path)
    return files


def get_certificate_storage_locations(device):
    """Return local NVRAM for every connected stack member or HA processor.

    Each subconnection addresses its member's local ``nvram:`` directly. This
    avoids IOS XE ``stby-nvram:`` filesystem operations, which can fail to
    return a prompt on supported Cat9k stack topologies.
    """
    return {label: ["nvram:"] for label, _ in _connection_items(device)}


def get_certificate_references(device,
                               patterns=generic.DEFAULT_CERTIFICATE_PATTERNS):
    """Return certificate references from the active stack connection."""
    return generic.get_certificate_references(_primary_connection(device),
                                              patterns)


def get_certificate_files(device, locations=None,
                          patterns=generic.DEFAULT_CERTIFICATE_PATTERNS):
    """Return matching certificate files for every selected connection."""
    files = {}
    for label, connection in _connection_items(device):
        endpoint_locations = _locations_for_endpoint(locations, label)
        if not endpoint_locations:
            continue
        inventory = generic.get_certificate_files(
            connection, endpoint_locations, patterns)
        files[label] = _flatten_values(inventory)
    return files


def delete_certificate_files(device, files):
    """Delete explicitly supplied certificate files on their connections."""
    connections = dict(_connection_items(device))
    if not set(files).issubset(connections):
        return generic.delete_certificate_files(device, files)

    deleted = {}
    for label, paths in files.items():
        requested = set(paths)
        present = set()
        for location in _files_by_location(paths):
            inventory = generic.get_certificate_files(
                connections[label], [location], patterns=("*",))
            present.update(inventory[location])
        paths = [path for path in paths if path in present]
        already_absent = requested - present
        if already_absent:
            log.info(
                "Skipping certificate files already absent on %s: %s",
                label, sorted(already_absent))
        result = generic.delete_certificate_files(
            connections[label], _files_by_location(paths))
        deleted[label] = _flatten_values(result)
    return deleted


def verify_certificate_references(device, references):
    """Verify referenced certificates exist on every connected member."""
    return all(
        generic.verify_certificate_references(connection, references)
        for _, connection in _connection_items(device)
    )


def get_certificate_storage_usage(device, locations=None):
    """Return local certificate storage usage for each connection."""
    usage = {}
    for label, connection in _connection_items(device):
        endpoint_locations = _locations_for_endpoint(locations, label)
        if not endpoint_locations:
            continue
        location_usage = generic.get_certificate_storage_usage(
            connection, endpoint_locations)
        if len(location_usage) == 1:
            usage[label] = next(iter(location_usage.values()))
        else:
            usage[label] = location_usage
    return usage
