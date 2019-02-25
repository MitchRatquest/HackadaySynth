/*
 * COMPILES TO ROUGHLY 63664 BYTES
 * FITS INTO 64KB FLASH
 * SEE DIGIKEY  497-6065-ND
 *  STM32F103R8T6
 *  5.08 QTY 1
 *  
 *  LCSC.COM HAS IT AT 3.62
 *  https://lcsc.com/product-detail/ST-Microelectronics_STMicroelectronics_STM32F103R8T6_STM32F103R8T6_C46034.html
 *
 * YOU CAN FIND ANOTHER ONE HERE AT 2.15
 * https://lcsc.com/product-detail/ST-Microelectronics_STMicroelectronics_STM32F103RBT6_STM32F103RBT6_C8735.html
 * SOMEHOW IT HAS 128K RAM? 
 *  
 *  63664 bytes (97%) of program storage space. Maximum is 65536 bytes.
 *  
 *  
 *  AS OF 2-23-19 ---->
 *  Sketch uses 63792 bytes (48%) of program storage space. Maximum is 131072 bytes.
Global variables use 5496 bytes (26%) of dynamic memory, leaving 14984 byte

  compiled using Board: "Generic STM32F103R series"
  Optimize: "Fastest -O3 with LTO"
  variant "STM32F103RB (20k RAM, 128k Flash)"
  cpu speed(72mhz)
  upload method serial
 *  
 */


#include <OSCBundle.h>
#include <SLIPEncodedSerial.h>
#include <OSCMessage.h>

SLIPEncodedSerial SLIPSerial(Serial);
//////////////////////////////////////////////////
#include "SPI.h"
#include "Adafruit_GFX_AS.h"
#include "Adafruit_ILI9341_STM.h"
#define TFT_DC       PC4
#define TFT_CS       PB0
#define TFT_RST      PC5
Adafruit_ILI9341_STM tft = Adafruit_ILI9341_STM(TFT_CS, TFT_DC, TFT_RST);
//lets set up some globals for drawing
uint16_t BACKGROUND = 0;    //black default
uint16_t TEXTCOLOR  = 1260; //anything bright will do
uint8_t  TEXTSIZE   = 3;    //nice default
const uint8_t CHARLENGTH[7] = {53,53,26,18,12,10,9}; //amount of characters per line
uint16_t CURSOR[2] = {0,0}; //top left of screen

//////////////////////////////////////////////

// encoder stuff below vvvvv
#define MAXENCODERS 1
volatile uint32_t encstate[MAXENCODERS];
volatile uint32_t encflag[MAXENCODERS];
boolean A_set[MAXENCODERS];
boolean B_set[MAXENCODERS];
volatile uint16_t encoderpos[MAXENCODERS];
volatile uint32_t  encodertimer = millis(); // acceleration measurement
uint32_t encoderpinA[MAXENCODERS] = {PB12}; // pin array of all encoder A inputs PB5
uint32_t encoderpinB[MAXENCODERS] = {PB13}; // pin array of all encoder B inputs PB4
uint32_t lastEncoderPos[MAXENCODERS];

// timer
#define ENCODER_RATE 1000    // in microseconds; 
HardwareTimer timer(1);

const uint8_t encButton = PB14;
volatile uint8_t previousButton = 0;
volatile uint8_t currentButton = 0;
uint32_t prevTime = 0;
//encoder stuff above ^^^^^
//keyboard stuff below vvvv
//const uint8_t numberOfButtons = 27;
const uint8_t numberOfButtons = 48;
uint8_t keyValuesRaw[numberOfButtons];
uint8_t keyValues[4][numberOfButtons];
uint8_t keyValuesLast[numberOfButtons];
/*
   GND - EN
   PA13 - S0
   PA14 - S1
   PA15 - S2
   PC11 - IN0
   PC12 - IN1
   PB3  - IN2
   PB4  - IN3
   PB5  - IN4
   PB6  - IN5
*/

uint8_t muxPins[3] = {PA13, PA14, PA15};
uint8_t MUX = 1;
uint8_t muxInputPins[6] = { PC11, PC12, PB3, PB4, PB5, PB6 };

