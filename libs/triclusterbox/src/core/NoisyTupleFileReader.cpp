// Copyright 2012,2013,2014,2016 Loïc Cerf (lcerf@dcc.ufmg.br)

// This file is part of paf.

// paf is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// paf is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with paf; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#include "NoisyTupleFileReader.h"

NoisyTupleFileReader::NoisyTupleFileReader(const char* noisyNSetFileNameParam, const char* inputDimensionSeparator, const char* inputElementSeparator, const vector<unordered_map<string, unsigned int>>& labels2IdsParam) : noisyNSetFileName(noisyNSetFileNameParam), noisyNSetFile(noisyNSetFileName), inputDimensionSeparator(inputDimensionSeparator), inputElementSeparator(inputElementSeparator), lineNb(0), labels2Ids(labels2IdsParam), nSet(), membershipDegree(0)
{
    if (!noisyNSetFile)
    {
        throw NoFileException(noisyNSetFileNameParam);
    }
    init();
}

void NoisyTupleFileReader::init()
{
    if (noisyNSetFile.eof())
    {
        noisyNSetFile.close();
        membershipDegree = 0;
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
    while (++dimensionIt != dimensions.end())
    {
        ++n;
    }
    nSet.resize(n);
    #ifdef VERBOSE_PARSER
    cout << noisyNSetFileName << ':' << lineNb << ": " << noisyNSetString << endl;
    #endif
    if (parseLine(dimensions.begin(), dimensions.end()))
    {
        next();
    }
}

const bool NoisyTupleFileReader::eof() const
{
    return membershipDegree == 0;
}

const vector<vector<unsigned int>>& NoisyTupleFileReader::tuples() const
{
    return nSet;
}

const float NoisyTupleFileReader::membership() const
{
    return membershipDegree;
}

void NoisyTupleFileReader::next()
{
    bool isLineToBeDisconsidered = true;
    while (isLineToBeDisconsidered)
    {
        if (noisyNSetFile.eof())
        {
            noisyNSetFile.close();
            membershipDegree = 0;
            return;
        }
        ++lineNb;
        string noisyNSetString;
        getline(noisyNSetFile, noisyNSetString);
        tokenizer<char_separator<char>> dimensions(noisyNSetString, inputDimensionSeparator);
        if (dimensions.begin() != dimensions.end())
        {
            #ifdef VERBOSE_PARSER
            cout << noisyNSetFileName << ':' << lineNb << ": " << noisyNSetString << endl;
            #endif
            isLineToBeDisconsidered = parseLine(dimensions.begin(), dimensions.end());
        }
    }
}

const bool NoisyTupleFileReader::parseLine(const tokenizer<char_separator<char>>::const_iterator dimensionBegin, const tokenizer<char_separator<char>>::const_iterator dimensionEnd)
{
    tokenizer<char_separator<char>>::const_iterator dimensionIt = dimensionBegin;
    tokenizer<char_separator<char>>::const_iterator membershipIt = dimensionBegin;
    while (++dimensionIt != dimensionEnd)
    {
        membershipIt = dimensionIt;
    }
    try
    {
        membershipDegree = lexical_cast<float>(*membershipIt);
        if (membershipDegree == 0)
        {
            return true;
        }
        if (membershipDegree < 0 || membershipDegree > 1)
        {
            throw bad_lexical_cast();
        }
    }
    catch (bad_lexical_cast &)
    {
        throw DataFormatException(noisyNSetFileName.c_str(), lineNb, ("the membership, " + *membershipIt + ", should be a float in [0, 1]!").c_str());
    }
    unsigned int dimensionId = 0;
    dimensionIt = dimensionBegin;
    int i = 0;
    for (unordered_map<string, unsigned int>& labels2IdsInDimension : labels2Ids)
    {
        vector<unsigned int>& nSetDimension = nSet[i];
        nSetDimension.clear();
        tokenizer<char_separator<char>> elements(*dimensionIt, inputElementSeparator);
        for (const string& element : elements)
        {
            const unordered_map<string, unsigned int>::const_iterator label2IdIt = labels2IdsInDimension.find(element);
            if (label2IdIt != labels2IdsInDimension.end())
            {
                nSetDimension.push_back(label2IdIt->second);
            }
        }
        if (++dimensionIt == dimensionEnd)
        {
            throw DataFormatException(noisyNSetFileName.c_str(), lineNb, ("less than the expected " + lexical_cast<string>(nSet.size()) + " dimensions!").c_str());
        }
        if (nSetDimension.empty())
        {
            return true;
        }
        ++i;
        ++dimensionId;
    }
    if (dimensionIt != membershipIt)
    {
        throw DataFormatException(noisyNSetFileName.c_str(), lineNb, ("more than the expected " + lexical_cast<string>(nSet.size()) + " dimensions!").c_str());
    }
    return false;
}
