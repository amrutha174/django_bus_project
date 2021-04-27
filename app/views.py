from django.shortcuts import render
import math,random
from app.models import *
from app import forms
import datetime
from django.db import connection
import requests
from django.core.mail import send_mail
import json
from django.shortcuts import redirect
import mysql.connector

#manual db connection
my_cursor=connection.cursor()
host='localhost'
port=3306
User='root'
password='root@123'
database='Bus_app1'
my_con=mysql.connector.connect(host=host,port=port,user=User,password=password,database=database)
my_cursor=my_con.cursor()

#text msg requirement
reqUrl='https://www.sms4india.com/api/v1/sendCampaign'
apiKey='ASEGS1KQEXVN4S4KN8ZVZYEL03ZS1PME'
secretKey='8ZGLYV0IOPFNCPLN'
useType='stage'
senderId='hamsbusbooking@gmail.com'

#function for e-mail seding
def sendPostRequest(reqUrl,apiKey,secretKey,useType,phoneNo,senderId,textMessage):
	req_params={
		'apiKey':apiKey,
		'secret':secretKey,
		'useType':useType,
		'phone':phoneNo,
		'message':textMessage,
		'senderId':senderId
	}
	return requests.post(reqUrl,req_params)


#Singup view 

def SignUpPage(request):
	DATE=datetime.datetime.now()
	MSG='Welcome to Busbooking-Website'

	lst=forms.BusForm

	if request.method=='POST':
		data_lst=forms.BusForm(request.POST)
		if data_lst.is_valid():
			sql1='select * from bus_app1.app_busbooking where `EMAIL`= %s'
			EMAIL=data_lst.cleaned_data['EMAIL']
			data=(EMAIL,)
			my_cursor.execute(sql1,data)
			res=my_cursor.fetchone()
			if res!=None:
				if(EMAIL==res[2]):
					return redirect(LoginPage)
				else:
					return render(request,'app/Exists.html')
			else:
				NAME=data_lst.cleaned_data['NAME']
				E_MAIL=data_lst.cleaned_data['EMAIL']
				PH=data_lst.cleaned_data['PH_NO']
				USERNAME=data_lst.cleaned_data['USERNAME']
				PASSWORD=data_lst.cleaned_data['PASSWORD']
				PH_NO=int(PH)
				data6=(NAME,E_MAIL,PH,USERNAME,PASSWORD)
				request.session['data6_ses']=data6
				otp=int(gen_otp())
				print(otp)
				print(type(otp))
				request.session['otp_ses']=otp
				send_mail('BusBooking',f"hello Your OTP is {otp}",'nishvikaabcbtm@gmail.com',[f'{E_MAIL}'])
				msg1=f"hello Your OTP is {otp} please verify it!!!"
				sendPostRequest(reqUrl,apiKey,secretKey,useType,PH_NO,senderId,msg1)
				return redirect(Checkotp)
	my_dict={'lst':lst}
	return render(request,'app/Signup.html',my_dict)

#when an existing email id is entered
def Exists(request):
	if request.method=='POST':
		return redirect(SingUpPage)
	return render(request,'app/exists.html')


#function to generate otp
def gen_otp():
	digits='0123456789'
	OTP=""

	for i in range(4):
		OTP+=digits[math.floor(random.random()*10)]
	return OTP


#function to validate otp 
def Checkotp(request):
	
	ds=forms.Otp_Ver
	
	if request.method=='POST':

		ds_data=forms.Otp_Ver(request.POST)
		print(ds_data)
		if ds_data.is_valid():
			OTP_ses=ds_data.cleaned_data['OTP']
			print(OTP_ses)
			print(type(OTP_ses))
			request.session['OTP_ses']=OTP_ses
			return redirect(NewUpdate)
	dict4={'ds':ds}
	return render(request,'app/otp.html',dict4)

#LoginPage
def LoginPage(request):
	ls=forms.LoginForm
	if request.method=='POST':
		ls_data=forms.LoginForm(request.POST)
	
		if ls_data.is_valid():
			sql2='select * from bus_app1.app_busbooking where `USERNAME`=%s and `PASSWORD`=%s'
			UN=ls_data.cleaned_data['USERNAME']
			PWD=ls_data.cleaned_data['PASSWORD']
			data=(UN,PWD)
			my_cursor.execute(sql2,data)
			res1=my_cursor.fetchone()
			request.session['CSID_ses']=res1[0]
			if res1!=None:
				return redirect(Details)
			else:
				return render(request,'Wpwd.html')
	dict2={'ls':ls}	
	return render(request,'app/login.html',dict2)

#Updating the user informantion to the db after succesfull authentication
def NewUpdate(request):
	otp=request.session.get('otp_ses')
	OTP_ses=request.session.get('OTP_ses')
	data6=request.session.get('data6_ses')
	if otp==OTP_ses:
		sql9='insert into bus_app1.app_busbooking (`NAME`,`EMAIL`,`PH_NO`,`USERNAME`,`PASSWORD`) values (%s,%s,%s,%s,%s)'
		my_cursor.execute(sql9,data6)
		my_con.commit()
		return redirect(LoginPage)
	else:
		return render(request,'app/notvalid.html')

#no buses for entred routes
def failure(request):
	if request.method=='POST':
		return redirect(Details)
	return render(request,'app/Nobus.html')


