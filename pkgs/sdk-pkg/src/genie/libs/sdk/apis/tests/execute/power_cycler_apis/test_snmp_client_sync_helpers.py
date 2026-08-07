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

    def test_snmpv3_set_logs_missing_credentials_for_type_error(self):
        logger = Mock()
        client = snmp_client.SNMPv3Client(
            "127.0.0.1", auth=None, log=logger
        )

        with patch.object(
            snmp_client,
            "set_cmd_sync",
            side_effect=TypeError("cannot convert 'NoneType' object to bytes"),
        ), self.assertRaisesRegex(TypeError, "NoneType.*bytes"):
            client.snmp_set("1.3.6.1.2.1.1.1.0", 1)

        logger.error.assert_called_once()
        log_message = " ".join(
            str(value) for value in logger.error.call_args.args
        )
        self.assertIn("SNMPv3 %s failed", log_message)
        self.assertIn("SET", log_message)
        self.assertIn(
            "username, security_level, auth_protocol, auth_key, "
            "priv_protocol, priv_key",
            log_message,
        )

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

    def test_set_cmd_sync_drains_pending_dispatcher_callbacks_before_close(self):
        errors = []
        expected = ("error_indication", "error_status", "error_index", "var_binds")

        class SnmpEngine:
            closed = False

            def close_dispatcher(self):
                self.closed = True

            def late_callback(self):
                if self.closed:
                    raise RuntimeError("Unregistered transport")

        async def set_cmd(snmp_engine, *args, **kwargs):
            loop = asyncio.get_running_loop()
            loop.set_exception_handler(
                lambda loop, context: errors.append(context)
            )
            loop.call_soon(snmp_engine.late_callback)
            return expected

        snmp_engine = SnmpEngine()
        transport = snmp_client.create_transport(object, "127.0.0.1", timeout=3)

        with patch.object(
            snmp_client, "_resolve_transport", AsyncMock(return_value="transport")
        ), patch.object(snmp_client, "set_cmd", set_cmd, create=True):
            result = snmp_client.set_cmd_sync(
                snmp_engine, "auth", transport, "context", "object_type"
            )

        self.assertEqual(result, expected)
        self.assertEqual(errors, [])
        self.assertTrue(snmp_engine.closed)
