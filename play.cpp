//
//  亮度感測
//
#include <iostream>
#include <wiringPi.h>
#include <mcp3004.h>
#include <wiringPi.h>
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>

using namespace std;

#define threshold 495 // 請修改此數值

// 調整伺服馬達移動角度
#define key_down 15
#define key_up 0

#define BASE 200   // SPI介面設定
#define SPI_CHAN 0 // 使用CH0

const int channel = 0;

const int motor = 1;    // WiringPi 編號 1，對應 GPIO18
const int minPwm = 50;  // 對應 1ms 脈寬（50）
const int maxPwm = 250; // 對應 2ms 脈寬（250）

void Press() {
    // angle 0~15
    int start_angle = press_up;
    int end_angle = press_down;
    int pwmValue = minPwm + (end_angle * (maxPwm - minPwm) / 180);
    pwmWrite(motor, pwmValue);
    delay(100);
    pwmValue = minPwm + (start_angle * (maxPwm - minPwm) / 180);
    pwmWrite(motor, pwmValue);
}

int main(void)
{
    cout << "Light Sensing" << endl;

    if (wiringPiSetup() == -1) // 設定WiringPi
        return 0;

    int count = 0 ;
    mcp3004Setup(BASE, SPI_CHAN); // 3004與3008為相同系列IC

    while (1) {
        int x = analogRead(BASE + channel); // 讀取類比輸入
        if (x > threshold) {
            cout << "Jump" << count << endl ;
            Press();
            count++ ;
        }
        //   cout << "Analog Value = " << x << endl;
        delay(50);
    }
    return 1;
}
