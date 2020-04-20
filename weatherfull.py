from tkinter import *
import requests
import json
from bs4 import BeautifulSoup
import webbrowser
from opencage.geocoder import OpenCageGeocode
import calendar
from tkinter import messagebox

root=Tk()
api_key = "d137043cf1ecf1f71d4f63e828eeb9a7"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
s=StringVar()
lat=1
lon=2
def f():
    global root,lat,lon
    city_name=s.get()
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url)
    x = response.json()
    if x['cod']!="404":
        y = x["main"] 

        current_temperature =y["temp"]
        l3['text']='%.2f'%(current_temperature - 273.15)
  
        current_pressure = y["pressure"]
        l5['text']=current_pressure

        current_humidity = y["humidity"]
        l7['text']=current_humidity

        z = x["weather"] 
        weather_description = z[0]["description"]
        l9['text']=weather_description
        llkey='d39bcd9700844b8290f3e10ce6272965'
        geocoder = OpenCageGeocode(llkey)
        query =city_name 
        results = geocoder.geocode(query)	
        lat = results[0]['geometry']['lat']
        lng = results[0]['geometry']['lng']
        #print (lat, lng)
    else:
        messagebox.showinfo("OOPS", "Invalid City Name")
        s.set('')
        

def seemap():
    webbrowser.open("https://www.google.com/maps/place/"+s.get())

def days():
    api_call = 'https://api.openweathermap.org/data/2.5/forecast?appid=' + api_key

    api_call += '&q=' + s.get()
    json_data = requests.get(api_call).json()

    location_data = {
        'city': json_data['city']['name'],
        'country': json_data['city']['country']
    }
    current_date = ''
    root1=Tk()
    root1.title('7days report')
    root1.config(bg='black',width=50)
    x1=Label(root1,text='date',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
    x1.grid(row=0,column=0,padx=5,pady=5)
    x2=Label(root1,text='time',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
    x2.grid(row=0,column=1,padx=5,pady=5)
    x3=Label(root1,text='Condition',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
    x3.grid(row=0,column=2,padx=5,pady=5)
    x4=Label(root1,text='C',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
    x4.grid(row=0,column=3,padx=5,pady=5)
    x5=Label(root1,text='F',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
    x5.grid(row=0,column=4,padx=5,pady=5)

    # Iterates through the array of dictionaries named list in json_data
    i=1
    for item in json_data['list']:
        j=0

        # Time of the weather data received, partitioned into 3 hour blocks
        time = item['dt_txt']

        # Split the time into date and hour [2018-04-15 06:00:00]
        next_date, hour = time.split(' ')

        # Stores the current date and prints it once
        if current_date != next_date:
            current_date = next_date
            year, month, day = current_date.split('-')
            date = {'y': year, 'm': month, 'd': day}
            d='\n{m}/{d}/{y}'.format(**date)
        
        # Grabs the first 2 integers from our HH:MM:SS string to get the hours
        hour = int(hour[:2])

        # Sets the AM (ante meridiem) or PM (post meridiem) period
        if hour < 12:
            if hour == 0:
                hour = 12
            meridiem = 'AM'
        else:
            if hour > 12:
                hour -= 12
            meridiem = 'PM'

        # Prints the hours [HH:MM AM/PM]
        t=('\n%i:00 %s' % (hour, meridiem))

        # Temperature is measured in Kelvin
        temperature = item['main']['temp']

        # Weather condition
        description = item['weather'][0]['description'],

        # Prints the description as well as the temperature in Celcius and Farenheit
        if i%2!=0:
            x6=Label(root1,text=d,bg='black',fg='white',bd=5,font=('arial',10),height=1,width=20)
            x6.grid(row=i,column=j,padx=5,pady=5)
            j+=1
            x7=Label(root1,text=t,bg='black',fg='white',bd=5,font=('arial',10),height=1,width=20)
            x7.grid(row=i,column=j,padx=5,pady=5)
            j+=1
            x8=Label(root1,text=description,bg='black',fg='white',bd=5,font=('arial',10),height=1,width=20)
            x8.grid(row=i,column=j,padx=5,pady=5)
            j+=1
            x9=Label(root1,text='%.2f'%(temperature - 273.15),bg='black',fg='white',bd=5,font=('arial',10),height=1,width=20)
            x9.grid(row=i,column=j,padx=5,pady=5)
            j+=1
            x10=Label(root1,text='%.2f'%(temperature * 9/5 - 459.67),bg='black',fg='white',bd=5,font=('arial',10),height=1,width=20)
            x10.grid(row=i,column=j,padx=5,pady=5)
        i+=1

root.title('Weather info')
root.configure(bg='#00b0bd')
l1=Label(root,text='Enter city name',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
l1.grid(row=0,column=0,padx=5,pady=5)
e1=Entry(root,textvariable=s,bg='#e0a8c0',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
e1.grid(row=0,column=1,padx=5,pady=5)

b=Button(root,text='submit',bg='#ffcccc',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED,command=f)
b.grid(row=1,column=1,padx=5,pady=5)

l2=Label(root,text='Temprature(in Celcius) =',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
l2.grid(row=2,column=0,padx=5,pady=5)
l3=Label(root,bg='#e0a8c0',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED,width='18')
l3.grid(row=2,column=1,padx=5,pady=5)

l4=Label(root,text='Atmospheric Pressure (in hPa unit) =',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
l4.grid(row=3,column=0,padx=5,pady=5)
l5=Label(root,bg='#e0a8c0',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED,width='18')
l5.grid(row=3,column=1,padx=5,pady=5)

l6=Label(root,text='Humidity (in percentage) =',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
l6.grid(row=4,column=0,padx=5,pady=5)
l7=Label(root,bg='#e0a8c0',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED,width='18')
l7.grid(row=4,column=1,padx=5,pady=5)

l8=Label(root,text='Description =',bg='#48a1c2',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED)
l8.grid(row=5,column=0,padx=5,pady=5)
l9=Label(root,bg='#e0a8c0',fg='black',bd=5,font=('arial',20,'bold'),relief=RAISED,width='18')
l9.grid(row=5,column=1,padx=5,pady=5)

b1=Button(root,text='See map',bg='black',fg='white',bd=5,font=('arial',20,'bold'),command=seemap,width=30)
b1.grid(row=7,column=1,padx=5,pady=5)

b2=Button(root,text='Next 4 days report',bg='black',fg='white',bd=5,font=('arial',20,'bold'),command=days,width=30)
b2.grid(row=7,column=0,padx=5,pady=5)

root.mainloop()
