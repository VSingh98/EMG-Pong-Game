volatile int sig0 = 0;
volatile int sig1 = 0;
volatile int stat = 0;
boolean newread = 0;
bool state = 0;
int preloader = 64286;

void setup()
{
  Serial.begin(115200);

  if(analogRead(A2)<512) {
    state = 0;            // Currently in calibration
    Serial.print('c');
  }
  else {
    state = 1;            // Currently in game mode
    Serial.print('s');
  }

  // initialize timer1 
  cli();           // disable all interrupts
  TCCR1A = 0;
  TCCR1B = 0;
  TCNT1 = preloader;            // preload timer 65536-16MHz/prescaler/200Hz
  TCCR1B |= (1 << CS11) | (1 << CS10);    // 64 prescaler
  TIMSK1 |= (1 << TOIE1);   // enable timer overflow interrupt
  sei();          // enable all interrupts
}
 
ISR(TIMER1_OVF_vect)
{
  TCNT1 = preloader;            // preload timer
  sig0 = analogRead(A0);
  sig1 = analogRead(A1);
  stat = analogRead(A2);
  newread = 1; // indicate a new sample has been read
}

void loop()
{
  if (newread) { // print to Serial if there is a new sample
    if(state==0 && stat > 512) {        // If in calibration, allow exit
      Serial.print('s');
      state = 1;
    }  
    Serial.print(sig0);
    Serial.print(" ");
    Serial.print(sig1);
    Serial.print("\n");
    newread = 0;
  }
}
