// Copyright 2012,2013,2014,2016 Loïc Cerf (lcerf@dcc.ufmg.br)

// This file is part of paf.

// paf is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// paf is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with paf; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#include "PatternFileReader.h"

PatternFileReader::PatternFileReader(const char* noisyNSetFileNameParam, const char* inputDimensionSeparator, const char* inputElementSeparator) : noisyNSetFileName(noisyNSetFileNameParam), noisyNSetFile(noisyNSetFileName), inputDimensionSeparator(inputDimensionSeparator), inputElementSeparator(inputElementSeparator), lineNb(0), ids2Labels(), labels2Ids(), nSet(){
    if (!noisyNSetFile){
        throw NoFileException(noisyNSetFileNameParam);
    }
    init();
}

void PatternFileReader::init()
{
    if (noisyNSetFile.eof())
    {
        noisyNSetFile.close();
        return;
    }
    ++lineNb;
    string noisyNSetString;
    getline(noisyNSetFile, noisyNSetString);
    tokenizer<char_separator<char>> dimensions(noisyNSetString, inputDimensionSeparator);
    tokenizer<char_separator<char>>::const_iterator dimensionIt = dimensions.begin();
    if (dimensionIt == dimensions.end())
    {
        init();
        return;
    }
    unsigned int n = 0;
    while (dimensionIt != dimensions.end())
    {
        ++n;
        ++dimensionIt;
    }
    if (n == 1)
    {
        throw DataFormatException(noisyNSetFileName.c_str(), lineNb, "at least two dimensions required!");
    }
    ids2Labels.resize(n);
    labels2Ids.resize(n);
    nSet.resize(n);
    #ifdef VERBOSE_PARSER
    cout << noisyNSetFileName << ':' << lineNb << ": " << noisyNSetString << endl;
    #endif
    parseLine(dimensions.begin(), dimensions.end());
}

const bool PatternFileReader::eof() const
{
    return nSet.empty();
}

const vector<vector<unsigned int>>& PatternFileReader::pattern() const
{
    return nSet;
}

void PatternFileReader::next()
{
    if (noisyNSetFile.eof())
    {
        noisyNSetFile.close();
        nSet.clear();
        return;
    }
    ++lineNb;
    string noisyNSetString;
    getline(noisyNSetFile, noisyNSetString);
    tokenizer<char_separator<char>> dimensions(noisyNSetString, inputDimensionSeparator);
    if (dimensions.begin() == dimensions.end())
    {
        next();
        return;
    }
    #ifdef VERBOSE_PARSER
    cout << noisyNSetFileName << ':' << lineNb << ": " << noisyNSetString << endl;
    #endif
    parseLine(dimensions.begin(), dimensions.end());
}

vector<vector<string>>&& PatternFileReader::captureIds2Labels()
{
    return move(ids2Labels);
}

vector<unordered_map<string, unsigned int>>&& PatternFileReader::captureLabels2Ids()
{
    return move(labels2Ids);
}

void PatternFileReader::parseLine(const tokenizer<char_separator<char>>::const_iterator dimensionBegin, const tokenizer<char_separator<char>>::const_iterator dimensionEnd)
{
    unsigned int dimensionId = 0;
    vector<vector<string>>::iterator ids2LabelsIt = ids2Labels.begin();
    tokenizer<char_separator<char>>::const_iterator dimensionIt = dimensionBegin;
    vector<vector<unsigned int>>::iterator nSetIt = nSet.begin();
    for (unordered_map<string, unsigned int>& labels2IdsInDimension : labels2Ids)
    {
        nSetIt->clear();
        tokenizer<char_separator<char>> elements(*dimensionIt, inputElementSeparator);
        for (const string& element : elements)
        {
            const pair<unordered_map<string, unsigned int>::const_iterator, bool> label2Id = labels2IdsInDimension.insert(pair<string, unsigned int>(element, ids2LabelsIt->size()));
            if (label2Id.second)
            {
                ids2LabelsIt->push_back(element);
            }
            nSetIt->push_back(label2Id.first->second);
        }
        if (dimensionIt == dimensionEnd)
        {
            throw DataFormatException(noisyNSetFileName.c_str(), lineNb, ("less than the expected " + lexical_cast<string>(nSet.size()) + " dimensions!").c_str());
        }
        ++dimensionIt;
        ++ids2LabelsIt;
        ++nSetIt;
        ++dimensionId;
    }
    if (dimensionIt != dimensionEnd)
    {
        throw DataFormatException(noisyNSetFileName.c_str(), lineNb, ("more than the expected " + lexical_cast<string>(nSet.size()) + " dimensions!").c_str());
    }
}
