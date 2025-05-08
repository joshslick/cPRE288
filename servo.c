#include "servo.h"
#include "Timer.h"
#include "button.h"
#include <stdbool.h>
#include <stdio.h>
// Global shared variables
// Use extern declarations in the header file


int clockwise = 0;
void servo_init (void){

  // YOUR CODE HERE
    SYSCTL_RCGCGPIO_R |= 0x02;
       SYSCTL_RCGCTIMER_R |= 0x02;

       while((SYSCTL_PRTIMER_R & 0x02) != 0x02){};
       while((SYSCTL_PRGPIO_R & 0x02) != 0x02){};

       GPIO_PORTB_DIR_R |= 0x20;
       GPIO_PORTB_DEN_R |= 0x20;
       GPIO_PORTB_AFSEL_R |= 0x20;
       GPIO_PORTB_PCTL_R |= 0x00700000;

       TIMER1_CTL_R &= 0xFEFF;
       TIMER1_CFG_R |= 0x4;
       TIMER1_TBMR_R |= 0xA;

       int pulse_period = 320000;

       TIMER1_TBILR_R = pulse_period & 0xFFFF;
       TIMER1_TBPR_R = pulse_period >> 16;
       TIMER1_CTL_R |= 0x0100;
}
int button1(int button, int angle){


    int i = 0;
        if(button == 1 && clockwise == 0){
            servo_move(angle+=1);
        }
        else if(button == 1 && clockwise == 1){
            servo_move(angle-=1);
        }
        else if(button == 2 && clockwise == 0){
                    servo_move(angle+=5);
                }
        else if(button == 2 && clockwise == 1){
                            servo_move(angle-=5);
                        }
        else if(button == 3 && clockwise == 0){
            clockwise = 1;
        }
        else if(button == 3 && clockwise == 1){
                    clockwise = 0;
                }
        else if(button == 4 && clockwise == 0){
            servo_move(5);
            angle = 5;
        }
        else if(button == 4 && clockwise == 1){
            servo_move(175);
                    angle = 175;
                }




        return angle;
}
void servo_move(uint16_t degrees){
    unsigned int turn = degrees*(133) + 10000;
        TIMER1_TBMATCHR_R = (320000 - turn) & 0xFFFF;
        TIMER1_TBPMR_R = (320000 - turn) >> 16;
}
