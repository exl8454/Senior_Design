/* Avcodado Arduino Controller */
/* Upload this sketch to Arduino platform, then connect the Arduino to RPi */
/* CURRENT TODO */
/* MOVE ALL THAT NESTED IF STATEMENT INTO HEADER FILE FOR CLEANER LOOK */

/* Headers */
#include <Servo.h>

/* Variables */
static int angle = 0; /* Actual angle */
static int center = 90; /* Center position of servo */
static int servoPin = 9; /* Pin attached for servo */
static int angle_amt = 1; /* Angle amount */
static int del = 0; /* Delay inbetween servo turn */

static char serial_buffer[100];
static char *token;

static long lasttime = 0;

static Servo servo;

void setup()
{
  Serial.begin(115200); /* Start comm */

  /* We will wait for start signal... */
  while(Serial.available() < 3);
  Serial.readBytesUntil('\n', serial_buffer, 100);

  token = strtok(serial_buffer, "\n");
  if(!strcmp(token, "avc_start")) /* If start signal was received */
  {
    if(test()) /* Test servo */
      Serial.print("ack\n"); /* Send acknowledge code back */
    else
      Serial.print("err 000\n"); /* Send error code back if error found */
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
    while(token != NULL)
    {
      if(!strcmp(token, "avc")) /* Proper start signal */
      {
        token = strtok(NULL, " "); /* Read next */
        if(!strcmp(token, "set")) /* RPi sending config to Arduino */
        {
          token = strtok(NULL, " "); /* Read next */
          if(!strcmp(token, "del")) /* If next code is delay */
          {
            token = strtok(NULL, " "); /* Read next */
            del = atoi(token); /* Convert next code to int to set delat */
          }
          if(!strcmp(token, "ctr"))
          {
            token = strtok(NULL, " ");
            setCenter(atoi(token));
          }
        }
        if(!strcmp(token, "get")) /* RPi requesting data from Arduino */
        {
          token = strtok(NULL, " "); /* Read next */
          if(!strcmp(token, "agl")) /* Angle request code */
            getAngle(); /* Return angle */
          if(!strcmp(token, "agr")) /* Raw angle request code */
            getRawAngle();
        }
      }
      token = strtok(NULL, " "); /* Check if other command is waiting */
    }
  }

  sweep(); /* For moving servo */
}

/* Returns current angle of servo
*  Note that servo value is not directly applied,
 * which means value from this function may not
*  be actual value of servo angle.
 */
void getAngle()
{
  Serial.print(angle + "\n");
}

/* Returns actual angle reading from servo.
*/
void getRawAngle()
{
  Serial.print((int)servo.read() + "\n");
}

/* Function for actual servo sweeping.
*  Function checks delay time between servo move.
 * Deflection angle can be changed from Avocado calls.
*/
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

/* Tests servo.
*  Servo moves from 0 to 180. While servo is moving,
 * Arduino will get servo angle value to check if given
*  angle value equals received angle value.
 */
bool test()
{
  for(angle = 0; angle <= 180; angle++)
  {
    servo.write(angle);
    int _angle;
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }
  for(angle = 180; angle >= 0; angle--)
  {
    servo.write(angle);
    int _angle;
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }

  return true;
}

/* Changes pin attached to for servo.
*  Note: Do not use it unless it HAS to be used.
 * Arduino disables PWM on pin 9 and 10 if these
*  pins are used as servo attached pin. Which means
 * if any device other than servo is attached which
*  requires PWM signal will NOT work.
 * For sanity check, Arduino will first check if current
*  pin is actually attached to a servo.
 */
void changePin(int newPin)
{
  if(servo.attached())
    servo.detach();

  servoPin = newPin;
  servo.attach(servoPin);
}

/* Sets center point of Arduino
*  For later use probably.
 */
void setCenter(int _center)
{
  center = _center;
}

