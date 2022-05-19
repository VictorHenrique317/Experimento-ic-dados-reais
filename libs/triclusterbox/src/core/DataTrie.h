#ifndef DataTrie_H
#define DataTrie_H

#include <vector>
#include <unordered_map>
#include <iostream>

template<class Key> class DataTrie{
private:
	Key prob, default_prob;
	unsigned int sumChilds;
	std::unordered_map<unsigned int, DataTrie*> childs;
public:
	~DataTrie();
	DataTrie(const Key &d);
	DataTrie(const std::vector<std::vector<unsigned int>> &nSet, const Key &k, const Key &d);

	int getChildsLen() const;

	void addSet(const std::vector<std::vector<unsigned int>>::const_iterator nSetBegin, const std::vector<std::vector<unsigned int>>::const_iterator nSetEnd, std::vector<unsigned int> &prefix, const Key &k);
	void addTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd, const Key &k);
	void delTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd);
	Key getTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd) const;

	Key sumSet(const std::vector<std::vector<unsigned int>> &tuples) const; //need + overload to class Key
};

template<class Key> DataTrie<Key>::~DataTrie(){
	for (auto &c : childs){
		delete c.second;
	}
}

template<class Key> DataTrie<Key>::DataTrie(const Key &d){
	sumChilds = 0;
	default_prob = d;
}

template<class Key> DataTrie<Key>::DataTrie(const std::vector<std::vector<unsigned int>> &nSet, const Key &k, const Key &d){
	sumChilds = 0;
	default_prob = d;
	std::vector<unsigned int> prefix;
	addSet(nSet.begin(), nSet.end(), prefix, k);
}

template<class Key> void DataTrie<Key>::addSet(const std::vector<std::vector<unsigned int>>::const_iterator nSetBegin, const std::vector<std::vector<unsigned int>>::const_iterator nSetEnd, std::vector<unsigned int> &prefix, const Key &k){
	if (nSetBegin == nSetEnd){
		addTuple(prefix.begin(), prefix.end(), k);
	}
	else{
		for (const auto& valueIt : *nSetBegin){
			prefix.push_back(valueIt);
			addSet(nSetBegin+1, nSetEnd, prefix, k);
			prefix.pop_back();
		}
	}
}

template<class Key> int DataTrie<Key>::getChildsLen() const{
	return sumChilds;
}

template<class Key> void DataTrie<Key>::addTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd, const Key &k){
	if (tupleBegin == tupleEnd){
		prob = k;
		return;
	}

	if (childs.find(*tupleBegin) == childs.end()){
		DataTrie<Key> *d = new DataTrie<Key>(default_prob);
		d->addTuple(tupleBegin+1, tupleEnd, k);
		childs[*tupleBegin] = d;
		sumChilds++;
	}
	else{
		sumChilds -= childs[*tupleBegin]->getChildsLen();
		childs[*tupleBegin]->addTuple(tupleBegin+1, tupleEnd, k);
		sumChilds += childs[*tupleBegin]->getChildsLen();
	}
}

template<class Key> void DataTrie<Key>::delTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd){
	if (tupleBegin == tupleEnd){
		return;
	}

	sumChilds--;

	if (childs.find(*tupleBegin) != childs.end()){
		childs[*tupleBegin]->delTuple(tupleBegin+1, tupleEnd);
		if (childs[*tupleBegin]->getChildsLen() == 0){
			delete childs[*tupleBegin];
			childs.erase(*tupleBegin);
		}
	}
}

template<class Key> Key DataTrie<Key>::getTuple(const std::vector<unsigned int>::const_iterator tupleBegin, const std::vector<unsigned int>::const_iterator tupleEnd) const{
	if (tupleBegin == tupleEnd){
		return prob;
	}

	if (childs.find(*tupleBegin) == childs.end()){
		return default_prob;
	}
	else{
		const DataTrie *v = childs.find(*tupleBegin)->second;
		return v->getTuple(tupleBegin+1, tupleEnd);
	}
}

template<class Key> Key DataTrie<Key>::sumSet(const std::vector<std::vector<unsigned int>> &tuples) const{
	double answer = 0;
	for (const auto& tuple : tuples){
		answer = answer + getTuple(tuple.begin(), tuple.end());
	}
	return answer;
}

#endif