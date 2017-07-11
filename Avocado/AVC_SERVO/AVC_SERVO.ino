/* Avcodado Arduino Controller */
/* Upload this sketch to Arduino platform, then connect the Arduino to RPi */

/* Headers */
#include <Servo.h>

/* Variables */
int angle = 0;
int servoPin = 9;
int angle_amt = 1;
int del = 0;

char serial_buffer[100];
char *token;

long lasttime = 0;

Servo servo;

void setup()
{
  Serial.begin(115200); /* Start comm */

  /* We will wait for start signal... */
  while(Serial.available() < 3);
  Serial.readBytesUntil('\n', serial_buffer, 100);

  token = strtok(serial_buffer, "\n");
  if(!strcmp(token, "avc_start")) /* If start signal was received */
  {
    Serial.print("ack\n"); /* Send acknowledge code back */
    servo.attach(servoPin); /* Attach servo to default pin */
  }
}

void loop()
{
  if(Serial.available()) /* Statement only works when RPi sent code */
  {
    Serial.readBytesUntil('\n', serial_buffer, 100); /* Read in max size of 100 */

    /* Split single-line command into code-by-code */
    /* Since delimiter is a whitespace, arduino will look through whitespaces */
    token = strtok(serial_buffer, " ");
    while(token != null)
    {
      if(!strcmp(token, "avc")) /* Proper start signal */
      {
        token = strtok(NULL, " "); /* Read next */
        if(!strcmp(token, "del")) /* If next code is delay */
        {
          token = strtok(NULL, " "); /* Read next */
          del = atoi(token); /* Convert next code to int to set delat */
        }
        if(!strcmp(token, "get")) /* RPi requesting data from Arduino */
        {
          token = strtok(NULL, " "); /* Read next */
          if(!strcmp(token, "agl")) /* Angle request code */
            getAngle(); /* Return angle */
        }
      }
      token = strtok(NULL, " "); /* Check if other command is waiting */
    }
  }

  sweep(); /* For moving servo */
}

void getAngle()
{
  Serial.print(angle + "\n");
}

void sweep()
{
  long currtime = millis();
  if((currtime - lasttime) >= del)
  {
    angle += angle_amt;
    if(angle >= 180 || angle <= 0)
      angle_amt = -angle_amt;

    servo.write(angle);
    lasttime = currtime;
  }
}

