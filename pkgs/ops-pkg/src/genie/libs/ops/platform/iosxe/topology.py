"""Normalized IOS XE physical-topology evidence for Platform Ops."""

from copy import deepcopy
import re


_MODULAR_MEMBER_PID_PREFIXES = ("C94", "C96")
_FIXED_MEMBER_PID_PREFIXES = ("C95",)
_MEMBER_CARD_PATTERN = re.compile(
    r"^Switch\s+(?P<member>\d+)\s+Slot\s+(?P<slot>\d+)\s+"
    r"(?P<card_type>Linecard|Supervisor|Router)$",
    re.IGNORECASE,
)
_MEMBER_DESCENDANT_PATTERN = re.compile(
    r"^(?P<parent>Switch\s+(?P<member>\d+)\s+Slot\s+"
    r"(?P<slot>\d+)\s+Linecard)\s+(?P<suffix>.+)$",
    re.IGNORECASE,
)
_MISSING = object()


def _overlay_set(overlay, location, target, key, value):
    previous = deepcopy(target[key]) if key in target else _MISSING
    target[key] = value
    overlay["changes"].append((location, key, previous, deepcopy(value)))


def _overlay_target(platform, location):
    if location[0] == "members":
        members = getattr(platform, "members", None)
        if not isinstance(members, dict):
            return None
        return members if len(location) == 1 else members.get(location[1])
    slots = getattr(platform, "slot", None)
    if not isinstance(slots, dict):
        return None
    if len(location) == 1:
        return slots
    category = slots.get(location[1])
    if not isinstance(category, dict):
        return None
    if len(location) == 2:
        return category
    card = category.get(location[2])
    if not isinstance(card, dict):
        return None
    if location[0] == "subslot":
        subslots = card.get("subslot")
        return subslots if isinstance(subslots, dict) else None
    return card


def _clear_inventory_overlay(platform):
    overlay = getattr(platform, "_inventory_topology_overlay", None)
    if not overlay:
        return
    for location, key, previous, value in reversed(overlay["changes"]):
        target = _overlay_target(platform, location)
        if not isinstance(target, dict) or target.get(key, _MISSING) != value:
            continue
        if previous is _MISSING:
            target.pop(key)
        else:
            target[key] = previous
    for location in reversed(overlay["created"]):
        target = _overlay_target(platform, location[:-1])
        if isinstance(target, dict) and target.get(location[-1]) == {}:
            target.pop(location[-1])
    for attribute in ("slot", "members"):
        if overlay.get("created_" + attribute) and not getattr(platform, attribute, None):
            delattr(platform, attribute)
    del platform._inventory_topology_overlay


def _safe_parse(device, command):
    try:
        parsed = device.parse(command)
    except Exception:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _inventory_members(member_inventory):
    members = {}
    for member_id, member_data in (member_inventory or {}).items():
        inventory = member_data.get("inventory", {})
        chassis = next((
            item for name, item in inventory.items()
            if re.fullmatch(
                r"Switch\s+{}(?:\s+Chassis)?".format(
                    re.escape(str(member_id))
                ),
                name,
                re.IGNORECASE,
            )
        ), None)
        if chassis:
            members[str(member_id)] = {
                "serial": chassis.get("sn"),
                "pid": chassis.get("pid"),
                "hw_revision": chassis.get("vid"),
            }
    return members


