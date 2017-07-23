/* Avcodado Arduino Controller */
/* Upload this sketch to Arduino platform, then connect the Arduino to RPi */
/* CURRENT TODO */
/* MOVE ALL THAT NESTED IF STATEMENT INTO HEADER FILE FOR CLEANER LOOK */

/* Parallax Cont. Servo 94 deg for stationary */
/* 84 and less for CW Rotation Full, 104 and more for CCW Rotation Full*/

#include "AVC_SERVO.h"

void setup()
{
  Serial.begin(115200); /* Start comm */
  Serial.println("ack"); /* Send acknowledge code back */

  startSequence();
}

void loop()
{
  sendData();
    
  processData();
}

