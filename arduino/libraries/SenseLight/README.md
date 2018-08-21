# SenseLight
Library for the Tris10 SenseLight sensor


## Functions

### SenseLight(uint8_t analogPin, uint8_t enablePin) [Initalizer]
> analogPin: Pin for analog input.

> enablePin: Pin to enable the LED on the SenseLight board.

Initaliser for the class.

### uint16_t get()
> No parameters

Returns the analog value read from the sensor at the last time the 'refresh' function was called.

### void enable()
> No parameters

Sets the enable pin HIGH to turn the SenseLight LED on.

### void disable()
> No parameters

Sets the enable pin LOW to turn the SenseLight LED off.\

### void refresh()

> No parameters

When called the sensor is read and the analog value is stored to a int in memory.
