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
        self._dev = Serial(port=self._devpath, timeout=10)

    def close(self):
        if self._dev is not None:
            self._dev.close()
            self._dev = None

    def write(self, attribute, *args):
        dtype, request, _ = self.API[attribute]
        dtype = dtype if isinstance(dtype, tuple) else (dtype,)
        if len(args) != len(dtype):
            raise ValueError('Number of arguments and data-types are not equal.')
        args = ((int(ar) if dt is bool else dt(ar)) for dt, ar in zip(dtype, args))
        self._write(request.format(*args))

    def read(self, attribute, *args):
        dtype, _, request = self.API[attribute]
        dtype = dtype if isinstance(dtype, tuple) else (dtype,)
        if len(args) + 1 != len(dtype):
            raise ValueError('Must have +1 more data-type than argument.')
        args = ((int(ar) if dt is bool else dt(ar)) for dt, ar in zip(dtype, args))
        ret = self._query(request.format(*args))
        dtype = dtype[-1]
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
        rdata = self._dev.readline()
        if not rdata.endswith(b'\n'):
            raise TimeoutError('Expected newline terminator.')
        return rdata.decode('utf-8').strip()

    def _query(self, data):
        """Write to device and read response.

        Args:
            data (str): write data

        Returns:
            str: data
        """
        self._write(data)
        return self._read()
