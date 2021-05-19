#include <Servo.h> //используем библиотеку для работы с сервоприводом

Servo servo; //объявляем переменную servo типа Servo

int a;
int servPos=90;
void setup() {
  Serial.begin(115200);
  servo.attach(10);
}

void loop() {
  a = 0;
  while (Serial.available() > 0) {
    a = Serial.read();
    Serial.println(a);
    //Serial.print("MESSAGE_OK");
    Serial.print("\n");
    if(a<255)
    a -= 128;
    
   }
  if(a==255) servPos = 90;
  else{ 
  servPos += a;
  }
  
  if(servPos<0) servPos = 0;
  if(servPos>180) servPos = 180;
  servo.write(servPos);

  delay(10);
}