//keyboard stuff above ^^^^^^
//knobs below vvvvv
/*
   PA0-4 are knobs
*/
const uint8_t numberOfKnobs = 5;
const uint8_t knobs[numberOfKnobs] = {PA0, PA1, PA2, PA3, PA4};
uint32_t knobValues[numberOfKnobs];
//knobs above ^^^^^^
void setup()
{
  pinMode(PC3,  OUTPUT);//tied to boost converter's enable pin
  digitalWrite(PC3, HIGH);// as long as this is high, the machine is 
  Serial.begin(115200);
  Serial.setTimeout(50);
  initEncoders();
  initKeyboard();
  initKnobs();
  //pinMode(PB0, OUTPUT);
  //inMode(PB4, INPUT_PULLUP);
  //pinMode(PB5, INPUT_PULLUP);
  tft.begin();
  tft.fillScreen(ILI9341_BLACK);
  tft.setRotation(1);
  tft.setTextSize(3);
  tft.print("the best way to  get to know a    synthesizer is to     touch it");
}

void loop()
{
  getOSC();
  sendEncoder();
  if (MUX) {
    keyDebounce();
    keyEvent();
  }
  readKnobs();
}

void getOSC()
{
  OSCMessage msgIn; //declares buffer
  uint32_t size = SLIPSerial.available();
  //uint32_t msgInSize = 0;
  while ((!SLIPSerial.endofPacket()) && (size > 0))
  {
    uint32_t size = SLIPSerial.available();
    while (size--)
    {
      msgIn.fill(SLIPSerial.read());
    }
  }
  if (!msgIn.hasError())
  {
    msgIn.dispatch("/getknobs", sendKnobs, 0);
    msgIn.dispatch("/hello", hello, 0);
    msgIn.dispatch("/encbutton", encoderRequest,0);
    msgIn.dispatch("/shutdown", shutdownPlease, 0);
    //^^^INTERFACE STUFF ABOVE
    //vvvGRAPHICS STUFF BELOW
    msgIn.dispatch("/bgfill", bgfill, 0);
    msgIn.dispatch("/invert", invertarea, 0);
    msgIn.dispatch("/waveform",waveform,0);
    msgIn.dispatch("/line",line,0);
    msgIn.dispatch("/text", text,0);
    msgIn.dispatch("/setcursor", setcursor,0);
    msgIn.dispatch("/setcolor", setcolor,0);
    msgIn.dispatch("/settextsize", settextsize,0);
    msgIn.dispatch("/rect",rect,0);
    msgIn.empty();
  }
  else {
    msgIn.empty();
  }
}

void shutdownPlease(OSCMessage &msg)
{
  digitalWrite(PC3, LOW);
  OSCMessage hello("/goodbye");
  hello.add((int32_t) 1);
  SLIPSerial.beginPacket();
  hello.send(SLIPSerial);
  SLIPSerial.endPacket();
  hello.empty();
}
uint8_t firstrun = 1; //simple flag 
uint8_t oldbuf[340];

void waveform(OSCMessage &msg)
{
  if (firstrun == 0)
  {
    int y;
    for (y = 0; y < 340-4; y++)
    {
      tft.drawLine(y, oldbuf[y+4],y+1, oldbuf[y+5], BACKGROUND); //erase the prev waveform
    }
  }
  uint8_t blobbuf[340]; //4 byte possible overflow at 320
  int x,bloblength;
  bloblength = msg.getBlob(0,blobbuf,340);
  for (x = 0; x < bloblength-4; x++)//assume first 4 are padding 
  {
    tft.drawLine(x, blobbuf[x+4],x+1, blobbuf[x+5], 2016);
    oldbuf[x+4] = blobbuf[x+4];
  }
  firstrun = 0;
}

void invertarea(OSCMessage &msg)
{
  uint16_t y,x,tmp,startx,starty,endx,endy;
  startx = msg.getInt(0);
  starty = msg.getInt(1);
  endx = msg.getInt(2);
  endy = msg.getInt(3);
  for (y = starty; y < endy; y++)
  {
    for (x = startx; x<endx; x++)
    {
      tmp =tft.readPixel(x,y);
      tft.drawPixel(x,y,~tmp);
    }
  }
}

