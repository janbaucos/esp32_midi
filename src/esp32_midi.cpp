#include <Control_Surface.h>

// Instantiate a MIDI Interface to use
USBMIDI_Interface midi;             // not possible to use with a hardware simulator like Wokwi
//USBSerialMIDI_Interface midi(115200);
//USBDebugMIDI_Interface midi = 115200;

// Instantiate an analog multiplexer
CD74HC4067 mux {
   A0,           // Analog input pin
   {4, 5, 6, 7}  // Address pins S0, S1, S2, S3
};              // Analog input pin and address pins S0, S1, S2, S3

// Create an array of potentiometers that send out
// MIDI Control Change messages when you turn the
// potentiometers connected to the eight input pins of
// the multiplexer
CCPotentiometer volumePotentiometers[] {
  {mux.pin(0), {MIDI_CC::Channel_Volume, Channel_1}},
  {mux.pin(1), {MIDI_CC::Channel_Volume, Channel_2}},
  {mux.pin(2), {MIDI_CC::Channel_Volume, Channel_3}},
  {mux.pin(3), {MIDI_CC::Channel_Volume, Channel_4}}
};

void setup() {
  // put your setup code here, to run once:
  //Serial.begin(115200);
  //Serial.println("Hello, ESP32-S3!");

  Control_Surface.begin(); 
}
 
// Update the Control Surface
void loop() {
  Control_Surface.loop();
}