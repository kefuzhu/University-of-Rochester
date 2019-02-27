# DSC 465, HW#2, Kefu Zhu

## Q1

### (a)

$L(p;x) = \prod_{i=1}^n {x_i -1 \choose r-1} p^r (1-p)^{x_i-r}$

Take the log of the likelihood, then we have 

$log(L(p;x)) = \sum_{i=1}^n log{x_i - 1 \choose r - 1} + rlog(p) + (x_i -r) log(1-p)$

Take the derivative of the log likelihood with respect to $p$ to find $\widehat{p}_{MLE}$

$\frac{\partial\ log(L(p;x))}{\partial\ p} = \sum_{i=1}^n \frac{r}{p} - \frac{x_i - p}{1-p} = 0$

$\frac{nr}{p} = \frac{\sum_{i=1}^n x_i - nr}{1-p}$

$\widehat{p} = \frac{nr}{\sum_{i=1}^n x_i}$

For a single observation $X$, $\ \widehat{p}_{MLE} = \frac{r}{X}$

### (b)

$\because$

$\pi(p) = \frac{1}{B(\alpha,\beta)} p^{\alpha -1}(1-p)^{\beta-1}$

$P(X=x|p) = {x-1 \choose r-1}p^r(1-p)^{x-r}$

$\therefore$
$\pi(p|x) = \frac{P(X=x|p)\ \pi(p)}{\int_{p=0}^1 P(X=x|p)\ \pi(p) \ \mathrm{d}p} = \frac{{x-1 \choose r-1}p^r(1-p)^{x-r} \cdot \frac{1}{B(\alpha,\beta)} p^{\alpha -1}(1-p)^{\beta-1}}{\int_{p=0}^1 {x-1 \choose r-1}p^r(1-p)^{x-r} \cdot \frac{1}{B(\alpha,\beta)} p^{\alpha -1}(1-p)^{\beta-1}\ \mathrm{d}p} \propto p^{r+\alpha-1}(1-p)^{x-r+\beta-1}$

Hence, the posterior density of $p$ given observation $X=x$ where $X$ ~ $nb(n,p)$ is $beta(r+\alpha, x-r+\beta)$, which is an example of **conjugate prior**

### (c)

$\because p_{prior}$ ~ $beta(\alpha, \beta)$

$\therefore E[\frac{1}{p_{prior}}] = \int_0^1 \frac{1}{p} \cdot \frac{p^{\alpha -1} (1-p)^{\beta - 1}}{B(\alpha,\beta)} = \frac{B(\alpha - 1, \beta)}{B(\alpha, \beta)} = \frac{\Gamma(\alpha-1)\Gamma(\beta)}{\Gamma(\alpha+\beta-1)} \cdot \frac{\Gamma(\alpha+\beta)}{\Gamma(\alpha-1)\Gamma(\beta)} = \frac{\alpha + \beta - 1}{\alpha -1} \rightarrow \widehat{\mu}_{prior} = \frac{r}{\widehat{p}_{prior}} = \frac{r\ (\alpha+\beta-1)}{\alpha-1}$

$\because p_{post}$ ~ $beta(r+\alpha, x-r+\beta)$

$\therefore E[\frac{1}{p_{post}}] = \int_0^1 \frac{1}{p} \cdot \frac{p^{r +\alpha -1} (1-p)^{x-r+\beta - 1}}{B(r+\alpha,x-r+\beta)} = \frac{B(r+\alpha - 1, x-r+\beta)}{B(r+\alpha, x-r+\beta)} = \frac{x+\alpha + \beta - 1}{r+\alpha -1} \rightarrow \widehat{\mu}_{post} = \frac{r}{\widehat{p}_{post}} = \frac{r\ (x+\alpha+\beta-1)}{r+\alpha-1}$

### (d)

$\widehat{\mu}_{post} = \frac{r}{\widehat{p}_{post}} = \frac{r\ (x+\alpha+\beta-1)}{r+\alpha-1} = \frac{r}{r+\alpha-1} x\ +\ \frac{r\ (\alpha + \beta-1)}{r+\alpha-1}$ 

$= \frac{r}{r+\alpha-1} x\ +\ \frac{\alpha-1}{r + \alpha-1} \cdot \frac{r\ (\alpha + \beta-1)}{\alpha-1}$

$ = \frac{r}{r+\alpha-1} x\ +\ (1 - \frac{r}{r+\alpha-1}) \cdot \frac{r\ (\alpha + \beta-1)}{\alpha-1}$

