% Parameters for poisson distribution
lambda = 5;
x = 0:50;

% Plot of poisson distribution with lambda = 5
stem(x,pdf('poiss',x,lambda));
axis([0,50,0,0.5]);
xlabel('x'); ylabel('pmf');title('Poisson distribution with \lambda = ' + string(lambda));

% check the value of x such that p(x) is not too small ( p(x) < 0.05)
clear all; close all;
lambda = 5;
x = 0:10;
p_x = pdf('poiss',x,n,p);
p_x < 0.05

% Calculate the MSE when n = 6. 10, 20, 50
clear all;
lambda = 5;
x = 2:8;
nList = [6,10,20,50];

for n = nList
    p = lambda/n;
    MSE = sum((pdf('bino',x,n,p) - pdf('poiss',x,lambda)).^2.*pdf('poiss',x,lambda));
    fprintf('n = %d, MSE = %.6f\n', n, MSE);
end
 