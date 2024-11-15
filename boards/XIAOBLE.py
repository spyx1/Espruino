#!/bin/false
# This file is part of Espruino, a JavaScript interpreter for Microcontrollers
#
# Copyright (C) 2013 Gordon Williams <gw@pur3.co.uk>
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# ----------------------------------------------------------------------------------------
# This file contains information for a specific board - the available pins, and where LEDs,
# Buttons, and other in-built peripherals are. It is used to build documentation as well
# as various source and header files for Espruino.
# ----------------------------------------------------------------------------------------
"""
source ./scripts/provision.sh ALL
rm bin/*.hex
make clean && BOARD=XIAOBLE RELEASE=1 make
uf2conv.py ./bin/*.hex -c -f 0xADA52840
mv flash.uf2 ~/Desktop/
"""
import pinutils
info = {
    "name": "Seeed Xiao BLE",
    "link": ["https://www.seeedstudio.com/Seeed-XIAO-BLE-nRF52840-p-5201.html"],
    "default_console": "EV_USBSERIAL",
    # 'default_console' : "EV_SERIAL1",
    # 'default_console_tx' : "D6",
    # 'default_console_rx' : "D7",
    # 'default_console_baudrate' : "9600",
    "variables": 14000,  # How many variables are allocated for Espruino to use. RAM will be overflowed if this number is too high and code won't compile.
    # 'bootloader' : 1,
    "binary_name": "espruino_%v_xiaoble.hex",
    "build": {
        "optimizeflags": "-Os",
        "libraries": [
            "BLUETOOTH",
            #  'NET',
            "GRAPHICS",
            # 'NFC',
            "NEOPIXEL",
            "JIT",
        ],
        "makefile": [
            "DEFINES += -DESPR_LSE_ENABLE",  # Ensure low speed external osc enabled
            "DEFINES += -DCONFIG_GPIO_AS_PINRESET",  # Allow the reset pin to work
            "DEFINES += -DNRF_USB=1 -DUSB",
            "DEFINES += -DNEOPIXEL_SCK_PIN=33 -DNEOPIXEL_LRCK_PIN=34",  # nRF52840 needs LRCK pin defined for neopixel
            "DEFINES += -DBLUETOOTH_NAME_PREFIX='\"XIAOBLE\"'",
            "DEFINES += -DSPIFLASH_READ2X",  # Read SPI flash at 2x speed using MISO and MOSI for IO
            "DEFINES += -DESPR_UNICODE_SUPPORT=1",
            "DEFINES += -DNRF_SDH_BLE_GATT_MAX_MTU_SIZE=131",  # 23+x*27 rule as per https://devzone.nordicsemi.com/f/nordic-q-a/44825/ios-mtu-size-why-only-185-bytes
            # 'DEFINES += -DPIN_NAMES_DIRECT=1', # Package skips out some pins, so we can't assume each port starts from 0
            "LDFLAGS += -Xlinker --defsym=LD_APP_RAM_BASE=0x2ec0",  # set RAM base to match MTU
            "NRF_SDK15=1",
        ],
    },
}
chip = {
    "part": "NRF52840",
    "family": "NRF52",
    "package": "AQFN73",
    "ram": 256,
    "flash": 1024,
    "speed": 64,
    "usart": 1,
    "spi": 1,
    "i2c": 2,
    "adc": 1,
    "dac": 0,
    "saved_code": {
        "address": ((0xF4 - 2 - 96) * 4096),  # Bootloader at 0xF4000
        "page_size": 4096,
        "pages": 96,
        "flash_available": 1024
        - (
            (0x26 + 0x20 + 2 + 96) * 4
        ),  # Softdevice 140 uses 38 pages of flash, bootloader 8, FS 2, code 10. Each page is 4 kb.
    },
}
devices = {
    "LED1": {"pin": "D26"},  # Pin negated in software
    "LED2": {"pin": "D30"},  # Pin negated in software
    "LED3": {"pin": "D6"},  # Pin negated in software
    # Pin D33 and D34 are used for clock when driving neopixels - as not specifying a pin seems to break things
    "BAT": {
        "pin_charging": "D17",  # active low
        "pin_voltage": "D31",
    },
    "NFC": {"pin_a": "D9", "pin_b": "D10"},
    "SPIFLASH": {
        "pin_cs": "D25",
        "pin_sck": "D21",
        "pin_mosi": "D20",
        "pin_miso": "D24",
        "pin_wp": "D22",
        "pin_rst": "D23",
        "size": 4096 * 512,  # 2MB
        "memmap_base": 0x60000000,  # map into the address space (in software)
    },
}
# left-right, or top-bottom order
board = {}
# schematic at https://files.seeedstudio.com/wiki/XIAO-BLE/Seeed-Studio-XIAO-nRF52840-Sense-v1.1.pdf
# pinout sheet https://files.seeedstudio.com/wiki/XIAO-BLE/XIAO-nRF52840-pinout_sheet.xlsx
# see also https://github.com/Seeed-Studio/Adafruit_nRF52_Arduino/blob/master/variants/Seeed_XIAO_nRF52840/variant.h
def get_pins():
    pins = pinutils.generate_pins(0, 47)  # 48 General Purpose I/O Pins.
    pinutils.findpin(pins, "PD2", True)["functions"]["ADC1_IN0"] = 0
    pinutils.findpin(pins, "PD3", True)["functions"]["ADC1_IN1"] = 0
    pinutils.findpin(pins, "PD4", True)["functions"]["ADC1_IN2"] = 0
    pinutils.findpin(pins, "PD5", True)["functions"]["ADC1_IN3"] = 0
    pinutils.findpin(pins, "PD9", True)["functions"]["NFC1"] = 0
    pinutils.findpin(pins, "PD10", True)["functions"]["NFC2"] = 0
    pinutils.findpin(pins, "PD17", True)["functions"]["NEGATED"] = 0
    pinutils.findpin(pins, "PD26", True)["functions"]["NEGATED"]=0;
    pinutils.findpin(pins, "PD28", True)["functions"]["ADC1_IN4"] = 0
    pinutils.findpin(pins, "PD29", True)["functions"]["ADC1_IN5"] = 0
    pinutils.findpin(pins, "PD31", True)["functions"]["ADC1_IN7"] = 0
    # D13 PIN_CHARGING_CURRENT
    # battery charging current see https://wiki.seeedstudio.com/XIAO_BLE/#battery-charging-current
    # HIGH: 100mA, LOW: 50mA
    # D14 VBAT_ENABLE
    # enable battery voltage reading by digitalWrite(D14, false)
    # D17 CHG
    # get charge state via digitalRead(D17)
    # HIGHT: not charging, LOW: charging
    # D31 PIN_VBAT
    # everything is non-5v tolerant
    for pin in pins:
        pin["functions"]["3.3"] = 0
    return pins
