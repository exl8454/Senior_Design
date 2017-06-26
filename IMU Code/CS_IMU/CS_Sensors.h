/*
	CS_Sensors.h
	Written By Charlie Shin
	
	Initial Release: 2017 June 26th
	Last Edited: 2017 June 26th
	
	Purpose of this code is to have set of addresses for Who Am I from different sensors
*/

#include <CS_I2C.h>

#include <CS_L3GD20H.h>

#define DPS_TO_RAD 0.017453293f

typedef struct Sensors
{
	/* Gyroscopes */
	/* L3GD20H Sensor */
	byte L3GD20H_ADDR	=	0x6B;
	byte L3GD20H_DEVN	=	0xD7;
	byte L3GD20H_IDCL	=	0x0F;
} cs_sensors;

cs_sensors sensors;

/*
	Returns Gyroscope device address, along with call ID 
	If no gyroscope is found, returns -1 for all three parameters
	This function assumes you already called Wire.begin()!
*/
void getGyro(byte *gyroAddr, byte *gyroIdcl, byte *gyroDevn)
{
	/* L3GD20H */
	readByte(*gyroAddr, sensors.L3GD20H_ADDR, sensors.L3GD20H_IDCL);
	if(*gyroAddr == sensors.L3GD20H_DEVN)
	{
		*gyroAddr = sensors.L3GD20H_ADDR;
		*gyroIdcl = sensors.L3GD20H_IDCL;
		*gyroDevn = sensors.L3GD20H_DEVN;
		
		writeByte(*gyroAddr, l3gd20h.ctrl_reg1, 0x00);
		writeByte(*gyroAddr, l3gd20h.ctrl_reg1, 0x0F);

		/* Going to have default rage of 2000DPS*/
		writeByte(*gyroAddr, l3gd20h.ctrl_reg4, l3gd20h.range_2000);
	}
}

/*
	Reads gyro added previously by getGyro function
*/
void readGyro(byte *gyroDevn, byte *gyroAddr, float *g)
{
	if(*gyroDevn == sensors.L3GD20H_DEVN) /* L3GD20H Gyro*/
	{
		uint8_t data[6];
		/* Reading 6 bytes */
		readMultiple(data, gyroAddr, l3gd20h.out_x_l, 0x80, 6);
		
		int16_t x = (int16_t)(data[0] | data[1] << 8);
		int16_t y = (int16_t)(data[2] | data[2] << 8);
		int16_t z = (int16_t)(data[4] | data[3] << 8);

		g[0] = (float)x * l3gd20h.dps_2000;
		g[1] = (float)y * l3gd20h.dps_2000;
		g[2] = (float)z * l3gd20h.dps_2000;

		g[0] *= DPS_TO_RAD;
		g[1] *= DPS_TO_RAD;
		g[2] *= DPS_TO_RAD;
	}
}
