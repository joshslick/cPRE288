#include "lcd.h"
#include "uart.h"
#include "movement.h"
#include "open_interface.h"
#include "Timer.h"
#include "adc.h"
#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <math.h>
#include "servo.h"
#include "ping.h"

/*int main(void)
{
    lcd_init();
    oi_t *sensor = oi_alloc();
    oi_init(sensor);
    uart_init(115200);
    adc_init();
    ping_init();
    servo_init();

    int degrees = 0, i, object_collision;
    float adc = 0, average_adc, distance_adc, distance_ping, average_distance, last = 0;
    unsigned int ping = 0;
    char adc_uart[20];
    char distance_uart[] = "Distance (cm)";
    char degrees_uart[] = "Degrees";
    char width_uart[] = "Width";
    int angles[40], j = 0, obj = 0, k = 0, temp;
    float object_distances[30];
    float object_distance_final[10];
    int s = 0, angle, width;
    char object_angle[10], object_width[10], input;

    // Print Header
    uart_sendStr("\n\r");
    uart_sendStr(distance_uart);
    for(i = 0; i < 15; i++) uart_sendChar(' ');
    uart_sendStr(degrees_uart);
    for(i = 0; i < 15; i++) uart_sendChar(' ');
    uart_sendStr(width_uart);
    uart_sendStr("\r\n");

    while (1) {


        scan:
        degrees = 0;
        last = 0;

        uart_sendStr("\n\rDegree | Distance (cm) | Graph\n\r");
        uart_sendStr("--------+----------------+------------------------------\n\r");

        while (degrees <= 180) {
            servo_move(degrees);
            adc = 0;
            for (i = 0; i < 3; i++) adc += adc_read();
            average_adc = adc / 3;

            ping = ping_read();
            distance_adc = (12289 * pow(average_adc, -0.861));
            distance_ping = (((float)ping / 16000000) * 34300) / 2;
            average_distance = distance_adc; // or average of both

            lcd_printf("%3.1f", average_distance);

            // UART Output with ASCII bar
            sprintf(adc_uart, "%3d°    |    %6.2f cm   | ", degrees, average_distance);
            uart_sendStr(adc_uart);

            int bar_length = (int)(average_distance / 2);
            if (bar_length > 30) bar_length = 30;
            for (i = 0; i < bar_length; i++) uart_sendChar('#');
            uart_sendStr("\r\n");

            // Object detection
            if (last - average_distance >= 10 && average_distance <= 50 && last <= 90) {
                angles[j++] = degrees;
                obj++;
                if (obj >= 5) object_distances[k++] = average_distance;
            } else if ((last - average_distance < 10) && last > 0 && obj >= 5) {
                last = average_distance;
                temp = ceil(k / 2.0) - 1;
                if (temp < 0) temp = 0;
                if (object_distances[temp] > 50 && temp > 0) temp--;

                object_distance_final[s] = object_distances[temp];
                angle = angles[(j / 2)];
                width = angles[j - 1] - angles[0];

                sprintf(adc_uart, "%6.2f", object_distance_final[s]);
                sprintf(object_angle, "%d", angle);
                sprintf(object_width, "%d", width);

                uart_sendStr("Obj @ ");
                uart_sendStr(adc_uart);
                uart_sendStr(" cm          Angle: ");
                uart_sendStr(object_angle);
                uart_sendStr("          Width: ");
                uart_sendStr(object_width);
                uart_sendStr("\r\n");

                obj = 0; j = 0; k = 0; s++;
            } else {
                j = 0; obj = 0; last = average_distance;
            }

            timer_waitMillis(200);
            degrees += 2;
        }

        // Control input loop
        while (1) {
            input = uart_receive();


            if (input == 'w') {
                object_collision = move_forward(sensor, 200);
                if (object_collision == 0) uart_sendStr("\n\rObject Hit! Please reverse");
            }
            else if (input == 'a') {
                turn_left(sensor, 90);
            }
            else if (input == 's') {
                move_backward(sensor, 200);
            }
            else if (input == 'd') {
                turn_right(sensor, 90);
            }
            else if (input == 'q') {
                goto done;
            }
            else if (input == 'm') {
                goto scan;
            }
            else if (input == 'c') {
                oi_update(sensor);
                if (sensor->cliffFrontLeftSignal < 1000 || sensor->cliffFrontRightSignal < 1000 ||
                    sensor->cliffLeftSignal < 1000 || sensor->cliffRightSignal < 1000) {
                    uart_sendStr("\n\rCliff Detected (drop-off)");
                } else {
                    uart_sendStr("\n\rNo Cliff Detected - Safe");
                }
            }
        }
    }

    done:
    oi_free(sensor);
    return 0;
}*/
