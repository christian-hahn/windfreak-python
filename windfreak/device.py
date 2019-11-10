from serial import Serial


class SerialDevice:

    def __init__(self, devpath):
        self._devpath = devpath
        self._dev = None
        self.open()

    def __del__(self):
        self.close()

    def open(self):
        if self._dev is not None:
            raise RuntimeError('Device has already been opened.')
        self._dev = Serial(port=self._devpath, timeout=1)

    def close(self):
        if self._dev is not None:
            self._dev.close()
            self._dev = None

    def write(self, attribute, *args):
        dtype, request, _ = self.API[attribute]
        if dtype is bool:
            args = (int(a) for a in args)
        self._write(request.format(*args))

    def read(self, attribute, *args):
        dtype, _, request = self.API[attribute]
        ret = self._query(request.format(*args))
        if dtype is bool:
            ret = int(ret)
            if ret not in (0, 1):
                raise ValueError('Invalid return value \'{}\' for type bool.'.format(ret))
        return dtype(ret)

    def _write(self, data):
        """Write to device.

        Args:
            data (str): write data
        """
        self._dev.write(data.encode('utf-8'))

    def _read(self):
        """Read from device.

        Returns:
            str: data
        """
        return self._dev.readline().decode('utf-8').strip()

    def _query(self, data):
        """Write to device and read response.

        Args:
            data (str): write data

        Returns:
            str: data
        """
        self._write(data)
        return self._read()
