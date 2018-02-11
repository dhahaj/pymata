
import threading, time, sys, serial

class PyMataSerial(threading.Thread):
    """
     This class manages the serial port for Arduino serial communications
    """

    # class variables
    arduino = serial.Serial()
    port_id = ""
    baud_rate = 57600
    timeout = 1
    command_deque = None

    def __init__(self, port_id, command_deque, baud_rate):
        """
        Constructor:
         :param command_deque: A reference to the deque shared with the _command_handler
         :param baud_rate: must match that of Arduino Sketch
        """
        self.port_id = port_id
        self.command_deque = command_deque
        self.baud_rate = baud_rate

        threading.Thread.__init__(self)
        self.daemon = True
        self.arduino = serial.Serial(self.port_id, self.baud_rate,
                                     timeout=int(self.timeout), writeTimeout=0)

        self.stop_event = threading.Event()

        # without this, running python 3.4 is extremely sluggish
        if sys.platform == 'linux':
            # noinspection PyUnresolvedReferences
            self.arduino.nonblocking()

    def stop(self):
        self.stop_event.set()

    def is_stopped(self):
        return self.stop_event.is_set()

    def open(self, verbose):
        """
        open the serial port using the configuration data
        returns a reference to this instance
        """
        # open a serial port
        if verbose:
            print('\nOpening Arduino Serial port %s ' % self.port_id)

        try:

            # in case the port is already open, let's close it and then
            # reopen it
            self.arduino.close()
            time.sleep(1)
            self.arduino.open()
            time.sleep(1)
            return self.arduino

        except Exception:
            # opened failed - will report back to caller
            raise

    def close(self):
        """
            Close the serial port
            return: None
        """
        try:
            self.arduino.close()
        except OSError:
            pass

    def write(self, data):
        """
            write the data to the serial port
            return: None
        """
        if sys.version_info[0] < 3:
            self.arduino.write(data)
        else:
            self.arduino.write(bytes([ord(data)]))

    # noinspection PyExceptClausesOrder
    def run(self):
        """
         This method continually runs. If an incoming character is available on the serial port
         it is read and placed on the _command_deque
     
	     @return: Never Returns
        """
        while not self.is_stopped():
            # we can get an OSError: [Errno9] Bad file descriptor when shutting down just ignore it
            try:
                if self.arduino.inWaiting():
                    c = self.arduino.read()
                    self.command_deque.append(ord(c))
                else:
                    time.sleep(.1)
            except OSError:
                pass
            except IOError:
                self.stop()
        self.close()











