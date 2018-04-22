#!/usr/bin/env python3.6
import urllib.request
from bs4 import BeautifulSoup
import re
import smtplib
import time

site= "https://in.bookmyshow.com/buytickets/avengers-infinity-war-3d-bengaluru/movie-bang-ET00074502-MT/" #Replace this your movieandcity url
date="20180427" #replace the date with the date for which you'd like to book tickets! Format: YYYYMMDD
site=site+date
venues = ['INMB', 'PVIV', 'PVIM'] #this can be found by inspecting the element data-id for the venue where you would like to watch
delay=300 #timegap in seconds between 2 script runs

TO = 'to@gmail.com' #mail id for which you want to get alerted
GMAIL_USER = 'from@gmail.com'
GMAIL_PASS = 'password'
SUBJECT = 'Tickets are now available, Book fast'
TEXT = 'The tickets are now available for the infinity war at the venue '

def send_email(venue):
    print("Sending Email")
    smtpserver = smtplib.SMTP("smtp.gmail.com",587)
    smtpserver.ehlo()
    smtpserver.starttls()
    smtpserver.ehlo
    smtpserver.login(GMAIL_USER, GMAIL_PASS)
    header = 'To:' + TO + '\n' + 'From: ' + GMAIL_USER
    header = header + '\n' + 'Subject:' + SUBJECT + '\n'
    print(header)
    msg = header + '\n' + TEXT + venue + ' \n\n'
    smtpserver.sendmail(GMAIL_USER, TO, msg)
    smtpserver.close()
    print('Email sent!!')

page = urllib.request.urlopen(site)
soup = BeautifulSoup(page, 'lxml')
soup = soup.find_all('div', {'data-online': 'Y'})
line = str(soup)
soup = BeautifulSoup(line, 'lxml')
for venue in venues:
    soup = soup.find_all('a', {'data-venue-code': venue})
    line = str(soup)
    result = re.findall('data-availability="A"', line)
    if len(result) > 0:
        print("Available at " + venue)
        send_email(venue)
    else:
        print("Not available yet at " + venue)
    soup = BeautifulSoup(line, 'lxml')

# # time.sleep(delay)
