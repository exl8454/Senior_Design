#include <CS_IMU.h>

long timestamp = -1;
float gx, gy, gz;

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
  /* Currently prints out
   *  [timestamp]ms X: [gyroX] Y: [gyroY] Z: [gyroZ]
  */
  long timeStart = millis();
  readSensor(&timestamp, &gx, &gy, &gz);
  Serial.println("Gyro Reading");
  Serial.print(timestamp); Serial.print("ms X: ");
  Serial.print(gx); Serial.print(" Y: ");
  Serial.print(gy); Serial.print(" Z: ");
  Serial.println(gz);
  long timeEnd = millis();

  /* Checks for 30ms interval. If interval exceeds 30ms, skip delay.
      If interval is less than 30 ms, do rest*/
  if((timeEnd - timeStart) < interval)
  {
    delay(interval - (timeEnd - timeStart));
  }
}