Define $q = \frac{r}{r+\alpha-1}$, then we can write 

<center>
$\widehat{\mu}_{post} = q \cdot \widehat{\mu}_{MLE} + (1-q) \cdot \widehat{\mu}_{prior}$
</center>

## Q2

### (a)

Define $r(t_i)$ as the number at risk and $d_i$ as the number of deaths

| $t_i$ | $d_i$ | $r(t_i)$ | $\widehat{p}_i$ | $\widehat{S}_t$ |
|:-----:|:---:|:------:|:------:|:-----:|
| 0 | 0 | 8 | 1 | 1 |
| 105 | 1 | 8 | $\frac{7}{8}$ | $\frac{7}{8}$ |
| 107.5 | 2 | 7 | $\frac{5}{7}$ | $\frac{5}{8}$ |
| 110 | 0 | 4 | 1 | $\frac{5}{8}$ |
| 115 | 2 | 3 | $\frac{1}{3}$ | $\frac{5}{24}$ |
| 120 | 1 | 1 | 0 | 0 |

## Q3

### (a)

Given a hazard rate $h(x)$, its corresponding cumulative hazard rate is 

<center>
$H(x) = \int_{y=0}^x h(y)\ \mathrm{d}y$
</center>

If exists another hazard rate $h'(x)$ that is proportional to $h(x)$ such as $h'(x) = C \cdot h(x)$, then the cumulative harzard rate for $h'(x)$ can be written as 

<center>
$H'(x) = \int_{y=0}^x C \cdot h'(y)\ \mathrm{d}y = C \cdot \int_{y=0}^x h'(y)\ \mathrm{d}y = C \cdot H(x)$
</center>

Therefore, if the hazard rates are proportional, the cumulative hazard rates will be proportional as well.

## Q4

### (a)

Given a mobile node $\theta = (\theta_x, \theta_y)$ and $\kappa = 8.25$

For stationary node $1$, $(x_1,y_1) = (-0.50,0.00)$, the transimission distance $\mu_1$ can be computed as

<center>
$\mu_1 = \sqrt{(\theta_x + 0.5)^2 + \theta_y^2}$
</center>
<br>

$\because f(z;\kappa,\mu) = \frac{\kappa}{\mu} (\frac{z}{\mu})^{\kappa - 1}e^{-(z/\mu)^{\kappa}}$

$\therefore f(z_1|\theta) = \frac{8.25}{\sqrt{(\theta_x + 0.5)^2 + \theta_y^2}} (\frac{z}{\sqrt{(\theta_x + 0.5)^2 + \theta_y^2}})^{7.25} e^{-(z/\sqrt{(\theta_x + 0.5)^2 + \theta_y^2})^{8.25}}$

Similarly, for stationary $1$ and $2$, since $(x_2,y_2) = (0.42,2.00), (x_3,y_3) = (1.50,1.27)$, 

we have 

<center>
$\mu_2 = \sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2}$

$\mu_3 = \sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2}$
</center>

Following the same computation, we can derive that

$f(z_2|\theta) = \frac{8.25}{\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2}} (\frac{z}{\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2}})^{7.25} e^{-(z/\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2})^{8.25}}$

$f(z_3|\theta) = \frac{8.25}{\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2}} (\frac{z}{\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2}})^{7.25} e^{-(z/\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2})^{8.25}}$

Since the strength of signal for three stationary nodes are independent from each other, we can write

$f(z_1,z_2,z_3|\theta) = f(z_1|\theta) \cdot f(z_2|\theta) \cdot f(z_3|\theta)$ 

$= \frac{8.25}{\sqrt{(\theta_x + 0.5)^2 + \theta_y^2}} (\frac{z_1}{\sqrt{(\theta_x + 0.5)^2 + \theta_y^2}})^{7.25} e^{-(z_1/\sqrt{(\theta_x + 0.5)^2 + \theta_y^2})^{8.25}} \cdot \frac{8.25}{\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2}} (\frac{z_2}{\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2}})^{7.25} e^{-(z_2/\sqrt{(\theta_x - 0.42)^2 + (\theta_y-2)^2})^{8.25}} \cdot \frac{8.25}{\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2}} (\frac{z_3}{\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2}})^{7.25} e^{-(z_3/\sqrt{(\theta_x - 1.5)^2 + (\theta_y-1.27)^2})^{8.25}}$

Having $\ f(z_1,z_2,z_3|\theta)$, we can now compute the posterior density

