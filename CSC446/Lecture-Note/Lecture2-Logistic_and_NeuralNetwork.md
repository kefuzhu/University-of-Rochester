# Lecture 2, Wednesday, 01/23

### Topics: 
- Logistic Regression
- Neural Network
- Stochastic Gradient Descent

## 1. Logistic Regression

Disadvantages of perceptron algorithm

- Does not provide probability, $P_w(y=1|x)$
- As long as all data points are classified right, no preference over decision boundaries (Do not try to find the boundary with largest margin)
- Do not converge for non-linear separable data points

**Sigmoid Function**
<center>
$\sigma(u) = \frac{e^u}{1+e^u}$

![](https://github.com/kefuzhu/University-of-Rochester/raw/master/CSC446/Lecture-Note/graphs/sigmoid.png)
</center>

$P_w(y=1|x)=\sigma(w^Tx) = \frac{e^{w^Tx}}{1+e^{w^Tx}}$

$P_w(y=-1|x)=1 - \sigma(w^Tx) =  \sigma(-w^Tx) = \frac{1}{1+e^{w^Tx}}$

In general, $P_w(y=y_n|x^{(n)}) = \sigma(y_nw^Tx^{(n)}) = \frac{e^{y_nw^Tx^{(n)}}}{1+e^{y_nw^Tx^{(n)}}}$

**Maximum Likelihood Estimation (MLE)**

<center>
$\max_w \prod_{n=1}^N P_w(y=y_n|x^{(n)})$
</center>

$log(L(x)) = log(\prod_{n=1}^N P_w(y=y_n|x^{(n)}))$

$=log(\prod_{n=1}^N P_w(y=y_n|x^{(n)}))$

$=log(\prod_{n=1}^N \frac{e^{y_nw^Tx^{(n)}}}{1+e^{y_nw^Tx^{(n)}}})$

$=\sum_n log(\frac{e^{y_nw^Tx^{(n)}}}{1+e^{y_nw^Tx^{(n)}}})$

$=\sum_n y_nw^Tx^{(n)} - log(1+e^{y_nw^Tx^{(n)}})$

To find the value of $w$ that maximize $L(x)$, we take the derivative of $L(x)$ with respect to $w$ and set it equal to zero

$\frac{\partial L}{\partial w} = 0 = \sum_n y_nx^{(n)} - \frac{y_nx^{n} \cdot e^{y_nw^Tx^{(n)}}}{1+e^{y_nw^Tx^{(n)}}} = \sum_n y_nx^{(n)}[1 - \sigma(y_nw^Tx^{(n)})]$

where $\sigma(y_nw^Tx^{(n)})$ is the probability that we classify correctly. In other words, $\frac{\partial L}{\partial w}$ does not change if we already classify correctly $\Rightarrow 1-\sigma(y_nw^Tx^{(n)}) \approx 0$

## 2. Gradient Descent

In gradient descent, we are trying to find $w$ that minimize $f(w)$. 

<center>
$\min_wf(w)$
</center>

In the case of MLE, the function $-f$ is the likelihood function $L$

<center>
$-f(w) = L(w), \nabla f(w) = -\frac{\partial L}{\partial w}$
</center>

```
# Algorithm sudo-code

Repeat until converge
	w <- w - α ⋅ ∇f(w)
```

## 3. Stochastic Gradient Descent (SGD)

<center>
$\min_wf(w)$, where $f(w) = \sum_{n=1}^N f_n(w)$ and $\nabla f(w) = \sum_{n=1}^N \nabla f_n(w)$
</center>

```
# Algorithm sudo-code

Repeat until converge
	For n
		w <- w - α ⋅ (ynx(n)[1−σ(ynwTx(n))])
```

```
# Algorithm sudo-code 
# Use SGD to maximize MLE

Repeat until converge
	For n from 1 to N
		w <- w + α ⋅ 
```

⚠️ ⚠️ ⚠️

- SGD makes update as scanning through each data point $f_n(w)$. However, GD computes the large sum $f(w)$ before making any update
- GD is more accurate than SGD because some data points are bad so SGD might move in wrong direction sometimes. However, GD always moves in the direction of $-\nabla f(w)$

**Note for learning rate $\alpha$**: 

Sometimes we want to decrease our learning rate as we are moving toward the local minimum, so we can better locate the optimal value. Therefore, we would like to decrease the value of our learning rate as the number of iterations grows

<center>
$\alpha \rightarrow \alpha_t$, where
$
\begin{cases}
\lim_{t \rightarrow \infty} \alpha_t = 0 \\
\sum_{t=0}^{\infty} \alpha_t = \infty
\end{cases}
$
</center>

- $\lim_{t \rightarrow \infty} \alpha_t = 0$ makes sure the learning rate is moving toward zero 
- $\sum_{t=0}^{\infty} \alpha_t = \infty$ makes sure the learning rate does not converge ($\alpha$ does not change much after the number of iteration passes certain value)

The common value for $\alpha_t$ is $\frac{\alpha}{t}$

## 4. Neural Network

**Theorem**: any decision surface can be approximated to arbitrary precision with enough nodes

- Too many nodes can potentially lead to overfitting

**Parameters**

- number of nodes
- number of layers
- $Z_i = g(w_i^Tx)$, where $Z_i$ is the neuron in the layer and $g$ is the **activation function**
	- **Sigmoid Function, $g = \sigma$**
	
		$\sigma(x) = \frac{e^x}{1+e^x}$ 
		
		![](https://github.com/kefuzhu/University-of-Rochester/raw/master/CSC446/Lecture-Note/graphs/sigmoid.png)
	 
	- **Hyperbolic Tangent Function, $g = tanh$**

		$tanh(x) = \frac{e^x-e^{-x}}{e^x+e^{-x}}$
		
		![](https://github.com/kefuzhu/University-of-Rochester/raw/master/CSC446/Lecture-Note/graphs/tanh.png)
	
	- **Rectified Linear Units, $g = relu$** 

		$relu(x) = \max\{0,x\}$
		
		<img src="https://github.com/kefuzhu/University-of-Rochester/raw/master/CSC446/Lecture-Note/graphs/relu.png" style="max-width:50%; width: 50%">