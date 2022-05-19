#include "Pattern.h"

vector<vector<string>> Pattern::ids2Labels;

Pattern::Pattern(const vector<vector<unsigned int>> &nSetParam){
	nSet = nSetParam;
	area = 1;
	last_id = 0;
	g = 0;

	for (const auto &dim : nSetParam)
		area *= dim.size();
}

Pattern::Pattern(const Pattern &other): nSet(other.getNSet()), area(other.getArea()), membershipSum(other.getMembershipSum()), g(other.getG()) {
}

ostream& operator<<(ostream& out, const Pattern& patternNode){
	vector<vector<string>>::const_iterator ids2LabelsIt = Pattern::ids2Labels.begin();

    for (int i = 0; i < Pattern::ids2Labels.size(); i++){
        if (ids2LabelsIt != Pattern::ids2Labels.begin()){
            out << " ";
        }

        const vector<unsigned int>& dimension = patternNode.getNSet()[i];
        out << (*ids2LabelsIt)[dimension.front()];
        const vector<unsigned int>::const_iterator end = dimension.end();

        for (vector<unsigned int>::const_iterator elementIt = dimension.begin(); ++elementIt != end; ){
            out << "," << (*ids2LabelsIt)[*elementIt];
        }
        ++ids2LabelsIt;
    }

    return out;
}

void Pattern::setNSet(vector<vector<unsigned int>> &nSetParam){
	nSet = nSetParam;
	area = 1;
	for (const auto &dim : nSetParam)
		area *= dim.size();
}

void Pattern::setMembershipSum(double acc){
	membershipSum = acc;
	if (area == 0) g = 0;
	else g = membershipSum * membershipSum / area;
}

void Pattern::setArea(unsigned int areaParam){
	area = areaParam;
}

const vector<vector<unsigned int>>& Pattern::getNSet() const{
	return nSet;
}

double Pattern::getMembershipSum() const{
	return membershipSum;
}

unsigned int Pattern::getArea() const{
	return area;
}

double Pattern::getG() const{
	return g;
}

bool Pattern::operator<(const Pattern &other) const{
	return cmpf(g, other.g) == -1;
}

Pattern Pattern::operator+(const Pattern &other) const{
	vector<vector<unsigned int>> ans;
	int i = 0;
	for (const auto& dimensionIt : other.getNSet()){
		set<unsigned int> dim;
		for (const auto& value : dimensionIt){
			dim.insert(value);
		}
		for (const auto& value : nSet[i++]){
			dim.insert(value);
		}

		vector<unsigned int> dimension;
		for (const auto& value : dim)
			dimension.push_back(value);
		ans.push_back(dimension);
	}
	return Pattern(ans);
}

void Pattern::getNTuplesFromNSet(const vector<vector<unsigned int>>::const_iterator& dimensionIt, const vector<vector<unsigned int> >::const_iterator& dimensionEnd, vector<unsigned int>& prefix, vector<vector<unsigned int>>& nTuples){
	if (dimensionIt == dimensionEnd){
		nTuples.push_back(prefix);
	}
	else{
		for (const auto& valueIt : *dimensionIt){
			prefix.push_back(valueIt);
			getNTuplesFromNSet(dimensionIt + 1, dimensionEnd, prefix, nTuples);
			prefix.pop_back();
		}
	}
}

vector<vector<unsigned int>> Pattern::toTuples() const{
	vector<vector<unsigned int> > answer;
	vector<unsigned int> prefix;
	prefix.reserve(nSet.size());
	Pattern::getNTuplesFromNSet(nSet.begin(), nSet.end(), prefix, answer);
	return answer;
}

void Pattern::setIds2Labels(vector<vector<string>>& ids2LabelsParam){
    ids2Labels = ids2LabelsParam;
}
