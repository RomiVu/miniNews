#pragma once
#include <iostream>
#include <vector>
#include <cmath>

using namespace std;

struct Point2d {
     double x;
     double y;
     Point2d() : x(0.0), y(0.0) {}
     Point2d(double a, double b) : x(a), y(b)   {} 
     Point2d(const Point2d &p) : x(p.x), y(p.y)  {}
     Point2d operator + (const Point2d& p) const { return Point2d(x+p.x, y+p.y); } 
     Point2d operator - (const Point2d& p) const { return Point2d(x-p.x, y-p.y); }
     Point2d operator * (double c) const { return Point2d(x*c, y*c); }
     Point2d operator / (double c) const { return Point2d(x/c, y/c); }

};

    
ostream& operator<< (ostream &out, const Point2d& p) { 
    out.precision(10);
    out << "Point(" << p.x << ", " << p.y << ")";
    return out;
}


struct Line2d {
     Point2d s;
     Point2d e;
     Point2d v; // vector
     Line2d() : s(0, 0), e(0, 0), v(0, 0) {}
     Line2d(const Point2d& a, const Point2d& b) : s(a), e(b), v(a-b) {} 
     Line2d(const Line2d& line) : s(line.s), e(line.e), v(line.v) {}
     Line2d operator + (const Line2d& line) const { return Line2d(s+line.s, e+line.e); } 
     Line2d operator - (const Line2d& line) const { return Line2d(s-line.s, e-line.e); }
     Line2d operator * (double c) const { return Line2d(s*c, e*c); }
     Line2d operator / (double c) const { return Line2d(s/c, e/c); }

     bool isVerticaltoX()  {  return v.x == 0;}
     bool isVerticaltoY()  {  return v.y == 0; }
    
};

ostream& operator<< (ostream &out, const Line2d& line) { 
    out.precision(10);
    out << "Line: ( " << line.s  <<  ", " << line.e  <<" ) and vector: " << line.v;
    return out;
}


vector<Point2d> getBezierCurve(const Point2d& p0, const Point2d& p1, const Point2d& p2, size_t num){
    vector<Point2d> rslt;

    for (size_t i=0; i<num ; ++i){
        double t = double(i) / double(num);

        double a = (1.0 - t)* (1.0 - t);
        double b = 2.0 * t * (1 - t);
        double c = t*t;
        Point2d temp = p0 * a + p1 * b + p2 * c;
        // cout.precision(10);
        // cout << "t, a, b, c=" << t << ' '<<  a << ' ' << b << ' ' << c << ", beizer curve point: "<<  temp << endl;
        rslt.push_back(temp);
    }
    return rslt;
}

vector<array<double, 3>> getTrainData(const vector<Point2d>& bezier, int xory){
    // xory == 0, for x, else for y;
    vector<array<double, 3>> rslt;

    if (xory == 0) {
        for (size_t i = 1; i < bezier.size(); i++){
            rslt.push_back(array<double, 3> { bezier[i].x, bezier[i-1].x, bezier[i-1].y });
        }
    } else {
        for (size_t i = 1; i < bezier.size(); i++){
            rslt.push_back(array<double, 3> { bezier[i].x, bezier[i-1].x, bezier[i-1].y });
        }
    }
    return rslt;
}



class Weights{
    public:
        vector<double> values { 0.0, 0.0 };
        double intercption = 0.0;
        size_t number = 2;

        void update(const vector<array<double, 3>>& data, const vector<double>& y_pred, double learning_rate);
};

void Weights::update(const vector<array<double, 3>>& data, const vector<double>& y_pred, double learning_rate){
    double dev_b; 
    double dev_w0;
    double dev_w1;

    for(size_t i=0; i<data.size(); i++){
        dev_b += (-2) * (data[i][0] - y_pred[i]);
        dev_w0 += (-2) * data[i][1] * (data[i][0] - y_pred[i]);
        dev_w1 += (-2) * data[i][2] * (data[i][0] - y_pred[i]);
    }
     
    intercption = (fabs(dev_b) > learning_rate ? intercption - dev_b : intercption) ;
    values[0] = (fabs(dev_w0) > learning_rate ? values[0] - dev_w0 : values[0]) ;
    values[1] = (fabs(dev_w1) > learning_rate ? values[1] - dev_w1 : values[1]) ;
}


class LinearRegression{
        
    private:
        vector<array<double, 3>> data;
        Weights weights;
        // fit a line given some x and weights
        void fit(vector<double>& y_pred){
            for(size_t i = 0; i < data.size(); i++){
                y_pred[i] = predict(data[i]);
            }
        }


    public:
        // Constructor
        LinearRegression(const vector<array<double, 3>>& data_train);

        double predict(const array<double, 3>& record){
            double prediction = 0.0;
            for(size_t i = 0; i < weights.number; i++){
                prediction += weights.values[i] * record[i+1];
            }
            return prediction + weights.intercption;
        }

        double predict(double x, double y){
            return x * weights.values[0] + y * weights.values[1] + weights.intercption;
        }

        // Train the regression model with some data
        void train(size_t max_iteration, double learning_rate){

            // Mallocating some space for prediction
            vector<double> y_predition(data.size(), 0.0);

            while(max_iteration > 0){
                fit(y_predition);
                weights.update(data, y_predition, learning_rate);
                max_iteration--;
            }
        }
};


LinearRegression::LinearRegression(const vector<array<double, 3>>& data_train) {
    for (size_t i = 0; i < data_train.size(); i++){
        data.push_back(array<double, 3> { data_train[i][0] , data_train[i][1], data_train[i][2] });
    }
}