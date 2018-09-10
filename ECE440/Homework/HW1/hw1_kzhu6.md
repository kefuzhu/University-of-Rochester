# ECE 440 HW#1, Kefu Zhu, kzhu6

## Question A

**Note**

- Blue line: p = 0.25
- Green line: p = 0.5
- Black line: p = 0.75

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW1/QuestionA.png)

## Question B

```
Under 100 experiments, the probability of reaching home is 0.07
Under 400 experiments, the probability of reaching home is 0.09
Under 700 experiments, the probability of reaching home is 0.10
Under 1000 experiments, the probability of reaching home is 0.09
Under 1300 experiments, the probability of reaching home is 0.08
Under 1600 experiments, the probability of reaching home is 0.09
Under 1900 experiments, the probability of reaching home is 0.09
Under 2200 experiments, the probability of reaching home is 0.08
Under 2500 experiments, the probability of reaching home is 0.08
```

**Answer**:
I select 1000 times of experiments and I estimate the probability of reaching home to be 0.9. The reason I select N to be 1000 is after many times of experiments, I find the result becomes stable for N larger than 1000 as shown above. Therefore, I think the result converges roughly around 1000 times of experiments.

## Question C

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW1/QuestionC.png)

## Question D

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW1/QuestionD.png)

## Question E

![Simulation Plot](https://github.com/datamasterkfz/University-of-Rochester/raw/master/ECE440/Homework/HW1/QuestionE.png)

**Answer**:
Given the scenario in the graph above, where $w_0 = 10, n = max_t = 1000$
, I estimate the probability distribution of $T_0$ to be **poisson distribution** with **average value of 50.76**

# Appendix

## Code for Question A
**casino.m**

```matlab
function [w, t, broke] = casino(w_0, bet, p, max_t)

    % Starting time
    t = 1;
    % Boolean to indicate broke or not
    broke = 0; 
    % Wealth starts with w_0
    w(t) = w_0;
    while ( (w(t)>0) && (t<max_t) )
       % Random outcome of this bet (win or lose with probablity of p for winning)
       x = random('bino', 1, p);

       % If win, add wealth by amount of bet
       if (x==1)                     
           w(t+1) = w(t) + bet;
       % If lose, substract wealth by amount of bet
       else 
           w(t+1) = w(t) - bet;
       end
       % Increment the time counter
       t = t + 1;
    end

    % If the while loop ends before reaching the maximum play time,
    % the person must be broke
    if t < max_t
        % Change the broke to 1
        broke = 1;  
    end
end
```

**casino_plot.m**

```matlab
% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 20;   
b = 1;      
p_list = [0.25,0.5,0.75];   
max_t=1000;

figure; hold on; grid on;

% Set axis limit
ylabel ('w(t)'); xlabel('t'); axis([0,max_t,0,200])

% Number of experiments for each p
experiments = 10;  
% Experiment for each p
for p = p_list
    if (p == 0.25)
        color = 'b';
    elseif (p == 0.5)
        color = 'g';
    else
        color = 'k';
    end
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
        plot(w,color)  
    end
end
```

## Code for Question B

**reach_home.m**

```matlab
% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 10;   
b = 1;      
p = 0.55;   
max_t=100;

% Number of experiments for each p
experiment_list = 100:300:2500;

for experiments = experiment_list
    % Number of times reach home
    broke_times = 0;
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
        broke_times = broke_times + broke;
    end
    fprintf('Under %d experiments, the probability of reaching home is %.2f\n', experiments, broke_times/experiments)
end
```

## Code for Question C

**reach_home2.m**

```matlab
% Clean up workspace. 
close all 
clear     
% Initialize parameters
w0_list = 1:1:20;   
b = 1;      
p = 0.55;   
max_t=100;
% Number of experiments for each p
experiments = 50;
% List to capture result from each experiment
home_prob = [];

figure; hold on; grid on;

% Set axis limit
ylabel ('Probability of Reach Home'); xlabel('w0'); axis([0,20,0,1])
for w_0 = w0_list
    % Number of times reach home
    broke_times = 0;
    % Add more times of experiments
    experiments = experiments + 50;
    % Show progress
    fprintf('w_0 = %d, experiments = %d\n', w_0, experiments)
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
        broke_times = broke_times + broke;
    end
    home_prob(end+1) = broke_times/experiments;
end
% Show the plot
plot(home_prob)
```

## Code for Question D

**reach_home3.m**

```matlab
% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0= 10;   
b = 1;      
p_list = 0.3:0.02:0.7;   
max_t=100;
% Number of experiments for each p
experiments = 500;
% List to capture result from each experiment
home_prob = [];

figure; grid on;

% Set axis limit
ylabel ('Probability of Reaching Home'); xlabel('p'); axis([0.3,0.7,0,1])
for p = p_list
    % Number of times reach home
    broke_times = 0;
    % Show progress
    fprintf('p = %.2f, ', p)
    for experiment = 1:experiments
        [w, t, broke] = casino(w_0, b, p, max_t);
        broke_times = broke_times + broke;
    end
    home_prob(end+1) = broke_times/experiments;
    fprintf('reach home prob = %.2f\n', broke_times/experiments)
end

% Show the plot
plot(home_prob)
```

## Code for Question E

**reach_home4.m**

```matlab
% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 10;   
b = 1;      
p = 0.4;   
max_t=1000;
% Number of experiments for each p
experiments = 1000;
% List to capture result from each experiment
T0 = [];

for experiment = 1:experiments
    [w, t, broke] = casino(w_0, b, p, max_t);
    T0(end+1) = t;
end

% Show the plot
histogram(T0,'Normalization','probability')
title('Distribution of T0 (w0 = 10, max_t = 1000)')
ylabel('Frequency')
xlabel('T0')
```