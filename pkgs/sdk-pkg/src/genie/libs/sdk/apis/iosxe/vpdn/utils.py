"""Utility functions for VPDN."""


def _resolve_local_names(
    request_dialin,
    accept_dialin,
    local_name=None,
    request_local_name=None,
    accept_local_name=None,
):
    """Resolve local name placement without breaking older callers."""

    resolved_request_local_name = request_local_name
    resolved_accept_local_name = accept_local_name

    if local_name is None:
        return resolved_request_local_name, resolved_accept_local_name

    if request_dialin and (not accept_dialin) and (request_local_name is None):
        resolved_request_local_name = local_name
    elif accept_local_name is None:
        resolved_accept_local_name = local_name

    return resolved_request_local_name, resolved_accept_local_name
