function ranks=ranks_by_random_walk(graph,N,initial_state)

    % Total number of states
    J=min(size(graph));
    % Number of neighbors for each state
    n_neighbors = sum(graph);
    
    k=max(n_neighbors);
    Neighbors=zeros(J,k);
    
    for i=1:J
        temp=find(graph(i,:));
        Neighbors(i,1:length(temp))=temp;
    end
    
    i=initial_state;
    nr_visits=zeros(J,1);
    
    for n=1:N
        nr_visits(i)=nr_visits(i)+1;
        i=Neighbors(i,randi(n_neighbors(i)));
    end
    
    ranks=nr_visits/N;
end