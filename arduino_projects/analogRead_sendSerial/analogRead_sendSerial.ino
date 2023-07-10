#include <SoftwareSerial.h>
SoftwareSerial debugSerial(10, 11); // RX, TX

const uint8_t ledPin =  LED_BUILTIN;
const uint8_t inputPin =  7;
const uint8_t debugPin =  9;
const long interval = 1000;
const uint8_t analogPins[] = {A0,A1,A2,A3,A4,A5,A6,A7,A8,A9,A10,A11};
const uint8_t analogPinsLength = 12;
const unsigned int BAUDRATE = 1200;

bool ledState = true;
unsigned long previousMillis = 0;

// the setup function runs once when you press reset or power the board
void setup() {
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(ledPin, OUTPUT);
  pinMode(debugPin, OUTPUT);
  pinMode(inputPin, INPUT_PULLUP);
  Serial.begin(BAUDRATE);
  Serial3.begin(BAUDRATE);

  debugSerial.begin(BAUDRATE);
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
  String message = "$";

  for(unsigned int i=0; i<analogPinsLength; i++) {
    unsigned int analogValue = analogRead(analogPins[i]);
    char buff[4];
    sprintf(buff, "%d", analogValue);
    message += buff;
    if (i < (analogPinsLength-1)) {
      message += ',';
    }
  }
  message += "\r\n";
  
//  unsigned int value[12];
//  for(unsigned int i=0; i<12; i++)
//    value[i] = analogRead(analogPins[i]);
//  
//  char buff[128];
//  sprintf(buff, "%d\r\n", value);

  //message = "A\r\n";
  debugSerial.write(message.c_str());
  Serial.write(message.c_str());
  Serial3.write(message.c_str());
//  if (value > 512)
//    digitalWrite(debugPin, HIGH);
//  else
//    digitalWrite(debugPin, LOW);
}
