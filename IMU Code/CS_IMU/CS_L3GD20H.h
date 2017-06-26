/*
	CS_L3GD20H.h
	Written by: Charlie Shin
	Initial Version: 2017 June 24th
	Last Edited: 2017 June 24th

	L3GD20H Sensor

	Complying with C89 standard
*/

typedef struct
{
	byte ctrl_reg1	=	0x20;
	byte ctrl_reg2	=	0x21;
	byte ctrl_reg3	=	0x22;
	byte ctrl_reg4	=	0x23;
	byte ctrl_reg5	=	0x24;
	
	byte range_250	=	0x00;
	byte range_500	=	0x10;
	byte range_2000	=	0x20;
	
	byte out_x_l	=	0x28;
	byte out_x_h	=	0x29;
	byte out_y_l	=	0x2A;
	byte out_y_h	=	0x2B;
	byte out_z_l	=	0x2C;
	byte out_z_h	=	0x2D;
	
	float dps_250	=	0.00875F;
	float dps_500	=	0.0175F;
	float dps_2000	=	0.070F;
} L3GD20H;

L3GD20H l3gd20h;
