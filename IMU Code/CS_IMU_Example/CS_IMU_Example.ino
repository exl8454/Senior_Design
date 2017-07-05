#include <CS_IMU.h>

long timestamp = -1;
float data[][3] = {{0, 0, 0}, {0, 0, 0}, {0, 0, 0}};

int interval = 10;

void setup()
{
  Serial.begin(115200);

  initSensor();

  Serial.println("Starting...");
  delay(1000);
}

void loop()
{
  long timeStart = millis();
  readSensor(&timestamp, data);
  long timeEnd = millis();

  /* Checks for 30ms interval. If interval exceeds 30ms, skip delay.
      If interval is less than 30 ms, do rest*/
  if((timeEnd - timeStart) < interval)
  {
    delay(interval - (timeEnd - timeStart));
  }
}
