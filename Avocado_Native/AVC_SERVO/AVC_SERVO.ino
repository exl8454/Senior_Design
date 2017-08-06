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
#if !DEBUG  
  Serial.println("ack"); /* Send acknowledge code back */
  startSequence();
#endif
}

void loop()
{
#if !DEBUG
  readPot();
  sendData();
  processData();
#else
  float sampled = readPot();
  Serial.print((int)sampled);
  Serial.print(" ");
  Serial.println(sampled);
#endif
}

