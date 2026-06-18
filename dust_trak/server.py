import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from dust_trak.adapter import DustTrak
from opcua_base.opcua_server import OPCUAServer


class DustTrakServer(OPCUAServer):
    def __init__(self, endpoint=None, use_virtual_device=True):
        self.config = []
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(self.current_dir, "config.json")
        with open(file_path, encoding="utf-8") as file:
            self.config = json.load(file)
        
        if endpoint is None:
            endpoint = f"opc.tcp://{self.config.get('opcua_server_ip', '0.0.0.0')}:{self.config.get('opcua_server_port', '4841')}"
        super().__init__(endpoint=endpoint, namespace="lab-usine")

        

        self.use_virtual_device = use_virtual_device

    async def start(self):
        await super().start()
        await self.create_equipment_node("DustTrak")

        await self.add_variable("DustTrak", "pm1_concentration", 0.0)
        await self.add_variable("DustTrak", "pm2_5_concentration", 0.0)
        await self.add_variable("DustTrak", "pm4_concentration", 0.0)
        await self.add_variable("DustTrak", "pm10_concentration", 0.0)

        if not self.use_virtual_device:
            self.adapter = DustTrak(config=self.config, virtual=False)
            self.adapter.start_capture()
        else:
            self.adapter = DustTrak(config=self.config, virtual=True)

    async def run(self):
        await self.start()
        try:
            while True:
                data = self.adapter.read_data()
                for key, value in data.items():
                    await self.set_value("DustTrak", key, value)
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            if not self.use_virtual_device:
                self.adapter.stop_capture()

if __name__ == "__main__":
    use_virtual = os.getenv("VIRTUAL_DEVICE", "true").lower() == "true"
    asyncio.run(DustTrakServer(use_virtual_device=use_virtual).run())