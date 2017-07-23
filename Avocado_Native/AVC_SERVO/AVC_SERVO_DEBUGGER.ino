/* Potentiometer Debugger */

float _angle = 0;
float angle = 0;

void setup()
{
  Serial.begin(115200);
}

void loop()
{
  int value = analogRead(0);
  float output = ((float) value / 1023.0f) * 340.0f;

  _angle = angle;
  angle = (0.5f * output) + (0.5f * _angle);
  Serial.println((int)angle);
}
