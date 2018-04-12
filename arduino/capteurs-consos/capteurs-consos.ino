/*
    Workshop IA 2018 - Erasme
    Simulateur d'allumage d'appareils électriques

    Chaque bouton pilote l'allumage un appareil avec son cycle de fonctionnement propre.
    L'extinction se fait automatiquement en fin de cycle.

    Un facteur d'échelle permet d'ajuster le temps réel à une échelle de temps plus courte
    1min réelle est représentée par 1 seconde sur la maquette.
*/
#include <Adafruit_NeoPixel.h>

#ifdef __AVR__
#include <avr/power.h>
#endif

#define NB_APPAREILS 10
#define LEDS_PIN 13

// Decommenter pour le mode debug
//#define DEBUG_MODE 1

// Facteur d'échelle de temps :
// Si sur la maquette 1mn réel est représentée en 1s alors le facteur de temps est égale à 1/60
#define TIME_FACTOR 0.833  // 1min = 1s 

// Strip de leds d'état des appareils
uint8_t gBrightness = 255;
Adafruit_NeoPixel strip = Adafruit_NeoPixel(NB_APPAREILS, LEDS_PIN, NEO_GRB + NEO_KHZ800);

// Structure pour la lecture des boutons
boolean buttonsStates[NB_APPAREILS];

// Structure pour un appareil électrique
typedef struct {
  String name = "";
  uint8_t state = LOW;
  uint8_t cycle_time = 60; // Temps de cycle (en minutes)
  uint32_t start_time = 0; // En milli-secondes depuis le boot de l'arduino
  uint8_t pin = 0; // Input Arduino
  uint8_t led = 0; // Index led  
} Appareil;

// Tableau d'appareils
Appareil appareils[NB_APPAREILS]; // tous les appareils de la maison

//------------------------------------------------------------------------------
// Setter
//------------------------------------------------------------------------------
Appareil initAppareils(String name = "", uint8_t cycle_time = 60, uint8_t pin = 0, uint8_t led = 0) {
  Appareil a;
  a.name = name;
  a.cycle_time = cycle_time;
  a.pin = pin;
  a.led = led;
  return a;
}

//------------------------------------------------------------------------------
// Init de tous les appareils de la maquette
//------------------------------------------------------------------------------
void IntiMaison() {
  appareils[0] = initAppareils("clothes iron", 60, 2, 0);
  appareils[1] = initAppareils("fridge", 10, 3, 2);
  appareils[2] = initAppareils("wet appliance", 120, 4, 6);
  appareils[3] = initAppareils("unknown", 60, 5, 9);
  appareils[4] = initAppareils("washing machine", 60, 6, 1);
  appareils[5] = initAppareils("motor", 30, 7, 3);
  appareils[6] = initAppareils("computer", 90, 8, 8);
  appareils[7] = initAppareils("clim1", 60, A0, 5);
  appareils[8] = initAppareils("clim2", 60, A1, 7);
  appareils[9] = initAppareils("TV", 15, A2, 4);
}
//------------------------------------------------------------------------------
//  Setup
//------------------------------------------------------------------------------
void setup() {
  Serial.begin(9600);
  delay(10);
  debug("DEBUG MMODE ACTIVE. Setup...");
  strip.begin();
  strip.setBrightness(gBrightness);
  // All leds black
  strip.clear();
  strip.show();

  // Initialisation des appareils
  IntiMaison();

  // Initialisation de tout les boutons
  for (int i = 0; i < NB_APPAREILS; i++) {
    pinMode(appareils[i].pin, INPUT);
    digitalWrite(appareils[i].pin, LOW);
    debug(appareils[i].name + " : Pin #" + String(appareils[i].pin));
    strip.setPixelColor(appareils[i].led, 0, 0, 0);
  }
  debug("END Setup.");
}

//------------------------------------------------------------------------------
// Loop for ever !
//------------------------------------------------------------------------------
void loop() {
  for (uint8_t i = 0; i < NB_APPAREILS; i++) {
    uint8_t butState = HIGH;
    butState = digitalRead(appareils[i].pin);
    // Détection front montant
    if (butState == HIGH) {
      // Changement d'état
      if (appareils[i].state == LOW) {
        debug("Allumage " + appareils[i].name);
        appareils[i].state = HIGH;
        uint32_t timeNow = millis();
        // Allummer et envoyer des données
        //Serial.println("{\"" + appareils[i].name + "\":" + timeNow + ", \"state\": 1 }");
        Serial.println(appareils[i].name);
        appareils[i].start_time = timeNow;
        strip.setPixelColor(appareils[i].led, 255, 255, 255);
      }
      // Debounce Button
      //delay(500);
    }

    // Si l'appareil est allumé, on regarde si l'appareil a fini son cycle
    if (appareils[i].state == HIGH) {
      uint32_t timeNow = millis();
      String debug_msg = "\n----------------------------\n" + appareils[i].name;
      debug_msg += " fonctionne depuis :" + String(timeNow - appareils[i].start_time);
      debug_msg += "/" + String((appareils[i].cycle_time * TIME_FACTOR * 1000));
      if (timeNow - appareils[i].start_time >= (appareils[i].cycle_time * TIME_FACTOR * 1000)) {
        debug_msg += "\n\t ===> Fin de cycle\n----------------------------\n";
        // Eteindre si son cycle est terminé
        appareils[i].state = LOW;
        strip.setPixelColor(appareils[i].led, 0, 0, 0);
      }
      debug(debug_msg);
      strip.show();
    }
  }
}

//------------------------------------------------------------------------------
// Debug functions
//------------------------------------------------------------------------------
void debug(int s) {
  debug(String(s));
}

void debug(String s) {
#ifdef DEBUG_MODE
  Serial.println(s);
#endif
}


