import asyncio
import unittest
from unittest.mock import AsyncMock, Mock, patch

from genie.libs.sdk.powercycler import snmp_client


class TestSnmpClientSyncHelpers(unittest.TestCase):
    def test_get_cmd_sync_resolves_transport_and_closes_dispatcher(self):
        snmp_engine = Mock()
        transport = snmp_client.create_transport(object, "127.0.0.1", timeout=3)
        resolved_transport = object()
        expected = ("error_indication", "error_status", "error_index", "var_binds")

        with patch.object(
            snmp_client, "_resolve_transport", AsyncMock(return_value=resolved_transport)
        ) as resolve_transport, patch.object(
            snmp_client, "get_cmd", AsyncMock(return_value=expected), create=True
        ) as get_cmd:
            result = snmp_client.get_cmd_sync(
                snmp_engine, "auth", transport, "context", "object_type", lookupMib=False
            )

        self.assertEqual(result, expected)
        resolve_transport.assert_awaited_once_with(transport)
        get_cmd.assert_awaited_once_with(
            snmp_engine,
            "auth",
            resolved_transport,
            "context",
            "object_type",
            lookupMib=False,
        )
        snmp_engine.close_dispatcher.assert_called_once_with()

    def test_set_cmd_sync_resolves_transport_and_closes_dispatcher(self):
        snmp_engine = Mock()
        transport = snmp_client.create_transport(object, "127.0.0.1", timeout=3)
        resolved_transport = object()
        expected = ("error_indication", "error_status", "error_index", "var_binds")

        with patch.object(
            snmp_client, "_resolve_transport", AsyncMock(return_value=resolved_transport)
        ) as resolve_transport, patch.object(
            snmp_client, "set_cmd", AsyncMock(return_value=expected), create=True
        ) as set_cmd:
            result = snmp_client.set_cmd_sync(
                snmp_engine, "auth", transport, "context", "object_type", lookupMib=False
            )

        self.assertEqual(result, expected)
        resolve_transport.assert_awaited_once_with(transport)
        set_cmd.assert_awaited_once_with(
            snmp_engine,
            "auth",
            resolved_transport,
            "context",
            "object_type",
            lookupMib=False,
        )
        snmp_engine.close_dispatcher.assert_called_once_with()

    def test_get_cmd_sync_closes_dispatcher_when_get_cmd_fails(self):
        snmp_engine = Mock()
        transport = snmp_client.create_transport(object, "127.0.0.1", timeout=3)
        resolved_transport = object()

        with patch.object(
            snmp_client, "_resolve_transport", AsyncMock(return_value=resolved_transport)
        ), patch.object(
            snmp_client, "get_cmd", AsyncMock(side_effect=RuntimeError("boom")), create=True
        ):
            with self.assertRaisesRegex(RuntimeError, "boom"):
                snmp_client.get_cmd_sync(
                    snmp_engine, "auth", transport, "context", "object_type"
                )

        snmp_engine.close_dispatcher.assert_called_once_with()

    def test_set_cmd_sync_runs_when_event_loop_is_already_running(self):
        snmp_engine = Mock()
        transport = snmp_client.create_transport(object, "127.0.0.1", timeout=3)
        resolved_transport = object()
        expected = ("error_indication", "error_status", "error_index", "var_binds")

        with patch.object(
            snmp_client, "_resolve_transport", AsyncMock(return_value=resolved_transport)
        ) as resolve_transport, patch.object(
            snmp_client, "set_cmd", AsyncMock(return_value=expected), create=True
        ) as set_cmd:

            async def invoke():
                return snmp_client.set_cmd_sync(
                    snmp_engine,
                    "auth",
                    transport,
                    "context",
                    "object_type",
                    lookupMib=False,
                )

            result = asyncio.run(invoke())

        self.assertEqual(result, expected)
        resolve_transport.assert_awaited_once_with(transport)
        set_cmd.assert_awaited_once_with(
            snmp_engine,
            "auth",
            resolved_transport,
            "context",
            "object_type",
            lookupMib=False,
        )
        snmp_engine.close_dispatcher.assert_called_once_with()
