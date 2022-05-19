// Copyright 2008,2009,2010,2011 Loïc Cerf (magicbanana@gmail.com)

// This file is part of n-set-diff.

// n-set-diff is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License version 3 as published by the Free Software Foundation

// n-set-diff is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

// You should have received a copy of the GNU General Public License along with n-set-diff; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

#ifndef INCORRECTNBOFDIMENSIONS_H_
#define INCORRECTNBOFDIMENSIONS_H_

#include <exception>
#include <string>
#include <boost/lexical_cast.hpp>

using namespace std;

class IncorrectNbOfDimensionsException : public exception
{
 protected:
  string nSet;
  unsigned int n;

 public:
  IncorrectNbOfDimensionsException();
  IncorrectNbOfDimensionsException(const string& nSetString, const unsigned int n);
  ~IncorrectNbOfDimensionsException() throw();
  const char* what() const throw();
};

#endif /*INCORRECTNBOFDIMENSIONS_H_*/