$\pi(\theta|z_1,z_2,z_3) \propto f(z_1,z_2,z_3|\theta) \cdot \pi(\theta)$, where $\pi(\theta)$ is a uniform prior density

## Q5

### (a)

$\because E[e^{tX}] = \int e^{tX}p(x) \mathrm{d}x$

$\therefore M_X(t) = E[e^{tX}] = \int e^{tX}p(x) \mathrm{d}x$

Then we have 

$\frac{\partial M_X(t)}{\partial t} = \frac{\partial}{\partial t}\int e^{tX}p(x) \mathrm{d}x = \int \frac{\partial}{\partial t} e^{tX}p(x) \mathrm{d}x = \int Xe^{tX}p(x) \mathrm{d}x$

For the $k$th moment of $X$,

$\frac{\partial^k M_X(t)}{\partial t^k} = \int \frac{\partial}{\partial t^k} e^{tX}p(x) \mathrm{d}x = \int X^ke^{tX}p(x) \mathrm{d}x$

$\rightarrow \frac{\mathrm{d}^k M_X(t)}{\mathrm{d}t^k} |_{t=0} = \int X^kp(x) \mathrm{d}x = E[X^k]$

### (b)

As described in the question, in natural parameteriazation, we have 

$\int_{-\infty}^{+\infty} f(x|\eta)\ \mathrm{d}x = \int_{-\infty}^{+\infty} \exp\{\eta T(x) - A(\eta)\}h(x)\ \mathrm{d}x = 1$ 

$\Rightarrow \int_{-\infty}^{+\infty} e^{\eta T(x)}h(x) = e^{A(\eta)}$

For the moment generating function of $T(x)$,

$m(t) = E[e^{tT(X)}] = \int_{-\infty}^{+\infty} e^{tT(X)} f(x|\eta)\ \mathrm{d}x = \int_{-\infty}^{+\infty} e^{tT(X)} e^{\eta T(x) - A(\eta)} h(x)\ \mathrm{d}x$

$= e^{-A(\eta)} \int_{-\infty}^{+\infty} e^{(t+\eta)T(x)}h(x)\ \mathrm{d}x$

$= e^{-A(\eta)} \cdot e^{A(t+\eta)}$

$= e^{A(t+\eta) - A(\eta)}$

Based on the result from part (a), we know that $\frac{\mathrm{d}^k m(t)}{\mathrm{d}t^k} |_{t=0} = E[T(X)^k]$

Therefore, we can write the mean of $T(X)$, $E[T(X)]$, as the following

<center>
$E[T(X)] = \frac{\mathrm{d}m(t)}{\mathrm{d}t} |_{t=0} = (e^{A(t+\eta) - A(\eta)} \cdot A'(t+\eta))|_{t=0} = A'(\eta)$
</center>

Similarly, we have

$E[T(X)^2] = \frac{\mathrm{d^2}m(t)}{\mathrm{d}t^2} |_{t=0} = (e^{A(t+\eta) - A(\eta)} \cdot A''(t+\eta) + e^{A(t+\eta) - A(\eta)} \cdot A'(t+\eta)^2)|_{t=0} = A''(\eta) + A'(\eta)^2$


Then the variance of $T(X)$ can be written as

<center>
$var(T(X)) = E[T(X)^2] - E^2[T(X)] = A''(\eta)$
</center>

### (c)

$\because L(\eta;X) = \ln f(x|\eta) = \eta T(X) - A(\eta) + \ln h(x)$

$\therefore$ 

$\frac{\mathrm{d} L(\eta;X)}{\mathrm{d}\eta} = T(X) - A'(\eta)$

$\frac{\mathrm{d^2} L(\eta;X)}{\mathrm{d}\eta^2} = - A''(\eta) < 0$

Notice that since the second derivative of the log likelihood function of the natural parameter is less than zero, it must be a concave function. To maximize $L(\eta;X)$, we take the derivate with respect to $\eta$ and set it to zero

<center>
$\frac{\mathrm{d} L(\eta;X)}{\mathrm{d}\eta} = T(X) - A'(\eta) = 0$

$T(X) = A'(\eta)$
</center>

Based on the result from part (b), we know that $E[T(X)] = A'(\eta)$. So we prove that if $\widehat{\eta} = \widehat{\eta}(X)$ is any solution to the equation $T(X) = E_{\eta}[T(X)]$ with respect to $\eta$, then it uniquely maximizes the the log likelihood function $L(\eta;X)$

