#include <vector>
#include <set>
#include <fstream>
#include <iostream>
#include <boost/tokenizer.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/program_options.hpp>
#include "sysexits.h"

#include "../utilities/NoFileException.h"
#include "IncorrectNbOfDimensionsException.h"

#include "Pattern.h"
#include "DataTrie.h"
#include "PatternFileReader.h"
#include "NoisyTupleFileReader.h"

#include "../../Parameters.h"

using namespace boost;
using namespace std;

namespace po = boost::program_options;

class IO{
private:
	string pattern_input, data_input;
	ofstream output;
	unsigned int sizes;

	vector<vector<string>> ids2Labels;
	vector<unordered_map<string, unsigned int>> labels2Ids;
	string inputDimensionSeparator;
	string inputElementSeparator;

	int flagError;

public:
	IO(int argc, char* argv[]);

	int fail();
	unsigned int getSizes() const;

	vector<Pattern*> readNSets() throw (IncorrectNbOfDimensionsException);
	void readTuples(DataTrie<double> &t) throw (IncorrectNbOfDimensionsException);
	void writePatterns(vector<Pattern*> &patterns);
};