void line(OSCMessage &msg)
{
  uint16_t x,y,xend,yend,color;
  x = msg.getInt(0);
  y = msg.getInt(1);
  xend = msg.getInt(2);
  yend = msg.getInt(3);
  color = msg.getInt(4);
  tft.drawLine(x,y,xend,yend,color);
}
void setcursor(OSCMessage &msg)
{
  uint16_t val1, val2;
  val1 = msg.getInt(0);
  val2 = msg.getInt(1);
  CURSOR[0] = val1;
  CURSOR[1] = val2;
  tft.setCursor(val1, val2);
}
void setcolor(OSCMessage &msg)
{
  uint16_t color;
  color = msg.getInt(0);
  TEXTCOLOR = color;
  tft.setTextColor(color);
}
void settextsize(OSCMessage &msg)
{
  uint8_t textsize;
  textsize = msg.getInt(0);
  TEXTSIZE = textsize;
  tft.setTextSize(textsize);
}
void hello(OSCMessage &msg)
{
  OSCMessage hello("/hello");
  hello.add((int32_t) 1);
  SLIPSerial.beginPacket();
  hello.send(SLIPSerial);
  SLIPSerial.endPacket();
  hello.empty();
}

void bgfill(OSCMessage &msg)
{
  uint16_t color;
  color = msg.getInt(0);
  BACKGROUND = color;
  tft.fillScreen(color);
}
void text(OSCMessage &msg)
{
  //first blank the line
  uint16_t blank = TEXTSIZE * 8;
  tft.fillRect(CURSOR[0],CURSOR[1],320, blank, BACKGROUND);

  
  uint8_t sizeofmessage = msg.size();//index at 1
  char bigstring[70];
  uint8_t index,tmp= 0;
  for (index = 0; index < sizeofmessage; index++)
  {
    if ( msg.isString(index) )
    {
      uint8_t datalength = msg.getDataLength(index);
      char littlestring[datalength];
      
      uint8_t stringsize = msg.getString(index, littlestring,datalength);
      if (index == 0)
      {
        strcpy(bigstring, littlestring);
        strcat(bigstring, " ");
      }
      else if ( index != 0 && index != sizeofmessage )
      {
        strcat(bigstring, littlestring);
        strcat(bigstring, " ");
      }
      else // no space at end
      {
        strcat(bigstring, littlestring);
      }
    }
    if ( msg.isInt(index) )
    {
      int n;
      char tempstr[12];
      long tempint = msg.getInt(index);
      n = sprintf(tempstr, "%d",tempint);
      snprintf(tempstr, n+1, "%d",tempint);
      if (index == 0)
      {
        strcpy(bigstring, tempstr);
        strcat(bigstring, " ");
      }
      else if ( index != 0 && index != sizeofmessage )
      {
      strcat(bigstring, tempstr);
      strcat(bigstring, " ");
      }
      else // no space at end
      {
        strcat(bigstring, tempstr);
      }
    }
    if ( msg.isFloat(index) )
    {
      int n;
      char tempstr[12];
      float tempfloat = msg.getFloat(index);
      n = sprintf(tempstr, "%5.2f",tempfloat);
      snprintf(tempstr, n, "%5.2f",tempfloat);
      if (index == 0)
      {
        strcpy(bigstring, tempstr);
        strcat(bigstring, " ");
      }
      else if ( index != 0 && index != sizeofmessage )
      {
      strcat(bigstring, tempstr);
      strcat(bigstring, " ");
      }
      else
      {
        strcat(bigstring, tempstr);
      }
    }
  }
  uint8_t i;
  char finalstring[CHARLENGTH[TEXTSIZE]];
  for (i = 0; i < CHARLENGTH[TEXTSIZE]; i++)
  {
    finalstring[i] = bigstring[i];
  }
  
  tft.print(finalstring);
}

void rect(OSCMessage &msg)
{
  uint16_t x,y,width,height,color;
  x = msg.getInt(0);
  y = msg.getInt(1);
  width = msg.getInt(2);
  height = msg.getInt(3);
  color = msg.getInt(4);
  //tft.drawRect() is just a fucking empty rect
  tft.fillRect(x,y,width, height, color);
}

void encoderRequest(OSCMessage &msg)
{
    OSCMessage msgEncoder("/encbut");
    msgEncoder.add((int32_t) digitalRead(encButton));
    SLIPSerial.beginPacket();
    msgEncoder.send(SLIPSerial);
    SLIPSerial.endPacket();
    msgEncoder.empty();
}

