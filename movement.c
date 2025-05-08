#include "movement.h"
#include "open_interface.h"
#include "lcd.h"
#include "uart.h"
#include <math.h>

double move_forward(oi_t *self, float centimeters){
    double distance = 0;
    oi_setWheels(200, 200);
    while(distance < centimeters){
        oi_update(self);
        if(self->bumpLeft ||self->bumpRight ){
            oi_setWheels(0, 0);
            return distance;
            }
        else if (self->cliffFrontLeftSignal < 1000 || self->cliffFrontRightSignal < 1000 ||
                self->cliffLeftSignal < 1000 || self->cliffRightSignal < 1000) {
                oi_setWheels(0, 0);
                uart_sendStr("\n\rCliff Detected (drop-off)");
                return distance;
            }
        distance += self->distance;
        }
       oi_setWheels(0, 0);
       return distance;
}
void move_backward(oi_t *self, float centimeters){
    double distance = 0;
    oi_setWheels(-200, -200);
    while(distance < centimeters){

        oi_update(self);
        distance -= self->distance;
    }
    oi_setWheels(0, 0);

}


void turn_left(oi_t *self, double degrees){
    lcd_init();
    oi_setWheels(-50, 50);
    oi_update(self);
    double angle = 0;
    degrees *= -1;
    while(angle > degrees){

        oi_update(self);
        angle += self->angle;
        }
    lcd_printf("%f", angle);
    oi_setWheels(0, 0);
}

void turn_right(oi_t *self, double degrees){
    oi_setWheels(50, -50);
    oi_update(self);
    double angle = 0;
    while(angle < degrees){

        oi_update(self);
        angle += self->angle;
        }
    oi_setWheels(0, 0);
}
