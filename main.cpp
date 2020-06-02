#include <iostream>
#include <vector>
#include <array>

#include "map.h"

using namespace std;


int main(){
    Point2d a(0, 100);
    Point2d b(100, 100);
    Point2d c(100, 0);
    
    vector<Point2d> rslt;
  
    rslt = getBezierCurve(a, b, c, 200);
    
    // label feature1 feature2
    vector<array<double, 3>> train_data_x = getTrainData(rslt, 0);
    vector<array<double, 3>> train_data_y = getTrainData(rslt, 1); 
    

    cout << "here no plobrem..." << train_data_x.size() << endl;
    
    // for(int i =0; i< train_data_x.size(); i++){
    //     cout << "getTrainData for x: "<< train_data_x[i][0] << ' ' <<  train_data_x[i][1] << ' ' << train_data_x[i][2] << endl;
    // }

    LinearRegression lr (train_data_x);
    lr.train(1000, 0.001);
    
    cout << "hreer  no plreasds " << endl;

    cout.precision(10);
    cout<< lr.predict(40, 60) << endl;

    return 0;
}