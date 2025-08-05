const int outputPin = 8;                 // Pin que se enciende y apaga
const unsigned long delayBeforeOn = 0;  // Espera antes de encender (5 segundos)
const unsigned long durationOn = 1000;     // Tiempo encendido (2 segundos)

struct Event {
  unsigned long onTime;   // Cuándo encender
  unsigned long offTime;  // Cuándo apagar
  bool onTriggered;
  bool active;
};

#define MAX_EVENTS 10
Event events[MAX_EVENTS];

void setup() {
  Serial.begin(9600);
  pinMode(outputPin, OUTPUT);
  digitalWrite(outputPin, LOW);

  // Inicializar estructura de eventos
  for (int i = 0; i < MAX_EVENTS; i++) {
    events[i].active = false;
  }
}

void loop() {
  // Leer del puerto serie
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '1') {
      scheduleEvent();
    }
  }

  unsigned long now = millis();

  for (int i = 0; i < MAX_EVENTS; i++) {
    if (events[i].active) {
      // Encender si corresponde
      if (!events[i].onTriggered && now >= events[i].onTime) {
        digitalWrite(outputPin, HIGH);
        events[i].onTriggered = true;
        Serial.println("⚡ Pin activado");
      }

      // Apagar si corresponde
      if (events[i].onTriggered && now >= events[i].offTime) {
        digitalWrite(outputPin, LOW);
        events[i].active = false;
        Serial.println("🔕 Pin desactivado");
      }
    }
  }
}

void scheduleEvent() {
  for (int i = 0; i < MAX_EVENTS; i++) {
    if (!events[i].active) {
      unsigned long now = millis();
      events[i].onTime = now + delayBeforeOn;
      events[i].offTime = events[i].onTime + durationOn;
      events[i].onTriggered = false;
      events[i].active = true;
      Serial.println("🕒 Orden recibida. Encendido programado en 5 segundos.");
      return;
    }
  }

  Serial.println("❌ Límite de eventos alcanzado. Espera a que se liberen.");
}
