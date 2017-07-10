/* Avcodado Arduino Controller */

#include <Servo.h>

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
  Serial.begin(115200);

  while(Serial.available() < 3);

  Serial.readBytesUntil('\n', serial_buffer, 100);

  token = strtok(serial_buffer, "\n");
  if(!strcmp(token, "avc_start"))
  {
    Serial.print("ack\n");
    servo.attach(servoPin);
  }
}

void loop()
{
  if(Serial.available())
  {
    Serial.readBytesUntil('\n', serial_buffer, 100);

    token = strtok(serial_buffer, " ");
    if(!strcmp(token, "avc"))
    {
      token = strtok(NULL, " ");
      if(!strcmp(token, "del"))
      {
        token = strtok(NULL, " ");
        del = atoi(token);
      }
      if(!strcmp(token, "get"))
      {
        token = strtok(NULL, " ");
        if(!strcmp(token, "agl"))
          getAngle();
      }
    }
    while(token != NULL)
      token = strtok(NULL, " ");
  }

  sweep();
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

