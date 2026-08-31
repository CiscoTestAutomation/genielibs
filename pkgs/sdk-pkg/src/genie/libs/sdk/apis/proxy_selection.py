"""Generic, device-scoped runtime proxy selection."""

import ipaddress
import logging
from collections.abc import Mapping

log = logging.getLogger(__name__)


def proxy_selection_config(device):
    """Return merged runtime selection hints when explicitly enabled.

    Device custom data overrides testbed custom data. Modes other than
    ``runtime`` deliberately preserve the generated/static proxy behavior.
    """
    from genie.libs.sdk.apis import utils as api_utils

    testbed = api_utils._runtime_proxy_get(device, 'testbed')
    testbed_custom = api_utils._runtime_proxy_get(
        testbed, 'custom', {}) or {}
    device_custom = api_utils._runtime_proxy_get(
        device, 'custom', {}) or {}
    testbed_config = api_utils._runtime_proxy_get(
        testbed_custom, 'proxy_selection', {}) or {}
    device_config = api_utils._runtime_proxy_get(
        device_custom, 'proxy_selection', {}) or {}
    if not isinstance(testbed_config, Mapping):
        testbed_config = {}
    if not isinstance(device_config, Mapping):
        device_config = {}
    config = dict(testbed_config)
    config.update(device_config)
    return config if config.get('mode') == 'runtime' else None


def device_management_ips(device):
    """Return ordered, normalized IPv4 and IPv6 management addresses."""
    from genie.libs.sdk.apis import utils as api_utils

    management = api_utils._runtime_proxy_get(
        device, 'management', {}) or {}
    addresses = api_utils._runtime_proxy_get(
        management, 'address', {}) or {}
    result = []
    for family in ('ipv4', 'ipv6'):
        values = api_utils._runtime_proxy_get(addresses, family, []) or []
        if not isinstance(values, (list, tuple)):
            values = [values]
        for value in values:
            try:
                address = str(ipaddress.ip_interface(str(value)).ip)
            except ValueError:
                log.debug(
                    "Ignoring malformed %s management address %r",
                    family, value)
                continue
            if address not in result:
                result.append(address)
    return result


def runtime_proxy_candidates(device, fallback_proxy=None):
    """Return discoverable proxy candidates in deterministic route order."""
    from genie.libs.sdk.apis import utils as api_utils

    config = proxy_selection_config(device)
    if not config:
        return []
    testbed = api_utils._runtime_proxy_get(device, 'testbed')
    servers = api_utils._runtime_proxy_get(testbed, 'servers', {}) or {}
    if not isinstance(servers, Mapping):
        return []
    return api_utils._runtime_proxy_candidate_plan(
        device, fallback_proxy, servers)[0]


def clear_runtime_proxy_cache(device):
    """Clear positive and negative runtime proxy cache entries for a device."""
    device.__dict__.pop('_runtime_proxy_cache', None)


def invalidate_runtime_proxy_cache(device, server_name, reason=None):
    """Invalidate a selected proxy and exclude it from the next selection.

    Args:
        device: Device that owns the runtime cache.
        server_name (str): Selected server whose result was contradicted.
        reason (str, optional): Diagnostic failure reason.

    Returns:
        bool: Whether a cached selection was invalidated.
    """
    from genie.libs.sdk.apis import utils as api_utils

    state = api_utils._runtime_proxy_cache_state(device, create=False)
    if not state:
        return False
    invalidated = False
    for key, result in list(state['selected'].items()):
        if result.get('server_name') != server_name:
            continue
        state['selected'].pop(key, None)
        state['negative'].setdefault(key, {})[server_name] = (
            reason or 'cached proxy invalidated')
        invalidated = True
    return invalidated


