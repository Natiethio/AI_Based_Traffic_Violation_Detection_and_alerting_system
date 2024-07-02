// Define the pin numbers for the LEDs
const int redLED = 13;
const int yellowLED = 12;
const int greenLED = 11;

void setup() {
  // Initialize the LED pins as outputs
  pinMode(redLED, OUTPUT);
  pinMode(yellowLED, OUTPUT);
  pinMode(greenLED, OUTPUT);

  // Initialize serial communication at 9600 bits per second
  Serial.begin(9600);
}

void loop() {
  // Red light on
  digitalWrite(redLED, HIGH);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, LOW);
  Serial.println("red");
  delay(15000); // Red light for 5 seconds

    // Yellow light on
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, HIGH);
  digitalWrite(greenLED, LOW);
  Serial.println("yellow");
  delay(3000); // Yellow light for 2 seconds

  // Green light on
  digitalWrite(redLED, LOW);
  digitalWrite(yellowLED, LOW);
  digitalWrite(greenLED, HIGH);
  Serial.println("green");
  delay(15000); // Green light for 5 seconds


}
