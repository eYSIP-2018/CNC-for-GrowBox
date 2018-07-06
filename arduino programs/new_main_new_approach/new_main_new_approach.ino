

// for encoder reference https://www.youtube.com/watch?v=S1JJc8YAJqQ

#define solenoidpin1 32   // these pins are used to control the solenoid
#define solenoidpin2 33

// pins of motor in x direction
#define mxen_a 4        // pwm pin 
#define mxa1 22         // pin1
#define mxa2 23         // pin2
#define encoderPin1_x 3  // encoder A signal
#define encoderPin2_x 2  // encoder B signal

// pins of motor in y direction
#define myen_b 5      // pwm pin 
#define myb1 24       // pin 1
#define myb2 25       // pin 2
#define encoderPin1_y 21    // encoder A signal
#define encoderPin2_y 20    // encoder B signal

// pins of motor in z direction
#define mzen_a 6    // pwm pin
#define mza1 27     // pin 1
#define mza2 26     // pin 2
#define encoderPin1_z 18    // encoder A signal
#define encoderPin2_z 19    // encoder B signal

// vaccum pump 
#define v_pump_en 7       // pwm pin
#define v_pump_b1 28      // pin 1
#define v_pump_b2 29      // pin 2




long count_x=0,count_y=0,count_z=0;    // encoder counts intialization
unsigned long timep,timec,etime;       // provision if we want to take track of time 
byte state_x ,statep_x,state_y,statep_y,state_z,statep_z;  
boolean A_x,B_x,A_y,B_y,A_z,B_z;    //input variables of encoders
volatile int QEM[16]={0,-1,0,1,1,0,-1,0,0,1,0,-1,-1,0,1,0};  // encoder count change descision table
volatile int index_x,index_y,index_z; //indices to access values of the QEM array

float rot_deg_x=0,rot_deg_y=0,rot_deg_z=0;// intialisation of degrees rotated
int CPR_x=29520,CPR_y=29520,CPR_z=29520;  // declaration of counts per revolution of encoders

/* actual linear distance variables 
 *  current=current co-ordinate 
 *  target=the coordinate where you want to go
*/

float x_current=0,x_past=0,x_target=0;   
float y_current=0,y_past=0,y_target=0;
float z_current=0,z_past=0,z_target=0;

char data[15];  // raw input string from rpi
int str[15];  // processed input string 

int water,seed;

void state_change_x()   // ISR for encoder x
{
 A_x=digitalRead(encoderPin1_x);
 B_x=digitalRead(encoderPin2_x);

  if( (A_x==HIGH) && (B_x==HIGH) ) state_x=0;
  if( (A_x==HIGH) && (B_x==LOW) ) state_x=1;
  if( (A_x==LOW) && (B_x==LOW) ) state_x=2;
  if( (A_x==LOW) && (B_x==HIGH) ) state_x=3;

 index_x=4*state_x+statep_x;  
 count_x=count_x+QEM[index_x];
 statep_x=state_x;
}

void state_change_y()   // ISR for encoder y
{
 A_y=digitalRead(encoderPin1_y);
 B_y=digitalRead(encoderPin2_y);

  if( (A_y==HIGH) && (B_y==HIGH) ) state_y=0;
  if( (A_y==HIGH) && (B_y==LOW) ) state_y=1;
  if( (A_y==LOW) && (B_y==LOW) ) state_y=2;
  if( (A_y==LOW) && (B_y==HIGH) ) state_y=3;

 index_y=4*state_y+statep_y;
 count_y=count_y+QEM[index_y];
 statep_y=state_y;
}

void state_change_z()     // ISR for encoder z
{
 A_z=digitalRead(encoderPin1_z);
 B_z=digitalRead(encoderPin2_z);

  if( (A_z==HIGH) && (B_z==HIGH) ) state_z=0;
  if( (A_z==HIGH) && (B_z==LOW) ) state_z=1;
  if( (A_z==LOW) && (B_z==LOW) ) state_z=2;
  if( (A_z==LOW) && (B_z==HIGH) ) state_z=3;

 index_z=4*state_z+statep_z;
 count_z=count_z+QEM[index_z];
 statep_z=state_z;
}