def select_runtime_proxy_for_device(
        device, fallback_proxy=None, target_port=None, cache=None,
        server_converter=None, target_prober=None):
    """Connect to and cache the best enabled proxy for a device.

    Args:
        device: Runtime pyATS device whose testbed owns server metadata.
        fallback_proxy (str, optional): Current generated/static proxy.
        target_port (int, optional): Target device SSH port, not the proxy
            server's own SSH service port. Derived from the active device
            connection, then defaults to 22.
        cache (dict, optional): Caller-owned cache state. By default state is
            attached to ``device``.
        server_converter (callable, optional): Injected generic server-to-Linux
            converter. Defaults to the device API implementation.
        target_prober (callable, optional): Injected generic remote TCP probe.
            Defaults to the device API implementation.

    Returns:
        dict or None: A stable result containing ``server_name``,
        ``proxy_device``, ``device_ip``, ``target_port``, ``subnet``,
        ``interface``, ``route_match``, full ``route`` metadata,
        ``connected``, ``target_proven``, ``probe_status``,
        ``target_probes``, ``cache_hit``, ``reason``, and ``failures``.
        Returns ``None`` when runtime mode is disabled or all candidates fail.

    Notes:
        The selector owns connections it creates only long enough to reject a
        candidate; it does not disconnect the selected proxy. Positive and
        negative outcomes are device-scoped. A cached selection is discarded
        if its proxy is disconnected. Call ``invalidate_runtime_proxy_cache``
        when an SDK path contradicts a cached selection, or
        ``clear_runtime_proxy_cache`` to reset all state. When target probe
        tooling is unavailable, route/fallback selection is allowed unless
        ``probe_fallback`` is explicitly false in runtime configuration.
    """
    from genie.libs.sdk.apis import utils as api_utils

    config = proxy_selection_config(device)
    if not config:
        return None

    testbed = api_utils._runtime_proxy_get(device, 'testbed')
    servers = api_utils._runtime_proxy_get(testbed, 'servers', {}) or {}
    if not isinstance(servers, Mapping):
        log.warning("Runtime proxy server metadata is not a mapping")
        return None
    route_candidates, fallbacks = api_utils._runtime_proxy_candidate_plan(
        device, fallback_proxy, servers)
    management_ips = device_management_ips(device)
    if not route_candidates:
        return None

    target_probe = bool(config.get('target_probe', False))
    probe_fallback = bool(config.get('probe_fallback', True))
    try:
        timeout = float(config.get('timeout', 3))
        if timeout <= 0:
            raise ValueError
    except (TypeError, ValueError):
        timeout = 3.0
    target_port = int(
        target_port or api_utils._runtime_proxy_target_port(device))

    key = api_utils._runtime_proxy_selection_key(
        device, management_ips, route_candidates, servers, target_port,
        target_probe, timeout, probe_fallback)
    state = api_utils._runtime_proxy_cache_state(device, cache)
    cached = state['selected'].get(key)
    if cached:
        if api_utils._runtime_proxy_is_connected(cached['proxy_device']):
            result = dict(cached)
            result['cache_hit'] = True
            api_utils._log_runtime_proxy_selection_decision(
                device, result, log)
            return result
        state['selected'].pop(key, None)

    negative = state['negative'].setdefault(key, {})
    failures = [f'{name}: {reason}' for name, reason in negative.items()]
    if route_candidates and all(name in negative for name in route_candidates):
        if failures:
            log.warning("No runtime proxy for %s: %s",
                        api_utils._runtime_proxy_get(
                            device, 'name', '<device>'),
                        '; '.join(failures))
        return None
    route_order, route_matches = api_utils._runtime_proxy_route_order(
        device, management_ips, route_candidates, servers)
    ordered = list(dict.fromkeys(route_order + fallbacks))
    unavailable_fallback = None
    for name in ordered:
        if name in negative:
            continue
        proxy = api_utils._runtime_proxy_device(
            device, name, server_converter)
        if proxy is None:
            reason = 'missing or unusable server metadata'
            negative[name] = reason
            failures.append(f'{name}: {reason}')
            continue
        connected_here = not api_utils._runtime_proxy_is_connected(proxy)
        probes = []
        if target_probe and management_ips:
            try:
                prober = target_prober or device.api.probe_tcp_from_server
                probes = prober(proxy, management_ips, target_port,
                                timeout=timeout)
            except Exception as exc:
                reason = f'connection/probe failed ({exc})'
                negative[name] = reason
                failures.append(f'{name}: {reason}')
                if (connected_here and
                        api_utils._runtime_proxy_is_connected(proxy)):
                    api_utils._runtime_proxy_disconnect(proxy)
                continue
        elif connected_here:
            try:
                proxy.connect()
            except Exception as exc:
                reason = f'connection failed ({exc})'
                negative[name] = reason
                failures.append(f'{name}: {reason}')
                continue

        route_ip, route = route_matches.get(
            name, (management_ips[0] if management_ips else None, None))
        target_proven = False
        probe_status = 'not_requested'
        if target_probe:
            if any(probe.get('reachable') for probe in probes):
                route_ip = next(probe['host'] for probe in probes
                                if probe.get('reachable'))
                target_proven = True
                probe_status = 'reachable'
            elif (probes and all(probe.get('status') == 'unavailable'
                                 for probe in probes) and probe_fallback):
                if unavailable_fallback is None:
                    unavailable_fallback = (name, proxy, route_ip, route,
                                            probes, connected_here)
                elif connected_here:
                    api_utils._runtime_proxy_disconnect(proxy)
                continue
            else:
                reason = ('target probe unavailable' if probes and all(
                    probe.get('status') == 'unavailable' for probe in probes)
                    else 'target not reachable')
                negative[name] = reason
                failures.append(f'{name}: {reason}')
                if connected_here:
                    api_utils._runtime_proxy_disconnect(proxy)
                continue

        result = api_utils._runtime_proxy_selection_result(
            name, proxy, route_ip, target_port, route, target_proven,
            probe_status, probes, failures)
        if unavailable_fallback and unavailable_fallback[5]:
            api_utils._runtime_proxy_disconnect(unavailable_fallback[1])
        state['selected'][key] = dict(result)
        api_utils._log_runtime_proxy_selection_decision(device, result, log)
        return result

    if unavailable_fallback:
        name, proxy, route_ip, route, probes, _ = unavailable_fallback
        result = api_utils._runtime_proxy_selection_result(
            name, proxy, route_ip, target_port, route, False, 'unavailable',
            probes, failures, reason='probe_unavailable')
        state['selected'][key] = dict(result)
        api_utils._log_runtime_proxy_selection_decision(device, result, log)
        return result

    if failures:
        log.warning("No runtime proxy for %s: %s",
                    api_utils._runtime_proxy_get(
                        device, 'name', '<device>'), '; '.join(failures))
    return None
