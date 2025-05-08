/*
 * adc.c
 *
 *  Created on: Mar 25, 2025
 *      Author: jossli01
 */
#include "adc.h"
void adc_init(void){
    SYSCTL_RCGCGPIO_R |= 0b00011010;
    SYSCTL_RCGCADC_R  |= 0x01;
    GPIO_PORTB_AFSEL_R |= 0b00010000;
    GPIO_PORTB_DIR_R &= 0b11101111;
    GPIO_PORTB_DEN_R &= 0b11101111;
    GPIO_PORTB_AMSEL_R |= 0b00010000;
    GPIO_PORTB_ADCCTL_R = 0x00;
    ADC0_ACTSS_R &= 0b0000;
    ADC0_EMUX_R |= ADC_EMUX_EM1_PROCESSOR;
    ADC0_SSMUX1_R = 0xA;
    ADC0_SSCTL1_R |= 0x0006;
    ADC0_SAC_R = 0x6;
    ADC0_ACTSS_R |= 0b0010;
}
int adc_read(void){
    int data;
    ADC0_PSSI_R = ADC_PSSI_SS1;
    while((ADC0_RIS_R & 2) == 0){

    }

    data = ADC0_SSFIFO1_R;
    return data;
}
