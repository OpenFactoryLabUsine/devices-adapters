import math
import time


class CNCAdapter:
    def __init__(self):
        self._start_time = time.time()
        self._state = {
            "CNC_Structure.PositionX": 3.65,
            "CNC_Structure.PositionY": 0.80,
            "CNC_Structure.PositionZ": 5.12,
            "CNC_Structure.RotationY": 270.00,

            "CNC_Bridge.PositionZ": -1000.0,

            "CNC_Rack.PositionX": -500.0,

            "CNC_Spindle.PositionY": -280.0,
            "CNC_Spindle.Speed": 5.0,

            "CNC_Succion_zone1.Etat": False,
            "CNC_Succion_zone2.Etat": False,
            "CNC_Succion_zone3.Etat": False,
            "CNC_Succion_zone4.Etat": False,
            "CNC_Succion_zone5.Etat": False,
            "CNC_Succion_zone6.Etat": False,

            "CNC_Succion_zone1.PositionX": 0.0,
            "CNC_Succion_zone1.PositionY": 0.0,
            "CNC_Succion_zone2.PositionX": 762.0,
            "CNC_Succion_zone2.PositionY": 0.0,
            "CNC_Succion_zone3.PositionX": 1219.2,
            "CNC_Succion_zone3.PositionY": 0.0,
            "CNC_Succion_zone4.PositionX": 0.0,
            "CNC_Succion_zone4.PositionY": 1524.0,
            "CNC_Succion_zone5.PositionX": 1219.2,
            "CNC_Succion_zone5.PositionY": 1524.0,
            "CNC_Succion_zone6.PositionX": 0.0,
            "CNC_Succion_zone6.PositionY": 2438.4,

            "CNC_Succion_zone1.DimensionX": 762.0,
            "CNC_Succion_zone1.DimensionY": 1524.0,
            "CNC_Succion_zone2.DimensionX": 457.2,
            "CNC_Succion_zone2.DimensionY": 1524.0,
            "CNC_Succion_zone3.DimensionX": 304.8,
            "CNC_Succion_zone3.DimensionY": 1524.0,
            "CNC_Succion_zone4.DimensionX": 1219.2,
            "CNC_Succion_zone4.DimensionY": 914.4,
            "CNC_Succion_zone5.DimensionX": 304.8,
            "CNC_Succion_zone5.DimensionY": 914.4,
            "CNC_Succion_zone6.DimensionX": 1524.0,
            "CNC_Succion_zone6.DimensionY": 609.6,
        }

    def read_data(self) -> dict:
        t = time.time() - self._start_time

        self._state["CNC_Bridge.PositionZ"] = math.sin(t * 0.1) * 1000.0

        self._state["CNC_Rack.PositionX"] = math.sin(t * 0.07) * 500.0

        self._state["CNC_Spindle.PositionY"] = math.sin(t * 0.2) * 140.0 - 140.0

        self._state["CNC_Spindle.Speed"] = max(0.0, math.sin(t * 0.15) * 10.0 + 10.0)

        rack_x = self._state["CNC_Rack.PositionX"]
        self._state["CNC_Succion_zone1.Etat"] = rack_x < -300
        self._state["CNC_Succion_zone2.Etat"] = -300 <= rack_x < -100
        self._state["CNC_Succion_zone3.Etat"] = -100 <= rack_x < 100
        self._state["CNC_Succion_zone4.Etat"] = 100 <= rack_x < 300
        self._state["CNC_Succion_zone5.Etat"] = rack_x >= 300
        self._state["CNC_Succion_zone6.Etat"] = abs(rack_x) < 200

        return self._state.copy()