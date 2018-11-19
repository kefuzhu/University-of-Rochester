


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