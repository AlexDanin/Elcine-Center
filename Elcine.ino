int BUTTON_PIN = 2;
int LED_PIN_1 = 8;
int LED_PIN_2 = 12;
int button_value = 0;
int old_button_value = 0;

char request;

boolean isStart = false;

void setup() {
  pinMode(LED_PIN_1, OUTPUT);
  pinMode(LED_PIN_2, OUTPUT);
  pinMode(BUTTON_PIN, INPUT);
  Serial.begin(19200);
}

void loop() {
  button_value = digitalRead(BUTTON_PIN);
  if (button_value != old_button_value) {
    isStart = !isStart;
      onSignal(isStart);
      if (isStart){
        Serial.println("game");
      }
      else if (!isStart){
        Serial.println("video");
      }
    old_button_value = button_value;
    }
  

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
