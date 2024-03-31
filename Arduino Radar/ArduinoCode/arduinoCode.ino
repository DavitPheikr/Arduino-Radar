#include <Servo.h>
const int trigPin = 10;
const int echoPin = 11;
float duration;
float distance;
Servo myServo; 
void setup() {
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT); 
  Serial.begin(9600);
  myServo.attach(12); 
}
void loop() {
  for(int i=0;i<=165;i++){  
  myServo.write(i);
  delay(30);
  distance = calculateDistance();
  Serial.print(i); 
  Serial.print(","); 
  Serial.println(distance); 
  }
  for(int i=180;i>0;i--){  
  myServo.write(i);
  delay(30);
  distance = calculateDistance();
  Serial.print(i);
  Serial.print(",");
  Serial.println(distance);
  }
}
float calculateDistance(){ 
  digitalWrite(trigPin, LOW); 
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH); 
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  duration = pulseIn(echoPin, HIGH); 
  distance= duration*0.034/2;
  return distance;
}