
#include "string.h"

#if 0		// CHANGE TO 1
// Remove the #if, when you have finished operator[]:

void string::operator = ( const string& s )
{ 
   if( len != s.len )
   {
      delete[] p; 
      len = s. len;
      p = new char[ len ];
   }

   for( size_t i = 0; i < len; ++ i )
      p[i] = s.p[i];
}
   
   void string::operator +=(char c) {
	   char *temp = new char[len + 1];
	   
	   for (int i = 0; i < len; i++)
		   temp[i] = p[i];
	   temp[len++] = c;
	   
	   delete[] p;
	   p = temp;
   }
   
   void string::operator +=(const string &s) {
	   char *temp = new char[len + s.size()];
	   
	   for (int i = 0; i < len; i++)
			temp[i] = p[i];
	   for (int i = 0; i < s.size(); i++)
			temp[i + len] = s[i];
	   
	   delete[] p;
	   p = temp;
	   len += s.size();
   }
   
   char string::operator [](size_t i) const {
	   if (i < len)
		   return p[i];
	   else
		   throw new std::runtime_error("There is no such character!");
   }
   
   char & string::operator [](size_t i) {
	   if (i < len)
		   return p[i];
	   else
		   throw new std::runtime_error("There is no such character!");
   }

bool operator ==(const string &s1, const string &s2) {
	if (s1.size() != s2.size())
		return false;
	
	for (int i = 0; i < s1.size(); i++) {
		if (s1[i] != s2[i])
			return false;
	}
	
	return true;
}

bool operator <(const string &s1, const string &s2) {
	if (s1.size() < s2.size())
		return true;
	else if (s1.size() > s2.size())
		return false;
	else {
		for (int i = 0; i < s1.size(); i++) {
			if (s1[i] < s2[i])
				return true;
			else if (s1[i] > s2[i])
				return false;
		}
		
		return false;
	}
}

string operator +(const string &s1, const string &s2) {
	string sum = string(s1);
	sum += s2;
	return sum;
}

std::ostream& operator << ( std::ostream& out, const string& s )
{
   for( size_t i = 0; i < s.size( ); ++ i )
      out << s[i];
   return out; 
}

#endif


