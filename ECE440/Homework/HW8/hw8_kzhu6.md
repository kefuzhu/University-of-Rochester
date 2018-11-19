# ECE 440, HW8, Kefu Zhu

## Question 7

### (A)

Because all varialbes are integer based, and the range of $X(t)$ is between $X_{min} = 0$ and $X_{max}$, the states of the CTMC should be any integer between 0 and $X_max$, where $X_{max}$ is nonnegative integer.

### (B)

Because we have

- $T_p$ ~ $exp(\lambda)$
- $T_c$ ~ $exp(\alpha)$
- $T_d$ ~ $exp(\beta)$

Follow the summary from the range table given in the question, it is obvious to show the foloowing $v_x$ for different scenarios


| Range | Possible Events | $v_x$ |
|:-----:|:---------------:|:-----:|
| A | premium | $\lambda$ |
| B | premium, claim paid at $X(t)$ | $\lambda + \alpha$ |
| C | preimum, claim | $\lambda + \alpha$ |
| D | preimum, claim, dividend | $\lambda + \alpha + \beta$ |
| E | claim, dividend | $\lambda + \beta$ |

### (C)

**(1) Possible transition states out of A**:

The only possible transition out of this state is having a payment of premium $\rightarrow$ State 1

**(2) Possible transition states out of B**

- A payment of preimum: $x + 1$
- A claim paid at $X(t)$: $x - x = 0$

**(3) Possible transition states out of C**

- A payment of preimum: $x + 1$
- A payment of claim: $x - c$

**(4) Possible transition states out of D**

- A payment of preimum: $x + 1$
- A payment of claim: $x - c$
- A payment of divident: $x - d$

**(5) Possible transition states out of E**

- A payment of claim: $x - c$
- A payment of divident: $x - d$

### (D)

Since we have alreadly listed all possible transition states for each range, it is easy to compute their transition probabilities given 

- $T_p$ ~ $exp(\lambda)$
- $T_c$ ~ $exp(\alpha)$
- $T_d$ ~ $exp(\beta)$

**(1) Transition probabilites out of A**:

- premium: $\frac{\lambda}{\lambda} = 1$

**(2) Transition probabilites out of B**

- premium: $\frac{\lambda}{\lambda + \alpha}$
- claim: $\frac{\alpha}{\lambda + \alpha}$

**(3) Transition probabilites out of C**

- premium: $\frac{\lambda}{\lambda + \alpha}$
- claim: $\frac{\alpha}{\lambda + \alpha}$

**(4) Transition probabilites out of D**

- premium: $\frac{\lambda}{\lambda + \alpha + \beta}$
- claim: $\frac{\alpha}{\lambda + \alpha + \beta}$
- divident: $\frac{\beta}{\lambda + \alpha + \beta}$

**(5) Transition probabilites out of E**

- claim: $\frac{\alpha}{\alpha + \beta}$
- divident: $\frac{\beta}{\alpha + \beta}$

### (E)

**cashflow.m**

```matlab
function [X,T]=cashflow(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max)
    index=1;
    X(index)=X_0;
    T(index)=0;
    while T(index)<T_max
        x=X(index);
        if x==0 
            tau=exprnd(1/lambda);
            T(index+1)=T(index)+tau;
            X(index+1)=x+1;
        elseif 0<x && x<c 
            tau=exprnd(1/(lambda+alpha));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha))
                X(index+1)=x+1;
            else
                X(index+1)=0;
            end
        elseif c<=x && x<X_r
            tau=exprnd(1/(lambda+alpha));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha))
                X(index+1)=x+1;
            else
                X(index+1)=x-c;
            end
        elseif X_r<=x && x<X_max
            tau=exprnd(1/(lambda+alpha+beta));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(lambda/(lambda+alpha+beta))
                X(index+1)=X(index)+1;
            elseif u<((lambda+alpha)/(lambda+alpha+beta))
                                X(index+1)=X(index)-c;
            else
                X(index+1)=X(index)-d;
            end
        elseif x==X_max
            tau=exprnd(1/(alpha+beta));
            T(index+1)=T(index)+tau;
            u=rand;
            if u<(alpha/(lambda+alpha))
                X(index+1)=x-c;
            else
                X(index+1)=x-d;
            end
        else
            disp('Out Of Range')
            break 
        end
        index=index+1;
    end
end
```

**Plot** 

```matlab
clc; clear all; close all;

X_0=200;
N=200;
r=0.04;
lambda=N;
alpha=r*N;
beta=4;
X_r=200;
X_max=300;
T_max=5;
d=30;
c=20;

[X,t]=cashflow(X_0,lambda,alpha,beta,c,d,X_r,X_max,T_max);

% Plot
hold on
grid on
xlabel('time')
ylabel('Cash Level')
title('Simulation of Evolution of Cash Level over 5 Years')
axis([0 5 0 310])
stairs(t,X);
```

![Question7_e](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW8/Question7_e.png)

### (F)

