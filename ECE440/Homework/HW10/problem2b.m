% Load data
cisco_stock_price
Z=log(close_price);
Y=Z(2:end)-Z(1:end-1);
N=length(Y);
h=1/365;

% Sample mean
mu_hat=sum(Y)/(N*h) 
% Sample variance
sigma_sqr_hat=sum((Y-mu_hat*h).^2)/((N-1)*h) 