void setup() 
{
  Serial.begin (9600);
   pinMode(solenoidpin1, OUTPUT);
   pinMode(solenoidpin2, OUTPUT);
   
  pinMode(mxen_a,OUTPUT);
  pinMode(mxa1,OUTPUT);
  pinMode(mxa2,OUTPUT);
  pinMode(encoderPin1_x, INPUT_PULLUP); 
  pinMode(encoderPin2_x, INPUT_PULLUP);
  
  pinMode(myen_b,OUTPUT);
  pinMode(myb1,OUTPUT);
  pinMode(myb2,OUTPUT);
  pinMode(encoderPin1_y, INPUT_PULLUP); 
  pinMode(encoderPin2_y, INPUT_PULLUP);
  
  pinMode(mzen_a,OUTPUT);
  pinMode(mza1,OUTPUT);
  pinMode(mza2,OUTPUT);
  pinMode(encoderPin1_z, INPUT_PULLUP); 
  pinMode(encoderPin2_z, INPUT_PULLUP);

  pinMode(v_pump_en,OUTPUT);
  pinMode(v_pump_b1,OUTPUT);
  pinMode(v_pump_b2,OUTPUT);
  
  
 timep=micros();
 
  A_x=digitalRead(encoderPin1_x);
  B_x=digitalRead(encoderPin2_x);

// intialisation of state of encoder of motor x

  if( (A_x==HIGH) && (B_x==HIGH) ) state_x=0;
  if( (A_x==HIGH) && (B_x==LOW) ) state_x=1;
  if( (A_x==LOW) && (B_x==LOW) ) state_x=2;
  if( (A_x==LOW) && (B_x==HIGH) ) state_x=3;
 
  A_y=digitalRead(encoderPin1_y);
  B_y=digitalRead(encoderPin2_y);

// intialisation of state of encoder of motor y
  if( (A_y==HIGH) && (B_y==HIGH) ) state_y=0;
  if( (A_y==HIGH) && (B_y==LOW) ) state_y=1;
  if( (A_y==LOW) && (B_y==LOW) ) state_y=2;
  if( (A_y==LOW) && (B_y==HIGH) ) state_y=3;
  
  A_z=digitalRead(encoderPin1_z);
  B_z=digitalRead(encoderPin2_z);

// intialisation of state of encoder of motor z
  if( (A_z==HIGH) && (B_z==HIGH) ) state_z=0;
  if( (A_z==HIGH) && (B_z==LOW) ) state_z=1;
  if( (A_z==LOW) && (B_z==LOW) ) state_z=2;
  if( (A_z==LOW) && (B_z==HIGH) ) state_z=3;

  // inturrupts 0,1,2,3,4,5,6  corresponds to 2,3,21,20,19,18 respectively 
  attachInterrupt(0, state_change_x, CHANGE); 
  attachInterrupt(1, state_change_x, CHANGE);
  
  attachInterrupt(2, state_change_y, CHANGE); 
  attachInterrupt(3, state_change_y, CHANGE);
  
  
  attachInterrupt(4, state_change_z, CHANGE); 
  attachInterrupt(5, state_change_z, CHANGE);
  
  digitalWrite(solenoidpin1,HIGH);
  digitalWrite(solenoidpin2,HIGH);

}

void loop()
{
 
  //input:
  for(int i=0;i<=14;i++)   // input string from rpi
  {
   while(Serial.available()==0) {}
   data[i]=Serial.read();
   if(data[i]=='!')
      {
          //if(i!=14) {Serial.println("Sorry, data lost or incorrect data"); goto input;}
          break;
      } 
  }
 
 /*  Serial.print("Data received is :");
  for(int i=0;i<=14;i++)
  {
   Serial.print(data[i]);
  }
  
  Serial.println("");*/ 
  
  if(data[0]=='@' && data[14]=='!')  
  {
    get_parameters();// function call to set parameters and string processing 
    
    if(str[13]==1 || str[13]==2)      //  co-ordinate system initialisation 
    {


      rot_deg_x=x_target*360/(20*7.9);
      count_x=rot_deg_x*CPR_x/360; 

        rot_deg_y=y_target*360/(20*8);
      count_y=rot_deg_y*CPR_y/360; 
      
         rot_deg_z=z_target*360/(8);
      count_z=rot_deg_z*CPR_z/360;
       // goto input;
    }
  /*  
    Serial.print("x : ");
    Serial.println(x_current);
    Serial.print("y : ");
    Serial.println(y_current);
    Serial.print("z : ");
    Serial.println(z_current);
    Serial.print("water  : ");
    Serial.println(water);
    Serial.print("seed : ");
    Serial.println(seed);*/
    
    
    // function calls according to inputs in string 
    
     if(seed==1) start_seeder();
     
     if(str[13]==0 || str[13]==2)
     {
             if(x_target!=x_current)  go_to_x(x_target);
            if(y_target!=y_current)   go_to_y(y_target);
            if(z_target!=z_current)   go_to_z(z_target);
     }
     
   
    
    
    if(seed==1)
    {
      digitalWrite(v_pump_b1,LOW); // pump  off after going to perfect location
      digitalWrite(v_pump_b2,LOW);
    }
    
    if(water==1) start_water();
   
      /*
       Serial.println("   you are now at :    "  );
       Serial.print("x = ");
       Serial.println(x_current);
       Serial.print("y = ");
       Serial.println(y_current);
       Serial.print("z = ");
       Serial.println(z_current);
       */
      timec=micros();
      etime=timec-timep;
      if(etime>1000000) 
      {
        // Serial.println(count);
          //rot_deg=count*360/(CPR);
          //Serial.println(rot_deg);
         timep=timec;  
      }
    }
     
 
  

Serial.write("@done!\n");
}

