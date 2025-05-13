########################################################################################################################
# BitStream Reader
#-----------------------------------------------------------------------------------------------------------------------
# A Python software for reading BitStream data of Power Integration Devices with BitStream Technology
#-----------------------------------------------------------------------------------------------------------------------
# 0.    To make this Class work you need to install "pyserial" which is a package handling the RS232 interfaces
#       No other precondition ins expected.
#
# 1.    Make an instance if the BitStreamReader Class
#
#       bs = BitStreamReader({'0673FF535488524867144359': 'ch1', '0669FF535488524867144013': 'ch2'})
#       You MUST provide a dictionary with strings representing a CHANNEL 'CH1' as a value and the corrosponding
#       device serial number as a key.
#
#       The class contains two static functions which can be used without instantiating, listing all devices
#       attached to the computer which can operate with BitStream.
#
#       a.  BitStreamReader.list_ports()
#       b.  BitStreamReader.find_nukleo_devices()
#
# 2.    Read Data
#
#       bs = BitStreamReader({'0673FF535488524867144359': 'ch1', '0669FF535488524867144013': 'ch2'})
#       while True:
#           telegram = bs.ch1.fetch()
#           make what you like with telegramn
#
#       telegram is an object containing all data for as SINGLE record read from the Nukleo.
#       telegram has further properties & functions making your live easier filtering, evaluating and formatting the data
#
#       flaglist = telegram.flaglist # Gives you all error & warning flags in human readable list format
#       print(telegram.flaglist) # Show it on screen
#
#       flagdict = telegram.flagdict # Gives you all error & warning flags in python dictionary format
#       print(telegram.flagdict) # Show it on screen
#

#       BitStreamReader ahs two valuable "Triggering" functions which can check if any of the BitStream-Flags showing
#       unexpected values.
#
#       a. Anyflag
#       if telegram.has_anyflag is True:  # Checs if ANY of the BitStream Flags shows unexpected results
#           print(telegram.flaglist)
#
#
#       b. customflag
#       if telegram.has_customflag is True:  # Checks the BitStream Flags shows unexpected results with a customer specific mask
#           print(telegram.flaglist)
#
#
#       Customflag has getters and setters. Getters showing the current state of a specific BitStream-Bit while
#       Setters enables or disables triggering for this specific Bit.
#
#       Getter Example:
#       Print(telegram.cf_trig_s_ot2) shows if the S_OT2 shows
#
#       Setter Example:
#       telegram.cf_trig_s_ot2 = False      # Disables triggering id S_OT2 shows up.
#
#       Thats it, have fun.
#
#   3.  Internals
#
#       a.  All Bitstream Data is preprocessed by the Nukleo-Device and FW. This FW can throw away BitStream Data if not
#       processable, you will never note that.
#
#       b.  All Nukleo Telegrams will be sent through a virtual serial intervace to your computer.
#       your computer has limitations on this buffer, please be aware. A buffer full/overflow will lead to lost data.
#
#       Countermeasure is to use telegram.fetch() in a regular way. This function is reading the COMPLETE UART-Buffer
#       regardless its size and hand it to an internal buffer.
#
#       c.  All Timestamp-Information is as per decoding with the BitStreamReader-Class in this moment you call fetch()
#       There is NO timestamp that the BitStream or the Nukleo is adding in advance.
#
#
#######################################################################################################################

import serial
import serial.tools.list_ports as list_ports
import datetime
from collections import deque


class RingBuffer:
    """ Class that implements a not-yet-full buffer. """
    def __init__(self, bufsize):
        self.bufsize = bufsize
        self.data = []

    class __Full:
        """ Class that implements a full buffer. """
        def add(self, x):
            """ Add an element overwriting the oldest one. """
            self.data[self.currpos] = x
            self.currpos = (self.currpos+1) % self.bufsize
        def get(self):
            """ Return list of elements in correct order. """
            return self.data[self.currpos:]+self.data[:self.currpos]

    def add(self,x):
        """ Add an element at the end of the buffer"""
        self.data.append(x)
        if len(self.data) == self.bufsize:
            # Initializing current position attribute
            self.currpos = 0
            # Permanently change self's class from not-yet-full to full
            self.__class__ = self.__Full

    def get(self):
        """ Return a list of elements from the oldest to the newest. """
        return self.data