#Updating the Register database regarding the customer and bus details
def Redir(request):
	sq='insert into bus_app1.app_register (`DATE`,`TIME`,`CSID`,`BID`,`Num_seats`,`Total_Fare`) values(%s,%s,%s,%s,%s,%s)'
	CSID=request.session.get('CSID_ses')
	BID=request.session.get('BID_ses')
	DATE=datetime.date.today()
	now=datetime.datetime.now()
	TIME=now.strftime("%H:%M:%S")
	Num_seats=request.session.get('Num_ses')
	Total_Fare=request.session.get('FARE_sess')

	data=(DATE,TIME,CSID,BID,Num_seats,Total_Fare)
	print(data)
	my_cursor.execute(sq,data)
	my_con.commit()
	msg=request.session.get('msg_ses')
	E_MAIL=request.session.get('Email_ses')
	send_mail('BusBooked',msg,'hamsbusbooking@gmail.com',[f'{E_MAIL}'])
	print('mail sent')
	PH_NO=request.session.get('Ph_ses')
	sendPostRequest(reqUrl,apiKey,secretKey,useType,PH_NO,senderId,msg)
	print('succussful')
	return render(request,'app/Success.html')


#Provides the user view to search for the required Route
def Details(request):
	sd=forms.BusDetailsForm
	if request.method=='POST':
		data=forms.BusDetailsForm(request.POST)

		if data.is_valid():
			FROM_H=data.cleaned_data['FROM']
			TO_H=data.cleaned_data['TO']
			sql_query='select * from bus_app1.app_busdetails where `FROM`=%s and `TO`=%s'
			data1=(FROM_H,TO_H)
			my_cursor.execute(sql_query,data1)
			rec=my_cursor.fetchone()
			print(rec)
			print(FROM_H)
			print(TO_H)
			if rec !=None:
				if FROM_H==rec[1] and TO_H==rec[2]:
					From_ses=FROM_H
					request.session['From_ses']=From_ses
					To_ses=TO_H
					request.session['To_ses']=To_ses
					return redirect(result)
				
				else:
					return redirect(failure)
	dict1={'sd':sd}
	return render(request,'app/Welcome.html',context=dict1)

#Provodes the Result for entered Route
def result(request):
	sq_query='select * from bus_app1.app_busdetails where `FROM`=%s and `TO`=%s'
	To_ses=request.session.get('To_ses')
	From_ses =request.session.get('From_ses')
	data=(From_ses,To_ses)
	my_cursor.execute(sq_query,data)
	my_cursor.execute(sq_query,data)
	res=my_cursor.fetchone()
	print(res)
	BID=res[0]
	BNAME=res[3]
	BTIME=res[4]
	BFARE=res[5]
	request.session['BID_ses']=BID
	dict3={'Ob1':BNAME,'Ob2':BTIME,'Ob3':BFARE,'Ob4':BID}
	if request.method=='POST':
		return redirect(Booked)
	return render(request,'app/result.html',context=dict3)

#view for Accepting and booking of the bus
def Booked(request):
	reg_lst=forms.Confirm
	if request.method=='POST':
		reg_data=forms.Confirm(request.POST)
		print(reg_data)
		if reg_data.is_valid():
			Num_seats=reg_data.cleaned_data['Num_Seats']
			request.session['Num_ses']=Num_seats
			sq_bk='select * from bus_app1.app_busbooking where CSID=%s'
			CSID=request.session.get('CSID_ses')
			data=(CSID,)
			my_cursor.execute(sq_bk,data)
			res3=my_cursor.fetchone()
			print(res3)
			CSID=res3[0]
			NAME=res3[1]
			E_MAIL=res3[2]
			request.session['Email_ses']=E_MAIL
			PH=res3[3]
			PH_NO=int(PH)
			request.session['Ph_ses']=PH_NO
			BID=request.session.get('BID_ses')
			sq_dt='select `Total_seats` from  bus_app1.app_busdetails where `BID`=%s'
			data1=(BID,)
			my_cursor.execute(sq_dt,data1)
			Total_seats=my_cursor.fetchone()
			print(Total_seats)

			Rem_Seats=Total_seats[0]-Num_seats
			print(Rem_Seats)
			
			up_sql='update bus_app1.app_busdetails SET `Total_seats` = %s where `BID`=%s'
			data2=(Rem_Seats,BID)

			my_cursor.execute(up_sql,data2)
			my_con.commit()

			print('No. of seats are updated')
			sq_dt='select * from  bus_app1.app_busdetails where BID=%s'
			
			my_cursor.execute(sq_dt,data1)
			res4=my_cursor.fetchone()
			print(res4)
			BUSNUM=res4[0]
			FROM=res4[1]
			TO=res4[2]
			BUSNAME=res4[3]
			BUSTIME=res4[4]
			Tot_FARE=res4[5]*Num_seats
			request.session['FARE_sess']=Tot_FARE
			msg=f'Hello  {NAME} This message is from H.A.M.S. Bus-booking Website regarding your booking of {Num_seats} seats in {BUSNAME} Bus  from {FROM} to {TO}, The Bus Number is {BUSNUM}, your boarding time is at {BUSTIME} and total fare is {Tot_FARE} Have safe Journey!!!'
			request.session['msg_ses']=msg
			
			return redirect(Redir)
	dict8 ={'reg_lst':reg_lst}
	return render(request,'app/confirm.html',dict8)