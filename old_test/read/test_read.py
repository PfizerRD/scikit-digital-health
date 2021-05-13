import pytest
from numpy import allclose, array

from ..base_conftest import *

from skimu.read import ReadCWA, ReadBin, ReadGT3X
from skimu.read.get_window_start_stop import get_window_start_stop


@pytest.mark.parametrize(
    "days_type",
    (
        "24hr",
        "full first, full last",
        "full first, partial last",
        "partial first, full last",
        "partial first, partial last",
    ),
)
def test_get_window_start_stop(days_type, windowing_data):
    w_input, w_output = windowing_data(days_type)

    starts, stops = get_window_start_stop(*w_input)

    assert allclose(starts, w_output[0])
    assert allclose(stops, w_output[1])


class TestReadAx3CWA(BaseProcessTester):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        # override specific necessary attributes
        cls.sample_data_file = resolve_data_path("ax3_data.h5", "read")
        cls.truth_data_file = resolve_data_path("ax3_data.h5", "read")
        cls.truth_data_keys = ["time", "accel"]
        cls.process = ReadCWA(bases=None, periods=None)

        cls.atol_time = 5e-5

    def test_none_file(self):
        with pytest.raises(ValueError):
            self.process.predict(file=None)

    def test_window(self):
        r = ReadCWA(bases=8, periods=12)

        assert r.window
        assert r.bases == array([8])
        assert r.periods == array([12])

    def test_window_warning(self):
        with pytest.warns(UserWarning):
            ReadCWA(bases=None, periods=12)
        with pytest.warns(UserWarning):
            ReadCWA(bases=8, periods=None)

    @pytest.mark.parametrize(
        ("base", "period"), ((-1, 12), (0, 25), (8, 30), (24, 12), (8, -12))
    )
    def test_window_bounds_error(self, base, period):
        with pytest.raises(ValueError):
            ReadCWA(bases=base, periods=period)

    def test_extension_warning_not_exist(self):
        with pytest.warns(UserWarning):
            with pytest.raises(FileNotFoundError):
                ReadCWA().predict("test.bin")


class TestReadAx6CWA(BaseProcessTester):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        # override specific necessary attributes
        cls.sample_data_file = resolve_data_path("ax6_data.h5", "read")
        cls.truth_data_file = resolve_data_path("ax6_data.h5", "read")
        cls.truth_data_keys = ["time", "accel", "gyro"]
        cls.process = ReadCWA(bases=8, periods=12)

        cls.atol_time = 5e-5
        cls.atol = 5e-6


class TestReadBin(BaseProcessTester):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        # override specific necessary attributes
        cls.sample_data_file = resolve_data_path("gnactv_data.h5", "read")
        cls.truth_data_file = resolve_data_path("gnactv_data.h5", "read")
        cls.truth_data_keys = ["time", "accel", "day_ends", "temperature"]

        cls.test_results = False
        cls.process = ReadBin(bases=8, periods=12)

        cls.atol = (
            5e-5  # this is for accel, because GeneActiv csv file values are truncated
        )

    def test_none_file(self):
        with pytest.raises(ValueError):
            self.process.predict(file=None)

    def test_window(self):
        r = ReadBin(bases=8, periods=12)

        assert r.window
        assert r.bases == [8]
        assert r.periods == [12]

    def test_window_warning(self):
        with pytest.warns(UserWarning):
            ReadBin(bases=None, periods=12)
        with pytest.warns(UserWarning):
            ReadBin(bases=8, periods=None)

    @pytest.mark.parametrize(
        ("base", "period"), ((-1, 12), (0, 25), (8, 30), (24, 12), (8, -12))
    )
    def test_window_bounds_error(self, base, period):
        with pytest.raises(ValueError):
            ReadBin(bases=base, periods=period)

    def test_extension_warning(self):
        with pytest.warns(UserWarning):
            with pytest.raises(OSError):
                ReadBin().predict("test.random")


# TODO: find an old version file to test on
class TestReadGT3X(BaseProcessTester):
    @classmethod
    def setup_class(cls):
        super().setup_class()

        # override specific necessary attributes
        cls.sample_data_file = resolve_data_path("gt3x_data.h5", "read")
        cls.truth_data_file = resolve_data_path("gt3x_data.h5", "read")
        cls.truth_data_keys = ["time", "accel", "day_ends"]

        cls.test_results = False
        cls.process = ReadGT3X(base=9, period=2)

    def test_none_file(self):
        with pytest.raises(ValueError):
            self.process.predict(file=None)

    def test_window(self):
        r = ReadGT3X(base=8, period=12)

        assert r.window
        assert r.base == 8
        assert r.period == 12

    def test_window_warning(self):
        with pytest.warns(UserWarning):
            ReadGT3X(base=None, period=12)
        with pytest.warns(UserWarning):
            ReadGT3X(base=8, period=None)

    @pytest.mark.parametrize(
        ("base", "period"), ((-1, 12), (0, 25), (8, 30), (24, 12), (8, -12))
    )
    def test_window_bounds_error(self, base, period):
        with pytest.raises(ValueError):
            ReadGT3X(base=base, period=period)

    def test_extension_warning(self):
        with pytest.warns(UserWarning):
            with pytest.raises(OSError):
                ReadGT3X().predict("test.random")