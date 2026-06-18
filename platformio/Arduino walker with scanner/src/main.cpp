#include <Arduino.h>
#include <Servo.h>

Servo servo;


const int ENA = 5; 
const int IN1 = 2; 
const int IN2 = 4; 
const int ENB = 6; 
const int IN3 = 7; 
const int IN4 = 8; 


const int TRIG_PIN = A0;
const int ECHO_PIN = A1;
const int SERVO_PIN = 11;

int predkosc = 180; 


void jedzDoPrzodu();
void jedzDoTylu();
void skrecWLewo();
void skrecWPrawo();
void zatrzymaj();
void radar();
int zmierzOdleglosc();

void setup() {
  Serial.begin(9600);


  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

  // Radar
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  servo.attach(SERVO_PIN);
  

  servo.write(90); 

  zatrzymaj();
}

void loop() {
  if (Serial.available() > 0) {
    char komenda = Serial.read();

    switch (komenda) {
      case 'F': jedzDoPrzodu(); break;
      case 'B': jedzDoTylu(); break;
      case 'L': skrecWLewo(); break;
      case 'R': skrecWPrawo(); break;
      case 'S': zatrzymaj(); break;
      case 'r': radar(); break;
    }
  }
}



int zmierzOdleglosc() {
  // generowanie krótkiego impulsu 10 mikrosekund na pinie Trig
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // nasluchiwanie echo
  long czas_powrotu = pulseIn(ECHO_PIN, HIGH, 30000); 
  
  if (czas_powrotu == 0) return -1; // zbyt daleko, brak odbicia w 30ms
  
  // wzor na predkosc dzwieku w powietrzu: 343 m/s = 0.034 cm/us
  int dystans_cm = czas_powrotu * 0.034 / 2;
  return dystans_cm;
}

void radar() {
  zatrzymaj(); 

  // obrót 0 -> 180 stopni (co 5 stopni)
  for (int kat = 0; kat <= 180; kat += 5) {
    servo.write(kat);
    delay(50); // czas, by mechanika serwa zdążyła dojechać
    
    int odleglosc = zmierzOdleglosc();

    // wysyłanie przez Bluetooth do Pythona w formacie: "R:kat,odleglosc"
    Serial.print("R:");
    Serial.print(kat);
    Serial.print(",");
    Serial.println(odleglosc);
  }

  // krok 2: obrót 180 -> 0 stopni
  for (int kat = 180; kat >= 0; kat -= 5) {
    servo.write(kat);
    delay(50);
    
    int odleglosc = zmierzOdleglosc();

    Serial.print("R:");
    Serial.print(kat);
    Serial.print(",");
    Serial.println(odleglosc);
  }

  // powrót na wprost po skanowaniu
  servo.write(90);
}


void jedzDoPrzodu() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, predkosc); analogWrite(ENB, predkosc);
}
void jedzDoTylu() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  analogWrite(ENA, predkosc); analogWrite(ENB, predkosc);
}
void skrecWLewo() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH); digitalWrite(IN4, LOW);
  analogWrite(ENA, predkosc); analogWrite(ENB, predkosc);
}
void skrecWPrawo() {
  digitalWrite(IN1, HIGH); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, HIGH);
  analogWrite(ENA, predkosc); analogWrite(ENB, predkosc);
}
void zatrzymaj() {
  digitalWrite(IN1, LOW); digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW); digitalWrite(IN4, LOW);
  analogWrite(ENA, 0); analogWrite(ENB, 0);
}