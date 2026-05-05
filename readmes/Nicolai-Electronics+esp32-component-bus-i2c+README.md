# ESP32 component: I2C bus management

A simple ESP-IDF component that makes working with I2C easier by abstracting away the I2C bus transaction structures for common I2C operations.

## Functions

To initialize an I2C master interface you can call:

```esp_err_t start_i2c(int bus, int pin_sda, int pin_scl, int clk_speed, bool pullup_sda, bool pullup_scl) ```

Arguments:
* bus: 0 for I2C0 controller, 1 for I2C1 controller
* pin_sda: GPIO pin number to use for data
* pin_scl: GPIO pin number to use for clock
* clk_speed: clock speed of the I2C bus in Hertz
* pullup_sda: enable internal weak pull-up on the data pin
* pullup_scl: enable internal weak pull-up on the clock pin

## Example
```
esp_err_t res = start_i2c(0, 26, 27, 4000, false, false);
```

Starts I2C bus 0 on pins 26 (sda) and 27 (scl) at 4kHz speed without using the internal pullups of the ESP32.
