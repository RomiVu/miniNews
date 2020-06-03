#include <iostream>
#include <vector>
#include <array>
#include <fstream>

#include "map.h"
#include "json.h"
#include "linearregression.h"

using namespace std;
using json = nlohmann::json;



int main(){
    Point2d a(0, 100);
    Point2d b(100, 100);
    Point2d c(100, 0);
    
    vector<Point2d> rslt;
  
    rslt = getBezierCurve(a, b, c, 100);
    
    // label feature1 feature2
    vector<array<double, 2>> features = getFeatureData(rslt);
    vector<array<double, 2>> labels = getLabeldata(rslt);

    json jsonfile;

    auto line1 = json::array();
    line1.push_back(json::array( {0, 0} ));
    line1.push_back(json::array( {0, 200} ));

    auto line2 = json::array();
    line2.push_back(json::array( {0, 0} ));
    line2.push_back(json::array( {200, 0} ));

    jsonfile["line1"] = line1;
    jsonfile["line2"] = line2;
 
    jsonfile["p0"] = json::array({ 100, 100 }); // control  point
    jsonfile["p1"] = json::array({ 0, 100 });// mid point of l1
    jsonfile["p2"] = json::array({ 100, 0 });// mid point of l2

    cout << " getTrainData here no plobrem..." << features.size() << endl;

    jsonfile["features"] = json::array();
    jsonfile["labels"] = json::array();

    for(int i=0; i< features.size(); i++){
        // cout << "getTrainData features: "<< data[i][0] << ' ' <<  data[i][1] << " --- label: " << data[i][2] << ' ' << data[i][3] <<  endl;
        jsonfile["features"].push_back(json::array( {features[i][0], features[i][1]}));
    }

    for(int i=0; i< labels.size(); i++){
        // cout << "getTrainData features: "<< data[i][0] << ' ' <<  data[i][1] << " --- label: " << data[i][2] << ' ' << data[i][3] <<  endl;
        jsonfile["labels"].push_back(json::array( {labels[i][0], labels[i][1]}));
    }

    string filename = "data.json";
    ofstream file(filename);
    file << setw(4) << jsonfile << endl;
    file.close();

    cout << "Saved successfully at " << filename << endl;

    LinearRegression lr (features, labels);

    return 0;
}

