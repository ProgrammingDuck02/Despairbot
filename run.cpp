#include <iostream>
#include <stdlib.h>
#include <direct.h>
#include <conio.h>
#include <stdio.h>
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
	printf("Bot stopped working\n");
	printf("Press any button to close runner");
	getch();
	return 0;
}
