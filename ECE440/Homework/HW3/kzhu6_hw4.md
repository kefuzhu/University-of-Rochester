# ECE 440 HW#3, Kefu Zhu, kzhu6

# Question 7

## (a)

**accept_Offer.m**

```matlab
function [acceptedX,n] = accept_Offer(J,K,L)
    % Create a list of random permutation of numbers from 1 to J
    offer = randperm(J);
    % The first Kth offers are rejected
    rejectOffer = offer(1:K);
    % sort the rejectOffer in ascending order
    rejectOffer_sorted = sort(rejectOffer);
    % Select the L-th best offer
    bestL = rejectOffer_sorted(L);
    for i = K+1:J
        % If found Xi such that Xi < X0, end the loop
        if (offer(i) < bestL)
            % Record the accepted offer Xi and the value of i
            acceptedX = offer(i);
            n = i;
            return;
        end
    end
    % If the loop did not end early, I will accept the last offer J
    acceptedX = offer(J);
    n = J;
end
```

## (b)

**pmf\_of\_rank.m**

```matlab
% Plot the pmf of ranks
function [] = pmf_of_rank(J,K,L,N)
    % Initialization
    accepted_rank = zeros(1,N);
    % Record the accepted rank value, the return time N is useless here
    for i=1:N
        [accepted_rank(i), tmp] = accept_Offer(J,K,L);
    end
    
    
    [freq, bin] = hist(accepted_rank,J);
    pmfList=freq/N;
    bar(1:J,pmfList);
    xlabel('x');ylabel('pmf');title('N = ' + string(N) + ', L = ' + string(L)); ylim([0,0.5]);
end
```

**problem7b.m**

```matlab
clear all;

% Set the value of J, K, L, N
J=50; K=30; L=1; N = 1000;

figure()
pmf_of_rank(J,K,L,N)

% Set the value of J, K, L
J=50; K=30; L=2; N = 1000;

figure()
pmf_of_rank(J,K,L,N)
```

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW3/Question7_b_L=1.png)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW3/Question7_b_L=2.png)

## (c)

**prob\_1\_versus_K.m**

```matlab
function []=prob_1_versus_K(J,L)
    N=1000;
    kList = L:J-1;
    prob_of_rank_1 = zeros(1,J-L);
    kIndex = 1;
    for K=kList
        % Initialization
        accepted_rank = zeros(1,N);
        % Record the accepted rank value, the return time N is useless here
        for i=1:N
            [accepte_rank(i),tmp] = accept_Offer(J,K,L);
        end
        [freq, bin] = hist(accepte_rank,J);
        pmf_vector = freq/N;
        prob_of_rank_1(1,kIndex) = pmf_vector(1,1);
        kIndex = kIndex + 1;
    end
    % Plot histogram
    bar(kList,prob_of_rank_1)
    xlabel('K');ylabel('P(X) = 1');
    title('P(X) = 1 for different K, J = ' + string(J) + ', L = ' + string(L) + ', N = ' + string(N));
    axis([0,J,0,0.5])
end
```

**problem7c.m**

```matlab
clear all;
% fix J
J=50;
for L=[1 2 5]
    figure()
    prob_1_versus_K(J,L)
end
```

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW3/Question7_c_L=1.png)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW3/Question7_c_L=2.png)

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW3/Question7_c_L=5.png)


## (d)

As defined in the problem, $P[X=X_J]$ can be represented by the following

$P[X =X_J]=P[{X_0 =1}∪{{X_0 =2}∩{X_J =1}}] =P[{X_0 =1}]+P[{X_0 =2}∩{X_J =1}]$

$\because P [{X_0 = 1}] = \frac{K}{J}$

$\because P[{X_0 =2}∩{X_J =1}]=P[X_0 =2,X_J =1]$

$= P[􏰀X_0 =2􏰂 | 􏰂X_J =1􏰁]P[X_J =1]$

$=\frac{K}{J-1} \cdot \frac{1}{J}$

$\therefore P[X=X_J]= \frac{K}{J} + \frac{K}{J-1} \cdot \frac{1}{J}$

## (e)

$P[X=1]=\sum_{n=1}^J 􏰇P[X=1|X_n =1]P[X_n =1]=􏰇 \sum_{n=1}^J P[X=1|X_n =1]\cdot \frac{1}{J}$

$\because$ If the first offer locates among the first K offers, it would note be accepted (Defined in the question)

$\therefore$
$
P[X=1|X_n=1] = 
\begin{cases}
0,\ 1 \le n \le K \\
P[X=1|X_n=1],\ n \ge K+1 \\
\end{cases}
$

$\therefore P[X=1]= \frac{1}{J} \cdot \sum_{n=K+1}^J P[X=1|X_n =1]$

$\because X_n = 1$ can only happens if the previous $K+1, ...,n-1$ offers are all smaller than $X_0$, which happens with probability $\frac{K}{n-1}$

$\therefore P[X=1]= \frac{1}{J} \cdot \sum_{n=K+1}^J \frac{K}{n-1} = \frac{K}{J} \cdot \sum_{n=K+1}^J \frac{1}{n-1}$

## (f)

$\sum_{n=K+1}^J \frac{1}{n-1} \approx \int_K^{J-1}\frac{1}{x} \mathrm{d}x = ln\frac{J-1}{K}$

Because in our problem set, $J$ is far greater than 1, therefore $ln\frac{J-1}{K} \approx ln\frac{J}{K}$ 

So we now have $P[X=1]= \frac{K}{J} \cdot ln\frac{J}{K}$

Take the derivate respect to $K$ to find the maximum value of $K$:

$\frac{\mathrm{d}}{\mathrm{d}K} P[X=1] \approx \frac{K}{J} \cdot ln(\frac{J}{K}) \frac{\mathrm{d}}{\mathrm{d}K}$

$= \frac{1}{J} \cdot ln(\frac{J}{K}) - \frac{K}{J} \cdot (\frac{K}{J} \cdot \frac{J}{K^2})$

$= \frac{1}{J} \cdot ln(\frac{J}{K}) - \frac{1}{J} = 0$

$\Rightarrow K = \frac{J}{e}$

Take $K = \frac{J}{e}$ back to the equation:

$P[X=1] = \frac{K}{J} \cdot ln\frac{J}{K} = \frac{1}{e} \cdot 1 \approx 0.37$
