/*	CS_IMU.h 
	Written by: Charlie Shin
	Initial Version: 2017 June 24th
	Last Edited: 2017 June 24th

	Current supporting IMU
	*L3GD20H + LSM303 Combo (L3GD20H is gyro, LSM303 is Accel+Mag combo)

	Complying with C89 standard
 */

#include <Arduino.h>

#include <CS_Sensors.h>

byte gyroAddr, gyroDevn, gyroIdcl; /* To store gyroscope register address */

/* Initializes sensor by checking its spec */
void initSensor()
{
	Wire.begin(); /* Start I2C Communication */
	
	getGyro(&gyroAddr, &gyroIdcl, &gyroDevn);
}

void readSensor(long* timestamp, float (*data)[3])
{
	/* Timestamp */
	*timestamp = millis();
	readGyro(&gyroDevn, &gyroAddr, data[0]); /* Gyroscope */
	/* Accelerometer */
	/* Magnetometer */
}
