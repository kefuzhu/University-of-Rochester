% Clean up workspace. 
close all 
clear     
% Initialize parameters
w_0 = 20;   
b = 1;      
p_list = [0.25,0.5,0.75];   
max_t=1000;

figure; hold on; grid on; xlabel('bet index'); 

% Set axis limit
ylabel ('w(t)'); xlabel('t'); axis([0,max_t,0,200])

% Number of experiments for each p
experiments = 10;  
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