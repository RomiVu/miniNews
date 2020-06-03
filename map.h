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

vector<array<double, 2>>  getFeatureData(const vector<Point2d>& bezier){
    vector<array<double, 2>> rslt;

    for (size_t i = 1; i < bezier.size(); i++){
        rslt.push_back(array<double, 2> { bezier[i-1].x, bezier[i-1].y });
    }

    return rslt;
}

vector<array<double, 2>> getLabeldata(const vector<Point2d>& bezier){
    vector<array<double, 2>> rslt;

    for (size_t i = 1; i < bezier.size(); i++){
        rslt.push_back(array<double, 2> { bezier[i].x, bezier[i].y });
    }

    return rslt;
}
