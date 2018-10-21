# ECE 440, HW#5, Kefu Zhu

## Question 7

### (G)

**aloha_uplink_simulation.m**

```matlab
function [x] = aloha_uplink_simulation(J,p,lambda,N)
    % Implementing no concurrence hypothesis is very difficult.
    % Instead, we assume arrivals have precedence over service.
    x=zeros(J,N);
    for t=1:N-1
        arrivals=binornd(1,lambda,J,1);
        is_there_packets=x(:,t)>0;
        decide_to_transmit=binornd(1,p,J,1);
        service = is_there_packets & decide_to_transmit & ~arrivals;
        % service = is_there_packets & decide_to_transmit;
        % Uncomment the line above to relax the non-concurrence assump.
        if sum(service)<=1
            x(:,t+1)=x(:,t)+arrivals-service;
        else
            x(:,t+1)=x(:,t)+arrivals;
        end
    end
end
```

**Visualize the simulation**

```matlab
clear all;

J=16;
p=1/J;
N=10^5;
lambda=0.9*p*(1-p)^(J-1);

x = aloha_uplink_simulation(J,p,lambda,N);

figure
stairs(1:1000,x(1:4,1:1000)');
title('Evolution of queues 1..4 over the first 1000 time slots')
xlabel('time')
ylabel('packets in queues 1..4')
legend('queue 1','queue 2','queue 3','queue 4','Location','Best')
```

![Question7_g]()

### (H)

```matlab
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
```

![Question7_h]()

From the simulation plot, we can see that the dominant system approach substantially underestimates the performance of the RA policy. For example, the probability of a queue being empty under the dominant system approach is 0.1, but the probability without this approach is close to 0.35. 

The performance difference is attributable to the detrimental effect of dummy packets. Without the dominant system approach, empty queues remain silent, increasing the probability of successful transmission of other queues by avoiding unnecessary collisions and positively impacting the system performance.