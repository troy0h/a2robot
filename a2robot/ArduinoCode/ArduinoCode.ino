int leftLed = 3;
int rightLed = 11;
int LM1 = 9;
int LM2 = 10;
int RM1 = 5;
int RM2 = 6;

void setup() {
  Serial.begin(9600); // Set the baud rate to match with ROS2
  pinMode(leftLed, OUTPUT); // Set the LED pin as an output
  pinMode(rightLed, OUTPUT);
  pinMode(LM1, OUTPUT);
  pinMode(LM2, OUTPUT);
  pinMode(RM1, OUTPUT);
  pinMode(RM2, OUTPUT);
}

void loop() {
  if (Serial.available() > 0) {
    char receivedChar = Serial.read();

    switch (receivedChar) {
      case '1':
        digitalWrite(leftLed, HIGH);
        digitalWrite(rightLed, LOW);
        Serial.println("Left Led ON");
        break;
        
      case '0':
        digitalWrite(rightLed, HIGH);
        digitalWrite(leftLed, LOW);
        Serial.println("Right Led ON");
        break;

      case 'q':
        digitalWrite(LM1, HIGH);
        digitalWrite(LM2, LOW);
        digitalWrite(RM1, LOW);
        digitalWrite(RM2, LOW);
        Serial.println("LM1 ON");
        break;

      case 'w':
        digitalWrite(LM1, LOW);
        digitalWrite(LM2, HIGH);
        digitalWrite(RM1, LOW);
        digitalWrite(RM2, LOW);
        Serial.println("LM2 ON");
        break;

      case 'a':
        digitalWrite(LM1, LOW);
        digitalWrite(LM2, LOW);
        digitalWrite(RM1, HIGH);
        digitalWrite(RM2, LOW);
        Serial.println("RM1 ON");
        break;

      case 's':
        digitalWrite(LM1, LOW);
        digitalWrite(LM2, LOW);
        digitalWrite(RM1, LOW);
        digitalWrite(RM2, HIGH);
        Serial.println("RM2 ON");
        break;

      case 't':
        digitalWrite(LM1, LOW);
        digitalWrite(LM2, LOW);
        digitalWrite(RM1, LOW);
        digitalWrite(RM2, LOW);
        digitalWrite(leftLed, LOW);
        digitalWrite(rightLed, LOW);
        Serial.println("MOTORS OFF, LEDs OFF");
        break;
    }
  }
}
