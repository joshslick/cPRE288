/**
 * lab5_template.c
 *
 * Template file for CprE 288 Lab 5
 *
 * @author Zhao Zhang, Chad Nelson, Zachary Glanz
 * @date 08/14/2016
 *
 * @author Phillip Jones, updated 6/4/2019
 * @author Diane Rover, updated 2/25/2021, 2/17/2022
 */


#include "timer.h"
#include "lcd.h"

#include "uart.h"  // Functions for communicating between CyBot and Putty (via UART1)
                         // PuTTy: Baud=115200, 8 data bits, No Flow Control, No Parity, COM1

#include "ping.h"  // Scan using CyBot servo and sensors



#define REPLACEME 0


int main(void) {
    uart_init(115200);
	timer_init(); // Must be called before lcd_init(), which uses timer functions
	lcd_init();

	char my_data;
	char command[100];
	int index = 0;

	lcd_printf("Running");

	while(1){
	    index = 0;
	    my_data = uart_receive();

	    while(my_data != '\n'){
	        command[index] = my_data;
	        index++;
	        my_data = uart_receive();
	    }

	    command[index] = '\n';
	    command[index+1] = 0;

	    lcd_printf("Got: %s", command);

	    uart_sendChar(command[0]);

	    if(command[0] != '\n'){
	        uart_sendChar('n');
	    }

	}
	return;
}
