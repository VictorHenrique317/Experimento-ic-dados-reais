#ifndef PATTERN_H
#define PATTERN_H

#include "util.h"

class Pattern{
public:

	Pattern(const vector<vector<unsigned int>> &nSetParam);
	Pattern(const Pattern &other);

	friend ostream& operator<<(ostream& out, const Pattern& patternNode);

	vector<vector<unsigned int>> toTuples() const;

	void setNSet(vector<vector<unsigned int>> &nSetParam);
	void setMembershipSum(double acc);
	void setArea(unsigned int areaParam);

	const vector<vector<unsigned int>>& getNSet() const;
	double getMembershipSum() const;
	unsigned int getArea() const;
	double getG() const;

	bool operator<(const Pattern &other) const;
	Pattern operator+(const Pattern &other) const;

	unsigned int last_id;

	static void setIds2Labels(vector<vector<string>>& ids2LabelsParam);

	class Comparator{
	public:
		Comparator(){}
		bool operator()(Pattern* const a, Pattern* const b){
			return (*a) < (*b);
		}
	};

protected:

	vector<vector<unsigned int>> nSet;
	double membershipSum, g;
	unsigned int area;

	static vector<vector<string>> ids2Labels;

	static void getNTuplesFromNSet(const vector<vector<unsigned int>>::const_iterator& dimensionIt,
			const vector<vector<unsigned int>>::const_iterator& dimensionEnd,
			vector<unsigned int>& prefix, vector<vector<unsigned int>>& nTuples);


};

#endif
