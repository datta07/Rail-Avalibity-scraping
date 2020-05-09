import sqlite3
import datetime
import requests
from datetime import timedelta
import time
import json
import threading
import os

os.environ['TZ']='Asia/Kolkata'
time.tzset()

#https://www.abhibus.com/trains/searchStation/SC
class TrainMon:
	def __init__(self,):
		self.deltaSleep()

	def note(self,matter):
		instantTime=time.strftime('%d-%m-%Y::')+time.strftime('%T')
		print(instantTime+':',matter)
		with open('logs.txt','a') as f:
			f.write(instantTime+':  '+matter+'\n')


	def get_status(self,trainNo,src,dst,time):
		toStnKeys={'ANV':'1467','CLX':'976','TPTY':'1419','WL':'195','BZA':'199','MAS':'266','SC':'193','TEL':'977','GNT':'1387','KCG':'1071'}
		headers={'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
		data={"trainNumber":trainNo,"class":"SL","quota":"GN","fromStnKey":int(toStnKeys[src]),"fromStnCode":src,"toStnKey":int(toStnKeys[dst]),"toStnCode":dst,"journeyDate":time}
		res=requests.post('https://www.abhibus.com/trains/getTrainAvailibilty',headers=headers,data=data).json()
		if (res['status']=='success'):
			print(res['avlFareData']['avlDayList'][0]['availablityStatus'])
			return res['avlFareData']['avlDayList'][0]['availablityStatus']
		else:
			return 'ENTER THE WRONG.....'

	def set_firebase(self,path,data):
		url1='https://guvi-41d93.firebaseio.com/trains/'+path+'/.json'
		if path=='':
			url1='https://guvi-41d93.firebaseio.com/'
		r = json.dumps(data)
		to_database = json.loads(r)
		requests.patch(url = url1 , json = to_database)

	def doAll(self,uploades):
		l=len(uploades)
		for i in range(l):
			arr=uploades.pop()
			tommorow=str(datetime.date.today()+datetime.timedelta(1))
			if (arr[-1]=='1'):
				status=self.get_status(arr[0],arr[2],arr[3],tommorow)
			else:
				status=self.get_status(arr[0],arr[2],arr[3],time.strftime('%Y-%m-%d'))
			self.note(': Uploading status of '+arr[0]+' from '+arr[2]+' to '+arr[3]+' as '+status)
			self.set_firebase(arr[2]+'-'+arr[3]+'/'+arr[0]+'/'+time.strftime('%d-%m-%Y')+':'+time.strftime('%A'),{time.strftime('%T'):status})
		self.note('uploaded the work of '+arr[1])

	def fetchData(self,nxtTime):
		#uploades=self.getInfo(2,'16:22')
		l=nxtTime.split(':')
		l[0]=str(int(l[0]))
		nxtTime=l[0]+':'+l[1]
		uploades=self.getInfo(2,nxtTime)
		print(uploades)
		if (uploades==[]):
			self.deltaSleep()
		else:
			threading.Thread(target=self.doAll,args=(uploades,)).start()
		self.deltaSleep()

	def deltaSleep(self):
		self.sch,self.times=self.getInfo(1)
		time1=time.strftime('%H:%M')
		for no,i in enumerate(self.times):
			k=i.split(':')
			if (len(k[0])==1):
				self.times[no]='0'+k[0]+':'+k[1]
		if (time1 not in self.times):
			self.times.append(time1)
		self.times.sort()
		try:
			nxtTime=self.times[self.times.index(time1)+1]
		except Exception:
			nxtTime=self.times[0]
		self.note('sleeping for next '+nxtTime)
		time.sleep(self.DeltaTime(nxtTime,time1,'-'))
		self.note('waked up at  '+time.strftime('%H:%M'))
		self.fetchData(nxtTime)


	def DeltaTime(self,ta,tb,operation):
		(t1,t2)=ta.split(':')
		(t3,t4)=tb.split(':')
		t1=timedelta(hours=int(t1),minutes=int(t2))
		t2=timedelta(hours=int(t3),minutes=int(t4))
		if (operation=='+'):
		    t=t1+t2
		else:
		    t=t1-t2
		return t.seconds


	def getInfo(self,purpose,time2=time.strftime('%H:%M')):
		con=sqlite3.connect('db1.db')
		if (purpose==1):
			values=con.execute('SELECT * FROM trains')
			times=[]
			sch=[]
			for i in values:
				times.append(i[1])
				sch.append(i)
			times=list(set(times))
			return (sch,times)
		else:
			values=con.execute('SELECT * FROM trains where time=?',(time2,))
			value=[]
			for i in values:
				value.append(i)
			return value

k=TrainMon()
