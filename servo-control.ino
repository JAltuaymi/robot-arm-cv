#include <Servo.h>

Servo s1,s2,s3,s4,s5;
int pins[] = {A0,A1,A3,A4,A5};

void setup() {
  Serial.begin(115200);
  s1.attach(pins[0]);
  s2.attach(pins[1]);
  s3.attach(pins[2]);
  s4.attach(pins[3]);
  s5.attach(pins[4]);
  
  ready();
}

void ready(){
  s2.write(165);
  delay(1000);
  s1.write(90);
  delay(1000);
  s3.write(90);
  delay(1000);
  s4.write(90);
  delay(1000);
  s5.write(68);
  delay(1000);
}

void go(int n1,int n2,int n3){
  s1.write(n1);
  delay(1000);
  s3.write(n3);
  delay(1000);
  for(int i = 165;i>=n2;i--){
  s2.write(i);
  delay(50);
  }
  delay(1000);
  
  
}

void eat(){
  s5.write(180);
  delay(1000);
  s2.write(165);
  delay(1000);
  s1.write(160);
  delay(1000);
  s3.write(24);
  delay(1000);
  s2.write(145);
  delay(1000);
  s5.write(68);
  delay(1000);
}




void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');

    int comma1 = data.indexOf(',');
    int comma2 = data.indexOf(',', comma1 + 1);

    int sup1 = data.substring(0, comma1).toInt();
    int sup2 = data.substring(comma1 + 1, comma2).toInt();
    int sup3 = data.substring(comma2 + 1).toInt();

    
    go(sup1,sup2,sup3);
    eat();
    s2.write(165);
    delay(1000);
    ready();

    
  }
}
