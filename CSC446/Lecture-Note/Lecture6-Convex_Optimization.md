# Lecture 6, Wednesday, 02/06

### Topics: 
- Convex Optimization
	- convex objective function: $\ f_0$
	- convex constraints: $\ f_i$

<center>
$\min_x f_0(x)$

such that $\ f_i(x) \le 0$, for $i \in 1,2,...,K$
</center>

Use Lagrangian to approximate $\ f_0(x)$

## Convex Dual

1. Convex optimization: $\min_x f_0(x)$ if $\ f_i(x) \le 0$
2. Set Lagrangian function, $L(x,\lambda) = f_0(x) + \sum_i^K \lambda_i \cdot f_i(x)$
3. Set $g(\lambda) = \min_x L(x,\lambda)$, by calculating $\frac{\partial L}{\partial x} = 0$
4. $\max_\lambda g(\lambda)$ such that $\lambda_i \ge 0$, by calculating $g'(\lambda) = 0$

$p^* = f_0(x^*)$, where $x^*$ is the optimal $x$

$d^* = g(\lambda^*)$, which is called **dual**

Weak duality: $p^* \ge d^*$

Strong duality: $p^* = d^*$

**Example 1**

<center>
$\min_x x^2$ such that $x\ge4$

$
\begin{cases}
f_0(x) = x^2 \\
f_1(x) = 4-x \le 0
\end{cases}
$
</center>

1. $\min_x x^2$ if $\ 4-x \le 0$
2. $L(x,\lambda) = x^2 + \lambda (4-x) \Rightarrow \frac{\partial L}{\partial x} = 2x - \lambda = 0 \Rightarrow x = \frac{\lambda}{2}$
3. $g(\lambda) = min_x L(x,\lambda) = \frac{\lambda^2}{4} + 4\lambda - \frac{\lambda^2}{2} = -\frac{\lambda^2}{4} + 4\lambda$
4. $g'(\lambda) = -\frac{\lambda}{2} + 4 = 0 \Rightarrow \lambda^* = 8$

Hence, $x^* = \frac{\lambda^*}{2} = 4$

**Check**

$p^* = f_0(x^*) = 16$

$d^* = g(\lambda^*) = 16$

Strong duality!

**Example 2**

<center>
$\min_x x^2$ such that $x\le4$

$
\begin{cases}
f_0(x) = x^2 \\
f_1(x) = x-4 \le 0
\end{cases}
$
</center>

1. $\min_x x^2$ if $\ x-4 \le 0$
2. $L(x,\lambda) = x^2 + \lambda (x-4) \Rightarrow \frac{\partial L}{\partial x} = 2x + \lambda = 0 \Rightarrow x = -\frac{\lambda}{2}$
3. $g(\lambda) = min_x L(x,\lambda) = \frac{\lambda^2}{4} - 4\lambda - \frac{\lambda^2}{2} = -\frac{\lambda^2}{4} - 4\lambda$
4. $g'(\lambda) = -\frac{\lambda}{2} - 4 = 0 \Rightarrow \lambda^* = -8$

$\because \lambda \ge 0$, $\ \therefore \lambda^*$ cannot be $-8$, the best possible value for $\lambda$ is 0, aka $\lambda^* = 0$

Hence, $x^* = -\frac{\lambda^*}{2} = 0$