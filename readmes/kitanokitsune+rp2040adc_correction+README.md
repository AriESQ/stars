# RP2040/RP2350 A/D non-linearity correction

The purpose of this project is to improve the non-linearity of the ADC in the RP2040 microcontroller, as described by the errata RP2040-E11, using software.  
Furthermore, the project will also cover RP2350.

***Note*** *Lost information cannot be restored. Only improving linearity is possible.*


## RP2040/RP2350 ADC non-linearity Measurement
Data are measured by [*measure.py*](./testboard/measure.py) with [this firmware](./testboard/picofirmware) and the circuit below. They are in [*testboard*](./testboard) folder. Board design files are [here](./testboard/designfiles).

[![ckt](./testboard/adc_test_board_schematic.png)](./testboard/adc_test_board_schematic.pdf)


The following graphs show ADC errors on actual Raspberry Pi Pico/Pico W/Pico 2/Pico 2W devices which I possess.

Y-axis is ADC error and X-axis is ADC readout (***not ADC input***).
## RP2040 ADC non-linearity
The raw data are [here](./actual_adc_data/data_rp2040/).  
[<img src="./actual_adc_data/data_rp2040/rp2040adc1.png" width="300">](./actual_adc_data/data_rp2040/rp2040adc1.png)
[<img src="./actual_adc_data/data_rp2040/rp2040adc2.png" width="300">](./actual_adc_data/data_rp2040/rp2040adc2.png)
[<img src="./actual_adc_data/data_rp2040/rp2040adc3.png" width="300">](./actual_adc_data/data_rp2040/rp2040adc3.png)
[<img src="./actual_adc_data/data_rp2040/rp2040adc4.png" width="300">](./actual_adc_data/data_rp2040/rp2040adc4.png)
[<img src="./actual_adc_data/data_rp2040/rp2040adc5.png" width="300">](./actual_adc_data/data_rp2040/rp2040adc5.png)  
The enormous discontinuities are observed at 512, 1536, 2560 and 3584.

## RP2350 ADC non-linearity
The raw data are [here](./actual_adc_data/data_rp2350/).  
[<img src="./actual_adc_data/data_rp2350/rp2350adc1.png" width="300">](./actual_adc_data/data_rp2350/rp2350adc1.png)
[<img src="./actual_adc_data/data_rp2350/rp2350adc2.png" width="300">](./actual_adc_data/data_rp2350/rp2350adc2.png)
[<img src="./actual_adc_data/data_rp2350/rp2350adc3.png" width="300">](./actual_adc_data/data_rp2350/rp2350adc3.png)
[<img src="./actual_adc_data/data_rp2350/rp2350adc4.png" width="300">](./actual_adc_data/data_rp2350/rp2350adc4.png)
[<img src="./actual_adc_data/data_rp2350/rp2350adc5.png" width="300">](./actual_adc_data/data_rp2350/rp2350adc5.png)  
RP2350 is improved compared to RP2040, but there's still some non-linearity remaining.


# General-Purpose Correction Code
By averaging the errors of the above five rp2040 devices and five rp2350 devices, I obtained the following code.

## RP2040 GENERAL-PURPOSE CODE
```Python
def rp2040adc_correction(d):
    '''
    rp2040 ADC Correction
      d     : 12 bit ADC readout (0~4095)
      return: corrected ADC value
    '''
    if d >= 4081:
        y = 4095
    elif d >= 3711:
        y = d + 14
    elif d >= 3584:
        y = d + 15
    elif d == 3583:
        y = 3583 + 10
    elif d >= 3455:
        y = d + 5
    elif d >= 2943:
        y = d + 6
    elif d >= 2560:
        y = d + 7
    elif d == 2559:
        y = 2559 + 3
    elif d >= 2431:
        y = d - 2
    elif d >= 2048:
        y = d - 1
    elif d == 2047:
        y = 2047 + 0
    elif d >= 1664:
        y = d + 1
    elif d >= 1536:
        y = d + 2
    elif d == 1535:
        y = 1535 - 3
    elif d >= 1407:
        y = d - 7
    elif d >= 895:
        y = d - 6
    elif d >= 512:
        y = d - 5
    elif d == 511:
        y = 511 - 10
    elif d >= 16:
        y = d - 15
    else:
        y = 0

    return y
```


## RP2350 GENERAL-PURPOSE CODE
```Python
def rp2350adc_correction(d):
    '''
    rp2350 ADC Correction
      d     : 12 bit ADC readout (0~4095)
      return: corrected ADC value
    '''
    if d >= 4079:
        y = 4095
    elif d >= 3905:
        y = d + 16
    elif d >= 3839:
        y = d + 15
    elif d >= 3489:
        y = d + 14
    elif d >= 3327:
        y = d + 13
    elif d >= 3105:
        y = d + 12
    elif d >= 2816:
        y = d + 11
    elif d >= 2783:
        y = d + 10
    elif d >= 2559:
        y = d + 9
    elif d >= 2304:
        y = d + 10
    elif d >= 2144:
        y = d + 9
    elif d >= 2047:
        y = d + 8
    elif d >= 1824:
        y = d + 9
    elif d >= 1792:
        y = d + 8
    elif d >= 1535:
        y = d + 7
    elif d >= 1280:
        y = d + 8
    elif d >= 1089:
        y = d + 7
    elif d >= 833:
        y = d + 6
    elif d >= 767:
        y = d + 5
    elif d >= 576:
        y = d + 4
    elif d >= 319:
        y = d + 3
    elif d >= 255:
        y = d + 2
    elif d >= 160:
        y = d + 1
    else:
        y = d

    return y
```

