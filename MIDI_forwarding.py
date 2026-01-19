import serial
import rtmidi

# --- CONFIGURATION ---
TELNET_HOST = "localhost"
TELNET_PORT = 4000
MIDI_PORT_NAME = "loopMIDI Port 1"   # Change to your virtual MIDI port name

# --- OPEN RFC2217 (telnet) SERIAL CONNECTION ---
url = f"rfc2217://{TELNET_HOST}:{TELNET_PORT}"
ser = serial.serial_for_url(url, baudrate=115200, timeout=1)

print(f"Connected to Wokwi RFC2217 at {url}")

# --- OPEN MIDI OUTPUT PORT ---
midiout = rtmidi.MidiOut()
ports = midiout.get_ports()

print("Available MIDI ports:", ports)

# Find the port by name
try:
    midi_index = ports.index(MIDI_PORT_NAME)
except ValueError:
    raise RuntimeError(f"MIDI port '{MIDI_PORT_NAME}' not found. "
                       f"Create it using rtpMIDI or another Win11 virtual MIDI driver.")

midiout.open_port(midi_index)
print(f"Forwarding MIDI to: {MIDI_PORT_NAME}")

# --- MAIN LOOP ---
print("Bridge running: Wokwi → RFC2217 → MIDI → Ableton")

try:
    while True:
        b = ser.read(1)
        if not b:
            continue

        status = b[0]

        # Standard 3‑byte MIDI messages
        if status & 0x80:
            data = ser.read(2)
            if len(data) == 2:
                msg = [status, data[0], data[1]]
                midiout.send_message(msg)
                print("Sent:", msg)

except KeyboardInterrupt:
    print("Stopping bridge...")

finally:
    ser.close()
    midiout.close_port()