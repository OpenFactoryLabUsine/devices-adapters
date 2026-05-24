import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from cnc.adapter import CNCAdapter
from opcua_base.opcua_server import OPCUAServer

EQUIPMENT_HIERARCHY = [
    {"name": "CNC_Structure",     "parent": None},
    {"name": "CNC_Bridge",        "parent": "CNC_Structure"},
    {"name": "CNC_Rack",          "parent": "CNC_Bridge"},
    {"name": "CNC_Spindle",       "parent": "CNC_Rack"},
    {"name": "CNC_Succion_zone1", "parent": "CNC_Structure"},
    {"name": "CNC_Succion_zone2", "parent": "CNC_Structure"},
    {"name": "CNC_Succion_zone3", "parent": "CNC_Structure"},
    {"name": "CNC_Succion_zone4", "parent": "CNC_Structure"},
    {"name": "CNC_Succion_zone5", "parent": "CNC_Structure"},
    {"name": "CNC_Succion_zone6", "parent": "CNC_Structure"},
]

# (equipment_name, variable_id, initial_value)
EQUIPMENT_VARIABLES: list[tuple[str, str, float | bool]] = [
    ("CNC_Structure",     "PositionX", 3.65),
    ("CNC_Structure",     "PositionY", 0.8),
    ("CNC_Structure",     "PositionZ", 5.12),
    ("CNC_Structure",     "RotationY", 270.0),

    ("CNC_Bridge",        "PositionZ", -1000.0),

    ("CNC_Rack",          "PositionX", -500.0),

    ("CNC_Spindle",       "PositionY", -280.0),
    ("CNC_Spindle",       "Speed",     5.0),

    ("CNC_Succion_zone1", "Etat",      False),
    ("CNC_Succion_zone2", "Etat",      False),
    ("CNC_Succion_zone3", "Etat",      False),
    ("CNC_Succion_zone4", "Etat",      False),
    ("CNC_Succion_zone5", "Etat",      False),
    ("CNC_Succion_zone6", "Etat",      False),

    ("CNC_Succion_zone1", "PositionX", 0.0),
    ("CNC_Succion_zone1", "PositionY", 0.0),
    ("CNC_Succion_zone2", "PositionX", 762.0),
    ("CNC_Succion_zone2", "PositionY", 0.0),
    ("CNC_Succion_zone3", "PositionX", 1219.2),
    ("CNC_Succion_zone3", "PositionY", 0.0),
    ("CNC_Succion_zone4", "PositionX", 0.0),
    ("CNC_Succion_zone4", "PositionY", 1524.0),
    ("CNC_Succion_zone5", "PositionX", 1219.2),
    ("CNC_Succion_zone5", "PositionY", 1524.0),
    ("CNC_Succion_zone6", "PositionX", 0.0),
    ("CNC_Succion_zone6", "PositionY", 2438.4),

    ("CNC_Succion_zone1", "DimensionX", 762.0),
    ("CNC_Succion_zone1", "DimensionY", 1524.0),
    ("CNC_Succion_zone2", "DimensionX", 457.2),
    ("CNC_Succion_zone2", "DimensionY", 1524.0),
    ("CNC_Succion_zone3", "DimensionX", 304.8),
    ("CNC_Succion_zone3", "DimensionY", 1524.0),
    ("CNC_Succion_zone4", "DimensionX", 1219.2),
    ("CNC_Succion_zone4", "DimensionY", 914.4),
    ("CNC_Succion_zone5", "DimensionX", 304.8),
    ("CNC_Succion_zone5", "DimensionY", 914.4),
    ("CNC_Succion_zone6", "DimensionX", 1524.0),
    ("CNC_Succion_zone6", "DimensionY", 609.6),
]


class CNCServer(OPCUAServer):
    def __init__(self, endpoint="opc.tcp://0.0.0.0:4842"):
        super().__init__(endpoint=endpoint, namespace="lab-usine")
        self.adapter = CNCAdapter()

    async def start(self):
        await super().start()
        for eq in EQUIPMENT_HIERARCHY:
            await self.create_equipment_node(eq["name"], parent=eq["parent"])
        for equipment_name, variable_name, initial_value in EQUIPMENT_VARIABLES:
            await self.add_variable(equipment_name, variable_name, initial_value)

    async def run(self):
        await self.start()
        try:
            while True:
                data = self.adapter.read_data()
                for equipment_name, variable_name, _ in EQUIPMENT_VARIABLES:
                    key = f"{equipment_name}.{variable_name}"
                    if key in data:
                        await self.set_value(equipment_name, variable_name, data[key])
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(CNCServer().run())