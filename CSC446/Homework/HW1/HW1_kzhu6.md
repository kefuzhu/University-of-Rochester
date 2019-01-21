# CSC446 Homework #1, Kefu Zhu

## 1. Bishop 1.3

**Suppose that we have three coloured boxes r (red), b (blue), and g (green).Box r contains 3 apples, 4 oranges, and 3 limes, box b contains 1 apple, 1 orange, and 0 limes, and box g contains 3 apples, 3 oranges, and 4 limes. If a box is chosen at random with probabilities p(r) = 0.2, p(b) = 0.2, p(g) = 0.6, and a piece of fruit is removed from the box (with equal probability of selecting any of the items in the box).**

### (A) What is the probability of electing an apple?

$P(Apple) = P(Apple|red) \cdot P(red) + P(Apple|blue) \cdot P(blue) + P(Apple|green) \cdot P(green)$

$= \frac{3}{10} \cdot 0.2 + \frac{1}{2} \cdot 0.2 + \frac{3}{10} \cdot 0.6$

$= 0.6 \cdot 0.2 + 0.5 \cdot 0.2 + 0.6 \cdot 0.6$

$= 0.58$

### (B) If we observe that the selected fruit is in fact an orange, what is the probability that it came from the green box?

$P(Orange) = P(Orange|red) \cdot P(red) + P(Orange|blue) \cdot P(blue) + P(Orange|green) \cdot P(green)$

$= \frac{4}{10} \cdot 0.2 + \frac{1}{2} \cdot 0.2 + \frac{3}{10} \cdot 0.6$

$= 0.4 \cdot 0.2 + 0.5 \cdot 0.2 + 0.6 \cdot 0.6$

$= 0.54$

$P(green|Orange) = \frac{P(Orange|green) \cdot P(green)}{P(Orange)} = \frac{0.3 \cdot 0.6}{0.54} = \frac{1}{3}$

## 2. Bishop 1.11

**By setting the derivatives of the log likelihood function (1.54) with respect to $\mu$ and $\sigma^2$ equal to zero, verify the results (1.55) and (1.56).**

<center>
<div align='left'>(1.54)</div>
$ln(p(x|\mu, \sigma^2)) = -\frac{1}{2\sigma^2} \sum_{n=1}^N (x_n - \mu)^2 - \frac{N}{2} ln\sigma^2 - \frac{N}{2} ln(2\pi)$
</center>

<center>
<div align='left'>(1.55)</div>
$\mu_{ML} = \frac{1}{N} \sum_{n=1}^N x_n$
</center>

<center>
<div align='left'>(1.56)</div>
$\sigma_{ML}^2 = \frac{1}{N} \sum_{n=1}^N (x_n - \mu_{ML})^2$
</center>

<br>

**Proof for 1.55**

Calculate the derivative of the log likelihood function (1.54) with respect to $\mu$

$\frac{\partial}{\partial \mu}\ ln(p(x|\mu, \sigma^2)) = -\frac{1}{2\sigma} \cdot (-2) \cdot \sum_{n=1}^N (x_n - \mu) + 0 + 0 = \frac{1}{\sigma^2} \sum_{n=1}^N (x_n - \mu)$

Maximize the log likelihood function by setting its derivatice to zero

$\frac{\partial}{\partial \mu}\ ln(p(x|\mu, \sigma^2)) = \frac{1}{\sigma^2} \sum_{n=1}^N (x_n - \mu) = 0$

$\Rightarrow \sum_{n=1}^N x_n = N \cdot \mu$

$\Rightarrow \mu = \frac{1}{N} \sum_{n=1}^N x_n$

**Proof for 1.56**

Calculate the derivative of the log likelihood function (1.54) with respect to $\sigma$

$\frac{\partial}{\partial \sigma}\ ln(p(x|\mu, \sigma^2)) = -\frac{1}{2} \cdot (-2) \cdot \sigma^{-3} \sum_{n=1}^N (x_n - \mu)^2 - \frac{N}{\sigma} + 0 = \frac{\sum_{n=1}^N (x_n - \mu)^2}{\sigma^3} - \frac{N}{\sigma}$

Maximize the log likelihood function by setting its derivatice to zero

$\frac{\partial}{\partial \sigma}\ ln(p(x|\mu, \sigma^2)) = \frac{\sum_{n=1}^N (x_n - \mu)^2}{\sigma^3} - \frac{N}{\sigma} = 0$

$\Rightarrow \sigma \sum_{n=1}^N (x_n - \mu)^2 = N \cdot \sigma^3$

$\Rightarrow \sigma^2 = \frac{1}{N} \sum_{n=1}^N (x_n - \mu)^2$

## 3.

**Let (X ${\perp\!\!\!\perp}$ Y) denote that X and Y are independent, and let (X ${\perp\!\!\!\perp}$ Y | Z) denote that X and Y are independent conditioned on Z (Bishop p. 373). Are the following properties true? Prove or disprove.**

### (A) (X ${\perp\!\!\!\perp}$ W | Z,Y) $\wedge$ (X ${\perp\!\!\!\perp}$ Y | Z) $\Rightarrow$ (X ${\perp\!\!\!\perp}$ Y,W | Z)

We have $P(X,Y,W\ |\ Z) = P(X\ |\ Y,W,Z) \cdot P(Y,W\ |\ Z)$

$\because X {\perp\!\!\!\perp} W\ |\ Z,Y$

$\therefore P(X,Y,W\ |\ Z) = P(X\ |\ Y,Z) \cdot P(Y,W\ |\ Z)$

$\because X {\perp\!\!\!\perp} Y\ |\ Z$

$\therefore P(X,Y,W\ |\ Z) = P(X\ |\ Z) \cdot P(Y,W\ |\ Z)$

Hence, we proved $X {\perp\!\!\!\perp} Y,W\ |\ Z$

### (B) (X ${\perp\!\!\!\perp}$ Y | Z) $\wedge$ (X ${\perp\!\!\!\perp}$ Y | W) $\Rightarrow$ (X ${\perp\!\!\!\perp}$ Y | Z,W)

We have $P(X,Y\ |\ Z,W) = P(X\ |\ Y,Z,W) \cdot P(Y\ |\ Z,W)$

$\because X {\perp\!\!\!\perp} Y\ |\ Z\ \mathrm{and}\ X {\perp\!\!\!\perp} Y\ |\ W$

$\therefore X {\perp\!\!\!\perp} Y\ |\ Z,W$

$\therefore P(X,Y\ |\ Z,W) = P(X\ |\ Z,W) \cdot P(Y\ |\ Z,W)$

Hence, we proved $X {\perp\!\!\!\perp} Y\ |\ Z,W$