def _inventory_member_slots(member_inventory):
    """Build member-qualified slot data from revision-1 inventory records."""
    slots = {"lc": {}, "rp": {}}
    linecards = {}
    descendants = []

    for member_data in (member_inventory or {}).values():
        for name, item in member_data.get("inventory", {}).items():
            if not isinstance(item, dict):
                continue
            card_match = _MEMBER_CARD_PATTERN.fullmatch(str(name))
            if card_match:
                category = (
                    "lc"
                    if card_match.group("card_type").lower() == "linecard"
                    else "rp"
                )
                full_slot = "{}/{}".format(
                    card_match.group("member"), card_match.group("slot")
                )
                normalized = {
                    "name": item.get("name") or name,
                    "pid": item.get("pid"),
                    "sn": item.get("sn"),
                    "hw_revision": item.get("vid"),
                    "full_slot": full_slot,
                    "subslot": {},
                }
                slots[category][full_slot] = normalized
                if category == "lc":
                    linecards[str(name).lower()] = normalized
                continue

            descendant_match = _MEMBER_DESCENDANT_PATTERN.fullmatch(str(name))
            if descendant_match:
                descendants.append((descendant_match, item, name))

    for match, item, name in descendants:
        parent = linecards.get(match.group("parent").lower())
        if parent is None:
            continue
        suffix = match.group("suffix").strip()
        mpa = re.fullmatch(r"(?P<mpa>\d+)", suffix)
        optic = re.fullmatch(
            r"(?P<mpa>\d+)(?:/|\s+Transceiver\s+)(?P<port>\d+)",
            suffix,
            re.IGNORECASE,
        )
        if mpa:
            subslot = mpa.group("mpa")
        elif optic:
            subslot = "{} transceiver {}".format(
                optic.group("mpa"), optic.group("port")
            )
        else:
            continue
        parent["subslot"][subslot] = {
            "name": item.get("name") or name,
            "pid": item.get("pid"),
            "sn": item.get("sn"),
            "hw_revision": item.get("vid"),
        }

    return slots


def _publish_member_slots(platform, member_inventory, overlay):
    member_slots = _inventory_member_slots(member_inventory)
    if not any(member_slots.values()):
        return
    slots = getattr(platform, "slot", None)
    if not isinstance(slots, dict):
        slots = {}
        platform.slot = slots
        overlay["created_slot"] = True

    for category, cards in member_slots.items():
        if not cards:
            continue
        if category not in slots:
            slots[category] = {}
            overlay["created"].append(("slot", category))
        platform_cards = slots[category]
        for full_slot, card in cards.items():
            existing = platform_cards.get(full_slot)
            if existing is None:
                existing = {}
                platform_cards[full_slot] = existing
                overlay["created"].append(("slot", category, full_slot))
                for field in ("name", "pid", "sn", "hw_revision", "full_slot"):
                    _overlay_set(
                        overlay, ("slot", category, full_slot),
                        existing, field, card[field],
                    )
            else:
                for field in ("pid", "sn"):
                    if (
                        existing.get(field)
                        and card.get(field)
                        and existing[field] != card[field]
                    ):
                        raise ValueError(
                            "Conflicting IOS XE member inventory {} for slot {}: "
                            "{} != {}".format(
                                field, full_slot, existing[field], card[field]
                            )
                        )
                for field in ("name", "pid", "sn", "hw_revision", "full_slot"):
                    if not existing.get(field) and card.get(field) is not None:
                        _overlay_set(
                            overlay, ("slot", category, full_slot),
                            existing, field, card[field],
                        )
            if not isinstance(existing.get("subslot"), dict):
                _overlay_set(
                    overlay, ("slot", category, full_slot),
                    existing, "subslot", {},
                )
            for subslot, value in card["subslot"].items():
                if subslot not in existing["subslot"]:
                    _overlay_set(
                        overlay, ("subslot", category, full_slot),
                        existing["subslot"], subslot, value,
                    )


