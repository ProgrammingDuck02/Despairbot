#include <fstream>
#include <iostream>
using namespace std;
bool startswith(string word, string pocz)
{
    int dl=pocz.size();
    if(dl>word.size()) return false;
    for(int i=0;i<dl;i++)
    {
        if(pocz[i]!=word[i]) return false;
    }
    return true;
}
string skip(string word, int howmuch)
{
    int dl=word.size();
    string wynik="";
    for(int i=howmuch,j=0;i<dl;i++,j++)
    {
        wynik+=" ";
        wynik[j]=word[i];
    }
    return wynik;
}
int str_to_int(string word)
{
    int wynik=0;
    bool dodatnio=true;
    if(startswith(word,"-"))
    {
        dodatnio=false;
        word=skip(word,1);
    }
    int dl=word.size();
    for(int i=1,j=dl-1;j>=0;j--,i*=10)
    {
        int cyfra=word[j]-'0';
        wynik+=(cyfra*i);
    }
    wynik*=(2*dodatnio-1);
    return wynik;
}
class student
{
public:
    string id,name,surn,gender,appe,items,s_items,ability,secret,dop,vote,image,identyfikator,message,additional;
    int age,punkty;
    bool invert;
    student(string _id)
    {
        id=_id;
        name="";
        surn="";
        gender="";
        appe="";
        items="";
        s_items="";
        ability="";
        secret="";
        dop="";
        vote="";
        image="";
        identyfikator="";
        message="";
        additional="";
        age=18;
        punkty=0;
        invert=false;
    }
};
int main()
{
    ifstream input;
    ofstream students,items,s_items;
    input.open("../students.txt",ios::in);
    students.open("../database/students.txt",ios::out|ios::trunc);
    items.open("../database/items.txt",ios::out|ios::trunc);
    s_items.open("../database/secret items.txt",ios::out|ios::trunc);
    students<<"ID;Imię;Nazwisko;Płeć;Wiek;Wygląd;Punkty;Zdolność;Sekret;Dopełniacz;Głos;ID identyfikatora;ID legitymacji;Invert;Dodatkowe informacje\n";
    items<<"ID;";
    for(int i=0;i<15;i++)
    {
        items<<"Przedmiot nr."<<i+1<<";";
    }
    items<<"\n";
    s_items<<"ID;";
    for(int i=0;i<15;i++)
    {
        s_items<<"Przedmiot nr."<<i+1<<";";
    }
    s_items<<"\n";
    string tempid="";
    bool foundid=false;
    while(!input.eof())
    {
        string akt;
        if(!foundid)
        {
            getline(input,akt);
            if(startswith(akt,"id="))
            {
                foundid=true;
                tempid=skip(akt,3);
            }
        }
        if(foundid)
        {
            foundid=false;
            student recruit(tempid);
            while(!input.eof())
            {
                getline(input,akt);
                if(startswith(akt,"id=")) {foundid=true;tempid=skip(akt,3);break;}
                if(startswith(akt,"name="))
                {
                    recruit.name=skip(akt,5);
                }
                if(startswith(akt,"surn="))
                {
                    recruit.surn=skip(akt,5);
                }
                if(startswith(akt,"gender="))
                {
                    recruit.gender=skip(akt,7);
                }
                if(startswith(akt,"appe="))
                {
                    recruit.appe=skip(akt,5);
                }
                if(startswith(akt,"items="))
                {
                    recruit.items=skip(akt,6);
                }
                if(startswith(akt,"s_items="))
                {
                    recruit.s_items=skip(akt,8);
                }
                if(startswith(akt,"ability="))
                {
                    recruit.ability=skip(akt,8);
                }
                if(startswith(akt,"secret="))
                {
                    recruit.secret=skip(akt,7);
                }
                if(startswith(akt,"dop="))
                {
                    recruit.dop=skip(akt,4);
                }
                if(startswith(akt,"vote="))
                {
                    recruit.vote=skip(akt,5);
                }
                if(startswith(akt,"image="))
                {
                    recruit.image=skip(akt,6);
                }
                if(startswith(akt,"identyfikator="))
                {
                    recruit.identyfikator=skip(akt,14);
                }
                if(startswith(akt,"message="))
                {
                    recruit.message=skip(akt,8);
                }
                if(startswith(akt,"additional="))
                {
                    recruit.additional=skip(akt,11);
                }
                if(startswith(akt,"invert="))
                {
                    if(startswith(akt,"invert=True"))
                    {
                        recruit.invert=true;
                    }
                    else
                    {
                        recruit.invert=false;
                    }
                }
                if(startswith(akt,"age="))
                {
                    recruit.age=str_to_int(skip(akt,4));
                }
                if(startswith(akt,"punkty="))
                {
                    recruit.punkty=str_to_int(skip(akt,7));
                }
            }
            students<<recruit.id<<";"<<
            recruit.name<<";"<<
            recruit.surn<<";"<<
            recruit.gender<<";"<<
            recruit.age<<";"<<
            recruit.appe<<";"<<
            recruit.punkty<<";"<<
            recruit.ability<<";"<<
            recruit.secret<<";"<<
            recruit.dop<<";"<<
            recruit.vote<<";"<<
            recruit.message<<";"<<
            recruit.identyfikator<<";";
            if(recruit.invert)
            {
                students<<"TAK;";
            }
            else
            {
                students<<"NIE;";
            }
            students<<recruit.additional<<"\n";
            string tempstring=recruit.id+";";
            string sakt=recruit.items;
            int dl=sakt.size();
            int buffer=tempstring.size();
            for(int i=0;i<dl;i++)
            {
                tempstring+=" ";
                if(sakt[i]=='\\'&&i!=dl-1)
                {
                    if(sakt[i+1]==',')
                    {
                        tempstring[i+buffer]=',';
                        i++;
                        buffer--;
                    }
                    else
                    {
                        tempstring[i+buffer]='\\';
                    }
                }
                else if(sakt[i]==',')
                {
                    i++;
                    buffer--;
                    tempstring[i+buffer]=';';
                }
                else
                {
                    tempstring[i+buffer]=sakt[i];
                }
            }
            tempstring+="\n";
            items<<tempstring;
            tempstring=recruit.id+";";
            sakt=recruit.s_items;
            dl=sakt.size();
            buffer=tempstring.size();
            for(int i=0;i<dl;i++)
            {
                tempstring+=" ";
                if(sakt[i]=='\\'&&i!=dl-1)
                {
                    if(sakt[i+1]==',')
                    {
                        tempstring[i+buffer]=',';
                        i++;
                        buffer--;
                    }
                    else
                    {
                        tempstring[i+buffer]='\\';
                    }
                }
                else if(sakt[i]==',')
                {
                    i++;
                    buffer--;
                    tempstring[i+buffer]=';';
                }
                else
                {
                    tempstring[i+buffer]=sakt[i];
                }
            }
            tempstring+="\n";
            s_items<<tempstring;
        }
    }
    students.close();
    items.close();
    s_items.close();
    return 0;
}
