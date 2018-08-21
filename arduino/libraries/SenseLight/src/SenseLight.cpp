#include "SenseLight.h"

SenseLight::SenseLight(uint8_t analogPin, uint8_t enablePin): _analogPin(analogPin), _enablePin(enablePin) {
	pinMode(_analogPin, INPUT);
	pinMode(_enablePin, OUTPUT);

	enable(); // Enable by default
}

SenseLight::~SenseLight() { /* NOTHING TO DECONSTRUCT */ }

uint16_t SenseLight::get() {
	return _value;
}

void SenseLight::enable() {
	digitalWrite(_enablePin, HIGH);
}

void SenseLight::disable() {
	digitalWrite(_enablePin, LOW);
}

void SenseLight::refresh() {
	_value = analogRead(_analogPin);
}