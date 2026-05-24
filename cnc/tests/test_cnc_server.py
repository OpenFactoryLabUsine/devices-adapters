import pytest_asyncio

from cnc.server import EQUIPMENT_HIERARCHY, EQUIPMENT_VARIABLES, CNCServer


@pytest_asyncio.fixture(scope="session")
async def cnc_server():
    s = CNCServer(endpoint="opc.tcp://localhost:4843")
    await s.start()
    yield s
    await s.stop()


class TestCNCServerStructure:
    async def test_all_equipment_nodes_created(self, cnc_server):
        for eq in EQUIPMENT_HIERARCHY:
            assert eq["name"] in cnc_server._nodes, f"Missing node: {eq['name']}"

    async def test_hierarchy_bridge_under_structure(self, cnc_server):
        structure_node = cnc_server._nodes["CNC_Structure"]
        bridge_node = cnc_server._nodes["CNC_Bridge"]
        parent = await bridge_node.get_parent()
        assert parent == structure_node

    async def test_hierarchy_rack_under_bridge(self, cnc_server):
        bridge_node = cnc_server._nodes["CNC_Bridge"]
        rack_node = cnc_server._nodes["CNC_Rack"]
        parent = await rack_node.get_parent()
        assert parent == bridge_node

    async def test_hierarchy_spindle_under_rack(self, cnc_server):
        rack_node = cnc_server._nodes["CNC_Rack"]
        spindle_node = cnc_server._nodes["CNC_Spindle"]
        parent = await spindle_node.get_parent()
        assert parent == rack_node

    async def test_suction_zones_under_structure(self, cnc_server):
        structure_node = cnc_server._nodes["CNC_Structure"]
        for i in range(1, 7):
            zone_node = cnc_server._nodes[f"CNC_Succion_zone{i}"]
            parent = await zone_node.get_parent()
            assert parent == structure_node


class TestCNCServerVariables:
    async def test_all_variables_created(self, cnc_server):
        for equipment_name, variable_name, _ in EQUIPMENT_VARIABLES:
            key = f"{equipment_name}.{variable_name}"
            assert key in cnc_server._variables, f"Missing variable: {key}"

    async def test_initial_values(self, cnc_server):
        assert await cnc_server.get_value("CNC_Structure", "PositionX") == 3.65
        assert await cnc_server.get_value("CNC_Structure", "RotationY") == 270.0
        assert await cnc_server.get_value("CNC_Bridge", "PositionZ") == -1000.0
        assert await cnc_server.get_value("CNC_Spindle", "Speed") == 5.0
        assert await cnc_server.get_value("CNC_Succion_zone1", "Etat") is False

    async def test_set_and_get_value(self, cnc_server):
        await cnc_server.set_value("CNC_Bridge", "PositionZ", 500.0)
        assert await cnc_server.get_value("CNC_Bridge", "PositionZ") == 500.0