# ECE 440 HW#2, Kefu Zhu, kzhu6

## Question 1

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW2/Question1_pmf.png)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW2/Question1_cdf.png)

## Question 7

### (A)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW2/Question7a_pmf.png)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW2/Question7a_cdf.png)

### (B)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW2/Question7b.png)

```matlab
% check the value of x such that p(x) is not too small ( p(x) < 0.05)
lambda = 5;
x = 0:10;
p_x = pdf('poiss',x,n,p);
p_x < 0.05
```
```
# Result
ans =

  1×11 logical array

   1   1   0   0   0   0   0   0   0   1   1
```

From the result, we only need to consider the MSE for $x = 2, 3, 4, 5, 6, 7, 8$

Below is the calculated MSE for $n = 6, 10, 20, 50$

```
n = 6, MSE = 0.018713
n = 10, MSE = 0.004260
n = 20, MSE = 0.000019
n = 50, MSE = 0.000000
```

### (D)

To approximate normal distribution with binomial distribution with large value of $n$, with mean of $np$ and variance of $np(1-p)$

The cdf of approximated normal distribution is $F(X) \approx \frac{1}{\sqrt{2\pi np(1-p)} } \int_{-\infty}^x e^{-\frac{(k-np)^2}{2np(1-p)}} \mathrm{d}k$

### (E)

Because in the approximation for Poisson distribution, we fixed the value of $\lambda$. As $n \rightarrow \infty$, the probability $(p = \frac{\lambda}{n})$ goes to zero

However, in the approximation for Normal distribution, we only fixed the value of probability $(p)$, which does not mean the probability goes to zero as $n \rightarrow \infty$. For example, in part(D), the value of $p$ holds at $0.5$ for any value of $n$

Therefore, because these two approximations have different assumptions, they are   approximating different limits

# Appendix

## Code for Question 1
**problem1.m**

```matlab
% pmf
x = [0 1];
p = [1/2 1/2];

% Plot for pmf
bar(x,p)
ylim([0,1.5]);ylabel("Probability");xlabel("X");title("pmf Plot of X");

% Generate figure in new window
figure
% cdf           
X = [-2,-1,0,1,2];
F = [0,0,0.5,1,1];
stairs(X, F)
ylim([0,1.5]);ylabel("Cumulative Probability");xlabel("X");title("cdf Plot of X");
```

## Code for Question 7

**problem7a**

```matlab
np = 5;
nList = [6,10,20,50];

i = 1 % position for subplot

for n = nList
    p = np/n
    
    figure(1) % plot of pmf
    subplot(2,2,i) % position for subplot
    
    stem(0:n,pdf('bino',0:n,n,p));
    title('n = '+string(n)); xlabel('x'); ylabel('pmf');
    grid on; axis([0,50,0,1]); % fix the x and y axis grid
    
    figure(2) % plot of cdf
    subplot(2,2,i) % position for subplot
    stairs(0:n,cdf('bino',0:n,n,p));
    title('n = ' + string(n)); xlabel('x'); ylabel('cdf');
    grid on; axis([0,50,0,1]); % fix the x and y axis grid

    i = i + 1 % increment the position index
end
```

**problem7b.m**

```matlab
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
    MSE = sum(pdf('poiss',x,n,p).*(pdf('bino',x,n,p) - pdf('poiss',x,n,p)).^2);
    fprintf('n = %d, MSE = %.6f\n', n, MSE);
end
```

**problem7d.m**

```matlab
clear all;
p = 0.5;
nList = [10 20 50];

index = 1;
for n = nList
    mean_normal = n*p;
    sd_normal = sqrt(n*p*(1-p));
    x=0:n;
    subplot(3,1,index);
    stairs(x,[binocdf(x,n,p)', normcdf(x,mean_normal,sd_normal)']);
    title('n = ' + string(n)); xlabel('x'); ylabel('cdf');
    legend('Binomial','Normal');
    grid on; axis([0,50,0,1]);
    
    % increment the position index
    index = index + 1;
end
```