# ECE 440, HW#7, Kefu Zhu

## Question 7

### (a)

```matlab
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
```

```matlab
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

```

<center>
![Question7_a_1](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW7/Question7_a_1.png)
</center>

```matlab
figure
pdf_approx = hist(sum(arrival(1:n/2,:)),x)/nr_experiments;
bar(x,pdf_approx)
hold on
plot(x,poisspdf(x,lambda*T/2),'r','Linewidth',2)
xlabel('t')
ylabel('pmf')
title('pmf of number of arrivals for a Poisson Process of \lambda=1, and for T=5')
legend('Estimated','Calculated','Location','Best')
```

<center>
![Question7_a_2](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW7/Question7_a_2.png)
</center>

### (b)

$N(t) = \sum_{i=1}^{t/h} N_i(h) = \sum_{i=1}^n N_i(h)$, where $N_i(h)$ ~ $Bernoulli(\lambda h)$

Because the sum of $n$ i.i.d Bernoulli RV with parameter $p$ equals to Binomial RV with parameter $np$, therefore $N(t)$ ~ $Binomial(\lambda t)$ ($np = \frac{\lambda}{h} \cdot \lambda h = \lambda t$)

By law of rare events, because $lim_{n \rightarrow \infty} p = 0$ and $np$ still equals to $\lambda h$, $N(t)$ ~ $Poisson(\lambda t)$

### (c)

```matlab
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
```

```matlab
%Compare with exponential pdf
figure
plot((1:n)*h,time_histogram/nr_experiments/h)
hold on
plot((1:n)*h,exppdf((1:n)*h,lambda),'r','Linewidth', 2)
xlabel('t')
ylabel('pdf')
title('pdf of first arrival time for a Poisson Process of \lambda=1')
legend('Estimated','Calculated','Location','Best')
```

<center>
![Question7_c_1](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW7/Question7_c_1.png)
</center>

```matlab
%Compare with exponential cdf
figure
plot((1:n)*h,cumsum(time_histogram/nr_experiments))
hold on
plot((1:n)*h,expcdf((1:n)*h,lambda),'r','Linewidth', 2)
xlabel('t')
ylabel('cdf')
title('cdf of first arrival time for a Poisson Process of \lambda=1')
legend('Estimated','Calculated','Location','Best')
```

<center>
![Question7_c_2](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW7/Question7_c_2.png)
</center>