from unittest.mock import patch

from cnc.adapter import CNCAdapter


class TestCNCAdapter:
    def test_read_data_returns_all_keys(self):
        adapter = CNCAdapter()
        data = adapter.read_data()

        expected_keys = [
            "CNC_Structure.PositionX", "CNC_Structure.PositionY",
            "CNC_Structure.PositionZ", "CNC_Structure.RotationY",
            "CNC_Bridge.PositionZ",
            "CNC_Rack.PositionX",
            "CNC_Spindle.PositionY", "CNC_Spindle.Speed",
            "CNC_Succion_zone1.Etat", "CNC_Succion_zone2.Etat",
            "CNC_Succion_zone3.Etat", "CNC_Succion_zone4.Etat",
            "CNC_Succion_zone5.Etat", "CNC_Succion_zone6.Etat",
            "CNC_Succion_zone1.PositionX", "CNC_Succion_zone1.PositionY",
            "CNC_Succion_zone1.DimensionX", "CNC_Succion_zone1.DimensionY",
        ]
        for key in expected_keys:
            assert key in data, f"Missing key: {key}"

    def test_fixed_values_unchanged(self):
        adapter = CNCAdapter()
        data = adapter.read_data()
        assert data["CNC_Structure.PositionX"] == 3.65
        assert data["CNC_Structure.PositionY"] == 0.8
        assert data["CNC_Structure.PositionZ"] == 5.12
        assert data["CNC_Structure.RotationY"] == 270.0
        assert data["CNC_Succion_zone1.PositionX"] == 0.0
        assert data["CNC_Succion_zone2.PositionX"] == 762.0
        assert data["CNC_Succion_zone1.DimensionX"] == 762.0

    def test_speed_is_non_negative(self):
        adapter = CNCAdapter()
        for _ in range(10):
            data = adapter.read_data()
            assert data["CNC_Spindle.Speed"] >= 0.0

    def test_exactly_one_suction_zone_active_per_range(self):
        adapter = CNCAdapter()

        with patch("cnc.adapter.time.time", return_value=adapter._start_time):
            # At t=0, sin(0) = 0, so rack_x = 0 → zone3 active
            data = adapter.read_data()
            assert data["CNC_Succion_zone3.Etat"] is True
            assert data["CNC_Succion_zone1.Etat"] is False

        with patch("cnc.adapter.time.time", return_value=adapter._start_time + 100):
            # sin(100 * 0.07) ≈ sin(7) ≈ 0.657 → rack_x ≈ 328 → zone5 active
            data = adapter.read_data()
            assert data["CNC_Succion_zone5.Etat"] is True

    def test_etat_values_are_bool(self):
        adapter = CNCAdapter()
        data = adapter.read_data()
        for i in range(1, 7):
            assert isinstance(data[f"CNC_Succion_zone{i}.Etat"], bool)