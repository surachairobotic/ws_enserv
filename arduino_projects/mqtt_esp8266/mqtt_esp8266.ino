/*
  Basic ESP8266 MQTT example
  This sketch demonstrates the capabilities of the pubsub library in combination
  with the ESP8266 board/library.
  It connects to an MQTT server then:
  - publishes "hello world" to the topic "outTopic" every two seconds
  - subscribes to the topic "inTopic", printing out any messages
    it receives. NB - it assumes the received payloads are strings not binary
  - If the first character of the topic "inTopic" is an 1, switch ON the ESP Led,
    else switch it off
  It will reconnect to the server if the connection is lost using a blocking
  reconnect function. See the 'mqtt_reconnect_nonblocking' example for how to
  achieve the same result without blocking the main loop.
  To install the ESP8266 board, (using Arduino 1.6.4+):
  - Add the following 3rd party board manager under "File -> Preferences -> Additional Boards Manager URLs":
       http://arduino.esp8266.com/stable/package_esp8266com_index.json
  - Open the "Tools -> Board -> Board Manager" and click install for the ESP8266"
  - Select your ESP8266 in "Tools -> Board"
*/

#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// Update these with values suitable for your network.

const char* ssid = "Enserv@Staff";
const char* password = "Enserv12345";
const char* mqtt_server = "10.2.253.115";
const unsigned int BAUDRATE = 1200;

WiFiClient espClient;
PubSubClient client(espClient);
unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE	(100)
char msg[MSG_BUFFER_SIZE];
int value = 0;
String msgOut = "", msgBuff = "";
bool bPush = false;

void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  randomSeed(micros());

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Create a random client ID
    String clientId = "ESP8266Client-", clientUser = "mqttclient", clientPassword = "%139User";
    //clientId += String(random(0xffff), HEX);
    //clientUser += String(random(0xffff), HEX);
    //clientPassword += String(random(0xffff), HEX);
    // Attempt to connect
    if (client.connect(clientId.c_str(), clientUser.c_str(), clientPassword.c_str())) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      client.publish("outTopic", "hello world");
      // ... and resubscribe
      // client.subscribe("inTopic");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(2000);
    }
  }
}

void setup() {
  //pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  Serial.begin(BAUDRATE);
  Serial.write("before setup_wifi()\r\n");
  setup_wifi();
  Serial.write("before client.setServer(mqtt_server, 1883)\r\n");
  client.setServer(mqtt_server, 1883);
  //Serial.write("before client.setCallback(callback)\r\n");
  //client.setCallback(callback);
}

void loop() {
  //  Serial.write("if (!client.connected()\r\n");
  if (!client.connected()) {
    reconnect();
  }
  //  Serial.write("client.loop()\r\n");
  client.loop();

  int lim = 300;
  while (Serial.available() > 0 && lim > 0) {
    lim -= 1;
    //    Serial.write("before serialBuff += Serial.read()");
    char cLetter = Serial.read();
    //    serialBuff += cLetter;
    //    serialBuff += 'X';
    if (bPush)
      msgBuff += cLetter;
    if (cLetter == '$') {
      msgBuff = "";
      bPush = true;
    }
    if (cLetter == '\n') {
      //      Serial.write("before msgOut = serialBuff");
      ++value;
      snprintf (msg, MSG_BUFFER_SIZE, "#%ld:%s", value, msgBuff.c_str());
      client.publish("outTopic", msg);

      bPush = false;
    }
  }
  //  msgOut = serialBuff;
  delay(100);
}
