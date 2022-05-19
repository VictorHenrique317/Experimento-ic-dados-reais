#include "IO.h"

IO::IO(int argc, char* argv[]){
	po::options_description generic("Generic Options");
	generic.add_options()
	("help,h", "produce help message")
	("version,V", "display version information and exit")
	("pattern-file", po::value<string>(), "set the pattern fragments file name");

	po::options_description mandatory("Mandatory options (on the command line)");
	mandatory.add_options()
	("dataset-file,f", po::value<string>(), "set data file");

	po::options_description opts("Basic configuration (on the command line or in the option file)");
	opts.add_options()
	("output,o", po::value<string>(), "Output file pattern");

	po::options_description all;
	all.add(generic).add(mandatory).add(opts);

	po::positional_options_description p;
	p.add("pattern-file", 1);
	p.add("dataset-file", 1);
	p.add("help", -1);

	po::variables_map vm;
	po::store(po::command_line_parser(argc, argv).options(all).positional(p).run(), vm);
	po::notify(vm);

	if (vm.count("version")){
		cout << "pp version 0.1.0" << endl;
		flagError = 1;
		return;
	}

	if (vm.count("help") || !vm.count("pattern-file")){
		cout << "Usage: pp [Options] pattern-file" << endl
			<< generic << mandatory << opts;
		flagError = 1;
		return;
	}

	string urlfile1 = "", urlfile2 = "", urlfile3 = "";
	if (vm.count("dataset-file")){
		urlfile1 = vm["dataset-file"].as< string >();
	}

	if (vm.count("pattern-file")){
		urlfile2 = vm["pattern-file"].as< string >();
	}

	if (vm.count("output")){
		urlfile3 = vm["output"].as< string >();
	}

	data_input = urlfile1;
	pattern_input = urlfile2;

	output.open(urlfile3.c_str());
	if (output.fail()){
		cerr << NoFileException(urlfile3.c_str()).what() << endl;
		flagError = EX_IOERR;
		return;
	}

	flagError = EX_OK;

	inputDimensionSeparator = " ";
	inputElementSeparator = ",";
}

int IO::fail(){
	return flagError;
}

unsigned int IO::getSizes() const{
	return sizes;
}

vector<Pattern*> IO::readNSets() throw (IncorrectNbOfDimensionsException){
	vector<Pattern*> patterns;

	try{
		// Parse patterns
		PatternFileReader patternFileReader(pattern_input.c_str(), inputDimensionSeparator.c_str(), inputElementSeparator.c_str());
		for (; !patternFileReader.eof(); patternFileReader.next()){
			patterns.push_back(new Pattern(patternFileReader.pattern()));
		}

		ids2Labels = patternFileReader.captureIds2Labels();
		labels2Ids = patternFileReader.captureLabels2Ids();

	}
	catch (std::exception& e){
		rethrow_exception(current_exception());
	}

	sizes = patterns[0]->getNSet().size();

	return patterns;
}

void IO::readTuples(DataTrie<double> &data) throw (IncorrectNbOfDimensionsException){

	try{

		for (NoisyTupleFileReader noisyTupleFileReader(data_input.c_str(), inputDimensionSeparator.c_str(), inputElementSeparator.c_str(), labels2Ids); !noisyTupleFileReader.eof(); noisyTupleFileReader.next()){
			Pattern p(noisyTupleFileReader.tuples());
			const vector<unsigned int> tuple = p.toTuples()[0];
			const double prob = noisyTupleFileReader.membership();

			if (prob > 0 && data.getTuple(tuple.begin(), tuple.end()) != 0){
				data.addTuple(tuple.begin(), tuple.end(), prob);
			}
		}

		Pattern::setIds2Labels(ids2Labels);
	}
	catch (std::exception& e){
		rethrow_exception(current_exception());
	}
}

void IO::writePatterns(vector<Pattern*> &patterns){
	for (Pattern* p : patterns){
		#ifdef OUTPUT
		output << *p << endl;
		#endif
	}
}
