clear all;
p = 0.5;
nList = [10 20 50];

index = 1;
for n = nList
    
    mean_normal = n*p;
    sd_normal = sqrt(n*p*(1-p));
    x=0:n;
    subplot(3,1,index);
    stairs(x,[binocdf(x,n,p)', normcdf(x,mean_normal,sd_normal)']);
    title('n = ' + string(n)); xlabel('x'); ylabel('cdf');
    legend('Binomial','Normal');
    grid on; axis([0,50,0,1]);
    
    % increment the position index
    index = index + 1;
end
