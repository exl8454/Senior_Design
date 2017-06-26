/*
	CS_I2C.h
	Written By Charlie Shin
	
	Initial Release: 2017 June 26th
	Last Edited: 2017 June 26th
	
	Handles I2C from Arduino
*/

#include <Wire.h>

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

/* Only use with sensors with assert capability! */
void readMultiple(byte *value, byte addr, byte reg, byte assrt, int readSize)
{
	Wire.beginTransmission(addr);
	Wire.write(reg | assrt);
	Wire.endTransmission();
	
	Wire.requestFrom(addr, (byte) readSize);
	while(!Wire.available() >= readSize);
	
	int i;
	for(i = 0; i < readSize; i++, value++)
	{
		value = Wire.read();
	}
}
