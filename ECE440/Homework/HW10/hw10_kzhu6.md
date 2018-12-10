# ECE 440, HW#10, Kefu Zhu

## Question 1 Arbitrages

### (A) Arbitrage with single booker

Based on the investment strategy, we have

$
\begin{cases}
6.6x - c > 0\rightarrow x > \frac{1}{6.6} \cdot c\\
8.1y - c > 0\rightarrow y > \frac{1}{8.1} \cdot c\\
1.2z - c > 0\rightarrow z > \frac{1}{1.2} \cdot c
\end{cases}
$

$\Rightarrow x+y+z > \frac{1}{6.6} \cdot c + \frac{1}{8.1} \cdot c + \frac{1}{1.2} \cdot c \Leftrightarrow c>1.11c$

Since $c > 0$, such condition can never be met, an arbitrage is not possible

### (B) Arbitrage with many bookers

Based on the odds provided in the question, the best strategy is to bet on country from booker with the highest odds. 

That means bet France win from Booker 1, bet Brazil win from Booker 3 and bet Other win from Booker 2. Similar to part (A), we have 

$
\begin{cases}
6.6x - c > 0\rightarrow x > \frac{1}{6.6} \cdot c\\
8.4y - c > 0\rightarrow y > \frac{1}{8.4} \cdot c\\
1.3z - c > 0\rightarrow z > \frac{1}{1.3} \cdot c
\end{cases}
$

$\Rightarrow x+y+z > \frac{1}{6.6} \cdot c + \frac{1}{8.4} \cdot c + \frac{1}{1.3} \cdot c \Leftrightarrow c>1.04c$

Since $c > 0$, such condition can never be met, an arbitrage is still not possible

## Question 2 Option pricing

### (A) Derivation 

Because for different $Y_n$ where $Y_n = Y_{(n-1)h}(h)$, they belong to disjoint intervals of length $h$, so $Y_n$ are i.i.d normals with mean $\mu h$ and variance $\sigma^2 h$

### (B) Determination of drift and volatility

```matlab
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
```

The result from above matlab calculation is $\mu = 0.6275$ and $\widehat{\sigma}^2 = 0.2174$

### (C) Is geometric Brownian motion a good model

```matlab
% Load CSCO data and set parameters
cisco_stock_price
Z = log(close_price);
Y = Z(2:end)-Z(1:end-1);
N = length(Y);
h = 1/365;
x = -0.1:0.01:0.1;
n_elements = histc(Y,x);
mu_hat = 0.6275;
sigma_sqr_hat = 0.2174;
```

```matlab
% Compare pdf
figure(1)
bar(x,n_elements/N/0.01)
hold on
x_padded = -0.1:0.001:0.1;
plot(x_padded,normpdf(x_padded,mu_hat*h,sqrt(sigma_sqr_hat*h)), 'Linewidth', 3)
title('Compare PDF');
grid on
axis([-0.1,0.1,0,25])
```

![pdf](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW10/Question2c_pdf.png)

```matlab
% Compare cdf
figure(2)
c_elements = cumsum(n_elements)/N;
bar(x,c_elements)
hold on
x_padded = -0.1:0.001:0.1;
plot(x_padded,normcdf(x_padded,mu_hat*h,sqrt(sigma_sqr_hat*h)), 'Linewidth', 3)
title('Compare CDF');
grid on
axis([-0.1,0.1,0,1])
```

![cdf](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW10/Question2c_cdf.png)

### (D) Expected return

Expected return = $E[\frac{e^{-\alpha t}X(t)}{X(0)}\ |\ X(0)] = e^{t\ (\widehat{\mu} - \alpha + \frac{\widehat{\sigma}^2}{2})}$

Given $\alpha = 3.75\%$ and $t=1$, $E[\frac{e^{-\alpha t}X(t)}{X(0)}\ |\ X(0)] \approx 2.01$

$P[log(\frac{e^{-\alpha t}X(t)}{X(0)}) \ge 0.05\ |\ X(0)] = P[Y(1) \ge 0.05 + 0.0375]$ 

$\because Y(1)$ ~ $N(\widehat{\mu},\widehat{\sigma}^2)\ \therefore P[Y(1) \ge 0.0875] \approx 0.88$


### (E) Risk neutral measure

### (F) Expected return for risk neutral measure

### (G) Derive the Black-Scholes formula

### (H) Determine option price

 