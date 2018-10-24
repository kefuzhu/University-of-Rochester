function ranks=ranks_by_probability_update(graph,N,initial_distribution)

    J=min(size(graph));
    pi_D=initial_distribution;
    n_neighbors = sum(graph);
    transition_probabilities = graph;
    
    for k=1:J
        if n_neighbors(k)>0
            transition_probabilities(k,:)=graph(k,:)/n_neighbors(k);
        else
            transition_probabilities(k,k)=1;
        end
    end
    
    for n=1:N
        pi_D=transition_probabilities'*pi_D;
    end
    
    ranks=pi_D;
end