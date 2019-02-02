# CSC 449, HW#1, Kefu Zhu

# Problem 3

## 1. Derive the form of the 3D structure tensor from the sum of squared dierences (SSD) error function

$E(u,v,w) = \sum_{x,y,t \in W} [I(x+u,y+v,t+w) - I(x,y,t)]^2$

$\approx_{Taylor\ approximation} \sum_{x,y,t \in W} [I(x,y,t) + u \cdot I_x + v \cdot I_y + w \cdot I_t - I(x,y,t)]^2$

$\approx \sum_{x,y,t \in W} [u \cdot I_x + v \cdot I_y + w \cdot I_t]^2$

$\approx \sum_{x,y,t \in W} [(u\ v\ w) \cdot 
\begin{pmatrix}
I_x \\
I_y \\
I_t
\end{pmatrix}
]^2$

$\approx \sum_{x,y,t \in W} (u\ v\ w) \cdot 
\begin{pmatrix}
I_x \\
I_y \\
I_t
\end{pmatrix} \cdot (I_x\ I_y\ I_t) \cdot
\begin{pmatrix}
u \\
v \\
w
\end{pmatrix}
$

$\approx (u\ v\ w) \cdot M \cdot \begin{pmatrix}
u \\
v \\
w
\end{pmatrix}$

where $M = 
\begin{pmatrix}
\sum I_x^2 & \sum I_xI_y & \sum I_xI_t \\
\sum I_xI_y & \sum I_y^2 & \sum I_yI_t \\
\sum I_xI_t & \sum I_yI_t & \sum I_t^2
\end{pmatrix}$

Define the eigenvalues of the $M$ matrix to be $\lambda_1, \lambda_2, \lambda_3$, where $\lambda_1, \lambda_2$ represent change in horizontal and vertical directions, and $\lambda_3$ represent change in time

The criterion to extract "3D corners" is to have large values for all $\lambda_1,\lambda_2,\lambda_3$

## 2. 

The variation among three eigenvalues $\lambda_1,\lambda_2,\lambda_3$ can be summarized as below

- Both $\lambda_1, \lambda_2$ are small $\rightarrow$ flat region
	- $\lambda_3$ is small, does not change with time
	- $\lambda_3$ is large, changes with time
- $($small $\lambda_1$, large $\lambda_2)$ or $($large $\lambda_1$, small $\lambda_2) \rightarrow$ edge 
	- $\lambda_3$ is small, does not change with time
	- $\lambda_3$ is large, changes with time
- Both $\lambda_1, \lambda_2$ are large $\rightarrow$ corner
	- $\lambda_3$ is small, does not change with time
	- $\lambda_3$ is large, changes with time