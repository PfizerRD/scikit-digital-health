import pytest
import h5py

from numpy import allclose

from skdh.read import ReadApdmH5


class TestReadBin:
    def test(self, apdm_file):
        res = ReadApdmH5("Lumbar", gravity_acceleration=9.81).predict(apdm_file)

        lumbar_sens = "XI-010284"
        with h5py.File(apdm_file) as f:
            acc = f['Sensors'][lumbar_sens]['Accelerometer'][()] / 9.81
            time = f['Sensors'][lumbar_sens]["Time"][()] / 1e6  # to seconds
            gyro = f['Sensors'][lumbar_sens]['Gyroscope'][()]
            temp = f['Sensors'][lumbar_sens]['Temperature'][()]

        assert allclose(res['accel'], acc)
        assert allclose(res['time'] - time[0], time - time[0])
        assert allclose(res['gyro'], gyro)
        assert allclose(res['temperature'], temp)

    def test_none_file_error(self):
        with pytest.raises(ValueError):
            ReadApdmH5("Lumbar").predict(None)

    def test_extension_warning(self):
        with pytest.warns(UserWarning) as record:
            with pytest.raises(Exception):
                ReadApdmH5("Lumbar").predict("test.random")

        assert len(record) == 1
        assert "File extension is not expected '.h5'" in record[0].message.args[0]