#include "IO.h"
#include "DataTrie.h"
#include "Solver.h"
#include "../../Parameters.h"

using namespace std;

int main(int argc, char* argv[]){

	IO io(argc, argv);

	if (io.fail() != EX_OK){
		return io.fail();
	}

	vector<Pattern*> patterns;

	try{
		#ifdef DEBUG
			cout << "* READING PATTERNS" << endl;
		#endif

		patterns = io.readNSets();
	}
	catch (IncorrectNbOfDimensionsException e){
		cerr << e.what();
		return EX_DATAERR;
	}

	vector<vector<unsigned int>> tmp(io.getSizes());
	Pattern all_sets(tmp);

	try{
		#ifdef DEBUG
			cout << "* READING TUPLES" << endl;
		#endif

		for (const auto& p : patterns){
			vector< vector<unsigned int> > tuples = p->toTuples();
			for (const auto& tuple : tuples){
				Solver::alldata.addTuple(tuple.begin(), tuple.end(), 2.0);
			}
			all_sets = all_sets + *p;
		}

		io.readTuples(Solver::alldata);
	}
	catch (IncorrectNbOfDimensionsException e){
		cerr << e.what();
		return EX_DATAERR;
	}

	vector<vector<unsigned int>> aux = all_sets.toTuples();
	for (const auto& tuple : aux){
		if (Solver::alldata.getTuple(tuple.begin(), tuple.end()) == 2)
			Solver::alldata.addTuple(tuple.begin(), tuple.end(), 0.0);
	}

	for (int i = 0; i < patterns.size(); i++){
		vector<vector<unsigned int>> aux = patterns[i]->toTuples();
		patterns[i]->setMembershipSum(Solver::alldata.sumSet(aux));
	}

	#ifdef DEBUG
		cout << "* RUNNING SOLVER" << endl;
	#endif

	Solver solver(all_sets);
	vector<Pattern*> hidden_patterns = solver.solveAll(patterns);
	io.writePatterns(hidden_patterns);

	for (Pattern *p : patterns)
	delete p;

	return EX_OK;
}
