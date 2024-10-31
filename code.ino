#include "braille.h"

byte alpha_pattern[26] = {
  0b00100000, // a
  0b00101000, // b
  0b00110000, // c
  0b00110100, // d
  0b00100100, // e
  0b00111000, // f
  0b00111100, // g
  0b00101100, // h
  0b00011000, // i
  0b00011100, // j
  0b00100010, // k
  0b00101010, // l
  0b00110010, // m
  0b00110110, // n
  0b00100110, // o
  0b00111010, // p
  0b00111110, // q
  0b00101110, // r
  0b00011010, // s
  0b00011110, // t
  0b00100011, // u
  0b00101011, // v
  0b00011101, // w
  0b00110011, // x
  0b00110111, // y
  0b00100111  // z
};

int dataPin = 2;
int latchPin = 3;
int clockPin = 4;
int no_module = 1;

braille bra(dataPin, latchPin, clockPin, no_module);

void setup() {
  Serial.begin(9600);
  bra.begin();
  pinMode(13, OUTPUT);  // Tone을 위한 핀 설정
}

void loop() {
  if (Serial.available()) {
    int ch = Serial.read();

    // 알파벳 대소문자 확인
    if ((ch >= 'A' && ch <= 'Z') || (ch >= 'a' && ch <= 'z')) {
      display(ch);       // 점자 출력
      tone(13, 1000);    // 소리 신호
      delay(100);
      noTone(13);
      delay(400);
      off();             // 모든 점 끄기
      delay(300);
    }
  }
}

void display(uint8_t ch) {
  int index = 0;

  if (ch >= 'a' && ch <= 'z') {
    index = ch - 'a';
  } else if (ch >= 'A' && ch <= 'Z') {
    index = ch - 'A';
  } else {
    off();
    return;
  }

  // 점자 패턴 출력
  for (int i = 0; i < 6; i++) {
    int value = (alpha_pattern[index] >> (5 - i)) & 0b00000001;
    if (value) {
      bra.on(0, i);
    } else {
      bra.off(0, i);
    }
  }
  bra.refresh();
}

void off() {
  for (int i = 0; i < 6; i++) {
    bra.off(0, i);
  }
  bra.refresh();
}
