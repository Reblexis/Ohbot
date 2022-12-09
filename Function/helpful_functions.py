import serial


def checkPort(p: str) -> bool:
    try:
        ser = serial.Serial(p[0], 19200)

        ser.timeout = 0.5
        ser.write_timeout = 0.5
        ser.flushInput()

        msg = "v" + "\n"
        ser.write(msg.encode('latin-1'))

        line = ser.readline()
        ser.close()

        subString = "v1".encode('latin-1')

        if line.find(subString) != -1:
            return True
        else:
            return False
    except:
        return False


def secure_val(val: float, min_val: float, max_val: float) -> float:
    if val < min_val:
        val = min_val
    elif val > max_val:
        val = max_val
    return val


def denormalize(val: float, min_val: float, max_val: float, zero_to_one: bool = False) -> float:
    if zero_to_one:
        val = (val * (max_val - min_val)) + min_val
    else:
        # The value is from -1 to 1
        val = (val + 1) * (max_val - min_val) / 2 + min_val
    return val
