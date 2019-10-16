import RPi.GPIO as GPIO
import time
import requests


class Laundry:
    def __init__(self, machine_type: str, machine_id: str):
        GPIO.setmode(GPIO.BOARD)
        # set pin 40 or GPIO21 as the input/output
        self._pin_to_circuit=40
        self._raw_light = 0
        self._weighted_average = 300
        self._machine_type = machine_type
        self._machine_id = machine_id
        self._base_url="ec2-54-180-114-209.ap-northeast-2.compute.amazonaws.com:8080"
        self._time_count = 5

    def rc_time (self):
        # RPI doesn't have any analog pins so we need to use the time it takes
        # to charge the capacitor instead to measure analog values
        _count = 0
        # output low voltage on GPIO pin
        GPIO.setup(self._pin_to_circuit, GPIO.OUT)
        GPIO.output(self._pin_to_circuit, GPIO.LOW)
        time.sleep(0.1)
        # change the pin back to input
        GPIO.setup(self._pin_to_circuit, GPIO.IN)
        #increment count until the pin goes high
        while (GPIO.input(self._pin_to_circuit) == GPIO.LOW):
            _count += 1
        self._raw_light = _count
        
    def calculate_wma(self):
        # use a weighted average to smooth the readings
        _tmp_weighted_average = 0.875*self._weighted_average + 0.125*self._raw_light
        self._weighted_average = _tmp_weighted_average
        

    def send_status(self):
        print("hello")
        pass

    def run(self):
        try:
            # Main loop
            while True:
                time.sleep(0.5)
                self.rc_time()
                self.calculate_wma()
                #print(self._weighted_average)
                bool_status = self._weighted_average>=300
                print(bool_status, int(self._weighted_average)) 
                self._time_count-=1
                if self._time_count <= 0:
                    self.send_status()
                    self._time_count=60
        #catch when script is interrupted, cleanup correctly
        except KeyboardInterrupt:
            pass
        finally:
            GPIO.cleanup()

laundry = Laundry("dryer", "10")
laundry.run()
