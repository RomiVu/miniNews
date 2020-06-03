#ifndef LINEARREGRESSION_HPP
#define LINEARREGRESSION_HPP

#include <vector>
#include <array>
#include <iostream>

#include <Eigen/Dense>
#include <Eigen/Core>
#include <unsupported/Eigen/MatrixFunctions>

using namespace std;

Eigen::VectorXd GetMean( const Eigen::MatrixXd & m );
Eigen::VectorXd GetStandardDeviation( Eigen::MatrixXd & m, const Eigen::VectorXd & mean );


class LinearRegression{
private:
	vector<array<double, 2>> features_;
    vector<array<double, 2>> labels_;
public:
	LinearRegression( const vector<array<double, 2>> & features, const vector<array<double, 2>> & labels );
	void Init();
	void Normalization( Eigen::MatrixXd & x );
	//double ComputeCost( const Eigen::MatrixXd & x, const Eigen::VectorXd & y, const Eigen::VectorXd & theta );
	void GradientDescent( const Eigen::MatrixXd & x, const Eigen::VectorXd & y, Eigen::VectorXd & theta, double alpha, int num_iters );
};

#endif //LINEARREGRESSION_HPP