# Arduino Sketch Code for IMU
--- 
* About
  * This code is used with L3GD20H + LSM303 Combination;  
    L3GD20H is the gyroscope module, while LSM303 has accelerometer and magnetometer(compass) in one.
  * Sample code has multiple libraries mixed up, which I will be modifying to merge all into one library.
* Sample Code
  * Sample code includes how to call library functions mostly, showing how to display three basic readings
    * Roll
    * Pitch
    * Yaw
* To Use
  * Connect +5V to VIN pin
  * Connect GND to GND pin
  * Connect SDA to SDA pin (If using Arduino UNO, connect to A4)
  * Connect SCL to SCL pin (If using Arduino UNO, connect to A5)
  * Add 10k resistor from +5V to SDA and SCL to add pull-up resistor
  * Make sure to move library files into Arduino IDE's libraries folder

* Maintainers
  * Charlie (Main)

---
Version History

* 1.0

> Initial version, no files added at this point  
> +Added README.md
