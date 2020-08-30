#include <iostream>
#include <stdlib.h>
#include <direct.h>
#define GetCurrentDir _getcwd
using namespace std;
std::string get_current_dir() {
   char buff[FILENAME_MAX];
   GetCurrentDir( buff, FILENAME_MAX );
   string current_working_dir(buff);
   return current_working_dir;
}
int main()
{
	string path="cd "+get_current_dir();
	system(path.c_str());
	system("python despairbot.py");
	return 0;
}
