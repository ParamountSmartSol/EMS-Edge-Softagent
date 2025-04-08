import minimalmodbus

instrument = minimalmodbus.Instrument('COM11', 2)  # port name, slave address
instrument.serial.baudrate = 9600
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_EVEN
instrument.serial.stopbits = 1
instrument.serial.timeout  = 2  # Adjust as needed
instrument.clear_buffers_before_each_transaction = True  # Helps with buffer issues

data = instrument.read_registers(2999, 124)
hex_values = [format(reg, '04X') for reg in data]
hex_string = ''.join(hex_values)
print(hex_string)