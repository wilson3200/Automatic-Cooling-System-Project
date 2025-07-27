import time
import os


# Temperature Sensor
from w1thermsensor import W1ThermSensor
# device_file = '/sys/bus/w1/devices/28-000000bef333/w1_slave'


# Sensor Mods
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')


# MAX 7219
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from PIL import ImageFont


# Kasa Smart Plug
import asyncio
from kasa import SmartPlug
from kasa.iot import IotPlug


# LED Display Setup
serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=180, rotate=1)
font = ImageFont.load_default()


# Set sensor
sensor = W1ThermSensor()


# Async function to control the smart plug based on temperature
async def main(temperature):
   plug = IotPlug("192.168.1.5")
   await plug.update()

    # Temperature values represented in degrees Celsius here
   if temperature > 22:
       if not plug.is_on:
           await plug.turn_on()
       else:
           print('temp is hot, plug is on')
   elif temperature < 20.5:
       if plug.is_on:
           await plug.turn_off()
       else:
           print('temp is cold, plug is off')
   else:
       print("allowing room to heat/cool")
   time.sleep(1)


# Main loop: read temp, display it, and control the plug
while True:
   temperature = sensor.get_temperature()
   print(f"Temperature: {temperature:.2f}")
   # Convert to Fahrenheit if desired:
   # temperature_f = (temperature * (9/5)) + 32
   text = str(f"{temperature:.2f}")


   with canvas(device) as draw:
       for i, char in enumerate(text):
           y = i * 8 - 1
           draw.text((i, y), char, font=font, fill="white")


   if __name__ == "__main__":
       asyncio.run(main(temperature))
