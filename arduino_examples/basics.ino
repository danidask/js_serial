void setup() {
  Serial.begin(115200);
}

void loop() {
  if (Serial.available()) {
    char buffer_serial[128];
    size_t nchars = Serial.readBytesUntil('\n', buffer_serial, 128);
    //Serial.readBytes(buffer_serial, 128);
    for (size_t i = 0; i < nchars; i++) {
      buffer_serial[i]++;
    }  
    delay(500);
    Serial.println(buffer_serial);
  }
  delay(50);
}
