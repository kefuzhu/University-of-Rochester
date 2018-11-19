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