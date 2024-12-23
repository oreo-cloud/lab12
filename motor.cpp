#include <wiringPi.h>
#include <iostream>
#include <chrono>
#include <iomanip>
#include <sstream>

using namespace std;

const int motor = 1;   // WiringPi 編號 1，對應 GPIO18
const int minPwm = 50; // 對應 1ms 脈寬（50）
const int maxPwm = 250; // 對應 2ms 脈寬（250）

void setServoAngle(int angle) {
    if (angle < 0 || angle > 180) {
        cout << "Invalid angle! Please enter a value between 0 and 180." << endl;
        return;
    }

    // 將校準後的角度映射到 PWM 值
    int pwmValue = minPwm + (angle * (maxPwm - minPwm) / 180);
    pwmWrite(motor, pwmValue);
    cout << "Servo angle set to " << angle << ", PWM: " << pwmValue << endl;
}

int main(void) {
    cout << "SG90 Servo Motor Angle Control with Hardware PWM (Non-linear Calibration)" << endl;

    if (wiringPiSetup() == -1) {
        cout << "WiringPi setup failed!" << endl;
        return 1;
    }

    pinMode(motor, PWM_OUTPUT); // 設定 GPIO18（WiringPi 1）為硬體 PWM

    // 設定硬體 PWM 時鐘和範圍
    pwmSetMode(PWM_MODE_MS);    // 使用標準 PWM 模式
    pwmSetRange(2000);          // 設定範圍為 2000（對應 20ms 週期）
    pwmSetClock(192);           // 設定時鐘為 192（19.2MHz / 192 = 100kHz）

    while (true) {
        int angle;
        cout << "Enter the servo angle (0-180): ";
        cin >> angle;

        setServoAngle(angle);
        delay(500); // 延遲 0.5 秒
    }

    return 0;
}