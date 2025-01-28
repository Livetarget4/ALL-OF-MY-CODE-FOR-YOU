int VRx = A0; // X-axis pin
//int VRy = A1; // Y-axis pin
int SW = 2;   // Joystick button pin

void setup() {
  Serial.begin(9600);
  pinMode(SW, INPUT_PULLUP); // Set the switch pin as input with pull-up resistor
}

void loop() {
  int xValue = analogRead(VRx);
  //int yValue = analogRead(VRy);
  int buttonState = digitalRead(SW);

  // Map the joystick values from 0-1023 to -1 to 1
  int mappedX = map(xValue, 0, 1023, -1, 1);

  // Send the mapped values and button state over serial
  Serial.print(mappedX);
  Serial.print(",");
  Serial.println(buttonState);

  delay(100); // Delay to prevent flooding the serial port
}
