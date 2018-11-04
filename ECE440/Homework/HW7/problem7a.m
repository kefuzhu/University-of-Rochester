clc; clear all; close all

% Set parameters
T=10;      
lambda= 1;
nr_experiments=10^4;
n=10^3;
h=T/n;
p = lambda*h;

% Generate arrivals for all times and experiments
arrival = binornd(1,p,n,nr_experiments);

% Compare with Poisson pmfs
x=0:30;
pdf_approx = hist(sum(arrival),x)/nr_experiments;
bar(x,pdf_approx)
hold on
plot(x,poisspdf(x,lambda*T),'r','Linewidth',2)
xlabel('t')
ylabel('pmf')
title('pmf of number of arrivals for a Poisson Process of \lambda=1, and for T=10')
legend('Estimated','Calculated','Location','Best')

figure
pdf_approx = hist(sum(arrival(1:n/2,:)),x)/nr_experiments;
bar(x,pdf_approx)
hold on
plot(x,poisspdf(x,lambda*T/2),'r','Linewidth',2)
xlabel('t')
ylabel('pmf')
title('pmf of number of arrivals for a Poisson Process of \lambda=1, and for T=5')
legend('Estimated','Calculated','Location','Best')