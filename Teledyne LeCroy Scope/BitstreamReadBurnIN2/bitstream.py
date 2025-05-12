import logging
from logging import raiseExceptions

import serial
import serial.tools.list_ports as list_ports
import datetime
import uuid
import easygui
import sys

# from PyQt6.QtHelp import removeCustomValue

'''def load_serial_number(device_name="Device 1"):
    # Find the current folder where script is running
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "stlink_serials.json")
    
    # Load the JSON file
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    try:
        serial_number = data["devices"][device_name]["serial_number"]
        return serial_number
    except KeyError:
        print(f"Device '{device_name}' not found in {json_path}.")
        return None
'''

#device_no = ""

class CustomFormatter(logging.Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629"""

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
ch2 = logging.StreamHandler()
ch2.setLevel(logging.DEBUG)
ch2.setFormatter(CustomFormatter('%(asctime)s | %(name)20s | %(levelname)8s | %(filename)-15s:%(lineno)-8d '
                                     '| %(message)-120s'))
log.addHandler(ch2)
log.info('Started')


class Bitstreamreader:
    """

    """
    _instances = 0
    _names = list()

    def __init__(self, known_devices=None, name: str = uuid.uuid1(), device_info=None, device_name=None):
        """
        :param known_devices:
        :param name: str
        """
        global device_no
        device_no = device_name

        Bitstreamreader._instances += 1
        self.name = name
        Bitstreamreader._names.append(self.name)
        self.classname = 'Bitstreamreader'
        self.classname = type(self).__qualname__
        self.uart_timeout = 5
        if known_devices:
            pass
            self._known_devices = known_devices
        else:
            # self._known_devices = {'0673FF535488524867144359': 'CHH1',
            #                        '0669FF535488524867144013': 'CHH2',
            #                        '066CFF495087534867072015': 'CHW1',
            #                        '066EFF535488524867225429': 'CHW2'
            # }
            # ****************************************************************************************************
            # Read from JSON file device name and HW serial no
            device_serial = device_info
            #device2_serial = load_serial_number("Device 2")
            
            #print(f"Device 1 SN: {device_serial}")
            #print(f"Device 2 SN: {device2_serial}")

            if device_serial:
                self._known_devices = {
                    device_serial: 'CH1'
                    #device2_serial: 'CH2'
                }
            else:
                raise ValueError("Could not load serial number for Devices attached - check the JSON stlink_serials.json file")

            # ****************************************************************************************************
            #self._known_devices = {'066BFF535488524867144156': 'CH1',
            #                       '066FFF535488524867153517': 'CH2'
            #}
        ports = serial.tools.list_ports.comports()

        self._nukleo_channels = self.enum_channels(self._known_devices)
        self._telegram_read_count = 0
        self._telegram_read_anyflag_count = 0
        self._telegram_read_customflag_count = 0
        self._anyflag_count = 0
        self._customflag_count = 0
    
    def __del__(self):
        Bitstreamreader._instances -= 1
        try:
            Bitstreamreader._names.remove(self.name)
        except:
            # logging.warning('LEVEL 1 - %s - Cannot delete a nonexistent instance name', self.name)
            Bitstreamreader._instances += 1
            pass

    @property
    def telegram_read_count(self):
        return self._telegram_read_count
    @telegram_read_count.setter
    def telegram_read_count(self, value):
        if not isinstance(value, int):
            raise TypeError('value must be an integer')
        self._telegram_read_count = value

    @property
    def telegram_read_anyflag_count(self):
        return self._telegram_read_anyflag_count
    @telegram_read_anyflag_count.setter
    def telegram_read_anyflag_count(self, value):
        if not isinstance(value, int):
            raise TypeError('value must be an integer')
        self._telegram_read_anyflag_count = value

    @property
    def telegram_read_customflag_count(self):
        return self._telegram_read_customflag_count
    @telegram_read_customflag_count.setter
    def telegram_read_customflag_count(self, value):
        if not isinstance(value, int):
            raise TypeError('value must be an integer')
        self._telegram_read_customflag_count = value

    def enum_channels(self, known_devices):
        """
        :param known_devices: list of known device serial numbers
        :return: a dictionary mapping channel names to Telegram objects representing the connected devices
        """
        enum_serial_ports = list_ports.comports(include_links=True)
        nukleo_channels = {}
        for serial_port in enum_serial_ports:
            if serial_port.serial_number in known_devices:
                # Add a new dictionary entry with KEY = Channel and VALUE = Telegram Object linked to the COM-Port where a specific Nukleo serial Number is connected
                try:
                    nukleo_channels.update({known_devices[serial_port.serial_number]: self.Telegram(
                        serial.Serial(port=serial_port.device, baudrate=355200, bytesize=8, timeout=0,
                                      stopbits=serial.STOPBITS_ONE))})
                except:
                    pass
        return nukleo_channels

    @staticmethod
    def list_ports():
        """
        :list_ports(self)
        List all available comports.

        :return: None
        """
        for port in list_ports.comports():
            print(
                f'Manufacturer: {port.manufacturer}, Description: {port.description}, Port: {port.name}, S/N: {port.serial_number}')

    def read_single(self, channel):
        """
        """
        function_name = self.read_single.__name__
        # log.info(f"{self.classname}.{function_name}() will be executed")
        if channel in self._nukleo_channels.keys():
            if rval := self._nukleo_channels.get(channel).fetch():
                if rval.anyflag:
                    self._anyflag_count += 1
                if rval.customflag:
                    self._customflag_count += 1
                self._telegram_read_count += 1
                return rval

        else:
            log.warning(f'Channel {channel} not available')
            return False


    def read_buffer(self, channel, readings=1):
        """Read whatever the buffer contains, count the occurence of all flags and return them.

        :param channel:
        :param readings:
        :return:
        """
        message = self.read_single(channel)
        return message


    @property
    def nukleo_channels(self):
        return self._nukleo_channels


    class Telegram:
        _STARTBIT = 274902941696
        # viso_uv_mask = 0b 00000000 00000001 00000000 00000000 00000000 = 16777216
        _S_UV = 16777216
        # viso_ov_mask = 0b 00000000 00000000 01000000 00000000 00000000 = 4194304
        _S_OV = 4194304
        # gm_mask = 0b 00000000 00000000 00100000 00000000 00000000 = 2097152
        _S_GM = 2097152
        # ot2_s_mask = 0b 00000000 00000000 00010000 00000000 00000000 = 1048576
        _S_OT2 = 1048576
        # ot1_s_mask = 0b 00000000 00000000 00001000 00000000 00000000 = 524288
        _S_OT1 = 524288
        # s_floos = 0b 00000000 00000000 00000100 00000000 00000000 = 262144
        _S_FLOOS = 262144
        # s_desat_mask = 0b 00000000 00000000 00000010 00000000 00000000 = 131072
        _S_DESAT = 131072
        # s_parity_mask = 0b 00000000 00000000 00000001 00000000 00000000 = 65536
        _S_PARITY = 65536
        # p_floos_mask = 0b 00000000 00000000 00000000 01000000 00000000 = 16384
        _P_FLOOS = 16384
        # p_ot1_mask = 0b 00000000 00000000 00000000 00100000 00000000 = 8192
        _P_OT1 = 8192
        # p_ot2_mask = 0b 00000000 00000000 00000000 00010000 00000000 = 4096
        _P_OT2 = 4096
        # p_oc_mask = 0b 00000000 00000000 00000000 00001000 00000000 = 2048
        _P_OC = 2048
        # p_dti_mask = 0b 00000000 00000000 00000000 00000010 00000000 = 512
        _P_DTI = 512
        # p_ilock_mask = 0b 00000000 00000000 00000000 00000001 00000000 = 256
        _P_ILOCK = 256
        _STOPBIT = 1


        """
        Class representing a Telegram message for communication.
        """
        def __init__(self, serialhandler):
            self.classname = type(self).__qualname__
            self._message = None
            self._message_timestamp = None
            self._anyflag = None
            self._customflag = None
            # XORIng the mask with the value to identify error or warning bits which are flagging
            # xor_mask = 0b 01000000 00000001 01111110 00000000 00000000 = 274902941696
            self._customflag_mask = 274902941696
            self._s_temp_filtered = 0
            self._streambuffer = b''
            self.buffersize = 0
            self._startbit = None
            self._serialhandler = serialhandler


        @property
        def anyflag(self):
            return self._anyflag
        
        @property
        def customflag(self):
            return self._customflag


        @property
        def customflag_mask(self):
            return self._customflag_mask
        @customflag.setter
        def customflag_mask(self, value_list: list):
            if not isinstance(value_list, list):
                raise TypeError('customflag must be a list')
            self._customflag_mask = 0
            for value in value_list:
                self._customflag_mask = self._customflag_mask | value




        def customflag_mask_bit_test(self, bit):
            """
            Checks if a specific bit is set in the custom flag mask.

            This method evaluates whether the bit at a given position
            within the custom flag mask is set (1) or not set (0). The
            custom flag mask is represented internally within the
            object, and the position of the bit is specified by the
            user.

            :param bit: The position of the bit to test in the custom flag mask.
            :type bit: int
            :return: True if the bit at the specified position is set, otherwise False.
            :rtype: bool
            :raises TypeError: If the provided `bit` parameter is not an integer.
            """
            if not isinstance(bit, int):
                raise TypeError('customflag must be an integer')
            if self._customflag_mask & (2 ** bit):
                return True
            else:
                return False


        def customflag_mask_bit_define(self, bit, value):
            """
            Sets or clears a specific bit in the `_customflag_mask` attribute of the
            object. The bit is specified by the `bit` parameter, and the action is
            determined based on the `value` parameter. If `value` is 1, the specified
            bit is set to 1. If `value` is 0, the specified bit is cleared (set to 0).
            The method enforces type checks for both `bit` and `value`, and ensures
            that the `value` parameter can only be 0 or 1.

            :param bit: The bit position to modify in the `_customflag_mask` attribute.
            :type bit: int
            :param value: The value to set the bit to, either 0 (clear) or 1 (set).
            :type value: int
            :return: None
            """
            if not isinstance(value, int):
                raise TypeError('value must be an integer')
            if not isinstance(bit, int):
                raise TypeError('bit must be an integer')
            if value not in [0, 1]:
                raise TypeError('value must be 0 or 1')

            if value == 0:
                self._customflag_mask = self._customflag_mask & ~(1<<bit)
            elif value == 1:
                self._customflag_mask = self._customflag_mask | (1<<bit)


        @property
        def raw_data(self):
            return self._message

        @property
        def timestamp(self):
            return self._message_timestamp

        @staticmethod
        def crc_ccitt_16(data):
            crc = 0xFFFF
            for byte in data:
                crc ^= (byte << 8)
                for _ in range(8):
                    if crc & 0x8000:
                        crc = (crc << 1) ^ 0x1021
                    else:
                        crc <<= 1

                    crc &= 0xFFFF

            return crc


        @staticmethod
        def calc_parity(x):
            y = x ^ (x >> 1)
            y = y ^ (y >> 2)
            y = y ^ (y >> 4)
            y = y ^ (y >> 8)
            y = y ^ (y >> 16)

            # Rightmost bit of y holds
            # the parity value if (y&1)
            # is 1 then parity is odd
            # else even
            if (y & 1):
                return False
            return True

        @property
        def f_startbit(self):
            if self._message & _STARTBIT:
                return False
            else:
                return True

        @property
        def s_temp(self):
            # Take Care, BIT 23 is always 0 and not a temperature bit
            # temperature_mask = 0b0011111101111110000000000000000000000000 = 272696868864
            if self._message is not None:
                temperature1 = (self._message & 0b0000000001111110000000000000000000000000) >> 25
                temperature2 = (self._message & 0b0011111100000000000000000000000000000000) >> 26
                return temperature1 + temperature2
            else:
                return None

        @property
        def s_temp_filtered(self):
            # temperature_mask = 0b0011111101111110000000000000000000000000 = 272696868864
            return self._s_temp_filtered

        @property
        def s_uv(self):
            # viso_uv_mask = 0b 00000000 00000001 00000000 00000000 00000000 = 16777216
            if self._message & self._S_UV:
                return False
            else:
                return True

        @property
        def s_ov(self):
            # viso__ov_mask = 0b 00000000 00000000 01000000 00000000 00000000 = 4194304
            if self._message & self._S_OV:
                return False
            else:
                return True

        @property
        def s_gm(self):
            # gm_mask = 0b 00000000 00000000 00100000 00000000 00000000 = 2097152
            if self._message & self._S_GM:
                return False
            else:
                return True

        @property
        def s_ot2(self):
            # ot2_s_mask = 0b 00000000 00000000 00010000 00000000 00000000 = 1048576
            if self._message & self._S_OT2:
                return False
            else:
                return True

        @property
        def s_ot1(self):
            # ot1_s_mask = 0b 00000000 00000000 00001000 00000000 00000000 = 524288
            if self._message & self._S_OT1:
                return False
            else:
                return True

        @property
        def s_floos(self):
            # s_floos = 0b 00000000 00000000 00000100 00000000 00000000 = 262144
            if self._message & self._S_FLOOS:
                return False
            else:
                return True

        @property
        def s_desat(self):
            # s_desat_mask = 0b 00000000 00000000 00000010 00000000 00000000 = 131072
            if self._message & self._S_DESAT:
                return False
            else:
                return True

        @property
        def s_parity(self):
            # s_parity_mask = 0b0011111101111111011111100000000000000000 = 272721903616
            parity = self.calc_parity((self._message & 274877775872) >> 17)
            # s_parity_mask = 0b 00000000 00000000 00000001 00000000 00000000 = 65536
            if self._message & self._S_PARITY and parity:
                return False
            elif not self._message & self._S_PARITY and not parity:
                return False
            else:
                return True

        @property
        def p_floos(self):
            # p_floos_mask = 0b 00000000 00000000 00000000 01000000 00000000 = 16384
            if self._message & self._P_FLOOS:
                return True
            else:
                return False

        @property
        def p_ot1(self):
            # p_ot1_mask = 0b 00000000 00000000 00000000 00100000 00000000 = 8192
            if self._message & self._P_OT1:
                return True
            else:
                return False

        @property
        def p_ot2(self):
            # p_ot2_mask = 0b 00000000 00000000 00000000 00010000 00000000 = 4096
            if self._message & self._P_OT2:
                return True
            else:
                return False

        @property
        def p_oc(self):
            # p_oc_mask = 0b 00000000 00000000 00000000 00001000 00000000 = 2048
            if self._message & self._P_OC:
                return True
            else:
                return False

        @property
        def p_dti(self):
            # p_dti_mask = 0b 00000000 00000000 00000000 00000010 00000000 = 512
            if self._message & self._P_DTI:
                return True
            else:
                return False

        @property
        def p_ilock(self):
            # p_ilock_mask = 0b 00000000 00000000 00000000 00000001 00000000 = 256
            if self._message & self._P_ILOCK:
                return True
            else:
                return False

        @property
        def f_stopbit(self):
            if self._message & self._STOPBIT:
                return False
            else:
                return True



        @property
        def flaglist(self):
            flags = []
            if self._anyflag:
                if self.s_uv:
                    flags.append('S_UV')
                if self.s_ov:
                    flags.append('S_OV')
                if self.s_gm:
                    flags.append('S_GM')
                if self.s_ot1:
                    flags.append('S_OT1')
                if self.s_ot2:
                    flags.append('S_OT2')
                if self.s_floos:
                    flags.append('S_FLOOS')
                if self.s_desat:
                    flags.append('S_DESAT')
                if self.s_parity:
                    flags.append('S_PARITY')
                if self.p_floos:
                    flags.append('P_FLOOS')
                if self.p_ot1:
                    flags.append('P_OT1')
                if self.p_ot2:
                    flags.append('P_OT2')
                if self.p_oc:
                    flags.append('P_OC')
                if self.p_dti:
                    flags.append('P_DTI')
                if self.p_ilock:
                    flags.append('P_ILOCK')
            return flags


        def flagdict(self):
            flagdict = {}
            flagdict.update({'S_UV': 1 if self.s_uv else 0})
            flagdict.update({'S_OV': 1 if self.s_ov else 0})
            flagdict.update({'S_GM': 1 if self.s_gm else 0})
            flagdict.update({'S_OT1': 1 if self.s_ot1 else 0})
            flagdict.update({'S_OT2': 1 if self.s_ot2 else 0})
            flagdict.update({'S_FLOOS': 1 if self.s_floos else 0})
            flagdict.update({'S_DESAT': 1 if self.s_desat else 0})
            flagdict.update({'S_PARITY': 1 if self.s_parity else 0})
            flagdict.update({'P_FLOOS': 1 if self.p_floos else 0})
            flagdict.update({'P_OT1': 1 if self.p_ot1 else 0})
            flagdict.update({'P_OT2': 1 if self.p_ot2 else 0})
            flagdict.update({'P_OC': 1 if self.p_oc else 0})
            flagdict.update({'P_DTI': 1 if self.p_dti else 0})
            flagdict.update({'P_ILOCK': 1 if self.p_ilock else 0})
            return flagdict



        def fetch(self):
            """
            Reads data from the UART buffer and processes it to identify a specific record frame.

            :return: The processed data from the UART buffer
            """
            function_name = self.fetch.__name__
            # log.info(f"{self.classname}.{function_name}() will be executed")
            rval_data = None
            self._anyflag = False
            self._message = None
            # Read the complete UART Buffer
            try:
                self._streambuffer = self._streambuffer + self._serialhandler.read(self._serialhandler.in_waiting)

            except serial.SerialException:
                print('Exception raised while reading UART buffer. COM-Port does not exists anymore.')
                easygui.msgbox("UART communication intrerupted(COM-Port does not exist anymore)!", title=device_no)
                sys.exit()

            # If more than 12 Bytes Data is available, continue with evaluation
            if len(self._streambuffer) > 12:
                # Search for two Bytes with a distance of 6 Bytes and an increasing number in range 0x80 - 0xff
                for i in range(len(self._streambuffer) - 6):
                    if self._streambuffer[i] > 127:

                        if (self._streambuffer[i] == (self._streambuffer[i + 6] - 1)) or ((self._streambuffer[i] == 0xFF) and (self._streambuffer[i + 6] == 0x80)):
                            # Found what we have searched for, identified a record frame
                            # Slice 6 Bytes of the Byte-Sequence starting with the Byte after the "Rolling-Byte"
                            
                            rval_data = int((self._streambuffer[i + 1:i + 6]).hex(), 16) # original code from Mike.
                            
                            #-----------------------------------------------------------------------------------------                            
                            # Only read 4 bytes if the first byte is zero, otherwise read 5
                            """if self._streambuffer[i] == 0x00:
                                rval_data = int((self._streambuffer[i + 1:i + 5]).hex(), 16)  # Only read 4 bytes
                            else:
                                rval_data = int((self._streambuffer[i + 1:i + 6]).hex(), 16)  # Read 5 bytes"""
                            #-----------------------------------------------------------------------------------------                                                    

                            self._message = rval_data
                            # print(f"Hex Value: {hex(self._message)}")
                            local_timestamp = datetime.datetime.now()
                            # ANDIng the value with the mask to sort out unneccessary data
                            # and_mask = 0b01000000 00000001 01111110 01111111 00000000 = 274902974208

                            # XORIng the mask with the value to identify error or warning bits which are flagging
                            # xor_mask = 0b 01000000 00000001 01111110 00000000 00000000 = 274902941696

                            if 274902941696 ^ (rval_data & 274902974208):
                                # At least one warning or error is detected
                                self._anyflag = True
                                self._message_timestamp = local_timestamp

                            
                            if self._customflag_mask ^ (rval_data & 274902974208):
                                # At least one warning or error is detected
                                self._customflag = True
                                self._message_timestamp = local_timestamp

                            # Update the filtered Temperature
                            self._s_temp_filtered += int((self.s_temp - self._s_temp_filtered) * 0.01)
                            # Truncate the buffer to the next potential record.
                            self._streambuffer = self._streambuffer[i + 6:]
                            self.buffersize = len(self._streambuffer)
                            break
            if rval_data:
                return self
            else:
                return None

