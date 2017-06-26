/*
	CS_L3GD20H.h
	Written by: Charlie Shin
	Initial Version: 2017 June 24th
	Last Edited: 2017 June 24th

	L3GD20H Sensor

	Complying with C89 standard
*/

/* Basic definitions */
#define L3GD20H_ADDR		0x6B	/* I2C call address*/
#define L3GD20H_ID			0xD7	/* Device ID*/

/* Control Register Addresses */
#define L3GD20H_WAI			0x0F	/* Who Am I*/
#define L3GD20H_CTRL_REG1	0x20	/* Control Register 1 */
#define L3GD20H_CTRL_REG2	0x21	/* Control Register 2 */
#define L3GD20H_CTRL_REG3	0x22	/* Control Register 3 */
#define L3GD20H_CTRL_REG4	0x23	/* Control Register 4 */
#define L3GD20H_CTRL_REG5	0x24	/* Control Register 5 */

/* Setting Register Addresses */
#define L3GD20H_RANGE_250	0x00	/* Scale for 250 DPS */
#define L3GD20H_RANGE_500	0x10	/* Scale for 500 DPS */
#define L3GD20H_RANGE_2000	0x20	/* Scale for 2000 DPS */

/* Output Register Addresses */
#define L3GD20H_OUT_X_L		0x28	/* Output for X axis (low) */
#define L3GD20H_OUT_X_H		0x29	/* Output for X axis (high) */
#define L3GD20H_OUT_Y_L		0x2A	/* Output for Y axis (low) */
#define L3GD20H_OUT_Y_H		0x2B	/* Output for Y axis (high) */
#define L3GD20H_OUT_Z_L		0x2C	/* Output for Z axis (low) */
#define L3GD20H_OUT_Z_H		0x2D	/* Output for Z axis (high) */

/* Conversion Data */
#define L3GD20H_250DPS		(0.00875F)    /* Roughly 22/256 for fixed point match */
#define L3GD20H_500DPS		(0.0175F)     /* Roughly 45/256 */
#define L3GD20H_2000DPS		(0.070F)      /* Roughly 18/256 */