void encoderButton( uint16_t delaytime)
{
  uint32_t currentTime = millis();
  if (currentTime - prevTime >= delaytime) //bad debounce time on crap rotary encoder
  {
    prevTime = currentTime;

    currentButton = digitalRead(encButton);
    if (currentButton != previousButton)
    {
      if (currentButton)
      {
        OSCMessage msgEncoder("/encbut");
        msgEncoder.add((int32_t) currentButton - previousButton);
        SLIPSerial.beginPacket();
        msgEncoder.send(SLIPSerial);
        SLIPSerial.endPacket();
        msgEncoder.empty();
        previousButton = 1;

      }
      if (!currentButton)
      {
        OSCMessage msgEncoder("/encbut");
        msgEncoder.add((int32_t) previousButton - currentButton);
        SLIPSerial.beginPacket();
        msgEncoder.send(SLIPSerial);
        SLIPSerial.endPacket();
        msgEncoder.empty();
        previousButton = 0;
      }
    }

  }
}

void sendEncoder()
{
  int32_t val;
  if ((lastEncoderPos[0] != encoderpos[0]))
  {
    if ((lastEncoderPos[0] > encoderpos[0])) val = -1;
    else val = 1;
    OSCMessage msgEncoder("/enc"); //not exactly sure what organelle is sending here?
    msgEncoder.add((int32_t) val); // is it a 1 or 0?
    SLIPSerial.beginPacket();
    msgEncoder.send(SLIPSerial);
    SLIPSerial.endPacket();
    msgEncoder.empty();
    encflag[0] = LOW;
    lastEncoderPos[0] = encoderpos[0];

  }
}
void readEncoders()
{
  for (uint8_t counter = 0; counter < MAXENCODERS; counter++)
  {
    if ( (gpio_read_bit(PIN_MAP[encoderpinA[counter]].gpio_device, PIN_MAP[encoderpinA[counter]].gpio_bit) ? HIGH : LOW) != A_set[counter] )
    {
      A_set[counter] = !A_set[counter];
      if ( A_set[counter] && !B_set[counter] )
      {
        if (millis() - encodertimer > 3)
        {
          encoderpos[counter] += 1;
        }
        else
          encoderpos[counter] += 5;
      }
      encodertimer = millis();
    }
    if ( (gpio_read_bit(PIN_MAP[encoderpinB[counter]].gpio_device, PIN_MAP[encoderpinB[counter]].gpio_bit) ? HIGH : LOW) != B_set[counter] )
    {
      B_set[counter] = !B_set[counter];
      if ( B_set[counter] && !A_set[counter] )
        if (millis() - encodertimer > 3)
        {
          encoderpos[counter] -= 1;
        }
        else
          encoderpos[counter] -= 5;
      encodertimer = millis();
    }
  }
}
void initEncoders()
{
  pinMode(encButton, INPUT_PULLDOWN);
  encodertimer = millis(); // acceleration measurement
  for (byte counter = 0; counter < MAXENCODERS; counter++)
  {
    encstate[counter] = HIGH;
    encflag[counter] = HIGH;
    A_set[counter] = false;
    B_set[counter] = false;
    encoderpos[counter] = 0;
    pinMode(encoderpinA[counter], INPUT_PULLUP);
    pinMode(encoderpinB[counter], INPUT_PULLUP);
    lastEncoderPos[counter] = 1;
  }
  // timer setup for encoder
  timer.pause();
  timer.setPeriod(ENCODER_RATE); // in microseconds
  timer.setChannel1Mode(TIMER_OUTPUT_COMPARE);
  timer.setCompare(TIMER_CH1, 1);  // Interrupt 1 count after each update
  timer.attachCompare1Interrupt(readEncoders);
  timer.refresh();
  timer.resume();
}
void initKeyboard()
{
  for (uint8_t x = 0; x < sizeof(muxInputPins); x++)
  {
    pinMode(muxInputPins[x], INPUT); //external pulldowns on board
  }
  for (uint8_t b = 0; b < sizeof(muxPins); b++)
  {
    pinMode(muxPins[b], OUTPUT);
  }
  for (uint8_t a = 0; a < sizeof(keyValuesLast); a++)
  {
    keyValuesLast[a] = 0;
  }
  /* THIS SHIT WORKS BUT DISABLES SPI1
  // some dark shit to get the jtag pins to be general GPIO
  //http://stm32duino.com/viewtopic.php?t=2158
  RCC_BASE->APB2ENR |= (uint32_t)RCC_APB2ENR_AFIOEN; // enable AFIO clock
  delay(1); // maybe not needed
  AFIO_BASE->MAPR = (uint32_t)(AFIO_MAPR_SPI1_REMAP | AFIO_DEBUG_NONE); // set AFIO registerRCC_BASE->
  */

//piss directly onto me
   RCC_BASE->APB2ENR |= (uint32_t)RCC_APB2ENR_AFIOEN; // enable AFIO clock
   AFIO_BASE->MAPR = (uint32_t)(AFIO_DEBUG_NONE);
  gpio_set_mode(GPIOA, 13, GPIO_OUTPUT_PP);
  gpio_set_mode(GPIOA, 14, GPIO_OUTPUT_PP);
  gpio_set_mode(GPIOA, 15, GPIO_OUTPUT_PP);
  
}
void keyEvent()
{
  for (uint8_t x = 0; x < numberOfButtons; x++)
  {
    if (keyValues[0][x] && keyValues[1][x] && keyValues[2][x] && keyValues[3][x])
    {
      if (!keyValuesLast[x])
      {
        //Serial.println(x);
        OSCMessage msgKey("/key");
        if (x == 13) msgKey.add((int32_t) 500); // is the cursed 13 newline haunting me  (yes it is!)
        else msgKey.add((int32_t) x);
        msgKey.add((int32_t) 100);
        SLIPSerial.beginPacket();
        msgKey.send(SLIPSerial);
        SLIPSerial.endPacket();
        msgKey.empty();

        keyValuesLast[x] = 1;
      }
    }
    if (keyValues[0][x] == 0 && keyValues[1][x] == 0 && keyValues[2][x] == 0 && keyValues[3][x] == 0)
    {
      if (keyValuesLast[x])
      {
        OSCMessage msgKey("/key");
        if (x == 13) msgKey.add((int32_t) 500); // is the cursed 13 newline haunting me  (yes it is!)
        else msgKey.add((int32_t) x);
        msgKey.add((int32_t) 0);
        SLIPSerial.beginPacket();
        msgKey.send(SLIPSerial);
        SLIPSerial.endPacket();
        msgKey.empty();

        keyValuesLast[x] = 0;
      }
    }
  }
}

