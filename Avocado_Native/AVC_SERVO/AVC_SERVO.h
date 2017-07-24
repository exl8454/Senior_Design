/* For Cleanup */

/* Headers */
#include <Arduino.h>
#include <Servo.h>

/* Defines */
#define ERR_SERVO_NO_MATCH "err 000"
#define ERR_SERVO_RUNNING "err 001"
#define DEBUG true

/* Variables */
int angle = 0; /* Actual angle */
int center = 90; /* Center position of servo */
int servoPin = 9; /* Pin attached for servo */
int angle_amt = 1; /* Angle amount */
int del = 50; /* Delay inbetween servo turn */

int offset = 90; /* Potentiometer's ACTUAL center */
int hi = 180; /* High side of potentiometer */
int lo = 0; /* Low side of potentiometer */

float LPF_Beta = 0.25; /* For Low-Pass Filter */
float output = 0;
float _output = 0;

char serial_buffer[100];
char *token;
char *delim = " \r\n\0";

long lasttime = 0;

Servo servo;

int potPin = 0;

bool isRunning = false;
bool stream = false;

/* Function Definition */
void startSequence();
void sendData();
void processData();
void sweep();
void toCenter();
void toAngle(int _angle);
void sweepTo(int _angle, int interval);
void sweepPot(int pot_target, int interval);
void changePin(int newPin);
void setCenter();
void getAngle();
void getRawAngle();
void getPot();
float readPot();
int readRawAngle();
int readAngle();
bool test();
void calibrate_a();
void calibrate_b();
void calibrate_c();
void calibrate_d();
void smoothPot();

void startSequence()
{
  /* We will wait for start signal... */
  while(Serial.available() < 1);
  Serial.readBytesUntil('\n', serial_buffer, 100);

  token = strtok(serial_buffer, delim);
  if(!strcmp(token, "avc_start")) /* If start signal was received */
  {
    servo.attach(servoPin); /* Attach servo to default pin */
    angle = servo.read();
    if(test()) /* Test servo */
    {
      sweepTo(90, 50);
      isRunning = false;
      Serial.println("ack"); /* Send acknowledge code back */
    }
    else
      Serial.println(ERR_SERVO_NO_MATCH); /* Send error code back if error found */
  }
}

void sendData()
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
}

