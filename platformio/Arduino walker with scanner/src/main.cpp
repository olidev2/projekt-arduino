#include <Arduino.h>

const int ENA = 5; 
const int IN1 = 2; 
const int IN2 = 4; 

const int ENB = 6; 
const int IN3 = 7; 
const int IN4 = 8; 

int predkosc = 180; 

// Deklaracje funkcji
void jedzDoPrzodu();
void jedzDoTylu();
void skrecWLewo();
void skrecWPrawo();
void zatrzymaj();

void setup() {
  Serial.begin(9600);

  pinMode(ENA, OUTPUT);
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  pinMode(ENB, OUTPUT);
  pinMode(IN3, OUTPUT);
  pinMode(IN4, OUTPUT);

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
    }
  }
}

void jedzDoPrzodu() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, predkosc);
  analogWrite(ENB, predkosc);
}

void jedzDoTylu() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, predkosc);
  analogWrite(ENB, predkosc);
}

void skrecWLewo() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, HIGH);
  digitalWrite(IN3, HIGH);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, predkosc);
  analogWrite(ENB, predkosc);
}

void skrecWPrawo() {
  digitalWrite(IN1, HIGH);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, HIGH);
  analogWrite(ENA, predkosc);
  analogWrite(ENB, predkosc);
}

void zatrzymaj() {
  digitalWrite(IN1, LOW);
  digitalWrite(IN2, LOW);
  digitalWrite(IN3, LOW);
  digitalWrite(IN4, LOW);
  analogWrite(ENA, 0);
  analogWrite(ENB, 0);
}