void keyDebounce() //debouncing method from organelle
{
  for (uint8_t t = 0; t < 4; t++)
  {
    scanKeys();
    for (uint8_t x = 0; x < numberOfButtons; x++)keyValues[t][x] = keyValuesRaw[x];
  }
}
void scanKeys() //uint8_t muxInputPins[6] = { PC11, PC12, PB3, PB4, PB5, PB6 };
{
  //for (uint8_t t = 0; t < 16; t++) //mux is 1to16
  for (uint8_t t = 0; t < 8; t++) //mux is 1to8
  {
    for (uint8_t pins = 0; pins < sizeof(muxPins); pins++)
    {
      digitalWrite(muxPins[pins], (t >> pins) & 1); //basic mux bitmath
    }
    delayMicroseconds(100); //depending on # of keys pressed, could be 1ma of current (50 seemed stable) NEEDS TO BE 100 I GUESS
    for (uint8_t x = 0; x < sizeof(muxInputPins); x++)
    {
      if (digitalRead(muxInputPins[x]) == 1) keyValuesRaw[t+(x*8)] = 1;  else keyValuesRaw[t+(x*8)] = 0;
    }
    
   // if (digitalRead(PA11)==1) keyValuesRaw[t] = 1; else keyValuesRaw[t] = 0;
   // if (digitalRead(PA7)==1) keyValuesRaw[t + 16] = 1; else keyValuesRaw[t + 16] = 0;
  }
}


void initKnobs()
{
  for (uint8_t x = 0; x < numberOfKnobs; x++)
  {
    pinMode(knobs[x], INPUT_ANALOG);
  }
}
void readKnobs()
{
  for (uint8_t x = 0; x < numberOfKnobs; x++)
  {
    knobValues[x] = analogRead(knobs[x]);
  }
}
void sendKnobs(OSCMessage &msg)
{
  OSCMessage msgKnobs("/knobs");
  for (uint8_t i = 0; i < 5; i++)
  {
    msgKnobs.add((int32_t) (knobValues[i] >> 2));
  }
  SLIPSerial.beginPacket();
  msgKnobs.send(SLIPSerial);
  SLIPSerial.endPacket();
  msgKnobs.empty();
}
