// Copyright 2012,2013,2014,2016 Loïc Cerf (lcerf@dcc.ufmg.br)

// This file is part of paf.

// paf is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// paf is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with paf; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#ifndef NOISY_TUPLE_READER_H_
#define NOISY_TUPLE_READER_H_

#include <unordered_map>
#include <fstream>
#include <boost/tokenizer.hpp>

#include "../../Parameters.h"
#include "../utilities/DataFormatException.h"
#include "../utilities/NoFileException.h"

#ifdef VERBOSE_PARSER
#include <iostream>
#endif

using namespace boost;

class NoisyTupleFileReader
{
public:
    NoisyTupleFileReader(const char* noisyNSetFileName, const char* inputDimensionSeparator, const char* inputElementSeparator, const vector<unordered_map<string, unsigned int>>& labels2Ids);

    const bool eof() const;
    const vector<vector<unsigned int>>& tuples() const;
    const float membership() const;
    void next();

protected:
    string noisyNSetFileName;
    ifstream noisyNSetFile;
    char_separator<char> inputDimensionSeparator;
    char_separator<char> inputElementSeparator;
    unsigned int lineNb;
    vector<unordered_map<string, unsigned int>> labels2Ids;
    vector<vector<unsigned int>> nSet;
    float membershipDegree;

    /* The two following method set membershipDegree to 0 if and only if the end of file is met */
    void init();
    const bool parseLine(const tokenizer<char_separator<char>>::const_iterator dimensionBegin, const tokenizer<char_separator<char>>::const_iterator dimensionEnd); /* returns whether the line is to be disconsidered (recursive calls to next can lead to a stack overflow) */
};

#endif /*NOISY_TUPLE_READER_H_*/
