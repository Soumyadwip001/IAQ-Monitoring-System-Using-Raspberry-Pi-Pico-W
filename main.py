from machine import Pin, ADC, I2C
from time import sleep
import dht
import ssd1306

# OLED I2C
i2c = I2C(0, scl=Pin(1), sda=Pin(0))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# Sensors
dht_sensor = dht.DHT22(Pin(15))        # DHT22 on GPIO 15
mq2 = ADC(Pin(26))                     # MQ-2 on ADC0 (GPIO 26)
dust_sensor = ADC(Pin(27))             # GP2Y1010AU0F on ADC1 (GPIO 27)
dust_led = Pin(14, Pin.OUT)            # IR LED trigger for GP2Y on GPIO 14

def read_dht22():
    try:
        dht_sensor.measure()
        return dht_sensor.temperature(), dht_sensor.humidity()
    except:
        return None, None

def read_mq2():
    raw = mq2.read_u16()
    return round((raw / 65535.0) * 3.3, 2)  # Voltage

def read_dust():
    # Pulse the IR LED for measurement
    dust_led.value(0)
    sleep(0.00028)
    value = dust_sensor.read_u16()
    sleep(0.00004)
    dust_led.value(1)
    return round((value / 65535.0) * 3.3, 2)

while True:
    temp, hum = read_dht22()
    gas = read_mq2()
    dust = read_dust()

    oled.fill(0)
    oled.text("IAQ Monitor", 20, 0)
    
    if temp is not None:
        oled.text(f"T:{temp}C H:{hum}%", 0, 16)
    else:
        oled.text("DHT Error", 0, 16)
        
    oled.text(f"Gas: {gas}V", 0, 32)
    oled.text(f"Dust: {dust}V", 0, 48)

    oled.show()
    sleep(2)
