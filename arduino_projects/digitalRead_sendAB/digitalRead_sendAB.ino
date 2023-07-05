#include <SoftwareSerial.h>
SoftwareSerial debugSerial(10, 11); // RX, TX

const int ledPin =  LED_BUILTIN;
const int inputPin =  7;
const int debugPin =  9;
const long interval = 1000;

bool ledState = true;
unsigned long previousMillis = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(ledPin, OUTPUT);
  pinMode(debugPin, OUTPUT);
  pinMode(inputPin, INPUT_PULLUP);
  Serial.begin(9600);

  debugSerial.begin(9600);
  debugSerial.println("debug mode!");
}

// the loop function runs over and over again forever
void loop() {
  unsigned long currentMillis = millis();

  if (currentMillis - previousMillis >= interval) {
    // save the last time you blinked the LED
    previousMillis = currentMillis;

    // set the LED with the ledState of the variable:
    digitalWrite(ledPin, ledState);
    ledState = !ledState;
    checkInputAndSend();
  }
}

void checkInputAndSend() {
  unsigned int value = analogRead(A0);
  char buff[128];
  sprintf(buff, "%d\r\n", value);
  debugSerial.write(buff);
  Serial.write(buff);
  if (value < 512)
    digitalWrite(debugPin, HIGH);
  else
    digitalWrite(debugPin, LOW);
}
