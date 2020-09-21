import discord, random, asyncio, linecache, os, numpy, time, requests
from datetime import datetime, timedelta, date
from PIL import Image,ImageColor,ImageDraw, ImageFont
from glob import glob
#Dane do pobrania z pliku
MURDERED=None
VOTES=False
STUDENTS=[]
SuperiorRole=None
THIEVES=None
CYCLE=None
GAME=False
KILLER=None
TOKEN=None
#Dane globalne
bot_id=""
PATH=""
PATHFONT=""
client=discord.Client()
Despairid=334435715058499584
RESET=False
RESETCHANNEL=None

class student:
    def __init__(self,id,name,surn,gender,age,appe,items,s_items,dop,punkty,ability,secret,vote,image,message,ident,invert,additional):
        self.id=id
        self.name=name
        self.surn=surn
        self.gender=gender
        self.age=age
        self.appe=appe
        self.items=items
        self.s_items=s_items
        self.punkty=punkty
        self.ability=ability
        self.secret=secret
        self.dop=dop
        self.vote=vote
        self.image=image
        self.message=message
        self.ident=ident
        self.invert=invert
        self.additional=additional
    def getembed(self,kolor):
        embed=discord.Embed(title="Identyfikator Uczniowski",color=kolor)
        global Despairid
        Despair=client.get_guild(Despairid)
        members=list(Despair.members)
        kto=None
        for i in range(len(members)):
            if members[i].id==self.id:
                kto=members[i]
                break
            if i+1==len(members):
                print("Nie znaleziono ",self.name, "na liście członków serwera")
                return None
        embed.set_author(name=kto.display_name+" ("+str(self.punkty)+")",icon_url=kto.avatar_url)
        if self.invert:
            embed.add_field(name="Imię",value=self.surn,inline=True)
            if not self.name=="???":
                embed.add_field(name="Nazwisko",value=self.name,inline=True)
        else:
            embed.add_field(name="Imię",value=self.name,inline=True)
            if not self.surn=="???":
                embed.add_field(name="Nazwisko",value=self.surn,inline=True)
        embed.add_field(name="Płeć",value=self.gender,inline=True)
        embed.add_field(name="Wiek",value=str(self.age),inline=True)
        if not self.additional=="":
            embed.add_field(name="Dodatkowe informacje",value=self.additional,inline=False)
        embed.set_footer(text="Wygenerowane: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if self.items=="":
            embed.add_field(name="Przedmioty",value="Brak przedmiotów!",inline=False)
        else:
            przedmioty=stringtolist(self.items,False)
            tempstr=przedmioty[0]
            for i in range(1,len(przedmioty)):
                tempstr=tempstr+"\n"+przedmioty[i]
            embed.add_field(name="Przedmioty",value=tempstr,inline=False)
        if self.image!="None":
            embed.set_thumbnail(url=self.image)
        return embed
    async def updateid(self):
        global Despairid
        Despair=client.get_guild(Despairid)
        nrkoloru=0
        members=list(Despair.members)
        for i in range(len(members)):
            if members[i].display_name.lower()==self.name.lower():
                nrkoloru=members[i].colour.value
                break
        embed=self.getembed(nrkoloru)
        idroom=client.get_channel(618050482065375243)
        if self.message==0:
            msg=await idroom.send(embed=embed)
            return int(msg.id)
        else:
            mes=await idroom.fetch_message(self.message)
            await mes.edit(embed=embed)
            return int(mes.id)
    def getmember(self):
        global Despairid
        Despair=client.get_guild(Despairid)
        ls=list(Despair.members)
        for i in range(len(ls)):
            if ls[i].id==self.id:
                return ls[i]
            if i+1==len(ls):
                raise NameError
#Funkcje obrazów
def paste(bground,pic,Y,X,Yorder=-1,Xorder=-1,transparent=False,t_color="white"):
    t_color=ImageColor.getcolor(t_color,bground.mode)
    pic=pic.convert(bground.mode)
    bX=bground.width
    bY=bground.height
    pX=pic.width
    pY=pic.height
    b_array=numpy.array(bground)
    p_array=numpy.array(pic)
    if Yorder<-1:
        Yorder=-1
    if Xorder<-1:
        Xorder=-1
    if Yorder>1:
        Yorder=1
    if Xorder>1:
        Xorder=1
    Y=int(Y-(Yorder+1)*pY/2)
    X=int(X-(Xorder+1)*pX/2)
    if Y+pY>bY:
        Y=bY-pY
    if X+pX>bX:
        X=bX-pX
    if Y<0:
        Y=0
    if X<0:
        X=0
    size=len(bground.mode)
    white=numpy.array(Image.new(bground.mode,(1,1),t_color))
    for y in range(Y,Y+pY):
        for x in range(X,X+pX):
            if transparent:
                if size==1:
                    if p_array[y-Y][x-X]==white[0][0]:
                        continue
                else:
                    check=True
                    for i in range(size):
                        if p_array[y-Y][x-X][i]!=white[0][0][i]:
                            check=False
                            break
                    if check:
                        continue
            b_array[y][x]=p_array[y-Y][x-X]
    return Image.fromarray(b_array)
    
def fit(bground,pic,Ys,Xs,Ye,Xe,fit_to=bool(0),transparent=False,t_color="white"):
    if Ys>=Ye or Xs>=Xe:
        return bground
    bY=bground.height
    bX=bground.width
    if Ys<0:
        Ys=0
    if Xs<0:
        Xs=0
    if Ye>bY:
        Ye=bY
    if Xe>bX:
        Xe=bX
    if not fit_to:
        proportion=pic.height/pic.width
        pic=pic.resize((Xe-Xs,(int((Xe-Xs)*proportion))))
        if transparent and Ye-Ys>pic.height:
            Ye=pic.height+Ys
        pic=pic.crop((0,0,pic.width,Ye-Ys))
    else:
        proportion=pic.width/pic.height
        pic=pic.resize(((int((Ye-Ys)*proportion),Ye-Ys)))
        if transparent and Xe-Xs>pic.width:
            Xe=pic.width+Xs
        pic=pic.crop((0,0,Xe-Xs,pic.height))
    return paste(bground,pic,Ys,Xs,transparent=transparent,t_color=t_color)

def wrappedtext(text,fontsize,width,czy_lista=False):
    expected_number=int(1.6*width/fontsize)
    lista=[]
    count=0
    while len(text)>expected_number:
        cross=expected_number-1
        space=False
        for i in range(expected_number):
            if text[expected_number-1-i]==' ':
                space=True
                cross=expected_number-i
                break
        lista.append(text[:cross])
        if not space:
            lista[count]=lista[count]+"-"
        count=count+1
        text=text[cross:]
    lista.append(text)
    newstring=""
    if czy_lista:
        lista[0]="-"+lista[0]
        for i in range(1,len(lista)):
            lista[i]="  "+lista[i]
    for i in range(len(lista)):
        newstring=newstring+lista[i]
        if not i+1==len(lista):
            newstring=newstring+"\n"
    return newstring

def saveid(ktos):
    global PATHFONT
    global PATH
    url="https://cdn.discordapp.com/attachments/735472342398009404/735473215383535636/legitymacja_uczen.png"
    template=Image.open(requests.get(url,stream=True).raw)
    image=None
    fit_to=False
    if not ktos.image=="None":
        image=Image.open(requests.get(ktos.image,stream=True).raw)
    else:
        url="https://cdn.discordapp.com/attachments/735472342398009404/735497662626922608/unknown.png"
        image=Image.open(requests.get(url,stream=True).raw)
        fit_to=True
    identyfikator=fit(template,image,111,102,631,580,fit_to)
    text=""
    if ktos.invert:
        text=ktos.surn+"\n"+ktos.name
    else:
        text=ktos.name+"\n"+ktos.surn
    draw=ImageDraw.Draw(identyfikator)
    font=ImageFont.truetype(PATHFONT+"Audiowide-Regular.ttf",size=80,encoding="UTF-8")
    draw.multiline_text(xy=(650,114),text=text,font=font,spacing=15)
    text="Wiek: "+str(ktos.age)
    font=ImageFont.truetype(PATHFONT+"Audiowide-Regular.ttf",size=50,encoding="UTF-8")
    draw.text(xy=(650,325),text=text,font=font)
    text="Punkty: "+str(ktos.punkty)
    font=ImageFont.truetype(PATHFONT+"Audiowide-Regular.ttf",size=60,encoding="UTF-8")
    draw.text(xy=(650,518),text=text,font=font)
    text=wrappedtext(ktos.additional,35,1005)
    font=ImageFont.truetype(PATHFONT+"Audiowide-Regular.ttf",size=35,encoding="UTF-8")
    draw.multiline_text(xy=(113,742),text=text,font=font)
    count=0
    items=stringtolist(ktos.items,False)
    for i in range(len(items)):
        text=wrappedtext(items[i],35,690,True)
        draw.multiline_text(xy=(1291,733+39*count),text=text,font=font)
        for j in range(len(text)):
            if text[j]=='\n':
                count=count+1
        count=count+1
    identyfikator.save(PATH+"identyfikatory/"+str(ktos.id)+".png")
    return identyfikator

async def updatelegit(ktos):
    global PATH
    kolor=None
    osoba=client.get_user(ktos.id)
    try:
        kolor=usertomember(osoba).colour
    except NameError:
        kolor=discord.Colour.default()
    embed=discord.Embed(title=None,color=kolor)
    room=client.get_channel(735472342398009404)
    saveid(ktos)
    file=discord.File(fp=PATH+"identyfikatory/"+str(ktos.id)+".png")
    mes=await room.send(file=file)
    url=mes.attachments[0].url
    embed.set_image(url=url)
    room=client.get_channel(735681326463844363)
    if ktos.ident==0:
        mes=await room.send(embed=embed)
        ktos.ident=mes.id
        saveall()
    else:
        mes=await room.fetch_message(ktos.ident)
        await mes.edit(embed=embed)

def getyear(t_date):
    return int(t_date[:4])

def getmonth(t_date):
    return int(t_date[5:7])

def getday(t_date):
    return int(t_date[8:10])

def nextcycle(t_date):
    month=int(t_date.strftime("%m"))
    day=int(t_date.strftime("%d"))
    if day%3==0:
        day=day+3
    else:
        day=day+day%3
    if day>30:
        day=day-30
        month=month+1
    return date(2020,month,day)

def chance(percentage):
    mood=random.randrange(0,99)
    if percentage>mood:
        return 1
    return 0

async def updateid(stud):
    global Despairid
    Despair=client.get_guild(Despairid)
    col=None
    members=list(Despair.members)
    for each in members:
        if each.display_name.lower()==stud.name.lower():
            col=each.colour
            break
    embed=stud.getembed(col)
    idroom=client.get_channel(618050482065375243)
    if stud.message=="None":
        msg=await idroom.send(embed=embed)
        return str(msg.id)
    else:
        mes=await idroom.fetch_message(stud.message)
        await mes.edit(embed=embed)
        return stud.message
    
def getmember(Name):
    global Despairid
    Despair=client.get_guild(Despairid)
    lis=list(Despair.members)
    for i in range(len(lis)):
        if lis[i].display_name.lower()==Name.lower():
            return lis[i]
    raise NameError

def is_in_list(owocek,lisek):
    count=0
    for i in lisek:
        count=count+(owocek==i)
    return count

def jestrola(human,RRRole):
    ls=list(human.roles)
    dl=len(ls)
    for i in range(dl):
        if ls[i].name.lower()==RRRole.lower():
            return True
    return False

def simplify(words):
    new=""
    blank=True
    for i in range(len(words)):
        if words[i]==' ':
            if blank==True:
                continue
            blank=True
        else:
            blank=False
        new=new+words[i]
    return new

def wordsnumber(sentence):
    sentence=simplify(sentence)
    count=1
    for i in range(len(sentence)):
        if sentence[i]==' ':
            count=count+1
    return count

def word(sentence,number):
    sentence=simplify(sentence)
    sentence=sentence+' '
    number=number-1
    it=0
    new=""
    while(number>0):
        if sentence[it]==' ':
            number=number-1
        it=it+1
    while(True):
        new=new+sentence[it]
        it=it+1
        if sentence[it]==' ':
            return new
        
def usertomember(user):
    global Despairid
    Despair=client.get_guild(Despairid)
    ls=list(Despair.members)
    for i in range(len(ls)):
        if ls[i].id==user.id:
            return ls[i]
        if i+1==len(ls):
            raise NameError
    
def strtolist(words):
    new=[]
    temps=""
    for i in range(len(words)):
        if words[i]=="\n":
            new.append(temps)
            temps=""
            continue
        temps=temps+words[i]
        if i==len(words)-1:
            new.append(temps)
    return new

def getstudent(Name):
    global STUDENTS
    for i in range(len(STUDENTS)):
        if STUDENTS[i].name.lower()==Name.lower():
            return STUDENTS[i]
    raise NameError

def getstudentindex(Name):
    global STUDENTS
    for i in range(len(STUDENTS)):
        if STUDENTS[i].name.lower()==Name.lower():
            return i
    raise NameError

def saveall():
    global STUDENTS
    global PATH
    plik=open(PATH+"students.txt","w",encoding="utf-8")
    for each in STUDENTS:
        plik.write("id="+str(each.id)+"\n")
        plik.write("name="+each.name+"\n")
        plik.write("surn="+each.surn+"\n")
        plik.write("gender="+each.gender+"\n")
        plik.write("age="+str(each.age)+"\n")
        plik.write("appe="+each.appe+"\n")
        plik.write("items="+each.items+"\n")
        plik.write("s_items="+each.s_items+"\n")
        plik.write("punkty="+str(each.punkty)+"\n")
        plik.write("ability="+each.ability+"\n")
        plik.write("secret="+each.secret+"\n")
        plik.write("dop="+each.dop+"\n")
        plik.write("vote="+each.vote+"\n")
        plik.write("image="+each.image+"\n")
        plik.write("identyfikator="+str(each.ident)+"\n")
        plik.write("message="+str(each.message)+"\n")
        if each.invert:
            plik.write("invert=True\n")
        else:
            plik.write("invert=False\n")
        plik.write("additional="+each.additional+"\n\n")
    plik.close()

def stringtolist(sentence,lower):
    lista=[]
    tempstring=""
    skip=0
    if lower:
        sentence=sentence.lower()
    for i in range(len(sentence)):
        if skip>0:
            skip=skip-1
            continue
        tempstring=tempstring+sentence[i]
        if i+1==len(sentence):
            lista.append(tempstring)
            break
        if not len(sentence)==i+2:
            if sentence[i+1]=='\\' and sentence[i+2]==',':
                tempstring=tempstring+","
                skip=2
                continue
        if sentence[i+1]==',':
            lista.append(tempstring)
            tempstring=""
            skip=2
    return lista

def listtostring(lista,lower):
    if lower:
        sentence=lista[0].lower()
    else:
        sentence=lista[0]
    for i in range(1,len(lista)):
        tempstr=""
        for j in range(len(lista[i])):
            if lista[i][j]==',':
                tempstr=tempstr+'\\'
            tempstr=tempstr+lista[i][j]
        if lower:
            sentence=(sentence+", "+tempstr).lower()
        else:
            sentence=sentence+", "+tempstr
    return sentence

@client.event
async def on_message(message):
    global VOTES
    global Despairid
    global STUDENTS
    global MURDERED
    global KILLER
    global SuperiorRole
    global GAME
    global PATH
    global bot_id
    if message.author==client.user:
        return
    if message.channel.type==discord.ChannelType.private:
        mes=message.content
        if mes.startswith("#StudentInformations"): #only if matching criteria for KP
            for i in range(len(STUDENTS)):
                if message.author.id==STUDENTS[i].id:
                    msg=("Dodałeś już wcześniej postać o imieniu "+STUDENTS[i].name+".\nAby zmienić postać skontaktuj się z jednym z aniołów").format(message)
                    await message.author.send(msg)
                    return
            profile=strtolist(mes)
            recruit=student(0,"","","",18,"","","","",0,"","","None","None",0,0,False,"")
            recruit.id=message.author.id
            for i in range(len(profile)):
                wiersz=profile[i]
                if wiersz.lower().startswith("imię: "):
                    recruit.name=wiersz[6:]
                    continue
                if wiersz.lower().startswith("nazwisko: "):
                    recruit.surn=wiersz[10:]
                    continue
                if wiersz.lower().startswith("płeć: "):
                    recruit.gender=wiersz[6:]
                    continue
                if wiersz.lower().startswith("wiek: "):
                    recruit.age=int(wiersz[6:])
                    continue
                if wiersz.lower().startswith("przedmioty: "):
                    recruit.items=wiersz[12:]
                    continue
                if wiersz.lower().startswith("wygląd: "):
                    recruit.appe=wiersz[8:]
                    continue
                if wiersz.lower().startswith("jak się odmienia imię w dopełniaczu: "):
                    recruit.dop=wiersz[37:]
                    continue
                if wiersz.lower().startswith("dodatkowe informacje: "):
                    recruit.additional=wiersz[22:]
                    continue
            if len(message.attachments)>0:
                recruit.image=message.attachments[0].url
            if GAME:
                recruit.message=await recruit.updateid()
            STUDENTS.append(recruit)
            color=usertomember(message.author).color
            ja=client.get_user(330392410964361217)
            embed=recruit.getembed(color)
            await ja.send(embed=embed)
            saveall()
            nazwapokoju=PATH+"rooms/pokój "+recruit.dop.lower()+".txt"
            pokoj=open(nazwapokoju,"w+",encoding="utf-8")
            pokoj.write("Pokój "+recruit.dop+" nie wygląda jakoś szczególnie wybitnie:\n-Łóżko\n-Szafka nocna\n-Szafa na ubrania\n-Łazienka\n-Włączona kamera nagrywająca każdy ruch")
            pokoj.close()
            msg="Gratulacje! Stworzyłeś postać o imieniu "+recruit.name+"!"
            await message.channel.send(msg)
            return
    mes=message.content
    if mes.startswith("//"):
        mes=mes[2:]
    if not mes.lower().startswith("d!"):
        return

    mes=mes[2:]
    if mes.lower().startswith("nazwisko"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=""
            if ktos.invert:
                msg=("Nazwisko "+ktos.dop+" to "+ktos.name).format(message)
            else:
                msg=("Nazwisko "+ktos.dop+" to "+ktos.surn).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("imię"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=""
            if ktos.invert:
                msg=("Imię "+ktos.dop+" to "+ktos.surn).format(message)
            else:
                msg=("Imię "+ktos.dop+" to "+ktos.imię).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("płeć"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=("Płeć "+ktos.dop+" to "+ktos.gender).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("wiek"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=("Wiek "+ktos.dop+" to "+str(ktos.age)).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("wygląd"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=(ktos.name+" wygląda tak: "+ktos.appe).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("informacje"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            msg=("Dodatkowe informacje o uczniu "+ktos.name+":\n"+ktos.additional).format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("przedmioty"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        else:
            if ktos.items=="":
                msg=(ktos.name+" nie ma żadnych przedmiotów!").format(message)
                await message.channel.send(msg)
            else:
                tempstr="Przedmioty "+ktos.dop+" to: "
                templist=stringtolist(ktos.items,False)
                for i in range(len(templist)):
                    tempstr=tempstr+"\n-"+templist[i]
                msg=tempstr.format(message)
                await message.channel.send(msg)
        return
    if mes.lower().startswith("sprzedmioty"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        if not test:
            if kto==usertomember(message.author).display_name:
                test=True
            else:
                msg="Jeśli chcesz wiedzieć rzeczy, których nie powinieneś, to polecam czarną biblię"
                await message.channel.send(msg)
                return
        if test:
            try:
                ktos=getstudent(kto)
            except NameError:
                msg="Nie znaleziono podanej nazwy w bazie danych"
                await message.channel.send(msg)
                return
            if ktos.s_items=="":
                msg=(ktos.name+" nie ma żadnych sekretnych przedmiotów!").format(message)
                await message.author.send(msg)
            else:
                tempstr="Sekretne przedmioty "+ktos.dop+" to: "
                templist=stringtolist(ktos.s_items,False)
                for i in range(len(templist)):
                    tempstr=tempstr+"\n-"+templist[i]
                msg=tempstr.format(message)
                await message.author.send(msg)
        return
    if mes.lower().startswith("punkty"):
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        ktos=None
        try:
            ktos=getstudent(kto)
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
        else:
            msg=(ktos.name+" ma "+str(ktos.punkty)+" punktów").format(message)
            await message.channel.send(msg)
        return
    if mes.lower().startswith("zdolność"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        if not test:
            if kto==usertomember(message.author).display_name:
                test=True
            else:
                msg="Jeśli chcesz wiedzieć rzeczy, których nie powinieneś, to polecam czarną biblię"
                await message.channel.send(msg)
                return
        if test:
            try:
                ktos=getstudent(kto)
            except NameError:
                msg="Nie znaleziono podanej nazwy w bazie danych"
                await message.channel.send(msg)
            else:
                msg=("Zdolność "+ktos.dop+" to: "+ktos.ability).format(message)
                await message.author.send(msg)
        return
    if mes.lower().startswith("sekret"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)==1:
            kto=usertomember(message.author).display_name
        else:
            kto=word(mes,2)
        if not test:
            if kto==usertomember(message.author).display_name:
                test=True
            else:
                msg="Jeśli chcesz wiedzieć rzeczy, których nie powinieneś, to polecam czarną biblię"
                await message.channel.send(msg)
                return
        if test:
            try:
                ktos=getstudent(kto)
            except NameError:
                msg="Nie znaleziono podanej nazwy w bazie danych"
                await message.channel.send(msg)
            else:
                msg=("Sekret "+ktos.dop+" to: "+ktos.secret).format(message)
                await message.author.send(msg)
        return
    if mes.startswith("+"):
        ind=None
        try:
            ind=getstudentindex(word(mes,2))
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        test=None
        try:
            test=not jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if test:
            msg="Brak uprawnień!"
            await message.channel.send(msg)
        else:
            try:
                STUDENTS[ind].punkty=STUDENTS[ind].punkty+1
            except IndexError:
                msg="Ups,coś poszło nie tak"
                await message.channel.send(msg)
                return
            else:
                if GAME:
                    STUDENTS[ind].message=await STUDENTS[ind].updateid()
                saveall()
                msg=("Dodano plusa uczniowi "+STUDENTS[ind].name).format(message)
                await message.channel.send(msg)
                
    if mes.startswith("-"):
        ind=None
        try:
            ind=getstudentindex(word(mes,2))
        except NameError:
            msg="Nie znaleziono podanej nazwy w bazie danych"
            await message.channel.send(msg)
            return
        test=None
        try:
            test=not jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if test:
            msg="Brak uprawnień!"
            await message.channel.send(msg)
        else:
            try:
                STUDENTS[ind].punkty=STUDENTS[ind].punkty-1
            except IndexError:
                msg="Ups,coś poszło nie tak"
                await message.channel.send(msg)
                return
            else:
                if GAME:
                    STUDENTS[ind].message=await STUDENTS[ind].updateid()
                saveall()
                msg=("Dodano minusa uczniowi "+STUDENTS[ind].name).format(message)
                await message.channel.send(msg)
                
    if mes.lower().startswith("ver"):
        msg="Aktualna wersja Despairbota: 2.1\nCo nowego:\n-Identyfikatory! (sprawdź d!showid)\n-Automatyczne aktualizacje idetyfikatorów na odpowiedim kanale\n-Sprawia, że jesteś breathtaking!*"
        await message.channel.send(msg)
        msg="*Tak naprawdę to nie"
        await message.channel.send(msg)
        return

    if mes.lower().startswith("help"):
        if wordsnumber(mes)==1:
            plik=open(PATH+"help-s.txt","r",encoding="utf-8")
            plik.close()
            mes="Oto lista komend Despairbota. Aby uzyskać szczegółowe informacje użyj komendy (d!help (komenda):"
            skip1=len(PATH+"help/")
            for each in glob(PATH+"help/*.txt"):
                skip2=len(each)-4
                mes+="\n"+each[skip1:skip2]
            await message.channel.send(mes)
            return
        elif(word(mes,2).lower()=="all"):
            if not jestrola(usertomember(message.author),SuperiorRole):
                msg="Dlaczego chcesz używać mocy która do ciebie nie należy?"
                await message.channel.send(msg)
                return
            for each in glob(PATH+"help/*.txt"):
                plik=open(each,"r",encoding="utf-8")
                await message.channel.send(plik.read())
                plik.close()
            return
        else:
            komenda=word(mes,2).lower()
            if not os.path.isfile(PATH+"help/"+komenda+".txt"):
                msg="błędna nazwa komendy"
                await message.channel.send(msg)
                return
            plik=open(PATH+"help/"+komenda+".txt","r",encoding="utf-8")
            await message.channel.send(plik.read())
            plik.close()
            return
            
    if mes.lower().startswith("opis"):
        room=mes[5:].lower()
        if not os.path.isfile(PATH+"rooms/"+room+".txt"):
            msg="Błędna nazwa pokoju"
            await message.channel.send(msg)
        else:
            plik=open(PATH+"rooms/"+room+".txt",encoding="utf-8")
            msg=("*"+plik.read()+"*").format(message)
            await message.channel.send(msg)
        return

    if mes.lower().startswith("rp"):
        if not message.author.id==330392410964361217:
            msg='Nie jesteś Mistrzem gry'.format(message)
            await message.channel.send(msg)
            return
        room=word(mes,2)
        msg=mes[(4+len(room)):].format(message)
        global Despairid
        Despair=client.get_guild(Despairid)
        lis=list(Despair.channels)
        for i in range(len(lis)):
            if lis[i].name==room:
                await lis[i].send(msg)
                return
        msg=("Nie można znaleźć kanału \""+room+"\"").format(message)
        await message.channel.send(msg)
        return

    if mes.lower().startswith("kill") and not mes.lower().startswith("killer"):
        if wordsnumber(mes)<2:
            msg="Brak informacji kogo mam zabić... żałosne"
            await message.channel.send(msg)
            return
        test=None
        try:
            test=not jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię w bazie danych serwera..."
            await message.channel.send(msg)
            return
        if test:
            msg="Brak uprawnień!\nMożesz zabić kogoś w inny sposób..."
            await message.channel.send(msg)
            return
        kto=None
        try:
            kto=getmember(word(mes,2))
        except NameError:
            msg="Bardzo chciałbym zabić tę osobę, ale nie mogę jej znaleźć na serwerze..."
            await message.channel.send(msg)
            return
        if not jestrola(kto,"Żywi"):
            msg="To nie jest dusza, którą jesteśmy zainteresowani"
            await message.channel.send(msg)
            return
        ktos=None
        test=False
        for each in STUDENTS:
            if STUDENTS.name.lower()==word(mes,2):
                ktos=None
                test=True
                break
        if not test:
            msg="Nie mogę znaleźć podanej osoby w spisie uczniów"
            await message.channel.send(msg)
            return
        name=ktos.name
        dop=ktos.dop
        plik=open(PATH+"deaths.txt")
        tem=plik.read()
        lista=strtolist(tem)
        murdermessage=lista[random.randrange(len(lista))]
        murdermessage.replace("%name%",name)
        murdermessage.replace("%dop%",dop)
        murderchannel=client.get_channel(459343107868065793)
        lis=list(Despair.roles)
        for each in lis:
            if each.name=="Żywi":
                await kto.remove_roles(each)
            if each.name=="Martwi":
                await kto.add_roles(each)
        if GAME:
            for each in STUDENTS:
                if each.id==kto.id:
                    each.message=await each.updateid()
                    break
        await murderchannel.send(murdermessage)
        return

    if mes.lower().startswith("save"):
        test=None
        try:
            test=jestrola(usertomember(message.author),"Żywi")
        except NameError:
            msg="Nie znaleziono cię na serwerze"
            await message.channel.send(msg)
            return
        if not test:
            msg="Rozumiem twoją chęć bycia mesjaszem, ale ty raczej już nie zmartwychwstaniesz, by ratować świat"
            await message.channel.send(msg)
            return
        try:
            kto=getmember(word(mes,2))
        except NameError:
            msg="Nie znaleziono podanego ucznia na serwerze"
            await message.channel.send(msg)
            return
        if not jestrola(kto,"Martwi"):
            msg=("Wiem, że "+kto.display_name+" męczy się z problemem życia, ale nie musisz go od tego... ratować").format(message)
            await message.channel.send(msg)
            return
        if not jestrola(kto,"Uświęcenie"):
            msg="Jego dusza jest dla nas... conajmniej bezwartościowa"
            await message.channel.send(msg)
            return
        saver=None
        try:
            saver=getstudentindex(usertomember(message.author).display_name)
        except NameError:
            msg="Nie można znaleźć cię na liście uczniów"
            await message.channel.send(msg)
            return
        try:
            STUDENTS[saver].punkty=STUDENTS[saver].punkty-1
            lis=list(kto.roles)
            for i in range(len(lis)):
                if lis[i].name=="Martwi":
                    await kto.remove_roles(lis[i])
                if lis[i].name=="Uświęcenie":
                    await kto.remove_roles(lis[i])
                if lis[i].name=="Żywi":
                    await kto.add_roles(lis[i])
        finally:
            saveall()
            msg=(+STUDENTS[saver].name+"dzięki rytułałowi wskrzesił ucznia "+kto.display_name).format(message)
            await message.channel.send(msg)
            return
        if GAME:
            for each in STUDENTS:
                if each.id==kto.id:
                    each.message=await each.updateid()
                    break
    
    if mes.lower().startswith("reap"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Nie znalazłem cię na serwerze mistrza Monokumy"
            await message.channel.send(msg)
            return
        if not test:
            msg="Nie jesteś godny używania tej komendy padawanie!"
            await message.channel.send(msg)
            return
        lista=[]
        for i in range(len(STUDENTS)):
            if STUDENTS[i].punkty<-4 and not jestrola(STUDENTS[i].getmember(),SuperiorRole):
                lista.append(STUDENTS[i].name+" "+STUDENTS[i].surn)
        korytarz=client.get_channel(585839587885187075)
        if len(lista)==0:
            msg="Nikt tym razem nie zasłużył na śmierć"
            await message.channel.send(msg)
            return
        msg="Niektórzy uczniowie poczuli na sobie spojrzenie Ezekiela"
        await korytarz.send(msg)
        mes="Osoby, które zasłużyły na śmierć:"
        for i in range(len(lista)):
            mes=mes+"\n"+lista[i]
        await message.author.send(mes.format(message))
        return

    if mes.lower().startswith("penalty"):
        punishment=1
        if wordsnumber(mes)>1:
            punishment=int(word(mes,2))
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Jak taki obrzydliwy człowiek, jak ty, śmie sądzić innych za nas...?"
            await message.channel.send(msg)
            return
        for i in range(len(STUDENTS)):
            test=None
            try:
                test=jestrola(STUDENTS[i].getmember(),"Żywi")
            except NameError:
                msg=("Błąd!\nNie znaleziono ucznia "+STUDENTS[i].name+" na serwerze!").format(message)
                await message.author.send(msg)
                continue
            if not test:
                continue
            STUDENTS[i].punkty=STUDENTS[i].punkty-punishment
        saveall()
        msg="Wszyscy żywi zostali odpowiednio ukarani..."
        await message.channel.send(msg)
        msg="***Tylko "+str(punishment)+"?***"
        await message.channel.send(msg)
        time.sleep(0.7)
        msg="Spokojnie, dostaną więcej w swoim czasie..."
        await message.channel.send(msg)
        return

    if mes.lower().startswith("reset") and not mes.lower().startswith("resetrooms"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        for i in range(len(STUDENTS)):
            STUDENTS[i].punkty=0
            if GAME: STUDENTS[i].updateid()
        saveall()
        msg="Punkty wszystkich zostały zresetowane do 0"
        await message.channel.send(msg)
        return

    if mes.lower().startswith("votes"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        mode=word(mes,2).lower()
        if mode=="on":
            if VOTES==True:
                msg="Ale głosowanie już jest włączone!"
                await message.channel.send(msg)
                return
            else:
                VOTES=True
                try:
                    cnt=open(PATH+"settings.txt",encoding="utf-8").readlines()
                    plik=open(PATH+"settings.txt","w",encoding="utf-8")
                    for i in cnt:
                        plik.write(i.replace("votes=0","votes=1"))
                    plik.close()
                finally:
                    msg="Włączono Głosowanie!"
                    await message.channel.send(msg)
                    return
        elif mode=="off":
            if VOTES==False:
                msg="Ale głosowanie już jest wyłączone!"
                await message.channel.send(msg)
                return
            else:
                VOTES=False
                for i in range(len(STUDENTS)):
                    STUDENTS[i].vote="None"
                saveall()
                try:
                    cnt=open(PATH+"settings.txt",encoding="utf-8").readlines()
                    plik=open("Despair/settings.txt","w",encoding="utf-8")
                    for i in cnt:
                        plik.write(i.replace("votes=1","votes=0"))
                    plik.close()
                finally:
                    msg="Wyłączono Głosowanie!"
                    await message.channel.send(msg)
                    return
        elif mode=="results":
            if VOTES==False:
                msg="Ale głosowanie aktualnie nawet nie jest włączone!"
                await message.channel.send(msg)
                return
            else:
                VOTES=False
                try:
                    cnt=open(PATH+"settings.txt",encoding="utf-8").readlines()
                    plik=open(PATH+"settings.txt","w",encoding="utf-8")
                    for i in cnt:
                        plik.write(i.replace("votes=1","votes=0"))
                    plik.close()
                finally:
                    msg="Wyłączono Głosowanie!"
                    await message.channel.send(msg)
                lista=[]
                for i in range(len(STUDENTS)):
                    lista.append(0)
                maks=0
                for i in range(len(STUDENTS)):
                    if not STUDENTS[i].vote=="None" and not STUDENTS[i].name.lower()==KILLER:
                        ind=None
                        try:
                            ind=getstudentindex(STUDENTS[i].vote)
                        except NameError:
                            msg=("Wystąpił problem z ładowaniem głosu ucznia "+STUDENTS[i].name+" (na ucznia "+STUDENTS[i].vote).format(message)
                            await message.channel.send(msg)
                            continue
                        lista[ind]=lista[ind]+1
                        STUDENTS[i].vote="None"
                        if maks<lista[ind]:
                            maks=lista[ind]
                saveall()
                wiad="Proszę, oto wyniki głosowania:"
                for i in range(maks):
                    for j in range(len(lista)):
                        if lista[j]==maks-i:
                            wiad=wiad+"\n"
                            if i==0:
                                wiad=wiad+"**"
                            wiad=wiad+STUDENTS[j].name+" - "+str(lista[j])
                            if i==0:
                                wiad=wiad+"**"
                await message.channel.send(wiad.format(message))
                return                       
        else:
            msg="Nie mogę rozpoznać komendy. Możesz powtórzyć?"
            await message.channel.send(msg)
            return
        
    if mes.lower().startswith("vote") and not mes.lower().startswith("votes"):
        if not VOTES:
            msg="Nie można teraz głosować!"
            await message.channel.send(msg)
            return
        test=None
        try:
            test=jestrola(usertomember(message.author),"Żywi")
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Tylko żywi mogą głosować!"
            await message.channel.send(msg)
            return
        kto=word(mes,2).lower()
        test=None
        try:
            test=jestrola(getmember(kto),"Żywi")
        except NameError:
            msg=("Nie mogę znaleźć ucznia "+word(mes,2)+", możesz powtórzyć?").format(message)
            await message.channel.send(msg)
            return
        if not test:
            msg="Można głosować jedynie na tych, którzy jeszcze nie umarli!"
            await message.channel.send(msg)
            return
        ind=None
        try:
            ind=getstudentindex(usertomember(message.author).display_name)
        except NameError:
            msg="Mam problem ze znalezieneim cię na liście uczniów..."
            await message.channel.send(msg)
            return
        if STUDENTS[ind].vote=="None":
            STUDENTS[ind].vote=word(mes,2)
            msg=("Brawo! Zagłosowałeś/aś na ucznia o imieniu \""+word(mes,2)+"\"").format(message)
            await message.channel.send(msg)
        else:
            msg=("Zmieniłeś/aś swój głos z \""+STUDENTS[ind].vote+"\" na \""+word(mes,2)+"\"").format(message)
            await message.channel.send(msg)
            STUDENTS[ind].vote=word(mes,2)
        saveall()
        return
    
    if mes.lower().startswith("clue"):
        test=None
        try:
            test=jestrola(usertomember(message.author),"Detektyw")
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Tylko detektywi mogą dodawać poszlaki"
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<2:
            msg="Już się robi! Dodaję poszlakę... A jaką?"
            await message.channel.send(msg)
            return
        clueroom=client.get_channel(521764573372612610)
        Embed=discord.Embed(title=mes[5:])
        Embed.color=discord.Colour.green()
        Embed.set_footer(text="Poszlaka dodana przez "+usertomember(message.author).display_name)
        await clueroom.send(embed=Embed)
        return
    
    if mes.lower().startswith("random"):
        start=int(word(mes,2))
        stop=int(word(mes,3))
        if(start>stop):
            tempint=start
            start=stop
            stop=tempint
        msg=('Losowa liczba z zakresu '+str(start)+'-'+str(stop)+': '+str(random.randrange(start,stop+1))).format(message)
        await message.channel.send(msg)
        return

    if mes.lower().startswith("randlist"):
        count=wordsnumber(mes)-1
        if count<1:
            msg="Za mało danych!"
            await message.channel.send(msg)
            return
        lista=[]
        for i in range(count):
            lista.append(word(mes,i+2))
        msg=('Wylosowałem: '+str(lista[random.randrange(count)])).format(message)
        await message.channel.send(msg)
        return

    if mes.lower().startswith("murdered"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if word(mes,2)=="clear":
            MURDERED=None
            plik=open(PATH+"settings.txt","r",encoding="utf-8")
            wiersze=strtolist(plik.read())
            new=""
            for i in range(len(wiersze)):
                wiersz=wiersze[i]
                if not wiersz.startswith("murdered="):
                    new=new+wiersz+"\n"
            plik.close()
            plik=open(PATH+"settings.txt","w",encoding="utf-8")
            plik.write(new)
            msg="Ciało zostało pomyślnie rzucone na pożarcie psom piekielnym"
            await message.channel.send(msg)
            return
        else:
            MURDERED=word(mes,2)
            plik=open(PATH+"settings.txt","a",encoding="utf-8")
            plik.write("\nmurdered="+word(mes,2))
            plik.close()
            msg="Zaznaczono człowieka o imieniu "+word(mes,2)+" jako martwego"
            await message.channel.send(msg)
            return

    if mes.lower().startswith("killer"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if word(mes,2)=="clear":
            KILLER=None
            plik=open(PATH+"settings.txt","r",encoding="utf-8")
            wiersze=strtolist(plik.read())
            new=""
            for i in range(len(wiersze)):
                wiersz=wiersze[i]
                if not wiersz.startswith("killer="):
                    new=new+wiersz+"\n"
            plik.close()
            plik=open(PATH+"settings.txt","w",encoding="utf-8")
            plik.write(new)
            msg="Usunięto oznaczenie zabójcy"
            await message.channel.send(msg)
            return
        else:
            KILLER=word(mes,2)
            plik=open(PATH+"settings.txt","a",encoding="utf-8")
            plik.write("\nkiller="+word(mes,2))
            plik.close()
            msg="Zaznaczono człowieka o imieniu "+word(mes,2)+" jako zabójcę"
            await message.channel.send(msg)
            return        

    if mes.lower().startswith("sekcja"):
        if not VOTES:
            msg="Spokojnie, na razie nikt nie umarł... Możesz to zmienić :wink:"
            await message.channel.send(msg)
            return
        kto=getstudent(MURDERED)
        ind=None
        try:
            ind=getstudentindex(usertomember(message.author).display_name)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        STUDENTS[ind].punkty=STUDENTS[ind].punkty-1
        saveall()
        miejsce=['Na żebrach wykreślone są słowa: ','Na kościach wyryte są słowa: ','Na czaszce wyryte są słowa: ']
        plik=open(PATH+"sekcja.txt","r",encoding="utf-8")
        sekcja=plik.read()
        plik.close()
        msg=(sekcja+"\n\n"+miejsce[random.randrange(len(miejsce))]+kto.secret).format(message)
        await message.author.send(msg)
        msg="Zdobywasz minusa za karę za sekcję zwłok!\nSprawdź DM żeby sprawdzić przebieg sekcji"
        await message.channel.send(msg)
        msg=("Uczeń "+STUDENTS[ind].name+" dokonał sekcji zwłok").format(message)
        nauczyciele=client.get_channel(585840021224030211)
        await nauczyciele.send(msg)
        return

    if mes.lower().startswith("give"):
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<3:
            msg="Brak odpowiedniej ilości danych"
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        kto=word(mes,2)
        tresc=mes[6+len(kto):]
        ind=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Nie znaleziono takiego ucznia"
            await message.channel.send(msg)
            return
        tempstr=""
        for i in range(len(tresc)):
            if tresc[i]==',':
                tempstr=tempstr+'\\'
            tempstr=tempstr+tresc[i]
        if STUDENTS[ind].items=="":
            STUDENTS[ind].items=tempstr
        else:
            STUDENTS[ind].items=STUDENTS[ind].items+", "+tempstr
        if GAME:
            STUDENTS[ind].message=await STUDENTS[ind].updateid()
        saveall()
        msg=("Dodano \""+tresc+"\" do listy przedmiotów ucznia "+kto).format(message)
        await message.channel.send(msg)
        return

    if mes.lower().startswith("sgive"):
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<3:
            msg="Brak odpowiedniej ilości danych"
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        kto=word(mes,2)
        tresc=mes[7+len(kto):]
        ind=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Nie znaleziono takiego ucznia"
            await message.channel.send(msg)
            return
        tempstr=""
        for i in range(len(tresc)):
            if tresc[i]==',':
                tempstr=tempstr+'\\'
            tempstr=tempstr+tresc[i]
        if STUDENTS[ind].s_items=="":
            STUDENTS[ind].s_items=tempstr
        else:
            STUDENTS[ind].s_items=STUDENTS[ind].s_items+", "+tempstr
        saveall()
        msg=("Dodano \""+tresc+"\" do listy ukrytych przedmiotów ucznia "+kto).format(message)
        await message.channel.send(msg)
        return

    if mes.lower().startswith("remove") and not mes.lower().startswith("removestudent"):
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<3:
            msg="Brak odpowiedniej ilości danych"
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        kto=word(mes,2)
        tresc=mes[8+len(kto):]
        ind=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Nie znaleziono takiego ucznia"
            await message.channel.send(msg)
            return
        przedmioty=stringtolist(STUDENTS[ind].items,True)
        try:
            przedmioty.remove(tresc.lower())
        except ValueError:
            przedmioty=stringtolist(STUDENTS[ind].s_items,True)
            try:
                przedmioty.remove(tresc.lower())
            except ValueError:
                msg="Nie znaleziono podanego przedmiotu w bazie danych"
                await message.channel.send(msg)
                return
            if len(przedmioty)==0:
                STUDENTS[ind].s_items=""
            else:
                STUDENTS[ind].s_items=listtostring(przedmioty,False)
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Zabrano sekretny przedmiot uczniowi "+kto).format(message)
            await message.channel.send(msg)
            return
        if len(przedmioty)==0:
            STUDENTS[ind].items=""
        else:
            STUDENTS[ind].items=listtostring(przedmioty,False)
        if GAME:
            STUDENTS[ind].message=await STUDENTS[ind].updateid()
        saveall()
        msg=("Zabrano przedmiot uczniowi "+kto).format(message)
        await message.channel.send(msg)
        return
        
    if mes.lower().startswith("set"):
        test=None
        try:
            test=jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<4:
            msg="Brak odpowiedniej ilości danych"
            await message.channel.send(msg)
            return
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        co=word(mes,2)
        kto=word(mes,3)
        tresc=mes[(6+len(co)+len(kto)):]
        ind=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Nie znaleziono takiego ucznia"
            await message.channel.send(msg)
            return
        if co.lower()=="zdolność":
            STUDENTS[ind].ability=tresc
            saveall()
            msg=("Ustawiono zdolność ucznia "+kto+" na \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="sekret":
            STUDENTS[ind].secret=tresc
            saveall()
            msg=("Ustawiono sekret ucznia "+kto+" na \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="imię":
            if STUDENTS[ind].invert:
                STUDENTS[ind].surn=tresc
            else:
                STUDENTS[ind].name=tresc
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Zmieniono imię ucznia z "+kto+" na \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="nazwisko":
            if STUDENTS[ind].invert:
                STUDENTS[ind].name=tresc
            else:
                STUDENTS[ind].surn=tresc
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Ustawiono nazwisko ucznia "+kto+" na \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="wygląd":
            STUDENTS[ind].appe=tresc
            saveall()
            msg=("Ustawiono wygląd ucznia "+kto+" na \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="wiek":
            STUDENTS[ind].age=int(tresc)
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Ustawiono wiek ucznia "+kto+" na \""+int(tresc)+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="dopełniacz":
            STUDENTS[ind].dop=tresc
            saveall()
            msg=("Ustawiono dopełniacz dla ucznia "+kto+" jako \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="płeć":
            STUDENTS[ind].gender=tresc
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Ustawiono płeć ucznia "+kto+" jako \""+tresc+"\"").format(message)
            await message.channel.send(msg)
            return
        if co.lower()=="informacje":
            STUDENTS[ind].additional=tresc
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            msg=("Ustawiono dodatkowe informacje ucznia "+kto+" na \""+tresc+"\"")
            await message.channel.send(msg)
            return
        if co.lower()=="odwróć":
            msg=""
            if tresc.lower()=="tak" or tresc.lower()=="true" or tresc.lower()=="yes" or tresc.lower()=="1":
                if not STUDENTS[ind].invert:
                    temp=STUDENTS[ind].name
                    STUDENTS[ind].name=STUDENTS[ind].surn
                    STUDENTS[ind].surn=temp
                STUDENTS[ind].invert=True
                msg="Zrozumiałem! Od dzisiaj będziemy mówić uczniowi "+STUDENTS[ind].name+" po nazwisku!"
            elif tresc.lower()=="nie" or tresc.lower()=="false" or tresc.lower()=="no" or tresc.lower()=="0":
                if STUDENTS[ind].invert:
                    temp=STUDENTS[ind].name
                    STUDENTS[ind].name=STUDENTS[ind].surn
                    STUDENTS[ind].surn=temp
                STUDENTS[ind].invert=False
                msg="Zrozumiałem! Od dzisiaj będziemy mówić uczniowi "+STUDENTS[ind].name+" po imieniu!"
            else:
                msg="Wybacz, nie zrozumiałem. Możesz powtórzyć?"
                await message.channel.send(msg)
                return
            await message.channel.send(msg)
            if GAME:
                STUDENTS[ind].message=await STUDENTS[ind].updateid()
            saveall()
            return
            
        msg="Nie rozpoznano typu wprowadzanych informacji"
        await message.channel.send(msg)
        return

    if mes.lower().startswith("showembed"):
        kto=None
        if wordsnumber(mes)<2:
            kto=usertomember(message.author).display_name.lower()
        else:
            kto=word(mes,2).lower()
        uczn=None
        for i in range(len(STUDENTS)):
            if STUDENTS[i].name.lower()==kto:
                uczn=STUDENTS[i]
                break
            if i+1==len(STUDENTS):
                msg="Nie znaleziono podanego ucznia na liście uczniów. Spróbuj ponownie za kilka lat"
                await message.channel.send(msg)
                return
        ident=uczn.getembed(uczn.getmember().colour)
        await message.channel.send(embed=ident)

    if mes.lower().startswith("update"):
        if not GAME:
            msg="Gra się jeszcze nie zaczęła"
            await message.channel.send(msg)
            return
        try:
            test=not jestrola(usertomember(message.author),SuperiorRole)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if test:
            msg="Nie możesz tego zrobić poproś anioła o update jeśli naprawdę tego potrzebujesz"
            await message.channel.send(msg)
            return
        kto=None
        if wordsnumber(mes)<2:
            kto="all"
        else:
            kto=word(mes,2).lower()
        if kto=="all":
            for each in STUDENTS:
                each.message=await each.updateid()
        else:
            for each in STUDENTS:
                if each.name.lower()==kto:
                    each.message=await each.updateid()
                    break
        saveall()
        return

    if mes.lower().startswith("zagadka"):
        if wordsnumber(mes)<2:
            msg="Poczekaj aż pierwsza zagadka się odblokuje"
            await message.channel.send(msg)
            return
        if word(mes,2)=="1":
            msg="Poczekaj aż pierwsza zagadka się odblokuje"
            await message.channel.send(msg)
            return
        if word(mes,2)=="2":
            msg="Poczekaj aż druga zagadka się odblokuje"
            await message.channel.send(msg)
            return
        if word(mes,2)=="3":
            msg="Poczekaj aż trzecia zagadka się odblokuje"
            await message.channel.send(msg)
            return
        msg="Nie rozpoznano numeru piętra"
        await message.channel.send(msg)
        return

    if mes.lower().startswith("hasło"):
        if wordsnumber(mes)<3:
            if word(mes,2).lower()=="alfa":
                msg="Udało ci się odgadnąć hasło do sekretnego pokoju na pierwszym piętrze!\nZaraz powiem o tym dyrektorowi. On załatwi formalności"
                await message.channel.send(msg)
                msg="Uczeń "+usertomember(message.author).display_name+" odgadnął hasło do  sekretnego pokoju na pierwszym piętrze"
                Monokuma=client.get_user(330392410964361217)
                await Monokuma.send(msg)
                return
            else:
                msg="Błędne hasło. Tym razem się nie udało"
                await message.channel.send(msg)
                return
        if word(mes,2)=="1":    
            if word(mes,3).lower()=="alfa":
                msg="Udało ci się odgadnąć hasło do sekretnego pokoju na pierwszym piętrze!\nZaraz powiem o tym dyrektorowi. On załatwi formalności"
                await message.channel.send(msg)
                msg="Uczeń "+usertomember(message.author).display_name+" odgadnął hasło do sekretnego pokoju na pierwszym piętrze"
                Monokuma=client.get_user(330392410964361217)
                await Monokuma.send(msg)
                return
            else:
                msg="Błędne hasło. Tym razem się nie udało"
                await message.channel.send(msg)
                return
        if word(mes,2)=="2":    
            if word(mes,3).lower()=="omega":
                msg="Udało ci się odgadnąć hasło do sekretnego pokoju na drugim piętrze!\nZaraz powiem o tym dyrektorowi. On załatwi formalności"
                await message.channel.send(msg)
                msg="Uczeń "+usertomember(message.author).display_name+" odgadnął hasło do sekretnego pokoju na drugim piętrze"
                Monokuma=client.get_user(330392410964361217)
                await Monokuma.send(msg)
                return
            else:
                msg="Błędne hasło. Tym razem się nie udało"
                await message.channel.send(msg)
                return
        if word(mes,2)=="3":    
            if word(mes,3).lower()=="gamma":
                msg="Udało ci się odgadnąć hasło do sekretnego pokoju na trzecim piętrze!\nZaraz powiem o tym dyrektorowi. On załatwi formalności"
                await message.channel.send(msg)
                msg="Uczeń "+usertomember(message.author).display_name+" odgadnął hasło do sekretnego pokoju na trzecim piętrze"
                Monokuma=client.get_user(330392410964361217)
                await Monokuma.send(msg)
                return
            else:
                msg="Błędne hasło. Tym razem się nie udało"
                await message.channel.send(msg)
                return
        msg="Błędny numer piętra"
        await message.channel.send(msg)
        return

    if mes.lower().startswith("steal"):
        global CYCLE
        global THIEVES
        kto=None
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not (jestrola(kto,"Żywi") or jestrola(kto,SuperiorRole)):
            msg="Tak bardzo tęsknisz za życiem złodzieja, że próbujesz nawet kraść zza grobu? Pathetic."
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<3:
            msg="Za mało informacji. Co ja mam z tym kurwa zrobić?"
            await message.channel.send(msg)
        test=jestrola(kto,SuperiorRole)
        today=date.today()
        if (CYCLE-today).days<=0 and not test:
            CYCLE=nextcycle(today)
            THIEVES=[]
            plik=open(PATH+"settings.txt","r",encoding="utf-8")
            hoe=plik.read()
            wiersze=strtolist(hoe)
            for i in range(len(wiersze)):
                if wiersze[i].startswith("cycle="):
                    wiersze[i]="cycle="+CYCLE.strftime("%Y-%m-%d")
                    break
            plik.close()
            plik=open(PATH+"settings.txt","w+",encoding="utf-8")
            for i in range(len(wiersze)):
                plik.write(wiersze[i]+"\n")
            plik.close()
            plik=open(PATH+"thieves.txt","w+",encoding="utf-8")
            plik.close()
        kto=kto.display_name
        number=is_in_list(kto,THIEVES)
        if number>1:
            msg="Nie kradniesz troszkę za dużo? Mama nie mówiła, że pójdziesz za to do piekła?"
            await message.channel.send(msg)
            return
        ind=None
        ind2=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Dziwne, nie wydaje nam się, że kiedyś cię widzieliśmy"
            await message.channel.send(msg)
            return
        try:
            ind2=getstudentindex(word(mes,2))
        except NameError:
            msg="Nie mogę znaleźć osoby którą chcesz okraść... Czy na pewno wszsystko z tobą w porządku?"
            await message.channel.send(msg)
            return
        if not test:
            THIEVES.append(kto)
            plik=open(PATH+"thieves.txt","w+",encoding="utf-8")
            for each in THIEVES:
                plik.write(each+"\n")
            plik.close()
        perc=50+10*STUDENTS[ind].punkty
        if perc>85:
            perc=85
        if perc<15:
            perc=15
        if message.author.id==294476268416532480:
            perc=perc+10
        if message.author.id==663807472732995638:
            perc=perc+15
        mes=simplify(mes)
        item=mes[(len("steal  ")+len(word(mes,2))):].lower()
        items=stringtolist(STUDENTS[ind2].items,True)
        s_items=stringtolist(STUDENTS[ind2].s_items,True)
        if test:
            perc=100
        if not (is_in_list(item,items) or is_in_list(item,s_items)):
            perc=0
        test=chance(perc)
        if test:
            msg=("Udało ci się ukraść "+item+" od "+STUDENTS[ind2].dop).format(message)
            await message.channel.send(msg)
            if STUDENTS[ind].s_items=="":
                STUDENTS[ind].s_items=item
            else:
                STUDENTS[ind].s_items=STUDENTS[ind].s_items+", "+item
            if (is_in_list(item,items)):
                lista=stringtolist(STUDENTS[ind2].items,True)
                lista.remove(item.lower())
                temp=""
                for i in range(len(lista)):
                    temp=temp+lista[i]
                    if not i==len(lista)-1:
                        temp=temp+", "
                STUDENTS[ind2].items=temp
            if (is_in_list(item,s_items)):
                lista=stringtolist(STUDENTS[ind2].s_items,True)
                lista.remove(item.lower())
                temp=""
                for i in range(len(lista)):
                    temp=temp+lista[i]
                    if not i==len(lista)-1:
                        temp=temp+", "
                STUDENTS[ind2].s_items=temp
            saveall()
        else:
            msg=("Niestety nie udało ci się ukraść "+item+" od "+STUDENTS[ind2].dop+". Mam nadzieję, że "+STUDENTS[ind2].name+" się o tym nie dowie :wink:").format(message)
            await message.channel.send(msg)
            if chance(80):
                kradziony=client.get_user(STUDENTS[ind2].id)
                msg=("Psst, "+kto+" probował cię okraść... Ja bym uważał na siebie").format(message)
                await kradziony.send(msg)
        GM=client.get_user(330392410964361217)
        msg=None
        if test:
            msg=(STUDENTS[ind].name+" ukradł "+item+" uczniowi "+STUDENTS[ind2].dop).format(message)
        else:
            msg=(STUDENTS[ind].name+" próbował ukraść "+item+" uczniowi "+STUDENTS[ind2].dop+", ale nie udało im się").format(message)
        await GM.send(msg)
        return

    if mes.lower().startswith("hide"):
        if wordsnumber(mes)<2:
            msg="Mam za mało informacji. I co ja mam z tym kurwa zrobić?"
            await message.channel.send(msg)
            return
        kto=word(mes,2).lower()
        item=mes[(len("hide  ")+len(kto)):].lower()
        temp=None
        try:
            temp=usertomember(message.author).display_name
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        if not temp==kto:
            if not jestrola(usertomember(message.author),SuperiorRole):
                msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
                await message.channel.send(msg)
                return
        ind=None
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg="Nie wydaje nam się, że znamy osobę o której mówisz. Możesz powtórzyć?"
            await message.channel.send(msg)
            return
        lista=stringtolist(STUDENTS[ind].items,True)
        slista=stringtolist(STUDENTS[ind].s_items,True)
        if is_in_list(item,lista):
            lista.remove(item)
            slista.append(item)
            if len(lista)>0:
                STUDENTS[ind].items=listtostring(lista,True)
            else:
                STUDENTS[ind].items=""
            if len(slista)>0:
                STUDENTS[ind].s_items=listtostring(slista,True)
            else:
                STUDENTS[ind].s_items=""
            saveall()
            msg="Pomyślnie ukryto przedmiot "+item+"!"
            await message.channel.send(msg)
            return
        elif is_in_list(item,slista):
            msg="Ale ten przedmiot jest już ukryty!"
            await message.channel.send(msg)
            return
        else:
            msg="Nie wydaje mi się, że posiadasz taki przedmiot"
            await message.channel.send(msg)
            return

    if mes.lower().startswith("expose"):
        temp=None
        try:
            temp=usertomember(message.author).display_name
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        Err=False
        kto=None
        memb=usertomember(message.author)
        if jestrola(memb,SuperiorRole):
            if wordsnumber(mes)<3:
                Err=True
            else:
                kto=word(mes,2).lower()
                mes=simplify(mes)
                item=mes[(len("expose  ")+len(kto)):].lower()
        else:
            if wordsnumber(mes)<2:
                Err=True
            else:
                kto=temp
                mes=simplify(mes)
                item=mes[7:]
        ind=None
        if Err:
            msg="Mam za mało informacji. I co ja mam z tym kurwa zrobić?"
            await message.channel.send(msg)
            return
        try:
            ind=getstudentindex(kto)
        except NameError:
            msg=None
            if jestrola(memb,SuperiorRole):
                msg="Nie wydaje nam się, że znamy osobę o której mówisz. Możesz powtórzyć?"
            else:
                msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        lista=stringtolist(STUDENTS[ind].items,True)
        slista=stringtolist(STUDENTS[ind].s_items,True)
        if is_in_list(item,slista):
            slista.remove(item)
            lista.append(item)
            if len(lista)>0:
                STUDENTS[ind].items=listtostring(lista,True)
            else:
                STUDENTS[ind].items=""
            if len(slista)>0:
                STUDENTS[ind].s_items=listtostring(slista,True)
            else:
                STUDENTS[ind].s_items=""
            saveall()
            msg="Pomyślnie odkryto przedmiot "+item+"!"
            await message.channel.send(msg)
            return
        elif is_in_list(item,lista):
            msg="Ale ten przedmiot jest już odkryty!"
            await message.channel.send(msg)
            return
        else:
            msg="Nie wydaje mi się, że posiadasz taki przedmiot"
            await message.channel.send(msg)
            return

    if mes.lower().startswith("botreset"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        msg="Resetowanie bota..."
        global RESET, RESETCHANNEL
        RESET=True
        RESETCHANNEL=message.channel
        await message.channel.send(msg)
        await client.on_ready()

    if mes.lower().startswith("gamestart"):
        GM=client.get_user(330392410964361217)
        if message.author!=GM:
            msg="Myślisz, że możesz pierwiastkować, co ci się podoba, joktogramie?"
            await message.channel.send(msg)
            return
        if GAME:
            msg="Albo coś się zróżniczkowało w twoim source kodzie, albo twoje IQ spadło do jednocyfrowej liczby"
            await message.channel.send(msg)
            return
        GAME=True
        lines=open(PATH+"settings.txt",encoding="utf-8").readlines()
        plik=open(PATH+"settings.txt","w+",encoding="utf-8")
        for each in lines:
            plik.write(each.replace("game=0","game=1"))
        plik.close()
        for each in STUDENTS:
            each.message=await each.updateid()
        saveall()
        msg="Let the game begin"
        await message.channel.send(msg,file=discord.File(fp=PATH+"gamestart.png"))
        for each in STUDENTS:
            await updatelegit(each)

    if mes.lower().startswith("gamestop"):
        GM=client.get_user(330392410964361217)
        if message.author!=GM:
            msg="Myślisz, że możesz pierwiastkować, co ci się podoba, joktogramie?"
            await message.channel.send(msg)
            return
        if not GAME:
            msg="Albo coś się zróżniczkowało w twoim source kodzie, albo twoje IQ spadło do jednocyfrowej liczby"
            await message.channel.send(msg)
            return
        GAME=False
        lines=open(PATH+"settings.txt",encoding="utf-8").readlines()
        plik=open(PATH+"settings.txt","w+",encoding="utf-8")
        for each in lines:
            plik.write(each.replace("game=1","game=0"))
        plik.close()
        msg="Okej, koniec gry. Hope it went well, huh?"
        await message.channel.send(msg)

    if mes.lower().startswith("editroom"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<2:
            msg="Za mało informacji. Co ja mam z tym kurwa zrobić?"
            await message.channel.send(msg)
            return
        room=word(mes.lower(),2)
        for i in range(len(room)):
            if room[i]=='_' or room[i]=="-":
                temps=room[:i]
                temps=temps+' '
                temps=temps+room[(1+i):]
                room=temps
        opis=mes[(10+len(room)):]
        plik=open(PATH+"rooms/"+room+".txt","w+",encoding="utf-8")
        plik.write(opis)
        plik.close()
        msg="Pomyslnie zmieniono opis pokoju na\""+opis+"\""
        await message.channel.send(msg)

    if mes.lower().startswith("resetrooms"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        for each in glob(PATH+"rooms - plain/*.txt"):
            temps=os.path.abspath(each)
            plik=open(temps,"r",encoding="utf-8")
            text=plik.read()
            plik.close()
            temps=temps.replace("rooms - plain","rooms")
            plik=open(temps,"w+",encoding="utf-8")
            plik.write(text)
            plik.close()
        msg="Wszystkie pliki zostały odnowione!"
        await message.channel.send(msg)
    
    if mes.lower().startswith("backuprooms"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        for each in glob(PATH+"rooms/*.txt"):
            temps=os.path.abspath(each)
            plik=open(temps,"r",encoding="utf-8")
            text=plik.read()
            plik.close()
            temps=temps.replace("rooms","rooms - plain")
            plik=open(temps,"w+",encoding="utf-8")
            plik.write(text)
            plik.close()
        msg="Utworzono backup pokoi!"
        await message.channel.send(msg)

    if mes.lower().startswith("legitymacja"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<2:
            msg="I co ja mam z tym zrobić niby? Powiedz mi czyja legitymacja"
            await message.channel.send(msg)
            return
        kto=word(mes,2)
        for each in STUDENTS:
            if each.name.lower()==kto.lower():
                await updatelegit(each)
                msg="Gotowe!"
                await message.channel.send(msg)
                return
        msg="Nie znalazlem ucznia o którym mówisz"
        await message.channel.send(msg)
    
    if mes.lower().startswith("logout"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if wordsnumber(mes)>1:
            if not word(mes,2).lower()==bot_id.lower():
                return
        room=client.get_channel(735472342398009404)
        msg="Bot został wyłączony"
        await room.send(msg)
        print("Logged out at "+time.asctime())
        await client.logout()
        return

    if mes.lower().startswith("showlogged"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        msg="Aktualnie bot hostuje z id: "+bot_id
        await message.channel.send(msg)
        return

    if mes.lower().startswith("removestudent"):
        try:
            kto=usertomember(message.author)
        except NameError:
            msg="Ezekiel nigdy o tobie nie pomyślał..."
            await message.channel.send(msg)
            return
        test=jestrola(kto,SuperiorRole)
        if not test:
            msg="Dlaczego chcesz używać mocy, która do ciebie nie należy?"
            await message.channel.send(msg)
            return
        if wordsnumber(mes)<2:
            msg="I co ja mam z tym kurwa zrobić?"
            await message.channel.send(msg)
            return
        kto=word(mes,2).lower()
        id=None
        for each in STUDENTS:
            if each.name.lower()==kto:
                id=each.id
                if not each.message==0:
                    idroom=client.get_channel(618050482065375243)
                    tempo=await idroom.fetch_message(each.message)
                    await tempo.delete()
                if not each.ident==0:
                    idroom=client.get_channel(735681326463844363)
                    tempo=await idroom.fetch_message(each.ident)
                    await tempo.delete()
                STUDENTS.remove(each)
                Despair=client.get_guild(Despairid)
                members=list(Despair.members)
                for member in members:
                    if member.id==id:
                        lis=list(Despair.roles)
                        for every in lis:
                            if every.name=="Żywi" or every.name=="Żywi" or every.name=="Żywi" or every.name.startswith("Zwycięzcy"):
                                await member.remove_roles(every)
                msg="Pomyślnie usunięto ucznia "+word(mes,2)
                await message.channel.send(msg)
                saveall()
                return
        msg="Nie mogłem znaleźć ucznia. Jesteś pewny, że już go nie usunąłeś?"
        await message.channel.send(msg)
        return        

@client.event
async def on_ready():
    global STUDENTS
    global MURDERED
    global KILLER
    global VOTES
    global SuperiorRole
    global THIEVES
    global CYCLE
    global RESET
    global RESETCHANNEL
    global GAME
    global PATH
    plik=open(PATH+"settings.txt","r",encoding="utf-8")
    hoe=plik.read()
    wiersze=strtolist(hoe)
    for i in range(len(wiersze)):
        wiersz=wiersze[i]
        if wiersz.startswith("votes="):
            if (wiersz=="votes=1" or wiersz=="votes=true"):
                VOTES=True
            else:
                VOTES=False
            continue
        if wiersz.startswith("game="):
            if (wiersz=="game=1" or wiersz=="game=true"):
                GAME=True
            else:
                GAME=False
            continue
        elif wiersz.startswith("superior="):
            SuperiorRole=wiersz[9:]
            continue
        elif wiersz.startswith("murdered="):
            MURDERED=wiersz[9:]
            continue
        elif wiersz.startswith("killer="):
            KILLER=wiersz[7:]
            continue
        elif wiersz.startswith("cycle="):
            word=wiersz[6:]
            day=getday(word)
            month=getmonth(word)
            year=getyear(word)
            CYCLE=date(year,month,day)
    plik.close()
    plik=open(PATH+"thieves.txt","r",encoding="utf-8")
    hoe=plik.read()
    THIEVES=strtolist(hoe)
    plik.close()
    itis=False
    STUDENTS=[]
    atleastone=False
    recruit=student(0,"","","",18,"","","","",0,"","","None","None",0,0,False,"")
    plik=open(PATH+"students.txt","r",encoding="utf-8")
    hoe=plik.read()
    wiersze=strtolist(hoe)
    for i in range(len(wiersze)):
        wiersz=wiersze[i]
        if itis==False:
            if wiersz.startswith("id="):
                atleastone=True
                recruit.id=int(wiersz[3:])
                itis=True
                continue
        else:
            if wiersz.startswith("name="):
                recruit.name=wiersz[5:]
                continue
            if wiersz.startswith("surn="):
                recruit.surn=wiersz[5:]
                continue
            if wiersz.startswith("gender="):
                recruit.gender=wiersz[7:]
                continue
            if wiersz.startswith("age="):
                recruit.age=int(wiersz[4:])
                continue
            if wiersz.startswith("appe="):
                recruit.appe=wiersz[5:]
                continue
            if wiersz.startswith("items="):
                recruit.items=wiersz[6:]
                continue
            if wiersz.startswith("s_items="):
                recruit.s_items=wiersz[8:]
                continue
            if wiersz.startswith("punkty="):
                recruit.punkty=int(wiersz[7:])
                continue
            if wiersz.startswith("ability="):
                recruit.ability=wiersz[8:]
                continue
            if wiersz.startswith("secret="):
                recruit.secret=wiersz[7:]
                continue
            if wiersz.startswith("dop="):
                recruit.dop=wiersz[4:]
                continue
            if wiersz.startswith("vote="):
                recruit.vote=wiersz[5:]
                continue
            if wiersz.startswith("image="):
                recruit.image=wiersz[6:]
                continue
            if wiersz.startswith("message="):
                recruit.message=int(wiersz[8:])
                continue
            if wiersz.startswith("identyfikator="):
                recruit.ident=int(wiersz[14:])
                continue
            if wiersz.startswith("invert="):
                if wiersz[7:]=="True":
                    recruit.invert=True
                continue
            if wiersz.startswith("additional="):
                recruit.additional=wiersz[11:]
                continue
            if wiersz.startswith("id="):
                STUDENTS.append(recruit)
                recruit=student(int(wiersz[3:]),"","","",18,"","","","",0,"","","None","None",0,0,False,"")
                continue
    if atleastone:
        STUDENTS.append(recruit)
    plik.close()
    if GAME:
        for each in STUDENTS:
            each.message=await each.updateid()
    saveall()
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    if(VOTES==True):
        print("Można głosować")
    if not MURDERED==None:
        print("Uczeń "+MURDERED+" jest oznaczny jako martwy")
    if not KILLER==None:
        print("Uczeń "+KILLER+" jest oznaczny jako morderca")
    await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="d!help "))
    print("-------")
    if not len(STUDENTS)==0:
        print("Znaleziono uczniów:")
        for i in range(len(STUDENTS)):
            if not STUDENTS[i].invert:
                print(STUDENTS[i].name+" "+STUDENTS[i].surn)
            else:
                print(STUDENTS[i].surn+" "+STUDENTS[i].name)
    print(" ")
    if RESET:
        RESET=False
        msg="Despairbot zresetowany pomyślnie"
        await RESETCHANNEL.send(msg)

plik=open(PATH+"TOKEN.txt","r",encoding="utf-8")
TOKEN=plik.read()
plik.close()

plik=open(PATH+"bot_id.txt","r",encoding="utf-8")
bot_id=plik.read()
plik.close()

client.run(TOKEN)
while RESET:
    client.run(TOKEN)
