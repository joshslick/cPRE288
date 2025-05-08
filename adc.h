/*
 * adc.h
 *
 *  Created on: Mar 25, 2025
 *      Author: jossli01
 */

#ifndef ADC_H_
#define ADC_H_
#include <inc/tm4c123gh6pm.h>
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include "Timer.h"

void adc_init(void);
int adc_read(void);


#endif
