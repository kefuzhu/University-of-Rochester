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