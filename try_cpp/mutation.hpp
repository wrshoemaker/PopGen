#ifndef MUTATION_HPP
#define MUTATION_HPP

#include <vector>
using namespace std;

typedef int Label;
Label null_label = -1;

class LabelGenerator{
    private:
        Label current_label;
    public:
        LabelGenerator(): current_label(0) {};
        Label get_next_label() {return current_label++;};
};


class Mutation{
public:
	Label label;
	double fitness;
};

inline bool operator < (const Mutation & x, const Mutation & y) {return x.label < y.label;}

Mutation null_mutation {null_label,0.0};

typedef std::vector<Mutation> MutationList;
#endif
