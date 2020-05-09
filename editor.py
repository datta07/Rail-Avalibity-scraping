#from GarudadevRailDb (part2 mainly used for adding new trains)
#adding database
import sqlite3
from datetime import timedelta

#creating db('may not be used next')
'''
con=sqlite3.connect('db1.db')
con.execute('CREATE TABLE trains (trainNo TEXT,time TEXT,src TEXT,dst TEXT,nxtDay TEXT)')
con.close()'''

#to perform delta operation b/w %H:%m
def DeltaTime(time,delta,operation,hours=0):
    [t1,t2]=time.split(':')
    t1=timedelta(hours=int(t1),minutes=int(t2))
    t2=timedelta(hours=hours,minutes=int(delta))
    if (operation=='+'):
        t=t1+t2
    else:
        t=t1-t2
    t=str(t).split(':')
    return t[0]+':'+t[1]

#to Add values into database
def AddDb(trainNo,time,src,dst,nxtDay):
    con=sqlite3.connect('db1.db')
    con.execute('INSERT INTO trains VALUES(?,?,?,?,?)',(trainNo,time,src,dst,nxtDay))
    con.commit()
    con.close()

#core function for adding and modification of database
def ModifyDb(trainNo,time,src,dst,nxtDay):
    time=DeltaTime(time,0,'-',4)
    times=[]
    times.append(DeltaTime(time,30,'-'))
    times.append(DeltaTime(time,10,'-'))
    times.append(DeltaTime(time,3,'+'))
    times.append(DeltaTime(time,7,'+'))
    times.append(DeltaTime(time,30,'+'))
    for i in times:
        AddDb(trainNo,i,src,dst,nxtDay)
    print('database updated as',time)
    print('added sucessfully')


trainNo=input('enter trainNo:-    ')
time=input('enter time:-    ')
src=input('enter src:-    ')
dst=input('enter dst:-    ')
nxtDay=input('enter nxtDay:-     ')

ModifyDb(trainNo,time,src,dst,nxtDay)

'''

        if (int(time2.split(':')[0])<10):
            time2=time2.split(':')
            time2=str(int(time2[0]))+':'+time2[1]
            self.note('modifying time as '+time2)
            '''