#include "Solver.h"

DataTrie<double> Solver::alldata(0.00);

Solver::Solver(const Pattern &allpatterns){
	nSetAll = allpatterns.getNSet();
	int xs = 0, n = alldata.getChildsLen(), k = nSetAll.size();
	unsigned int name = 0;
	total_size = allpatterns.getArea();

	total_data = total_square_data = 0;
	for (const auto& tuple: allpatterns.toTuples()){
		double vlr = alldata.getTuple(tuple.begin(), tuple.end());
		if (vlr == 0) continue;

		total_square_data += vlr*vlr;
		total_data += vlr;
	}

}

Solver::~Solver(){}

Pattern* Solver::solve(const Pattern* fragment){
	double actualG = fragment->getG();
	vector<vector<unsigned int>> nSetF = fragment->getNSet();
	double membershipSumF = fragment->getMembershipSum();
	unsigned int areaF = fragment->getArea();
	unsigned int n = nSetAll.size();

	vector<set<unsigned int>> sortedNSet(n);
	for (int i = 0; i < n; i++)
		for (const auto& el : nSetF[i])
			sortedNSet[i].insert(el);

	vector<set<unsigned int>> sortedNSetF = sortedNSet;

	while(true){
		unsigned int dim = INT_MAX, el = INT_MAX, area_aux;
		double membershipSum_aux;

		for (int i = 0; i < n; i++){
			vector<vector<unsigned int>> nSet = nSetF;
			nSet[i].clear();
			for (const auto &j : nSetAll[i]){
				nSet[i].push_back(j);
				double membershipSum = membershipSumF;
				unsigned int area = areaF;

				Pattern aux(nSet);
				vector<vector<unsigned int>> aux_tuples = aux.toTuples();
				double diff = alldata.sumSet(aux_tuples);

				if (sortedNSet[i].find(j) == sortedNSet[i].end()){
					membershipSum += diff;
					area += aux.getArea();
				}
				else if (sortedNSetF[i].find(j) == sortedNSetF[i].end()){
					membershipSum -= diff;
					area -= aux.getArea();
				}

				double new_g = membershipSum * membershipSum / area;
				if (new_g > actualG){
					actualG = new_g;
					dim = i;
					el = j;
					area_aux = area;
					membershipSum_aux = membershipSum;
				}

				nSet[i].pop_back();
			}
		}

		if (dim == INT_MAX) break;
#ifdef VERBOSE_DEBUG
		cout << "dim: " << dim << " el: " << el << " G: " << actualG << endl
			<< " membershipSum: " << membershipSum_aux << " area: " << area_aux << endl;
#endif

		vector<vector<unsigned int>> nSet = nSetF;
		if (sortedNSet[dim].find(el) == sortedNSet[dim].end()){
			sortedNSet[dim].insert(el);
			nSet[dim].push_back(el);
		}
		else{
			sortedNSet[dim].erase(el);
			for (auto it = nSet[dim].begin(); it != nSet[dim].end(); it++){
				if (*it == el){
					nSet[dim].erase(it);
					break;
				}
			}
		}
		nSetF = nSet;
		membershipSumF = membershipSum_aux;
		areaF = area_aux;
	}

	Pattern *ans = new Pattern(nSetF);
	ans->setMembershipSum(membershipSumF);
	return ans;
}

void Solver::updateSet(const vector<vector<unsigned int>>::const_iterator nSetBegin, const vector<vector<unsigned int>>::const_iterator nSetEnd, vector<unsigned int> &prefix, Pattern *actual, DataTrie<double> &t){
	if (nSetBegin == nSetEnd){
		double s = t.getTuple(prefix.begin(), prefix.end());
		if (s != 1.0){
			actual->setArea(actual->getArea()+1);
			actual->setMembershipSum(actual->getMembershipSum() + alldata.getTuple(prefix.begin(), prefix.end()));
		}
	}
	else{
		for (const auto& valueIt : *nSetBegin){
			prefix.push_back(valueIt);
			updateSet(nSetBegin+1, nSetEnd, prefix, actual, t);
			prefix.pop_back();
		}
	}
}

vector<Pattern*> Solver::solveAll(vector<Pattern*> &patterns){
	vector<Pattern*> answer;
	vector<unsigned int> prefix;
	priority_queue<Pattern*, vector<Pattern*>, Pattern::Comparator> q;
	DataTrie<double> t(0.00);

#ifdef DEBUG
	cout << "* Main solve Phase" << endl;
#endif

	for (int i = 0; i < patterns.size(); i++){
		q.push(patterns[i]);
	}

	while (!q.empty()){
		Pattern* actual = q.top();
		q.pop();

#ifdef DEBUG
		cout << "Getting fragment " << *actual << endl << "    G=" << actual->getG() << std::endl;
#endif

		if (actual->last_id == answer.size()){
			Pattern *bigpat = solve(actual);
#ifdef DEBUG
			cout << "expanded to: " << *bigpat << endl;
#endif
			answer.push_back(bigpat);
			t.addSet(bigpat->getNSet().begin(), bigpat->getNSet().end(), prefix, 1.00);
		}
		else{
			actual->setArea(0);
			actual->setMembershipSum(0);
			updateSet(actual->getNSet().begin(), actual->getNSet().end(), prefix, actual, t);
			actual->last_id = answer.size();

			if (actual->getG() > 0)
				q.push(actual);
		}
	}

	return answer;
}
