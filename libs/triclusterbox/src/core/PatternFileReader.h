// Copyright 2012,2013,2014,2016 Loïc Cerf (lcerf@dcc.ufmg.br)

// This file is part of paf.

// paf is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// paf is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with paf; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#ifndef PATTERN_FILE_READER_H_
#define PATTERN_FILE_READER_H_

#include <unordered_map>
#include <fstream>
#include <boost/tokenizer.hpp>

#include "../../Parameters.h"
#include "../utilities/vector_hash.h"
#include "../utilities/DataFormatException.h"
#include "../utilities/NoFileException.h"

#ifdef VERBOSE_PARSER
#include <iostream>
#endif

using namespace boost;

class PatternFileReader
{
 public:
  PatternFileReader(const char* noisyNSetFileName, const char* inputDimensionSeparator, const char* inputElementSeparator);

  const bool eof() const;
  const vector<vector<unsigned int>>& pattern() const;
  void next();

  /* WARNING: next cannot be called after the following methods */
  vector<vector<string>>&& captureIds2Labels();
  vector<unordered_map<string, unsigned int>>&& captureLabels2Ids();

 protected:
  string noisyNSetFileName;
  ifstream noisyNSetFile;
  char_separator<char> inputDimensionSeparator;
  char_separator<char> inputElementSeparator;
  unsigned int lineNb;
  vector<vector<string>> ids2Labels;
  vector<unordered_map<string, unsigned int>> labels2Ids;
  vector<vector<unsigned int>> nSet;

  void init();
  void parseLine(const tokenizer<char_separator<char>>::const_iterator dimensionBegin, const tokenizer<char_separator<char>>::const_iterator dimensionEnd);
};

#endif /*PATTERN_FILE_READER_H_*/
