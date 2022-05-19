#include <map>
#include <queue>
#include <algorithm>
#include "Pattern.h"
#include "DataTrie.h"
#include "../../Parameters.h"

const double BETA = (sqrt(5) - 1) / 2;

class Solver{
private:

	vector<vector<unsigned int>> nSetAll;

	double total_square_data, total_data;
	unsigned int total_size;

	Pattern* solve(const Pattern *fragment);

	void updateSet(const vector<vector<unsigned int>>::const_iterator nSetBegin,
		const vector<vector<unsigned int>>::const_iterator nSetEnd, vector<unsigned int> &prefix,
		Pattern *actual, DataTrie<double> &t);

public:
	Solver(const Pattern &allpatterns);
	~Solver();

	vector<Pattern*> solveAll(vector<Pattern*> &patterns);

	static DataTrie<double> alldata;
};
