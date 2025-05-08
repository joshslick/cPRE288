
#include "uart.h"
#include <math.h>

void uart_init(int baud){
    SYSCTL_RCGCGPIO_R |= 0b00000010;      // enable clock GPIOB (page 340)
    SYSCTL_RCGCUART_R |= 0b00000010;      // enable clock UART1 (page 344)
    GPIO_PORTB_AFSEL_R = 0b00000011;      // sets PB0 and PB1 as peripherals (page 671)
    GPIO_PORTB_PCTL_R  = 0x00000011;       // pmc0 and pmc1       (page 688)  also refer to page 650
    GPIO_PORTB_DEN_R   = 0b00000011;        // enables pb0 and pb1
    GPIO_PORTB_DIR_R   = 0b00000001;        // sets pb0 as output, pb1 as input

    //compute baud values [UART clock= 16 MHz]
    double fbrd;
    int    ibrd;
    double brd;
    brd = (16000000) / (16*baud); // page 903
    ibrd = floor(brd);
    fbrd = round((brd - ibrd) * 64 + 0.5);


    UART1_CTL_R &= 0xFFFFFFFE;      // disable UART1 (page 918)
    UART1_IBRD_R = 0x8;        // write integer portion of BRD to IBRD
    UART1_FBRD_R = 0x2C;   // write fractional portion of BRD to FBRD
    UART1_LCRH_R = 0b01100000;        // write serial communication parameters (page 916) * 8bit and no parity
    UART1_CC_R   = 0x0;          // use system clock as clock source (page 939)
    UART1_CTL_R |= 0x00000001;        // enable UART1
}

void uart_sendChar(char data){
	while((UART1_FR_R & 0b00100000) != 0){
	}
	UART1_DR_R = data;
}

char uart_receive(void){
	uint32_t temp;
	char data;
	int timer = 0;
	while((UART1_FR_R & 0b00010000) != 0){
	        if(timer >= 10){
	            return 'f';
	        }
	        timer +=1;
	    }
	temp = UART1_DR_R;
	if(temp & 0xF00){
	    GPIO_PORTF_DATA_R = 0xF;
	}else{
	    data =  (char) UART1_DR_R & 0xFF;
	}
	return data;

}

void uart_sendStr(const char *data){
    int i;
           for (i = 0; i < strlen(data); i++) {
               uart_sendChar(data[i]);

           }
}
