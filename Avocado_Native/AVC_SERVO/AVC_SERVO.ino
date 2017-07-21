/* Avcodado Arduino Controller */
/* Upload this sketch to Arduino platform, then connect the Arduino to RPi */
/* CURRENT TODO */
/* MOVE ALL THAT NESTED IF STATEMENT INTO HEADER FILE FOR CLEANER LOOK */

/* Headers */
#include <Servo.h>

/* Variables */
int angle = 0; /* Actual angle */
int center = 90; /* Center position of servo */
int servoPin = 9; /* Pin attached for servo */
int angle_amt = 1; /* Angle amount */
int del = 50; /* Delay inbetween servo turn */

char serial_buffer[100];
char *token;
char *delim = " $\r\n\0";

long lasttime = 0;

Servo servo;

int potPin = 0;

bool isRunning = false;

void setup()
{
  Serial.begin(115200); /* Start comm */

  /* We will wait for start signal... */
  while(Serial.available() < 1);
  Serial.readBytesUntil('$', serial_buffer, 100);

  token = strtok(serial_buffer, delim);
  if(!strcmp(token, "avc_start")) /* If start signal was received */
  {
    servo.attach(servoPin); /* Attach servo to default pin */
    if(test()) /* Test servo */
    {
      Serial.println("ack"); /* Send acknowledge code back */
      isRunning = true;
    }
    else
      Serial.println("err 000"); /* Send error code back if error found */
  }
}

void loop()
{
  int potVal = analogRead(potPin); /* Read potentiometer */
  float angle = ((float) potVal / 1023.0f) * 340.0f;

  long currtime = millis();
  if((currtime - lasttime) >= del)
  {
    if(isRunning)
      sweep();
    lasttime = currtime;
  }
    
  if(Serial.available()) /* Statement only works when RPi sent code */
  {
    Serial.readBytesUntil('$', serial_buffer, 100); /* Read in max size of 100 */

    /* Split single-line command into code-by-code */
    /* Since delimiter is a whitespace, arduino will look through whitespaces */
    token = strtok(serial_buffer, delim);
    while(token != NULL)
    {
      if(!strcmp(token, "avc")) /* Proper start signal */
      {
        token = strtok(NULL, delim); /* Read next */
        if(!strcmp(token, "stp"))
        {
          isRunning = false;
          toCenter();
          Serial.println("ack");
        }
        else if(!strcmp(token, "swp"))
        {
          angle_amt = 1; /* Reset direction */
          isRunning = true;
          Serial.println("ack");
        }
        else if(!strcmp(token, "gto"))
        {
          token = strtok(NULL, delim);
          if(!strcmp(token, "ctr"))
          {
            isRunning = false;
            toCenter();
          }
          else if(!strcmp(token, "str"))
          {
            /* Start */
          }
          else if(!strcmp(token, "end"))
          {
            /* End */
          }
          else
          {
            isRunning = false;
            toAngle(atoi(token));
          }
        }
        else if(!strcmp(token, "set")) /* RPi sending config to Arduino */
        {
          token = strtok(NULL, delim); /* Read next */
          if(!strcmp(token, "del")) /* If next code is delay */
          {
            token = strtok(NULL, delim); /* Read next */
            del = atoi(token); /* Convert next code to int to set delat */
            Serial.println(del);
          }
          if(!strcmp(token, "ctr"))
          {
            setCenter();
          }
          if(!strcmp(token, "clb")) /* Calibration */
          {
             /* TODO Add Calibration function */
          }
        }
        else if(!strcmp(token, "get")) /* RPi requesting data from Arduino */
        {
          token = strtok(NULL, delim); /* Read next */
          if(!strcmp(token, "agl")) /* Angle request code */
            getAngle(); /* Return angle */
          if(!strcmp(token, "agr")) /* Raw angle request code */
            getRawAngle();
          if(!strcmp(token, "pot")) /* Get potentiometer */
            getPot(angle);
        }
      }
      token = strtok(NULL, delim);
    }
  }
}

/* Function for actual servo sweeping.
*  Function checks delay time between servo move.
 * Deflection angle can be changed from Avocado calls.
*/
void sweep()
{
  angle += angle_amt;
  if(angle > 180 || angle < 0)
    angle_amt = -angle_amt;

  servo.write(angle);
}

/* Returns current angle of servo
*  Note that servo value is not directly applied,
 * which means value from this function may not
*  be actual value of servo angle.
 */
void getAngle()
{
  Serial.println(angle);
}

/* Returns actual angle reading from servo.
*/
void getRawAngle()
{
  Serial.println((int)servo.read());
}

/* Returns attached potentiometer's reading
 */
void getPot(float angle)
{
  Serial.println(angle);
}

/* Sets servo agle to center
*  Center angle can be changed via setCenter() function.
 */
void toCenter()
{
  angle = center;
  servo.write(angle);
}

/* Moves servo to target angle
*  angle must be sent as integer
 */
void toAngle(int _angle)
{
  angle = _angle;
  servo.write(angle);
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
void setCenter()
{
  center = servo.read();
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
    delay(del);
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }
  for(angle = 180; angle >= 0; angle--)
  {
    servo.write(angle);
    int _angle;
    delay(del);
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }

  return true;
}

/* For continuous rotation servo! */

/* Calibrates servo with potentiometer
*  Use only with full-cycle servo
 */
void calibrate()
{
  
}

