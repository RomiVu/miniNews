#include "linearregression.h"

Eigen::VectorXd GetMean( const Eigen::MatrixXd & m ){
    Eigen::VectorXd mean( m.cols() );
    for( int i = 0; i < m.cols(); ++i ){
        mean[ i ] = m.col( i ).mean();
    }
    return mean;
}

Eigen::VectorXd GetStandardDeviation( Eigen::MatrixXd & m, const Eigen::VectorXd & mean ){
    double variance; 
    Eigen::VectorXd stdvar( m.cols() );
    for( int i = 1; i < m.cols(); ++i ){
        variance = ( ( m.array().col( i ) - mean[ i ] ).array().pow( 2 ) ).sum();
        stdvar[ i ] = sqrt( variance / ( m.rows() - 1 ) );
        variance = 0;
    }
    return stdvar;
}


LinearRegression::LinearRegression( const vector<array<double, 2>> & features, const vector<array<double, 2>> & labels ){
    features_ = features;
    labels_ = labels;
	Init();
}

void LinearRegression::Init(){
	Eigen::MatrixXd x( features_.size(), 2 ); // features
	Eigen::MatrixXd y( labels_.size(), 2 ); // labels

    for (size_t i= 0; i<features_.size(); i++){
        x(i, 0) = features_[i][0]; // feature 1
        x(i, 1) = features_[i][1]; // feature 2
        // x(i, 2) = 1.0; // Intercept 
    }

    for (size_t i= 0; i<labels_.size(); i++){
        y(i, 0) = labels_[i][0];
        y(i, 1) = labels_[i][1];
    }

    // cout << "====== x ========" << endl;
    // cout << x << endl;

    // cout << "====== y ========" << endl;
    // cout << y << endl;

	/******** Initialize Weights ********/

	Eigen::MatrixXd theta( y.cols(), x.cols() );
    for (auto i=0; i<y.cols(); i++){
            theta.row(i).setZero();
    }

    // cout << "====== theta ========" << endl;
    // cout << theta << endl;

	/******** Normalize Data ********/

 	Normalization( x, y );

 	/******** Set up Parameters for Gradient Descent ********/

 	double alpha = 0.01; // Learning Rate 
 	double num_iters = 100; // Epochs 
 	GradientDescent( x, y, theta, alpha, num_iters );
    cout.precision(10);
    cout << theta  << endl;
    //std::cout << j_history << std::endl; //Print the cost during every iteration of Gradient Descent 
}

void LinearRegression::Normalization( Eigen::MatrixXd & x, Eigen::MatrixXd & y ){
    Eigen::VectorXd mean_x = GetMean( x );
    // cout << "====== mean ========" << endl;
    // cout << mean << endl;

    // Eigen::VectorXd stddev = GetStandardDeviation( x, mean );
    // cout << "====== stddev ========" << endl;
    // cout << stddev << endl;
    
    for( int i = 0; i < x.cols(); ++i )
        x.array().col( i ) -= mean_x[ i ];
    
    // cout << "====== after delete mean: X: " << endl;
    // cout << x << endl;

    Eigen::VectorXd mean_y = GetMean( y );

    for( int k = 1; k < x.cols(); ++k ){
        x.col( k ) /= stddev[ k ];
    }
}

// double LinearRegression::ComputeCost( const Eigen::MatrixXd & x, const Eigen::VectorXd & y, const Eigen::VectorXd & theta ){
//     int m = y.size();
//     Eigen::VectorXd result = ( x * theta - y );
//     result = result.array().pow( 2 );
//     double J = result.sum();
//     J /= ( 2 * m );
//     return J; 
// }

void LinearRegression::GradientDescent( const Eigen::MatrixXd & x, const Eigen::VectorXd & y, Eigen::VectorXd & theta, double alpha, int num_iters ){
    int m = y.size(); //Length of results 
    int n = x.cols(); // Number of features 
    double result;
    Eigen::MatrixXd temp;

    Eigen::VectorXd h;
    Eigen::VectorXd t;
    while (num_iters > 0){
        h = x * theta; 
        t = Eigen::VectorXd::Zero( n );
        for( int j = 0; j < m; ++j ){
            result = h[ j ] - y[ j ];
            temp = x.row( j ).transpose() * result;
            t = t + temp;
        }
        theta = theta - ( alpha * t ) / m;
        // cout << "NOW iteration times : "<< num_iters << " theta: " << theta << endl;
        num_iters--;
    }
}