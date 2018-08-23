#ifndef SENSELIGHT_H
#define SENSELIGHT_H

#include "Arduino.h"

class SenseLight {
public:
	SenseLight(uint8_t analogPin, uint8_t enablePin);
	~SenseLight();

	uint16_t get();
	void enable();
	void disable();
	void refresh();
private:
	uint8_t _analogPin;
	uint8_t _enablePin;

	uint16_t _value = 0;
};

#endif /* SENSELIGHTSLAVE_H */