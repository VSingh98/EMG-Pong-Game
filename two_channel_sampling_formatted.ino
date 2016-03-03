volatile int sig0 = 0;
volatile int sig1 = 0;
volatile unsigned long currtime = 0.0;
boolean newread = 0;
int preloader = 64286;

void setup()
{
  Serial.begin(115200);
  Serial.print('s');

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
  currtime = micros();
  newread = 1; // indicate a new sample has been read
}

void loop()
{
  if (newread) { // print to Serial if there is a new sample
    Serial.print(currtime);
    Serial.print(" ");
    Serial.print(sig0);
    Serial.print(" ");
    Serial.print(sig1);
    Serial.print("\n");
    newread = 0;
  }
}
