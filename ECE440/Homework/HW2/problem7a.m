np = 5;
nList = [6,10,20,50];

i = 1 % position for subplot

% Plot pmf and cdf of binomial distribution for different value of n
for n = nList
    % Calculate the current p value
    p = np/n
    
    figure(1) % plot of pmf
    subplot(2,2,i) % position for subplot
    
    stem(0:n,pdf('bino',0:n,n,p));
    title('n = '+string(n)); xlabel('x'); ylabel('pmf');
    grid on; axis([0,50,0,1]); % fix the x and y axis grid
    
    figure(2) % plot of cdf
    subplot(2,2,i) % position for subplot
    stairs(0:n,cdf('bino',0:n,n,p));
    title('n = ' + string(n)); xlabel('x'); ylabel('cdf');
    grid on; axis([0,50,0,1]); % fix the x and y axis grid

    i = i + 1 % increment the position index
end