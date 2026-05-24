import pytest
import pytest_asyncio

from opcua_base.opcua_server import OPCUAServer


@pytest_asyncio.fixture(scope="session")
async def server():
    s = OPCUAServer(endpoint="opc.tcp://localhost:14850")
    await s.start()
    yield s
    await s.stop()


class TestCreateEquipmentNode:
    async def test_creates_root_node(self, server):
        await server.create_equipment_node("TestDevice")
        assert "TestDevice" in server._nodes

    async def test_creates_child_node(self, server):
        await server.create_equipment_node("TestParent")
        await server.create_equipment_node("TestChild", parent="TestParent")
        assert "TestChild" in server._nodes

    async def test_unknown_parent_raises(self, server):
        with pytest.raises(ValueError):
            await server.create_equipment_node("Orphan", parent="NonExistent")


class TestAddAndGetVariable:
    async def test_add_and_read_variable(self, server):
        await server.create_equipment_node("VarDevice")
        await server.add_variable("VarDevice", "temperature", 0.0, writable=True)
        await server.set_value("VarDevice", "temperature", 42.0)
        assert await server.get_value("VarDevice", "temperature") == 42.0

    async def test_add_bool_variable(self, server):
        await server.create_equipment_node("BoolDevice")
        await server.add_variable("BoolDevice", "active", False, writable=True)
        await server.set_value("BoolDevice", "active", True)
        assert await server.get_value("BoolDevice", "active") is True

    async def test_unknown_equipment_raises_on_add(self, server):
        with pytest.raises(ValueError):
            await server.add_variable("NonExistent", "temperature", 0.0)

    async def test_unknown_variable_raises_on_set(self, server):
        await server.create_equipment_node("SetDevice")
        with pytest.raises(ValueError):
            await server.set_value("SetDevice", "nonexistent", 1.0)

    async def test_unknown_variable_raises_on_get(self, server):
        await server.create_equipment_node("GetDevice")
        with pytest.raises(ValueError):
            await server.get_value("GetDevice", "nonexistent")