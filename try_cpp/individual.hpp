#ifndef INDIVIDUAL_HPP
#define INDIVIDUAL_HPP

#include <memory>
#include "object_pool.hpp"
#include "mutation.hpp"

class Individual{
public:
    double weight; // for search
	double fitness;	// fitness of lineage
	std::shared_ptr<MutationList> mutations; // list of tracked mutations that this lineage has. fixed mutations are stored externally.
	Individual(double weight): fitness(1.0), weight(weight){mutations = std::make_shared<MutationList>();};

    bool operator<(const double p) const { return weight < p; }

	void add_mutation(Mutation & mutation)
	{
        if (mutations.unique()){
	       fitness *= mutation.fitness;
	       mutations->push_back(mutation);
        }
        else{
            std::make_shared<MutationList>(*mutations).swap(mutations);
            fitness *= mutation.fitness;
            mutations->push_back(mutation);
        }
	}

	void add_mutation(Mutation && mutation)
	{
        if (mutations.unique()){
           fitness *= mutation.fitness;
           mutations->push_back(mutation);
        }
        else{
            std::make_shared<MutationList>(*mutations).swap(mutations);
            fitness *= mutation.fitness;
            mutations->push_back(mutation);
        }
	}

    Mutation & get_earliest_mutation(){
        if(mutations->size() > 0){
            return mutations->front();
        }
        else{
          return null_mutation;
    	}
   	}

    void remove_earliest_mutation(){
        mutations->erase(mutations->begin());
    }
};

typedef std::vector<Individual> Population;

#endif