$\because \frac{\mathrm{d} P_{xy}(t)}{\mathrm{d} t} = P^{'}(xy) = \sum_{k = 0, k \ne y}^{\infty} q_{ky}P_{xk}(t) - v_y P_{xy}(t)$

$\therefore$ 

**Range A**

$P^{'}(xy) = \alpha \sum_{k=1}^c P_{x,k} - \lambda P_{x,y}$

**Range B**

$P^{'}(xy) = \lambda P_{x,y-1} + \alpha P_{x,y+c} - (\lambda + \alpha) P_{x,y}$

**Range C**

- $y < x_r - d: P^{'}(xy) = \lambda P_{x,y-1} + \alpha P_{x,y+c} - (\lambda + \alpha) P_{x,y}$
- $y \ge x_r - d: P^{'}(xy) = \lambda P_{x,y-1} + \alpha P_{x,y+c} + \beta P_{x,y+d} - (\lambda + \alpha) P_{x,y}$

**Range D**

- $y \le min(X_{max} - c, X_{max} - d): P^{'}(xy) = \lambda P_{x,y-1} + \alpha P_{x,y+c} + \beta P_{x,y+d} - (\lambda + \alpha + \beta) P_{x,y}$
- $y > min(X_{max} - c, X_{max} - d): P^{'}(xy) = \lambda P_{x,y-1} - (\lambda + \alpha + \beta) P_{x,y}$
- $c < d,\ min(X_{max} - d < y \le X_{max} - c: P^{'}(xy) = \lambda P_{x,y-1} + \alpha P_{x,y+c} - (\lambda + \alpha + \beta) P_{x,y}$
- $d < c,\ min(X_{max} - c < y \le X_{max} - d: P^{'}(xy) = \lambda P_{x,y-1} + \beta P_{x,y+d} - (\lambda + \alpha + \beta) P_{x,y}$

**Range E**

$P^{'}(xy) = \lambda P_{x,y-1} - (\alpha + \beta) P_{x,y}$

### (G)

$\because \frac{\mathrm{d} P_{xy}(t)}{\mathrm{d} t} = P^{'}(xy) = \sum_{k = 0, k \ne x}^{\infty} q_{xk}P_{ky}(t) - v_x P_{xy}(t)$

$\therefore$

**Range A**

$P^{'}(xy) = \lambda P_{x+1,y} - P_{x,y}$

**Range B**

$P^{'}(xy) = \lambda P_{x+1,y} + \alpha P_{0,y} - (\lambda + \alpha) P_{x,y}$

**Range C**

$P^{'}(xy) = \lambda P_{x+1,y} + \alpha P_{x-c,y} - (\lambda + \alpha) P_{x,y}$

**Range D**

$P^{'}(xy) = \lambda P_{x+1,y} + \alpha P_{x-c,y} + \beta P_{x-d,y} - (\lambda + \alpha + \beta) P_{x,y}$

**Range E**

$P^{'}(xy) = \alpha P_{x-c,y} + \beta P_{x-d,y} - (\alpha + \beta) P_{x,y}$

### (H)

**Kolmogrov_F**

```matlab
function [R]=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max)
    % initialization
    R=zeros(X_max+1); 
    % Range A:
    R(1,1)=-lambda;
    R(1,2:c+1)=alpha;
    % Range B:
    for i=2:c
        R(i,i-1)=lambda;
        R(i,i+c)=alpha;
        R(i,i)=-(lambda+alpha);
    end
    % Range C-1:
    for i=c+1:X_r-d
        R(i,i-1)=lambda;
        R(i,i+c)=alpha;
        R(i,i)=-(lambda+alpha);
    end
    % Range C_2:
    for i=X_r-d+1:X_r
        R(i,i-1)=lambda;
        R(i,i+c)=alpha;
        R(i,i+d)=beta;
        R(i,i)=-(lambda+alpha);
    end
    % Range D_1:
    for i=X_r+1:X_max-d+1
        R(i,i-1)=lambda;
        R(i,i+c)=alpha;
        R(i,i+d)=beta;
        R(i,i)=-(lambda+alpha+beta);
    end
    % Range D_2:
    for i=X_max-d+2:X_max-c+1
        R(i,i-1)=lambda;
        R(i,i+c)=alpha;
        R(i,i)=-(lambda+alpha+beta);
    end
    % Range D_3:
    for i=X_max-c+2:X_max
        R(i,i-1)=lambda;
        R(i,i)=-(lambda+alpha+beta);
    end
    % Range E:
    R(X_max+1, X_max)=lambda;
    R(X_max+1, X_max+1)=-(alpha+beta);
```

**Plot**

```matlab
R=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max);
p0=zeros(X_max+1,1);
p0(X_0+1,1)=1;
T=0:0.25:5;
figure
hold on
xlabel('X')
ylabel('pmf')
title('pmf of the states between 0 and 5 over quarterly intervals')
axis([0 300 0 0.016])
for t=T
     pmf=expm(R.*t)*p0;
     plot(0:X_max,pmf)
end
```

![Question7_h](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW8/Question7_h.png)

### (I)

Because dividends can only be paid when $x$ is in range (D) or (E), we can declare that 

$P$(at least one dividend paid) $= 1 – P$(no dividends paid) $\approx 0.64$ 

Then the probability of paying dividends in a given quarter can be estimated as 0.64 times the probability that $X(t) \ge X_r$. We repeat this procedure for every quarter and plot the result below

```matlab
R=Kolmogrov_F(lambda,alpha,beta,c,d,X_r,X_max);
p0=zeros(X_max+1,1);
p0(X_0+1,1)=1;
T=0.25:0.25:5;
prob=zeros(20,1);
figure
hold on
xlabel('time (years)')
ylabel('Prob. of dividend')
axis([0 5 0.2 0.30])
for t=T
        pmf=expm(R.*t)*p0;
        prob(t/0.25) = sum(pmf(201:end))*0.64;
end
set(gca);
stairs(T,prob);
grid on
```

![Question7_i](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW8/Question7_i.png)

As shown on the plot, the probability of paying dividends will decrease as time increase. And eventually this probability tend to converge around 0.21.