void processData()
{
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
        else if(!strcmp(token, "clb")) /* Calibration */
        {
          if(!isRunning)
          {
            token = strtok(NULL, delim);
            if(!strcmp(token, "tpa"))
              calibrate_a();
            else if(!strcmp(token, "tpb"))
              calibrate_b();
            else if(!strcmp(token, "tpc"))
              calibrate_c();
            else if(!strcmp(token, "tpd"))
              calibrate_d();
            else calibrate_a();
          }
          else
            Serial.println(ERR_SERVO_RUNNING);
        }
        else if(!strcmp(token, "sdn")) /* Shutdown Sequence */
        {
          sweepTo(90, 50);
          while(Serial.available())
            Serial.read();

          servo.detach();
          Serial.end();
        }
        else if(!strcmp(token, "set")) /* RPi sending config to Arduino */
        {
          token = strtok(NULL, delim); /* Read next */
          if(!strcmp(token, "del")) /* If next code is delay */
          {
            token = strtok(NULL, delim); /* Read next */
            del = atoi(token); /* Convert next code to int to set delat */
            Serial.print(del);
            Serial.println(" ack");
          }
          if(!strcmp(token, "ctr")) /* Manual setting for center */
          {
            if(!isRunning)
              setCenter();
            else
              Serial.println(ERR_SERVO_RUNNING);
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
  if(angle >= 180 || angle <= 0)
    angle_amt = -angle_amt;
  if(angle == -1)
    angle = 0;
  if(angle == 181)
    angle = 180;

  servo.write(angle);
  readPot();
}

/* Sets servo agle to center
*  Center angle can be changed via setCenter() function.
 */
void toCenter()
{
  sweepTo(center, del);
}

/* Moves servo to target angle
*  angle must be sent as integer
 */
void toAngle(int _angle)
{
  sweepTo(_angle, del);
}

/* Moves servo to target angle using sweep method.
*  Use this function to carefully move servo.
 */
void sweepTo(int _angle, int interval)
{
  if(angle > _angle)
    angle_amt = -1;
  else if(angle < _angle)
    angle_amt = 1;

  while(angle != _angle)
  {
    angle += angle_amt;
    servo.write(angle);
    readPot();
    delay(interval);
  }
}

/* Moves servo to target potentiometer angle.
 *  
 */
void sweepPot(int pot_target, int interval)
{
  int pot_current = (int)readPot();
  
  if(pot_current > pot_target)
    angle_amt = 1;
  if(pot_current < pot_target)
    angle_amt = -1;

  while(pot_current != pot_target && angle <= 180 && angle >= 0)
  {
    angle += angle_amt;
    servo.write(angle);
    pot_current = (int)readPot();
    delay(interval);
  }

  sweepTo(90, 100);
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
  offset = (int) readPot();
  Serial.print(offset);
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

  _output = output;
  output = (LPF_Beta * angle) + ((1 - LPF_Beta) * _output);
  
  Serial.print(output);
  Serial.println(" ack");
}

/* Reads potentiometer, but does not send through
*  Serial port.
 */
float readPot()
{
  int analog = analogRead(0);
  float angle = ((float) analog / 1023.0f) * 340.0f;

  _output = output;
  output = (LPF_Beta * angle) + ((1 - LPF_Beta) * _output);

  return output;
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
  sweepTo(0, 50);
  
  for(angle = 0; angle <= 180; angle++)
  {
    readPot();
    servo.write(angle);
    int _angle;
    delay(25);
    _angle = servo.read();
    if(angle != _angle)
      return false;
  }
  for(angle = 180; angle >= 0; angle--)
  {
    readPot();
    servo.write(angle);
    int _angle;
    delay(25);
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

/* Single sweep, fast method
*  Servo starts at 0 degree, then sweeps to 180 degree at
 * one-half interval. Potentiometer is read low, then starts
*  sweeping to far end, up to 0 degrees. Potentiometer is
 * read high, then calculates center offset by taking linear
*  midpoint method.
 */
void calibrate_a()
{
  sweepTo(0, 50);
  delay(1000);

  for(angle = 0; angle <= 180; angle++)
  {
    servo.write(angle);
    delay(25);
    readPot();
  }
  delay(1000);
  float _lo = readPot();

  for(angle = 180; angle >= 0; angle--)
  {
    servo.write(angle);
    delay(25);
    readPot();
  }
  delay(1000);
  float _hi = readPot();
  
  hi = (int) _hi;
  lo = (int) _lo;
  float _offset = ((_hi + _lo) / 2);
  offset = (int) _offset;
  delay(1000);
  sweepPot(offset, 100);
  Serial.print(hi); Serial.print(" ");
  Serial.print(offset); Serial.print(" ");
  Serial.print(lo); Serial.print(" ");
  Serial.println("ack");
}

/* Single Sweep, angle-by-angle method.
*  Servo starts at 90 degrees, then sweeps to 180 degrees
 * at much slower rate. Each time servo is moved by 1 degree,
*  potentiometer value is measured, then saved at target
 * variables.
*  Once sweeping is completed, center offset is caculated by
 * linear midpoint method.
*/
void calibrate_b()
{
  float _lo = 0;
  float _offset = 90;
  float _hi = 180;
  
  sweepTo(90, 50);
  delay(1000);
  while(angle <= 180)
  {
    angle++;
    servo.write(angle);
    delay(200);
    _lo = readPot();
  }
  delay(1000);
  while(angle != 90)
  {
    angle--;
    servo.write(angle);
    delay(200);
    readPot();
  }
  delay(1000);
  while(angle >= 0)
  {
    angle--;
    servo.write(angle);
    delay(200);
    _hi = readPot();
  }
  delay(1000);

  hi = (int) _hi;
  lo = (int) _lo;
  _offset = ((_hi + _lo) / 2);
  offset = (int) _offset;
  delay(1000);
  sweepPot(offset, 100);
  Serial.print(hi); Serial.print(" ");
  Serial.print(offset); Serial.print(" ");
  Serial.print(lo); Serial.print(" ");
  Serial.println("ack");
}

/* Near-Edge refining method.
*  Servo starts at 0 degree, then moves towards 180 degrees.
 * 10 degrees before approaching, servo slows down, and samples
*  potentiometer at much faster rate. Potentiometer value is
 * replaced if new measurement is lower than previous one.
*  Servo moves towards 0 degree, at normal speed.
 * 10 degrees before approaching, servo slows down, and samples
*  potentiometer at much faster rate. Potentiometer value is
 * replaced if new measurement is higher than previous one.
*  Center offset is calculated by linear midpoint method.
 */
void calibrate_c()
{
  float _lo = 340;
  float _offset = 90;
  float _hi = 0;

  float __lo = 0;
  float __hi = 0;

  int i = 0;
  
  sweepTo(0, 25);
  for(angle = 0; angle <= 170; angle++)
  {
    servo.write(angle);
    delay(50);
    __lo = readPot();
    if(__lo < _lo)
      _lo = __lo;
  }
  for(angle = 170; angle <= 180; angle++)
  {
    servo.write(angle);
    for(i = 0; i < 500; i++)
    {
      __lo = readPot();
      if(__lo < _lo)
        _lo = __lo;
      delay(1);
    }
  }

  delay(1000);

  for(angle = 180; angle >= 10; angle--)
  {
    servo.write(angle);
    delay(50);
    __hi = readPot();
    if(__hi > _hi)
      _hi = __hi;
  }
  for(angle = 10; angle >= 0; angle--)
  {
    servo.write(angle);
    for(i = 0; i < 500; i++)
    {
      __hi = readPot();
      if(__hi > _hi)
        _hi = __hi;
      delay(1);
    }
  }

  delay(1000);

  hi = (int)_hi;
  offset = (int)((_lo + _hi) / 2);
  lo = (int)_lo;
  delay(1000);
  sweepPot(offset, 100);
  Serial.print(hi); Serial.print(" ");
  Serial.print(offset); Serial.print(" ");
  Serial.print(lo); Serial.print(" ");
  Serial.println("ack");
}

/* Manual Method
*  Servo sweeps to 180 degrees, then detaches self, so user
 * can move shaft with hand. Once each position is manually
*  moved, potentiometer value is read and stored.
 */
void calibrate_d()
{
  sweepTo(180, 50);

  delay(1000);
  servo.detach();
  Serial.println("rdy ack");
  while(Serial.available() < 1)
    readPot();

  float _lo = readPot();
  servo.attach(servoPin);
  angle = servo.read();
  sweepTo(90, 50);
  while(Serial.available())
    Serial.read();

  delay(1000);
  servo.detach();
  Serial.println("rdy ack");
  while(Serial.available() < 1)
    readPot();

  float _offset = readPot();
  servo.attach(servoPin);
  angle = servo.read();
  sweepTo(0, 50);
  while(Serial.available())
    Serial.read();

  delay(1000);
  servo.detach();
  Serial.println("rdy ack");
  while(Serial.available() < 1)
    readPot();

  float _hi = readPot();
  servo.attach(servoPin);
  angle = servo.read();
  while(Serial.available())
    Serial.read();

  hi = (int)_hi;
  offset = (int)_offset;
  lo = (int)_lo;
  delay(1000);
  sweepPot(offset, 100);
  Serial.print(hi); Serial.print(" ");
  Serial.print(offset); Serial.print(" ");
  Serial.print(lo); Serial.print(" ");
  Serial.println("ack");
}

void smoothPot()
{
  sweepTo(0, 50);
  for(angle = 0; angle <= 180; angle++)
  {
    servo.write(angle);
    readPot();
    delay(50);
  }
  for(angle = 180; angle >= 0; angle--)
  {
    servo.write(angle);
    readPot();
    delay(50);
  }
}
