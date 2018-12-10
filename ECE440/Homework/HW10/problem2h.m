% Load CSCO data and set parameters
cisco_stock_price
Z=log(close_price);
Y=Z(2:end)-Z(1:end-1);
N=length(Y);
h=1/365;
mu_hat=sum(Y)/(N*h);
sigma_sqr_hat=sum((Y-mu_hat*h).^2)/((N-1)*h);
alpha=0.0375;

X_0=close_price(1,1);
EX=X_0*exp(mu_hat+sigma_sqr_hat/2);
K=[0.8,1,1.2]*EX;
a=(log(K/X_0)-(alpha-sigma_sqr_hat/2))/(sqrt(sigma_sqr_hat));
b=a-sqrt(sigma_sqr_hat);
Q_a=1-normcdf(a,0,1);
Q_b=1-normcdf(b,0,1);
c=X_0*Q_b-exp(-alpha)*K.*Q_a