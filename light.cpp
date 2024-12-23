//
//  亮度感測
//
#include <iostream>
#include <wiringPi.h>
#include <mcp3004.h>

using namespace std;

#define BASE 200    // SPI介面設定
#define SPI_CHAN 0  // 使用CH0

const int channel = 0 ;

int main(void)
{
   cout << "Light Sensing" << endl;
    
   if (wiringPiSetup () == -1)  // 設定WiringPi  
      return 0;

   mcp3004Setup(BASE, SPI_CHAN);  // 3004與3008為相同系列IC

   while(1) {
      int x = analogRead(BASE + channel) ;  // 讀取類比輸入
      cout << "Analog Value = " << x << endl;
		 delay(500);
 }
    return 1;
}
