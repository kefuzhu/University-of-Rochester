clc; clear all; close all;

X_0=200;
N=200;
r=0.04;
lambda=N;
alpha=r*N;
beta=4;
X_r=200;
X_max=300;
T_max=5;
d=30;
c=20;

[X,t]=cashflow(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max);

% Plot
hold on
grid on
xlabel('time')
ylabel('Cash Level')
title('Simulation of Evolution of Cash Level over 5 Years')
axis([0 5 0 310])
stairs(t,X);