def populate_topology(platform, member_inventory=None):
    """Publish normalized topology facts and member-qualified slot trees."""
    _clear_inventory_overlay(platform)
    overlay = {
        "changes": [], "created": [],
        "created_members": False, "created_slot": False,
    }
    platform._inventory_topology_overlay = overlay
    platform.member_inventory = (
        member_inventory if isinstance(member_inventory, dict) else {}
    )

    inventory_members = _inventory_members(member_inventory)
    if inventory_members:
        members = getattr(platform, "members", None)
        if not isinstance(members, dict):
            members = {}
            platform.members = members
            overlay["created_members"] = True
        for member_id, inventory_member in inventory_members.items():
            if member_id not in members:
                members[member_id] = {}
                overlay["created"].append(("members", member_id))
            member = members[member_id]
            for field, value in inventory_member.items():
                if value is not None and not member.get(field):
                    _overlay_set(
                        overlay, ("members", member_id), member, field, value,
                    )

    inventory = member_inventory or {}
    member_linecards = any(
        re.search(r"\bSlot\s+\d+\s+Linecard$", name, re.IGNORECASE)
        for member in inventory.values()
        for name in member.get("inventory", {})
    )
    learned_linecards = bool(
        (getattr(platform, "slot", {}) or {}).get("lc", {})
    )
    member_pids = {
        str(member.get("pid") or "").strip().upper()
        for member in (getattr(platform, "members", {}) or {}).values()
        if isinstance(member, dict) and member.get("pid")
    }
    platform_pid = str(
        getattr(platform, "chassis", None)
        or getattr(platform, "rtr_type", None)
        or ""
    ).strip().upper()
    all_modular_member_pids = bool(member_pids) and all(
        pid.startswith(_MODULAR_MEMBER_PID_PREFIXES)
        for pid in member_pids
    )
    all_fixed_member_pids = (
        bool(member_pids)
        and all(
            pid.startswith(_FIXED_MEMBER_PID_PREFIXES)
            for pid in member_pids
        )
    ) or (
        not member_pids
        and platform_pid.startswith(_FIXED_MEMBER_PID_PREFIXES)
    )
    if member_linecards or all_modular_member_pids:
        platform.is_modular = True
    elif all_fixed_member_pids:
        platform.is_modular = False
    elif learned_linecards:
        platform.is_modular = True
    else:
        platform.is_modular = None
    platform.modularity_confident = platform.is_modular is not None
    if platform.is_modular is True:
        _publish_member_slots(platform, member_inventory, overlay)

    platform.chassis_type = None
    platform.chassis_type_confident = False
    platform.chassis_member_count = None
    platform.topology_incomplete_reason = None

    stackwise = _safe_parse(platform.device, "show stackwise-virtual")
    switch_data = _safe_parse(platform.device, "show switch")
    stack = switch_data.get("switch", {}).get("stack", {})
    if not isinstance(stack, dict):
        stack = {}
    if stack:
        not_ready = {
            str(member_id): str(member.get("state") or "").strip()
            for member_id, member in stack.items()
            if str(member.get("state") or "").strip().lower() != "ready"
        }
        if not_ready:
            platform.topology_incomplete_reason = (
                "configured stack members are not ready: "
                + ", ".join(
                    "member {}={}".format(member_id, state)
                    for member_id, state in sorted(not_ready.items())
                )
            )
            return

    if stackwise.get("enabled") is True:
        if not stack:
            platform.topology_incomplete_reason = (
                "StackWise Virtual is enabled but no member state was learned"
            )
            return
        platform.chassis_type = "stackwise_virtual"
        platform.chassis_type_confident = True
        platform.chassis_member_count = len(stack) if len(stack) > 1 else 2
        return

    if stack:
        if len(stack) > 1:
            platform.chassis_type = "stack"
            platform.chassis_type_confident = True
            platform.chassis_member_count = len(stack)
            return

    redundancy = _safe_parse(platform.device, "show redundancy states")
    mode = str(redundancy.get("mode") or "").strip().lower()
    peer_state = str(redundancy.get("peer_state") or "").strip().lower()
    communications = str(redundancy.get("communications") or "").strip().lower()
    valid_peer = peer_state and not any(
        marker in peer_state
        for marker in ("disabled", "unknown", "not present")
    )
    if mode == "duplex" and (valid_peer or communications == "up"):
        platform.chassis_type = "dual_rp"
        platform.chassis_type_confident = True
        platform.chassis_member_count = 2
    elif mode in {"simple", "simplex"}:
        platform.chassis_type_confident = True
        platform.chassis_member_count = 1
