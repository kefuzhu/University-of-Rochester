function [x] = aloha_uplink_simulation(J,p,lambda,N)
    % Implementing no concurrence hypothesis is very difficult.
    % Instead, we assume arrivals have precedence over service.
    x=zeros(J,N);
    for t=1:N-1
        arrivals=binornd(1,lambda,J,1);
        is_there_packets=x(:,t)>0;
        decide_to_transmit=binornd(1,p,J,1);
        service = is_there_packets & decide_to_transmit & ~arrivals;
        % service = is_there_packets & decide_to_transmit;
        % Uncomment the line above to relax the non-concurrence assump.
        if sum(service)<=1
            x(:,t+1)=x(:,t)+arrivals-service;
        else
            x(:,t+1)=x(:,t)+arrivals;
        end
    end
end