void get_parameters()  // This function processes input string from rpi and coverts the ascii data into int data string and sets parameters which are to be sent to different functions
{
 for(int i=0;i<=14;i++)
  {
    str[i]=(data[i])-48;  // conversion from ascii to int 
  }
    x_target=1000*str[1]+100*str[2]+10*str[3]+1*str[4];
    y_target=100*str[5]+10*str[6]+1*str[7];
    z_target=100*str[8]+10*str[9]+1*str[10];
    
    water=str[11];
    seed=str[12];
    
    if(str[13]==2)   // if we want to move in -ve direction explicitly 
    {
          x_target=-1*x_target;
          y_target=-1*y_target;
          z_target=0;
    }
   
}

void go_to_x(float x_target)  // This function takes input of x-coordinate where we need to go and get us there
{

            
          
     if(x_target>x_current)
       {
            while(x_target>x_current)  //forward or in positive direction  or clockwise
            {
               digitalWrite(mxa1,HIGH);
               digitalWrite(mxa2,LOW);
               analogWrite(mxen_a,200);               
              rot_deg_x=count_x*360/(CPR_x);             
              x_current=rot_deg_x*(20*7.9)/(360);        //  x=deg*no of teeth*pitch/360
            } 
       }  
       else if(x_target<x_current)
       {
            while(x_target<x_current)  //backward or in negative direction  or anti-clockwise
              {
                 digitalWrite(mxa1,LOW);
                 digitalWrite(mxa2,HIGH);
                 analogWrite(mxen_a,200);
                rot_deg_x=count_x*360/(CPR_x);
                x_current=rot_deg_x*(20*9.2)/(360);        //  x=deg*no of teeth*pitch/360
              } 
       }
           digitalWrite(mxa1,LOW);
           digitalWrite(mxa2,LOW);
     
        
}

void go_to_y(float y_target) // This function takes input of y-coordinate where we need to go and get us there
{

          
       if(y_target>y_current)
       {   
              while(y_target>y_current)  //forward or in positive direction  or clockwise
              {
                 digitalWrite(myb1,HIGH);
                 digitalWrite(myb2,LOW);
                 analogWrite(myen_b,200);
                rot_deg_y=count_y*360/(CPR_y);
                y_current=rot_deg_y*(20*8)/(360);        //  y=deg*no of teeth*pitch/360
              } 
       }  

       else if(y_target<y_current)
       {
          while(y_target<y_current)  //backward or in negative direction  or anti-clockwise
            {
               digitalWrite(myb1,LOW);
               digitalWrite(myb2,HIGH);
               analogWrite(myen_b,200);
              rot_deg_y=count_y*360/(CPR_y);
              y_current=rot_deg_y*(20*8.35)/(360);        //  y=deg*no of teeth*pitch/360
            } 
       }
           digitalWrite(myb1,LOW);
           digitalWrite(myb2,LOW);
          
         
}


void go_to_z(float z_target) // This function takes input of z-coordinate where we need to go and get us there
{

         
        if(z_target>z_current)
        {
                while(z_target>z_current)  //forward or in positive direction  or clockwise
                {
                   digitalWrite(mza1,HIGH);
                   digitalWrite(mza2,LOW);
                   analogWrite(mzen_a,255);
                  rot_deg_z=count_z*360/(CPR_z);
                  z_current=rot_deg_z*(8)/(360);        //  z=deg*no of teeth*pitch/360
                } 
        } 

        else if (z_target<z_current)
        {
              while(z_target<z_current)  //backward or in negative direction  or anti-clockwise
                {
                   digitalWrite(mza1,LOW);
                   digitalWrite(mza2,HIGH);
                   analogWrite(mzen_a,255);
                  rot_deg_z=count_z*360/(CPR_z);
                  z_current=rot_deg_z*(8)/(360);        //  z=deg*no of teeth*pitch/360
                } 
        }
        
           digitalWrite(mza1,LOW);
           digitalWrite(mza2,LOW);
         
}

void start_seeder()   // function to seed plants  i.e to actuate the vacumm pump 
{    
        go_to_x(50);   // going to location of seed compartment 
        go_to_y(225);
        go_to_z(100);
       digitalWrite(v_pump_b1,LOW);  // vaccum pump starts and picks up seed
      digitalWrite(v_pump_b2,HIGH);
      analogWrite(v_pump_en,255); 
      delay(5000);
      go_to_z(0);     //arm retracting 
  
}

void start_water()  //function to water the plants i.e. to actuate the solenoid valve
{
   digitalWrite(solenoidpin1,LOW);
   digitalWrite(solenoidpin2,LOW);
   delay(2000);
   digitalWrite(solenoidpin1,HIGH);
   digitalWrite(solenoidpin2,HIGH);
   
}


