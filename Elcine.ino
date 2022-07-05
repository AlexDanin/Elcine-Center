#define BUTTON_PIN 2
#define LED_PIN_1 13
#define LED_PIN_2 12

boolean buttonWasUp = true;
boolean isStart = false;

char request;

void setup() {
  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);

  Serial.begin(19200);
}

void loop() {
  boolean buttonIsUp = digitalRead(BUTTON_PIN);

  if (buttonWasUp && !buttonIsUp) {
    delay(10);
    buttonIsUp = digitalRead(BUTTON_PIN);
    if (!buttonIsUp) {
      isStart = !isStart;
      onSignal(isStart);
      if (isStart){
        Serial.println("game");
      }
      else if (!isStart){
        Serial.println("video");
      }
    }
  }
  buttonWasUp = buttonIsUp;

  if (Serial.available() > 0) {
    request = Serial.read();
    if (request == '1'){
      Serial.println("video");
      isStart = false;
      onSignal(isStart);
    }
  }
}

void onSignal(bool flag){
  if (flag){
    digitalWrite(LED_PIN_1, true);
    delay(20);
    digitalWrite(LED_PIN_1, false);
  }
  else if (!flag){
    digitalWrite(LED_PIN_2, true);
    delay(20);
    digitalWrite(LED_PIN_2, false);
  }
}