class BitStreamReader:
    """
    Represents a class responsible for managing bitstream communication channels.

    This class provides mechanisms to manage and interact with multiple communication 
    channels for bitstream operations, including initialization with known devices, 
    tracking instances, and managing connected channels represented by Telegram objects. 
    It provides utilities to interact with NUCLEO devices and manages associated 
    attributes such as timeouts and read counts. Static methods are provided to help 
    discover and interact with serial ports.

    :ivar _instances: Number of active BitStreamReader instances.
    :type _instances: int
    :ivar _names: List of the names of all instantiated BitStreamReader objects.
    :type _names: list
    :ivar ch1: Placeholder for channel 1, which may represent a Telegram object or channel instance.
    :type ch1: Optional[Any]
    :ivar ch2: Placeholder for channel 2, which may represent a Telegram object or channel instance.
    :type ch2: Optional[Any]
    :ivar ch3: Placeholder for channel 3, which may represent a Telegram object or channel instance.
    :type ch3: Optional[Any]
    :ivar ch4: Placeholder for channel 4, which may represent a Telegram object or channel instance.
    :type ch4: Optional[Any]
    :ivar ch5: Placeholder for channel 5, which may represent a Telegram object or channel instance.
    :type ch5: Optional[Any]
    :ivar ch6: Placeholder for channel 6, which may represent a Telegram object or channel instance.
    :type ch6: Optional[Any]
    :ivar ch7: Placeholder for channel 7, which may represent a Telegram object or channel instance.
    :type ch7: Optional[Any]
    :ivar ch8: Placeholder for channel 8, which may represent a Telegram object or channel instance.
    :type ch8: Optional[Any]
    :ivar ch9: Placeholder for channel 9, which may represent a Telegram object or channel instance.
    :type ch9: Optional[Any]
    :ivar ch10: Placeholder for channel 10, which may represent a Telegram object or channel instance.
    :type ch10: Optional[Any]
    :ivar ch11: Placeholder for channel 11, which may represent a Telegram object or channel instance.
    :type ch11: Optional[Any]
    :ivar ch12: Placeholder for channel 12, which may represent a Telegram object or channel instance.
    :type ch12: Optional[Any]
    :ivar ch13: Placeholder for channel 13, which may represent a Telegram object or channel instance.
    :type ch13: Optional[Any]
    :ivar ch14: Placeholder for channel 14, which may represent a Telegram object or channel instance.
    :type ch14: Optional[Any]
    :ivar ch15: Placeholder for channel 15, which may represent a Telegram object or channel instance.
    :type ch15: Optional[Any]
    :ivar ch16: Placeholder for channel 16, which may represent a Telegram object or channel instance.
    :type ch16: Optional[Any]
    :ivar classname: The name of the current class, used for meta information or debugging.
    :type classname: str
    :ivar uart_timeout: UART timeout value in seconds for channel operations.
    :type uart_timeout: int
    :ivar _channel_count: Number of communication channels managed.
    :type _channel_count: int
    :ivar _known_devices: Dictionary containing known device serial numbers mapped to their respective channels.
    :type _known_devices: dict
    :ivar _nukleo_channels: Dictionary of active communication channels associated with their Telegram objects.
    :type _nukleo_channels: dict
    :ivar _telegram_read_count: Count of Telegram read operations performed.
    :type _telegram_read_count: int
    :ivar _customflag_trigger_count: Count of custom flag trigger events.
    :type _customflag_trigger_count: int
    :ivar _anyflag_trigger_count: Count of any flag trigger events.
    :type _anyflag_trigger_count: int
    """
    _instances = 0
    _names = list()
    ch1 = None
    ch2 = None
    ch3 = None
    ch4 = None
    ch5 = None
    ch6 = None
    ch7 = None
    ch8 = None
    ch9 = None
    ch10 = None
    ch11 = None
    ch12 = None
    ch13 = None
    ch14 = None
    ch15 = None
    ch16 = None

  
    def __init__(self, anyflag_mask: int = 274902974271, known_devices=None, name: str = 'bitstreamreader'):
        """
        :param known_devices:
        :param name: str

        """
        BitStreamReader._instances += 1
        self.name = name + str(BitStreamReader._instances)
        BitStreamReader._names.append(self.name)
        self.classname = 'Bitstreamreader'
        self.classname = type(self).__qualname__
        self._anyflag_mask = anyflag_mask
        self.uart_timeout = 5
        self._channel_count = 0
        if known_devices:
            if not isinstance(known_devices, dict):
                raise TypeError('known_devices must be a dictionary')
            for key, value in known_devices.items():
                if not isinstance(key, str):
                    raise TypeError('known_devices keys must be string')
                if not isinstance(value, str):
                    raise TypeError('known_devices values must be string')
                if not key.isalnum():
                    raise ValueError('known_devices keys must be alphanumeric')
                if not value.isalnum():
                    raise ValueError('known_devices values must be alphanumeric')
                if len(value) > 4:
                    raise ValueError('known_devices values must be at most 4 characters long')
                known_devices[key] = value.lower()
            self._known_devices = known_devices
        else:
            self._known_devices = BitStreamReader.find_nukleo_devices('STMicroelectronics STLink Virtual COM Port')
        self._nukleo_channels = self.channel_creator(self._known_devices)
        self._telegram_read_count = 0
        self._customflag_trigger_count = 0
        self._anyflag_trigger_count = 0
        self._anyflag_filter = 0


    def __del__(self):
        del self._known_devices
        del self._nukleo_channels
        del self._telegram_read_count
        del self._customflag_trigger_count
        del self._anyflag_trigger_count
        BitStreamReader._instances -= 1
        try:
            BitStreamReader._names.remove(self.name)
        except:
            BitStreamReader._instances += 1
            pass

    @property
    def read_count(self):
        """
        Returns the total read count accumulated across all Nukleo channels.

        This property computes the sum of the read counts from individual channels
        available in the `_nukleo_channels` attribute. Each channel contributes its
        `read_count` to the total value.

        :rtype: int
        :return: The total read count across all Nukleo channels.
        """
        counts = 0
        for channel in self._nukleo_channels.values():
            counts += channel.read_count
        return counts

    @property
    def anyflag_trigger_count(self):
        """
        Calculates the total trigger count for any flag across all channels.

        This property iterates through all Nukleo channel objects stored within
        the current instance and sums up their respective `anyflag_trigger_count`
        values. It provides a consolidated count of any flag triggers.

        :return: Total count of any flag triggers across all channels
        :rtype: int
        """
        counts = 0
        for channel in self._nukleo_channels.values():
            counts += channel.anyflag_trigger_count
        return counts

    def channels(self) -> dict:
        """
        Retrieves the internal dictionary containing channel information.

        :return: A dictionary containing channel data.
        :rtype: dict
        """
        return self._nukleo_channels


    def channel_creator(self, known_devices) -> dict:
        """
        :param known_devices: list of known device serial numbers
        :return: a dictionary mapping channel names to Telegram objects representing the connected devices
        """
        if known_devices is None:
            return False
        if not isinstance(known_devices, dict):
            raise TypeError('known_devices must be a dictionary')

        enum_serial_ports = list_ports.comports(include_links=True)
        nukleo_channels = {}
        for serial_port in enum_serial_ports:
            if serial_port.serial_number in known_devices:
                # Add a new dictionary entry with KEY = Channel and VALUE = Telegram Object linked to the COM-Port where a specific Nukleo serial Number is connected
                self._channel_count += 1
                exec(f'BitStreamReader.{known_devices[serial_port.serial_number]} = self.Telegram(serial.Serial(port=serial_port.device, baudrate=355200, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE), anyflag_mask=self._anyflag_mask, channel=known_devices[serial_port.serial_number])')
                # exec(f'BitStreamReader.{known_devices[serial_port.serial_number]} = self.Telegram(serial.Serial(port=serial_port.device, baudrate=355200, bytesize=8, timeout=0, stopbits=serial.STOPBITS_ONE), known_devices[serial_port.serial_number])')

                nukleo_channels.update({f'{known_devices[serial_port.serial_number]}': eval(f'BitStreamReader.{known_devices[serial_port.serial_number]}')})
        return nukleo_channels


    @staticmethod
    def find_nukleo_devices(identifier='STMicroelectronics STLink Virtual COM Port') -> dict:
        """
        Find and return connected NUCLEO devices based on their description.

        This static method scans through available serial ports and searches for devices 
        matching the provided identifier in their description. Upon finding a match, it 
        maps the device's serial number to a generated channel name (e.g., 'ch1', 'ch2', etc.), 
        providing a dictionary of connected NUCLEO devices. This method ensures that input 
        validations are performed for the identifier, raising exceptions as needed.

        :param identifier: The description to search for in the serial port devices.
            Defaults to 'STMicroelectronics STLink Virtual COM Port'.
        :type identifier: str
        :return: Dictionary mapping the serial number of detected devices to channel 
            identifiers like 'ch1', 'ch2', etc.
        :rtype: dict
        :raises ValueError: If the identifier is None.
        :raises TypeError: If the identifier is not a string.
        """
        if identifier is None:
            raise ValueError('identifier cannot be None')
        if not isinstance(identifier, str):
            raise TypeError('identifier must be a string')
        index = 0
        known_devices = {}
        for port in list_ports.comports():
            if identifier in port.description:
                index += 1
                known_devices[port.serial_number] = f'ch{index}'
        return known_devices

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

    @property
    def nukleo_channels(self) -> dict:
        """
        Gets the Nukleo channels data as a dictionary.

        This property provides access to the stored channels data managed by the
        class. The returned dictionary consists of the channel details that are
        internally tracked.

        :return: Dictionary containing the current Nukleo channel data.
        :rtype: dict
        """
        return self._nukleo_channels

    class Telegram:
        """
        Represents a Telegram object that encapsulates raw BitStream information,
        including S0, S1, and additional evaluation results of the Nukleo-BitStream
        decoder. This class manages and processes data flags, message attributes, and
        bit-masked configurations both for secondary (IGD) and primary (LDI) sides.

        The purpose of this class is to maintain state, manage serial communication,
        and enable configuration via bit-masks for specified flags. The class also
        supports various data flag checks and adjustments based on start or specific
        conditions.

        :ivar classname: The name of the class as a string.
        :type classname: str
        :ivar _message: Holds the current message content.
        :type _message: Optional[str]
        :ivar _timestamp: Timestamp of the last accessed data.
        :type _timestamp: Optional[datetime.datetime]
        :ivar _anyflag: Indicates the presence of the "anyflag".
        :type _anyflag: Optional[bool]
        :ivar _anyflag_mask: Bit-mask configuration for "anyflag".
        :type _anyflag_mask: int
        :ivar _anyflag_trigger_count: Counter for the number of triggers for "anyflag".
        :type _anyflag_trigger_count: int
        :ivar _customflag: Indicates custom flag state.
        :type _customflag: Optional[bool]
        :ivar _customflag_trigger_count: Counter for custom flag state changes.
        :type _customflag_trigger_count: int
        :ivar _read_count: Total count of read operations.
        :type _read_count: int
        :ivar _s_temp_filtered: Filtered temperature data for secondary flag.
        :type _s_temp_filtered: int
        :ivar _streambuffer: The binary stream buffer for processing.
        :type _streambuffer: bytes
        :ivar buffersize: The size of the stream buffer.
        :type buffersize: int
        :ivar _serialhandler: The handler object managing serial communication.
        :type _serialhandler: [Type of serialhandler]
        :ivar _channel: Indicates the channel configuration if applicable.
        :type _channel: Optional
        :ivar _nukleo_buffer_overflow: Flag for buffer overflow conditions.
        :type _nukleo_buffer_overflow: bool
        :ivar _nukleo_buffer_overflow_count: Counter for buffer overflow occurrences.
        :type _nukleo_buffer_overflow_count: int
        :ivar _message_log: Ring buffer storing recent messages.
        :type _message_log: RingBuffer
        :ivar _flagdict: Dictionary for tracking flag-based states.
        :type _flagdict: dict
        :ivar _flagdict_start: Timestamp for the start of flag-based tracking.
        :type _flagdict_start: datetime.datetime
        """
        # IMPORTANT FOR UNDERSTANDING!!!!!!
        # A "Telegram" is containing the RAW BitStream information PLUS
        # S0 + S1 + Additional evaluation results of the Nukleo-BitStream Decoder
        # All Bits are described below
        
        # Secondary side (IGD) information statrs with _S_
        # Primary side (LDI) information statrs with _P_

        # startbit_mask = 0b 10000000 00000000 00000000 00000000 00000000 = 549755813888
        _TELEGRAM_TIMEOUT = 549755813888
        # startbit_mask = 0b 01000000 00000000 00000000 00000000 00000000 = 274902941696
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
        _BUFFER_OVERFLOW = 32
        _FRAME_ERROR = 16
        _FRAME_LENGTH = 8 
        _S1_MASK = 4
        _SO_MASK = 2
        _STOPBIT = 1

        def __init__(self, serialhandler, anyflag_mask=274902974271, channel=None):
            self.classname = type(self).__qualname__
            self._message = None
            self._timestamp = datetime.datetime.now()
            self._anyflag = None
            self._anyflag_mask = anyflag_mask
            self._anyflag_trigger_count = 0
            self._customflag = None
            self._customflag_trigger_count = 0
            self._read_count = 0
            self._s_temp_filtered = 0
            self._streambuffer = b''
            self._buffersize = 0
            self._serialhandler = serialhandler
            self._channel = channel
            self._message_log = RingBuffer(100000)
            self._flagdict = {}
            self._flagdict_start = datetime.datetime.now()
            self._telegram_received = True
            self._telegram_timeout = 1
            self._has_bitstream_warning = False
            self._has_bitstream_error = False
            self._has_transmission_error = False
            self._byte_index = 0

            self._n_buffer_overflow_event = False
            self._n_buffer_overflow_event_count =0



        def __del__(self):
            self._serialhandler.close()

        @property
        def channel(self) -> str:
            """
            Represents a property for accessing the private attribute `_channel` of an object.

            The `channel` property allows external access to the underlying `_channel`
            attribute, ensuring encapsulation and abstraction in the object. This helps in
            keeping the internal representation hidden while providing controlled access
            to its value.

            :return: The value of the `_channel` attribute.
            :rtype: str
            """
            return self._channel

        @property
        def has_nukleo_buffer_overflow(self) -> bool:
            """
            Checks and resets the Nukleo buffer overflow flag.

            This method acts as both a getter and a resetter for the Nukleo buffer
            overflow flag. If the flag is set to True, its value is returned, and it
            is then reset to False.

            :return: The current value of the Nukleo buffer overflow flag before it
                gets reset.
            :rtype: bool
            """
            rval = self._nukleo_buffer_overflow
            self._nukleo_buffer_overflow = False
            return rval

        @property
        def has_anyflag(self) -> bool:
            """
            Checks the value of a specific flag.

            This property is used to determine whether the `_anyflag` attribute
            is set to True or False. The presence and value of this flag often
            indicate specific conditions or configurations within the system.

            :return: Returns `True` if `_anyflag` is set, otherwise returns `False`.
            :rtype: bool
            """
            return self._anyflag

        @property
        def has_transmission_error(self):
            return self._has_transmission_error

        @property
        def has_bitstream_error(self):
            return self._has_bitstream_error

        @property
        def has_bitstream_warning(self):
            return self._has_bitstream_warning

        @property
        def read_count(self) -> int:
            """
            Getter method for the read_count property which allows access to the 
            _private attribute '_read_count'. This property provides the count 
            of read operations or a relevant numerical value associated with the object.

            :return: The value of the '_read_count' attribute
            :rtype: int
            """
            return self._read_count

        @property
        def buffer_size(self):
            return self._buffersize

        @property
        def anyflag_trigger_count(self) -> int:
            """
            Gets the count of anyflag triggers.

            This property retrieves the value of the `_anyflag_trigger_count`
            attribute, representing the count of triggers for any flags that
            occurred.

            :rtype: int
            :return: The count of anyflag triggers.
            """
            return self._anyflag_trigger_count
        @anyflag_trigger_count.setter
        def anyflag_trigger_count(self, value):
            """
            Sets the value for the '_anyflag_trigger_count' attribute.

            :param value: The number of times the anyflag trigger has been activated.
                          Must be a non-negative integer.
            :type value: int
            :raises TypeError: If the value is not an integer.
            :raises ValueError: If the value is less than 0.
            """
            if not isinstance(value, int):
                raise TypeError('value must be an integer')
            if value < 0:
                raise ValueError('value must be greater than or equal to 0')
            self._anyflag_trigger_count = value

        @property
        def telegram_timeout(self):
            return self._telegram_timeout
        @telegram_timeout.setter
        def telegram_timeout(self, value):
            if not isinstance(value, (int)):
                raise TypeError('value must be an int')
            if value <= 0:
                raise ValueError('value must be greater than 0')
            self._telegram_timeout = value

        @property
        def nukleo_buffer_overflow_count(self) -> int:
            """
            Getter for the `_nukleo_buffer_overflow_count` attribute, representing the number
            of buffer overflow occurrences encountered in a system or process. The count is
            typically used for monitoring and diagnostics purposes.

            :return: Current count of buffer overflow occurrences.
            :rtype: int
            """
            return self._nukleo_buffer_overflow_count


        @property
        def anyflag_mask_startbit(self) -> bool:
            """
            Indicates whether the `STARTBIT` flag is set within the current `_anyflag_mask`.

            This property evaluates the bitwise operation between the `_anyflag_mask` attribute
            and the `_STARTBIT` constant to assess whether the specific flag is active. Returns
            a boolean value representing the result.

            :return: True if the `STARTBIT` flag is set in the `_anyflag_mask`, otherwise False.
            :rtype: bool
            """
            return True if self._anyflag_mask & self._STARTBIT else False
        @anyflag_mask_startbit.setter
        def anyflag_mask_startbit(self, value):
            """
            Sets the value of the `_anyflag_mask` attribute's `STARTBIT` flag based on the input.

            The method updates the `_anyflag_mask` by using the `STARTBIT` constant. If the
            parameter's value is `True`, it sets the `STARTBIT` flag within the binary mask.
            If the value is `False`, it removes the `STARTBIT` flag from the mask. The method
            ensures the flag is correctly manipulated to represent the input state within the
            internal representation.

            :param value: A boolean to enable (True) or disable (False) the `STARTBIT` flag
                          in the `_anyflag_mask`.
            :type value: bool
            """
            if value is True:
                self._anyflag_mask |= self._STARTBIT
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._STARTBIT)


        @property
        def anyflag_mask_s_uv(self):
            return True if self._anyflag_mask & self._S_UV else False
        @anyflag_mask_s_uv.setter
        def anyflag_mask_s_uv(self, value):
            if value is True:
                self._anyflag_mask |= self._S_UV
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_UV)

        @property
        def anyflag_mask_s_ov(self):
            return True if self._anyflag_mask & self._S_OV else False
        @anyflag_mask_s_ov.setter
        def anyflag_mask_s_ov(self, value):
            if value is True:
                self._anyflag_mask |= self._S_OV
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_OV)

        @property
        def anyflag_mask_s_gm(self):
            return True if self._anyflag_mask & self._S_GM else False
        @anyflag_mask_s_gm.setter
        def anyflag_mask_s_gm(self, value):
            if value is True:
                self._anyflag_mask |= self._S_GM
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_GM)

        @property
        def anyflag_mask_s_ot2(self):
            return True if self._anyflag_mask & self._S_OT2 else False
        @anyflag_mask_s_ot2.setter
        def anyflag_mask_s_ot2(self, value):
            if value is True:
                self._anyflag_mask |= self._S_OT2
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_OT2)

        @property
        def anyflag_mask_s_ot1(self):
            return True if self._anyflag_mask & self._S_OT1 else False
        @anyflag_mask_s_ot1.setter
        def anyflag_mask_s_ot1(self, value):
            if value is True:
                self._anyflag_mask |= self._S_OT1
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_OT1)

        @property
        def anyflag_mask_s_floos(self):
            return True if self._anyflag_mask & self._S_FLOOS else False
        @anyflag_mask_s_floos.setter
        def anyflag_mask_s_floos(self, value):
            if value is True:
                self._anyflag_mask |= self._S_FLOOS
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_FLOOS)

        @property
        def anyflag_mask_s_desat(self):
            return True if self._anyflag_mask & self._S_DESAT else False
        @anyflag_mask_s_desat.setter
        def anyflag_mask_s_desat(self, value):
            if value is True:
                self._anyflag_mask |= self._S_DESAT
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_DESAT)

        @property
        def anyflag_mask_s_parity(self):
            return True if self._anyflag_mask & self._S_PARITY else False
        @anyflag_mask_s_parity.setter
        def anyflag_mask_s_parity(self, value):
            if value is True:
                self._anyflag_mask |= self._S_PARITY
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S_PARITY)

        @property
        def anyflag_mask_p_floos(self):
            return True if self._anyflag_mask & self._P_FLOOS else False
        @anyflag_mask_p_floos.setter
        def anyflag_mask_p_floos(self, value):
            if value is True:
                self._anyflag_mask |= self._P_FLOOS
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_FLOOS)

        @property
        def anyflag_mask_p_ot1(self):
            return True if self._anyflag_mask & self._P_OT1 else False
        @anyflag_mask_p_ot1.setter
        def anyflag_mask_p_ot1(self, value):
            if value is True:
                self._anyflag_mask |= self._P_OT1
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_OT1)

        @property
        def anyflag_mask_p_ot2(self):
            return True if self._anyflag_mask & self._P_OT2 else False
        @anyflag_mask_p_ot2.setter
        def anyflag_mask_p_ot2(self, value):
            if value is True:
                self._anyflag_mask |= self._P_OT2
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_OT2)

        @property
        def anyflag_mask_p_oc(self):
            return True if self._anyflag_mask & self._P_OC else False
        @anyflag_mask_p_oc.setter
        def anyflag_mask_p_oc(self, value):
            if value is True:
                self._anyflag_mask |= self._P_OC
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_OC)

        @property
        def anyflag_mask_p_dti(self):
            return True if self._anyflag_mask & self._P_DTI else False
        @anyflag_mask_p_dti.setter
        def anyflag_mask_p_dti(self, value):
            if value is True:
                self._anyflag_mask |= self._P_DTI
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_DTI)

        @property
        def anyflag_mask_p_ilock(self):
            return True if self._anyflag_mask & self._P_ILOCK else False
        @anyflag_mask_p_ilock.setter
        def anyflag_mask_p_ilock(self, value):
            if value is True:
                self._anyflag_mask |= self._P_ILOCK
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._P_ILOCK)

        @property
        def anyflag_mask_buffer_overflow(self):
            return True if self._anyflag_mask & self._BUFFER_OVERFLOW else False
        @anyflag_mask_buffer_overflow.setter
        def anyflag_mask_buffer_overflow(self, value):
            if value is True:
                self._anyflag_mask |= self._BUFFER_OVERFLOW
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._BUFFER_OVERFLOW)

        @property
        def anyflag_mask_frame_error(self):
            return True if self._anyflag_mask & self._FRAME_ERROR else False
        @anyflag_mask_frame_error.setter
        def anyflag_mask_frame_error(self, value):
            if value is True:
                self._anyflag_mask |= self._FRAME_ERROR
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._FRAME_ERROR)

        @property
        def anyflag_mask_frame_length(self):
            return True if self._anyflag_mask & self._FRAME_LENGTH else False
        @anyflag_mask_frame_length.setter
        def anyflag_mask_frame_length(self, value):
            if value is True:
                self._anyflag_mask |= self._FRAME_LENGTH
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._FRAME_LENGTH)

        @property
        def anyflag_mask_s1(self):
            return True if self._anyflag_mask & self._S1_MASK else False
        @anyflag_mask_s1.setter
        def anyflag_mask_s1(self, value):
            if value is True:
                self._anyflag_mask |= self._S1_MASK
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._S1_MASK)

        @property
        def anyflag_mask_so(self):
            return True if self._anyflag_mask & self._SO_MASK else False
        @anyflag_mask_so.setter
        def anyflag_mask_so(self, value):
            if value is True:
                self._anyflag_mask |= self._SO_MASK
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._SO_MASK)

        @property
        def anyflag_mask_stopbit(self):
            return True if self._anyflag_mask & self._STOPBIT else False
        @anyflag_mask_stopbit.setter
        def anyflag_mask_stopbit(self, value):
            if value is True:
                self._anyflag_mask |= self._STOPBIT
            else:
                self._anyflag_mask &= (0xFFFFFFFFFF ^ self._STOPBIT)


        @property
        def raw_data(self):
            return self._message

        @property
        def timestamp(self):
            return self._timestamp

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
        def anyflag_mask(self):
            return self._anyflag_mask

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
        def so_event(self):
            # so_event_mask = 0b 00000000 00000000 00000000 00000000 00000010 = 2
            if self._message & self._SO_MASK:
                return True
            else:
                return False

        @property
        def s1_event(self):
            # s1_event_mask = 0b 00000000 00000000 00000000 00000000 00000100 = 4
            if self._message & self._S1_MASK:
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
        def n_buffer_overflow(self):
            return True if self._message & self._BUFFER_OVERFLOW else False

        @property
        def n_frame_error(self):
            return True if self._message & self._FRAME_ERROR else False

        @property
        def n_frame_length(self):
            return True if self._message & self._FRAME_LENGTH else False

        @property
        def telegram_timeout(self):
            return True if self._message & self._TELEGRAM_TIMEOUT else False

        @property
        def flagdict(self):
            flagdict = self._flagdict
            flagdict_start = self._flagdict_start
            self._flagdict = {}
            self._flagdict_start = datetime.datetime.now()
            return {'channel': self._channel, 'interval_start': flagdict_start, 'interval_end': datetime.datetime.now(), 'telegrams_read': self._read_count, 'data': flagdict}


        def _set_event_flaga(self, message, filter_mask):
            self._n_event = False
            self._b_event = False
            self._p_event = False
            self._s_event = False

            filtered_message = message & filter_mask


            if message & self._SO:
                self._so_event = True
                self._so_events +=1
            else:
                self._so_event = False


            if message & self._S1:
                self._s1_event = True
                self._s_event = True
                self._s1_events +=1
            else:
                self._s1_event = False

            if message & self._S_UV:
                self._s_uv_event = True
                self._s_event = True
                self._s_uv_events += 1
            else:
                self._s_uv_event = False

            if message & self._S_OV:
                self._s_ov_event = True
                self._s_event = True
                self._s_ov_events += 1
            else:
                self._s_ov_event = False

            if message & self._S_GM:
                self._s_gm_event = True
                self._s_event = True
                self._s_gm_events += 1
            else:
                self._s_gm_event = False

            if message & self._S_OT1:
                self._s_ot1_event = True
                self._s_event = True
                self._s_ot1_events += 1
            else:
                self._s_ot1_event = False

            if message & self._S_OT2:
                self._s_ot2_event = True
                self._s_event = True
                self._s_ot2_events += 1
            else:
                self._s_ot2_event = False

            if message & self._S_FLOOS:
                self._s_floos_event = True
                self._s_event = True
                self._s_floos_events += 1
            else:
                self._s_floos_event = False

            if message & self._S_DESAT:
                self._s_desat_event = True
                self._s_event = True
                self._s_desat_events += 1
            else:
                self._s_desat_event = False

            if message & self._S_PARITY:
                self._s_parity_event = True
                self._s_event = True
                self._s_parity_events += 1
            else:
                self._s_parity_event = False

            if message & self._P_FLOOS:
                self._s_parity_event = True
                self._s_event = True
                self._s_parity_events += 1
            else:
                self._s_parity_event = False

            if message & self._P_OT1:
                self._p_ot1_event = True
                self._p_event = True
                self._p_ot1_events += 1
            else:
                self._p_ot1_event = False

            if message & self._P_OT2:
                self._p_ot2_event = True
                self._p_event = True
                self._p_ot2_events += 1
            else:
                self._p_ot2_event = False

            if message & self._P_OC:
                self._p_oc_event = True
                self._p_event = True
                self._p_oc_events += 1
            else:
                self._p_oc_event = False

            if message & self._P_DTI:
                self._p_dti_event = True
                self._p_event = True
                self._p_dti_events += 1
            else:
                self._p_dti_event = False

            if message & self._P_ILOCK:
                self._p_ilock_event = True
                self._p_event = True
                self._p_ilock_events += 1
            else:
                self._p_ilock_event = False

            if message & self._FRAME_LENGTH:
                self._n_frame_length_event = True
                self._n_event = True
                self._n_frame_length_events += 1
            else:
                self._n_frame_length_event = False

            if message & self._FRAME_ERROR:
                self._n_frame_error_event = True
                self._n_event = True
                self._n_frame_error_events += 1
            else:
                self._n_frame_error_event = False

            if message & self._BUFFER_OVERFLOW:
                self._n_buffer_overflow_event = True
                self._n_event = True
                self._n_buffer_overflow_events += 1
            else:
                self._n_buffer_overflow_event = False

            if self.telegram_timeout is True:
                self._n_timeout_event = True
                self._n_event = True
                self._n_timeout_events += 1
            else:
                self._n_timeout_event = False

            if self._p_event or self._s_event:
                self._b_event_event = True

        @property
        def flaglist(self) -> list:
            flags = []

            if self.so_event:
                # If an SO-Event happens, the FluxLink Data is probably corrupted.
                # For this reason it makes no sense to add the corrupted data in the flaglist
                flags.append("SO-EVENT")
                self._flagdict.update({'SO-EVENT': self._flagdict.get('SO-EVENT', 1) + 1})
            elif self._anyflag:
                if self.s1_event:
                    flags.append("S1-EVENT")
                    self._flagdict.update({'S1-EVENT': self._flagdict.get('S1-EVENT', 1) + 1})
                if self.s_uv:
                    flags.append('S_UV')
                    self._flagdict.update({'S_UV': self._flagdict.get('S_UV', 1) + 1})
                if self.s_ov:
                    flags.append('S_OV')
                    self._flagdict.update({'S_OV': self._flagdict.get('S_OV', 1) + 1})
                if self.s_gm:
                    flags.append('S_GM')
                    self._flagdict.update({'S_GM': self._flagdict.get('S_GM', 1) + 1})
                if self.s_ot1:
                    flags.append('S_OT1')
                    self._flagdict.update({'S_OT1': self._flagdict.get('S_OT1', 1) + 1})
                if self.s_ot2:
                    flags.append('S_OT2')
                    self._flagdict.update({'S_OT2': self._flagdict.get('S_OT2', 1) + 1})
                if self.s_floos:
                    flags.append('S_FLOOS')
                    self._flagdict.update({'S_FLOOS': self._flagdict.get('S_FLOOS', 1) + 1})
                if self.s_desat:
                    flags.append('S_DESAT')
                    self._flagdict.update({'S_DESAT': self._flagdict.get('S_DESAT', 1) + 1})
                if self.s_parity:
                    flags.append('S_PARITY')
                    self._flagdict.update({'S_PARITY': self._flagdict.get('S_PARITY', 1) + 1})
                if self.p_floos:
                    flags.append('P_FLOOS')
                    self._flagdict.update({'P_FLOOS': self._flagdict.get('P_FLOOS', 1) + 1})
                if self.p_ot1:
                    flags.append('P_OT1')
                    self._flagdict.update({'P_OT1': self._flagdict.get('P_OT1', 1) + 1})
                if self.p_ot2:
                    flags.append('P_OT2')
                    self._flagdict.update({'P_OT2': self._flagdict.get('P_OT2', 1) + 1})
                if self.p_oc:
                    flags.append('P_OC')
                    self._flagdict.update({'P_OC': self._flagdict.get('P_OC', 1) + 1})
                if self.p_dti:
                    flags.append('P_DTI')
                    self._flagdict.update({'P_DTI': self._flagdict.get('P_DTI', 1) + 1})
                if self.p_ilock:
                    flags.append('P_ILOCK')
                    self._flagdict.update({'P_ILOCK': self._flagdict.get('P_ILOCK', 1) + 1})
                if self.n_frame_length:
                    flags.append('N_FRAMELENGTH')
                    self._flagdict.update({'N_FRAMELENGTH': self._flagdict.get('N_FRAMELENGTH', 1) + 1})
                if self.n_frame_error:
                    flags.append('N_FRAME_ERROR')
                    self._flagdict.update({'N_FRAME_ERROR': self._flagdict.get('N_FRAME_ERROR', 1) + 1})
                if self.n_buffer_overflow:
                    flags.append('N_BUFFER_OVERFLOW')
                    self._flagdict.update({'N_BUFFER_OVERFLOW': self._flagdict.get('N_BUFFER_OVERFLOW', 1) + 1})
                if self.telegram_timeout is True:
                    flags.append('TELEGRAM_TIMEOUT')
                    self._flagdict.update({'TELEGRAM_TIMEOUT': self._flagdict.get('TELEGRAM_TIMEOUT', 1) + 1})
            return flags



        def fetch(self) -> (list, bool):
            """
            Reads data from the UART buffer and processes it to identify a specific record frame.

            Fetch is retrieving the RAW data without any data postprocessing.
            Other functions of class Telegram are used to process the data.


            :return: The processed data from the UART buffer
            """
            function_name = self.fetch.__name__
            data = None
            self._anyflag = False
            self._customflag = False
            self._message = None
            self._has_bitstream_warning = False
            self._has_bitstream_error = False
            self._has_transmission_error = False
            # Read the complete UART Buffer
            while self._message is None:
                try:
                    bytes_to_read = self._serialhandler.in_waiting
                    if bytes_to_read > 0:
                        self._streambuffer = self._streambuffer + self._serialhandler.read(self._serialhandler.in_waiting)
                except serial.SerialException:
                    print('Exception raised while reading UART buffer. COM-Port does not exists anymore.')
                # If less than 13 Bytes Data is available, break the while loop
                if len(self._streambuffer) < 13:
                    if self._telegram_received is False:
                        if (datetime.datetime.now() - self._timestamp) > datetime.timedelta(seconds=self._telegram_timeout):
                            # Set a virtual telegram with no Errors/Warnings but a TELEGRAM_TIMEOUT
                            self._message = 0b1100000000000001011111100000000000000001
                            self._anyflag = True
                            self._has_transmission_error = True
                            self._anyflag_trigger_count += 1
                    else:
                        self._telegram_received = False
                    break
                # If more than 12 Bytes Data is available, continue with evaluation
                else:
                    self._telegram_received = True
                    # Search for two Bytes with a distance of 6 Bytes and an increasing number in range 0x80 - 0xff

                    for i in range(len(self._streambuffer) - 6):
                        # Rolling bytes are always above 127 all other bytes not
                        if self._streambuffer[i] & 128:
                            self._byte_index = self._streambuffer[i] & 127


                            # # Find the rolling byte
                            # if (self._streambuffer[i] == (self._streambuffer[i + 6] - 1)) or ((self._streambuffer[i] == 255) and (self._streambuffer[i + 6] == 128)):
                            #     # Found what we have searched for, identified a record frame
                            #     # Slice 6 Bytes of the Byte-Sequence starting with the Byte after the "Rolling-Byte"
                            data = int((self._streambuffer[i + 1:i + 6]).hex(), 16)
                            # self._BUFFER_OVERFLOW = 32
                            if data & 32:
                                self._n_buffer_overflow_event = True
                                self._n_buffer_overflow_event_count += 1

                            # If an SO / FRAME / LENGTH issue occures, all BitStream Data is corrupted by nature
                            # To avoid issues with further processing the data will be replaced with error free data
                            # self._SO_MASK | self._FRAME_ERROR | self._FRAME_LENGTH = 26
                            if data & 26:
                                # 0b 01000000 00000001 01111110 00000000 00011111 = 274902941727
                                data = 274902941727
                                _general_error = True
                                self._bitstream_error = True
                            else:
                                _general_error = False

                            self._message = data
                            self._timestamp = datetime.datetime.now()
                            self._read_count += 1
                            # AND-ing the value with the mask to sort out unneccessary data
                            # and_mask = 0b01000000 00000001 01111110 01111111 00111111 = 274902974271

                            # XORIng the mask with the value to identify error or warning bits which are flagging
                            # xor_mask = 0b01000000 00000001 01111110 00000000 00000101 = 274902941701
                            #                            0b1 01111110 00000000 00000000
                            data_differences_to_expected = 274902941701 ^ data
                            if (data_differences_to_expected) & 274902974271 & self._anyflag_mask:
                                # At least one warning or error is detected
                                self._anyflag = True
                                self._anyflag_trigger_count += 1
                                # self._STOPBIT | self._BUFFER_OVERFLOW | self._FRAME_ERROR | self._FRAME_LENGTH= 274902941753
                                if data_differences_to_expected & 274902941753:
                                    self._has_transmission_error = True
                                # self._S_FLOOS | self._S_DESAT= 409600
                                # self._SO_MASK = 2
                                if (data_differences_to_expected & 409600) or (self._message & 2):
                                    self._has_bitstream_error = True
                                # self._S_OV | self._S_GM | self._S_OT1 | self._S_OT2 | self._P_ILOCK | self._P_DTI | self._P_OC | self._P_OT1 | self._P_OT2 = 24656640
                                if data_differences_to_expected & 24656640:
                                    self._has_bitstream_warning = True

                            # Update the filtered Temperature
                            if _general_error is False:
                                self._s_temp_filtered += int((self.s_temp - self._s_temp_filtered) * 0.01)

                            # Truncate the buffer to the next potential record.
                            self._streambuffer = self._streambuffer[i + 6:]
                            self._buffersize = len(self._streambuffer)
                            break # Break the For-Loop

            if self._message is not None:
                return self
            else:
                return None
