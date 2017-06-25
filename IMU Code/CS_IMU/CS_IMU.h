/*	CS_IMU.h 
	Written by: Charlie Shin
	Initial Version: 2017 June 24th
	Last Edited: 2017 June 24th

	Current supporting IMU
	*L3GD20H + LSM303 Combo (L3GD20H is gyro, LSM303 is Accel+Mag combo)

	Complying with C89 standard
 */

#include <Arduino.h>
#include <Wire.h>

#include <CS_L3GD20H.h>

#define DPS_TO_RAD 0.017453293f

byte gyroscope = -1; /* To store gyroscope register address */

void readByte(byte* value, byte addr, byte reg)
{
	Wire.beginTransmission(addr);
	Wire.write(reg);
	Wire.endTransmission();

	Wire.requestFrom((byte) addr, (byte) 1);
	while (!Wire.available());

	*value = Wire.read();
	Wire.endTransmission();
}

void writeByte(byte addr, byte reg, byte value)
{
	Wire.beginTransmission(addr);
	Wire.write((uint8_t)reg); Wire.write((uint8_t)value);
	Wire.endTransmission();
}

/* Initializes sensor by checking its spec */
void initSensor()
{
	Wire.begin(); /* Start I2C Communication */

	/* First we need to see which sensors we are using */
	/* Starting with Gyroscope */
	byte gyrodevice = -1;
	readByte(&gyrodevice, L3GD20H_ADDR, L3GD20H_WAI);
	if (gyrodevice == L3GD20H_ID) /* If device ID is same as L3GD20H gyro sensor */
	{
		Serial.print("Gyroscope: L3GD20H("); Serial.print(gyrodevice, HEX); Serial.println(")");
		gyroscope = L3GD20H_ADDR;
		writeByte(gyroscope, L3GD20H_CTRL_REG1, 0x00);
		writeByte(gyroscope, L3GD20H_CTRL_REG1, 0x0F);

		writeByte(gyroscope, L3GD20H_CTRL_REG4, L3GD20H_RANGE_2000); /* Going to have default rage of 2000DPS*/
	}
	else
		gyroscope = -1;
}

void readSensor(long* timestamp, float* gx, float* gy, float* gz)
{
	/* Timestamp */
	*timestamp = millis();
	/* Gyroscope First */
	uint8_t xl, xh, yl, yh, zl, zh;

	/* Reading data from sensor */
	readByte(&xl, gyroscope, L3GD20H_OUT_X_L); readByte(&xh, gyroscope, L3GD20H_OUT_X_H);
	readByte(&yl, gyroscope, L3GD20H_OUT_Y_L); readByte(&yh, gyroscope, L3GD20H_OUT_Y_H);
	readByte(&zl, gyroscope, L3GD20H_OUT_Z_L); readByte(&zh, gyroscope, L3GD20H_OUT_Z_H);

	/* This is raw data, in TWO'S COMPLEMENT! */
	*gx = (int16_t)(xl | (xh << 8));
	*gy = (int16_t)(yl | (yh << 8));
	*gz = (int16_t)(zl | (zh << 8));

	/* Converting into DPS with conversion */
	/* Skipping range check (default is 2000DPS)*/
	*gx *= L3GD20H_2000DPS;
	*gy *= L3GD20H_2000DPS;
	*gz *= L3GD20H_2000DPS;

	/* Convert to radians per second*/
	*gx *= DPS_TO_RAD;
	*gy *= DPS_TO_RAD;
	*gz *= DPS_TO_RAD;

	/* End of gyroscope */
}