## Correction result by the general-purpose code
Y-axis is ADC error and X-axis is ADC input (***not ADC readout***).
### RP2040 ADC correction result by the general-purpose code
[<img src="./images/rp2040_gc1.png" width="300">](./images/rp2040_gc1.png)
[<img src="./images/rp2040_gc2.png" width="300">](./images/rp2040_gc2.png)
[<img src="./images/rp2040_gc3.png" width="300">](./images/rp2040_gc3.png)
[<img src="./images/rp2040_gc4.png" width="300">](./images/rp2040_gc4.png)
[<img src="./images/rp2040_gc5.png" width="300">](./images/rp2040_gc5.png)  
The red line shows the error with correction, and the cyan line shows the error without correction.

### RP2350 ADC correction result by the general-purpose code
[<img src="./images/rp2350_gc1.png" width="300">](./images/rp2350_gc1.png)
[<img src="./images/rp2350_gc2.png" width="300">](./images/rp2350_gc2.png)
[<img src="./images/rp2350_gc3.png" width="300">](./images/rp2350_gc3.png)
[<img src="./images/rp2350_gc4.png" width="300">](./images/rp2350_gc4.png)
[<img src="./images/rp2350_gc5.png" width="300">](./images/rp2350_gc5.png)  
The red line shows the error with correction, and the cyan line shows the error without correction.


# Best Calibration by Individual Code
If you can use individual code for each device, that means each device has its own customized firmware, you can use the following formula that gives better correction:

`ADC_CORRECTED = ADC_READOUT + rp2040adc_err[ADC_READOUT]`

Where `rp2040adc_err[]` is the array created by [*calc_err.py*](./actual_adc_data/data_rp2040), and has error data for specific device measured by yourself using [*measure.py*](./testboard/measure.py) and the [*firmware*](./testboard/picofirmware). (Each device needs its own `rp2040adc_err[]`.)

**Individual code templates:**  
+ C/C++ template ([template_rp2040adc.h](./template_rp2040adc.h), [template_rp2350adc.h](./template_rp2350adc.h))
+ Python template ([template_rp2040adc.py](./template_rp2040adc.py), [template_rp2350adc.py](./template_rp2350adc.py))

## Embed Individual Calibration Data in the Pico's Flash ROM
You can embed the individual ADC calibration data in the last 4KB block of a flash ROM on a pico board, using [*pico_adc_chk.py*](./testboard/pico_adc_chk.py) and the [*firmware*](./testboard/picofirmware).

The embedded calibration data area can be accessed as an emulated EEPROM using [Arduino-Pico](https://github.com/earlephilhower/arduino-pico).  
Here is the example sketch of Arduino-Pico.
```cpp
#include "hardware/adc.h"
#include "EEPROM.h"

int8_t const *adc_cal_data;

void setup()
{
    EEPROM.begin(4096);       /* start emulated EEPROM */
    adc_cal_data = reinterpret_cast<int8_t const *>(EEPROM.getConstDataPtr());

    Serial.begin(9600);
    adc_init();
    adc_gpio_init(26);        /* A0 = GPIO26 */
    analogReadResolution(12); /* resolution = 12bit */
}

void loop()
{
    uint16_t n;

    n = analogRead(A0);
    Serial.println(n+adc_cal_data[n]);

    delay(100);
}
```

## Calibration result by individual code
Y-axis is ADC error and X-axis is ADC input (***not ADC readout***).
### RP2040 ADC calibration result by individual code
[<img src="./images/rp2040_ic1.png" width="300">](./images/rp2040_ic1.png)
[<img src="./images/rp2040_ic2.png" width="300">](./images/rp2040_ic2.png)
[<img src="./images/rp2040_ic3.png" width="300">](./images/rp2040_ic3.png)
[<img src="./images/rp2040_ic4.png" width="300">](./images/rp2040_ic4.png)
[<img src="./images/rp2040_ic5.png" width="300">](./images/rp2040_ic5.png)  
The red line shows the error with correction, and the cyan line shows the error without correction.

### RP2350 ADC calibration result by individual code
[<img src="./images/rp2350_ic1.png" width="300">](./images/rp2350_ic1.png)
[<img src="./images/rp2350_ic2.png" width="300">](./images/rp2350_ic2.png)
[<img src="./images/rp2350_ic3.png" width="300">](./images/rp2350_ic3.png)
[<img src="./images/rp2350_ic4.png" width="300">](./images/rp2350_ic4.png)
[<img src="./images/rp2350_ic5.png" width="300">](./images/rp2350_ic5.png)  
The red line shows the error with correction, and the cyan line shows the error without correction.
