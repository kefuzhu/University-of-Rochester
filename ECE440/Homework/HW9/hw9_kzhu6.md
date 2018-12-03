# ECE 440, HW#9, Kefu Zhu

## Question 7

### (A)

Because $t_1 \ne t_2 \rightarrow t_1 - t_2 \ne 0$, and we have
 
$\delta(t) =
\begin{cases}
\infty,\ t = 0\\
0,\ t \ne 0
\end{cases}
$

so $\delta(t_1 - t_2) = 0$. Then $R_W(t_1, t_2) = 0$, which tells us that $W(t_1)$ and $W(t_2)$ are uncorrelated. But since $W(t)$ is a Gaussian process, uncorrelation implies independence, so $W(t_1)$ and $W(t_2)$ are also independent.

### (B)

**(1) Show that the process $X(t)$ is Gaussian**

Because $W(t)$ is a Gaussian process and $X(t)$ is a linear functional of $W(t)$, $X(t)$ is also a Gaussian process.

**(2) Compute the mean and autocorrelation functions of $X(t)$**

$\mu_X(t) = E[\int_0^t W(u)\ du] = \int_0^t E[W(u)] du = \int_0^t \mu_W(u) du = 0$

$R_X(t_1,t_2) = E[\int_0^{t_1}\int_0^{t_2} W(u)W(v)\ dv\ du]$

$= \int_0^{t_1}\int_0^{t_2} E[W(u)W(v)]\ dv\ du$

$= \int_0^{t_1}\int_0^{t_2} \sigma^2 \cdot \delta(u - v)\ dv\ du$

- If $t_1 < t_2$:

$= \int_0^{t_1}\int_0^{t_1} \sigma^2 \cdot \delta(u - v)\ d\ vdu + \int_0^{t_1}\int_{t_1}^{t_2} \sigma^2 \cdot \delta(u - v)\ dv\ du$

$= \int_0^{t_1}\int_0^{t_1} \sigma^2 \cdot \delta(u - v)\ dv\ du$

$= \int_0^{t_1} \sigma^2 du$

$= \sigma^2 \cdot t_1$

- If $t_1 > t_2$:

$= \int_0^{t_2}\int_0^{t_2} \sigma^2 \cdot \delta(u - v)\ dv\ du + \int_0^{t_2}\int_{t_2}^{t_1} \sigma^2 \cdot \delta(u - v)\ dv\ du$

$= \int_0^{t_2}\int_0^{t_2} \sigma^2 \cdot \delta(u - v)\ dv\ du$

$= \int_0^{t_2} \sigma^2 du$

$= \sigma^2 \cdot t_2$

To summarize, $R_X(t_1,t_2) = \sigma^2 \cdot \min(t_1,t_2)$

**(3) Compute $P(X(t) > a)$ for arbitrary $a$ and $t>0$**

$var(X(t)) = E[X^2(t)] - E^2[X(t)] = R_X(t,t) - \mu_X^2(t) = \sigma^2 t$

Based on Gaussian pdf,

$P(X(t) > a) = \int_0^{\infty} \frac{1}{\sqrt(2\pi\sigma^2t)} \cdot \exp(-\frac{x^2}{2\sigma^2t})\ dx$

### (C)

$\mu_{W_h}(n) = E[W_h(n)] = E[\int_{nh}^{(n+1)h} W(u)\ du] = \int_{nh}^{(n+1)h}E[W(u)]\ du = \int_{nh}^{(n+1)h} \mu_W(u)\ du = 0$

$R_{W_h}(n_1,n_2) = E[\int_{n_1h}^{(n_1+1)h}\int_{n_2h}^{(n_2+1)h} W(u)W(v)\ du\ dv]$

$= \int_{n_1h}^{(n_1+1)h}\int_{n_2h}^{(n_2+1)h} E[W(u)W(v)]\ du\ dv$

$= \int_{n_1h}^{(n_1+1)h}\int_{n_2h}^{(n_2+1)h} \sigma^2\delta(u-v) \ du\ dv$

- When $n_1 = n_2$, $R_{W_h}(n_1,n_2) = \sigma^2h$
- When $n_1 \ne n_2$, $R_{W_h}(n_1,n_2) = 0$ 

By defining discrete-time $\delta_d(n) = 
\begin{cases}
1,\ n = 0\\
0,\ n \ne 0\\
\end{cases}$, we can express $R_{W_h}(n_1,n_2)$ as $\sigma^2h\delta_d(n_1-n_2)$

### (D)

**problem7_d**

```matlab
% Set parameters
h=0.01; sigma=1; t_MAX=10;

W_vector=normrnd(0,sigma*sqrt(h),1,t_MAX/h);
X_vector=cumsum(W_vector);

% Plot sample path
plot(h:h:t_MAX,X_vector);
xlabel('time');title('Weiner Process Simulated, h = ' + string(h));
grid on; axis([0 t_MAX -5 5])
```

![]()