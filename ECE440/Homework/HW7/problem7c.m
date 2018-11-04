clc; clear all; close all;

% Set parameters
T=10;
lambda= 1;
nr_experiments=10^4;
n=1000;
h=T/n;
p = lambda*h;

% Generate arrivals for all times and experiments
arrival = binornd(1,p,n,nr_experiments);

% Compute time of first arrival
time=0;
experiment=1;
time_histogram = zeros(n,1);
while (experiment <= nr_experiments) && (time < n)
    time = time+1;
    if arrival(time, experiment)
        time_histogram(time)=time_histogram(time)+1;
        experiment = experiment+1;
        time=0;
    end
end

%Compare with exponential pdf
figure
plot((1:n)*h,time_histogram/nr_experiments/h)
hold on
plot((1:n)*h,exppdf((1:n)*h,lambda),'r','Linewidth', 2)
xlabel('t')
ylabel('pdf')
title('pdf of first arrival time for a Poisson Process of \lambda=1')
legend('Estimated','Calculated','Location','Best')

%Compare with exponential cdf
figure
plot((1:n)*h,cumsum(time_histogram/nr_experiments))
hold on
plot((1:n)*h,expcdf((1:n)*h,lambda),'r','Linewidth', 2)
xlabel('t')
ylabel('cdf')
title('cdf of first arrival time for a Poisson Process of \lambda=1')
legend('Estimated','Calculated','Location','Best')