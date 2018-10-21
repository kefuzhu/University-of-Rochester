clear all;

J=16;
p=1/J;
N=10^5;
lambda=0.9*p*(1-p)^(J-1);

x = aloha_uplink_simulation(J,p,lambda,N);

Q1=max(x(1,:));
frequencies=zeros(1,Q1+1);
for i=0:Q1
    frequencies(1,i+1)=sum(x(1,:)==i);
end

rho=lambda/(p*(1-p)^(J-1));

A=[frequencies/N;(1-rho)*(rho.^(0:Q1))];
A=A';
figure
bar(0:Q1,A, 1);
axis([-1 Q1 0 0.4])
xlabel('Number of Packets in Queue')
ylabel('Calculated Probability')