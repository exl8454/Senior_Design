/* Avcodado Arduino Controller */
/* Upload this sketch to Arduino platform, then connect the Arduino to RPi */
/* CURRENT TODO */
/* MOVE ALL THAT NESTED IF STATEMENT INTO HEADER FILE FOR CLEANER LOOK */

/* Headers */
#include <Servo.h>

/* Defines */
#define ERR_SERVO_NO_MATCH "err 000"
#define ERR_SERVO_RUNNING "err 001"

/* Variables */
int angle = 0; /* Actual angle */
int center = 90; /* Center position of servo */
int servoPin = 9; /* Pin attached for servo */
int angle_amt = 1; /* Angle amount */
int del = 50; /* Delay inbetween servo turn */

int offset = 90; /* Potentiometer's ACTUAL center */
int hi = 180; /* High side of potentiometer */
int lo = 0; /* Low side of potentiometer */

char serial_buffer[100];
char *token;
char *delim = " \r\n\0";

long lasttime = 0;

Servo servo;

int potPin = 0;

bool isRunning = false;
bool stream = false;

void setup()
{
  Serial.begin(115200); /* Start comm */

  /* We will wait for start signal... */
  while(Serial.available() < 1);
  Serial.readBytesUntil('\n', serial_buffer, 100);

  token = strtok(serial_buffer, delim);
  if(!strcmp(token, "avc_start")) /* If start signal was received */
  {
    servo.attach(servoPin); /* Attach servo to default pin */
    if(test()) /* Test servo */
    {
      Serial.println("ack"); /* Send acknowledge code back */
      calibrate();
      toCenter();
      isRunning = false;
    }
    else
      Serial.println(ERR_SERVO_NO_MATCH); /* Send error code back if error found */
  }
}

void loop()
{
  long currtime = millis();
  if((currtime - lasttime) >= del)
  {
    if(isRunning)
      sweep();
    if(stream)
    {
      Serial.print(readAngle()); Serial.print(" ");
      Serial.print(readRawAngle()); Serial.print(" ");
      Serial.print(readPot()); Serial.println(" ack");
    }
    lasttime = currtime;
  }
    
  if(Serial.available()) /* Statement only works when RPi sent code */
  {
    Serial.readBytesUntil('\n', serial_buffer, 100); /* Read in max size of 100 */

    /* Split single-line command into code-by-code */
    /* Since delimiter is a whitespace, arduino will look through whitespaces */
    token = strtok(serial_buffer, delim);
    while(token != NULL)
    {
      if(!strcmp(token, "avc")) /* Proper start signal */
      {
        token = strtok(NULL, delim); /* Read next */
        if(!strcmp(token, "srt")) /* Start */
        {
          token = strtok(NULL, delim);
          if(!strcmp(token, "str")) /* Start stream mode*/
          {
            stream = true;
          }
        }
        else if(!strcmp(token, "stp")) /* Stop */
        {
          token = strtok(NULL, delim);
          if(!strcmp(token, "str")) /* Stop stream mode */
          {
            stream = false;
            Serial.println("ack");
          }
          else
          {
            isRunning = false;
            Serial.println("ack");
          }
        }
        else if(!strcmp(token, "ctr")) /* Move to center */
        {
          isRunning = false;
          toCenter();
          Serial.println("ack");
        }
        else if(!strcmp(token, "swp")) /* Start sweeping */
        {
          angle_amt = 1; /* Reset direction */
          isRunning = true;
          Serial.println("ack");
        }
        else if(!strcmp(token, "gto")) /* Goto angle */
        {
          token = strtok(NULL, delim);
          isRunning = false;
          toAngle(atoi(token));
          Serial.print(angle);
          Serial.println(" ack");
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
          if(!strcmp(token, "ctr")) /* Manual setting for center */
          {
            if(!isRunning)
            {
              setCenter();
            }
            else
            {
              Serial.println(ERR_SERVO_RUNNING);
            }
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
          else if(!strcmp(token, "agr")) /* Raw angle request code */
            getRawAngle();
          else if(!strcmp(token, "pot")) /* Get potentiometer */
            getPot();
          else
          {
            Serial.print(readAngle()); Serial.print(" ");
            Serial.print(readRawAngle()); Serial.print(" ");
            Serial.print(readPot()); Serial.println(" ack");
          }
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
  if(angle == -1)
    angle = 0;
  if(angle == 181)
    angle = 180;

  servo.write(angle);
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
*  Arduino reads potentiometer value to set center.
 */
void setCenter()
{
  center = (int) readPot();
  Serial.print(center);
  Serial.println(" ack");
}

/* Returns current angle of servo
*  Note that servo value is not directly applied,
 * which means value from this function may not
*  be actual value of servo angle.
 */
void getAngle()
{
  Serial.print(angle);
  Serial.println(" ack");
}

/* Returns actual angle reading from servo.
*/
void getRawAngle()
{
  Serial.print((int)servo.read());
  Serial.println(" ack");
}

/* Returns attached potentiometer's reading
 */
void getPot()
{
  int analog = analogRead(0);
  float angle = ((float) analog / 1023.0f) * 340.0f;
  
  Serial.print(angle);
  Serial.println(" ack");
}

/* Reads potentiometer, but does not send through
*  Serial port.
 */
float readPot()
{
  int analog = analogRead(0);
  float angle = ((float) analog / 1023.0f) * 340.0f;

  return angle;
}

/* Reads servo angle, but does not send through
*  Serial port.
 */
int readRawAngle()
{
  return (int) servo.read();
}

/* Reads current angle setting, but does not send
*  through Serial port.
 */
int readAngle()
{
  return angle;
}

/* Tests servo.
*  Servo moves from 0 to 180. While servo is moving,
 * Arduino will get servo angle value to check if given
*  angle value equals to received angle value.
 * Note that this function does not check integration
*  between servo and potentiometer.
 * Use calibrate() function for servo-potentiometer
*  calibration.
 */
bool test()
{
  for(angle = 0; angle <= 180; angle++)
  {
    servo.write(angle);
    int _angle;
    delay(10);
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }
  for(angle = 180; angle >= 0; angle--)
  {
    servo.write(angle);
    int _angle;
    delay(10);
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }

  return true;
}

/* Calibrates servo with potentiometer.
*  Standard servo will rotate to maximum and
 * minimum bound and checks with potentiometer.
*  Potentiometer angle then be off-set with
 * measured value.
*  Note that offset value is floored to nearest
 * integer, so measurement error may happen.
*/
void calibrate()
{
  /* Rotate servo to 90 */
  servo.write(90);
  /* Settle down before calibration */
  delay(1000);
  
  /* Rotate servo to 0 */
  servo.write(0);
  /* Wait for some milli to settle down */
  delay(1000);
  /* Read pot and set low side */
  float _hi = readPot();

  delay(1000);
  
  /* Rotate servo to 180 */
  servo.write(180);
  /* Wait for some milli to settle down */
  delay(1000);
  /* Read pot and set high side */
  float _lo = readPot();

  delay(1000);
  
  /* Calculate mid-point and save as offset value */
  hi = (int) _hi;
  lo = (int) _lo;
  float _offset = ((hi + lo) / 2);
  offset = (int) _offset;
  Serial.print(hi); Serial.print(" ");
  Serial.print(offset); Serial.print(" ");
  Serial.print(lo); Serial.print(" ");
  Serial.println("ack");
}

