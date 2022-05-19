// Copyright 2008,2009,2010,2011 Loïc Cerf (magicbanana@gmail.com)

// This file is part of n-set-diff.

// n-set-diff is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// n-set-diff is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with n-set-diff; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#include "IncorrectNbOfDimensionsException.h"

IncorrectNbOfDimensionsException::IncorrectNbOfDimensionsException(): nSet(), n(0)
{
}

IncorrectNbOfDimensionsException::IncorrectNbOfDimensionsException(const string& nSetParam, const unsigned int nParam): nSet(nSetParam), n(nParam)
{
}

IncorrectNbOfDimensionsException::~IncorrectNbOfDimensionsException() throw()
{
}

const char* IncorrectNbOfDimensionsException::what() const throw()
{
  return (nSet + " has " + boost::lexical_cast<string>(nSet.size()) + " dimensions! (" + boost::lexical_cast<string>(n) + " required)").c_str();
}
