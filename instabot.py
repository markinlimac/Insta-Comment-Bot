# -*- coding: utf-8 -*-

import re
import csv
from time import sleep
import os
import sys
import pathlib
from timeit import default_timer as timer
import datetime
import instaloader

class GetFollowees:
    def __init__(self, insta):
        self.insta = insta
    
    def makeFolloweesCSV(self):    
        pathlib.Path('downloads/').mkdir(parents=True, exist_ok=True) #pegar o diretorio atual
        start = timer()

        f = open('input.txt','r')
        accounts = f.read()
        p = accounts.split('\n')

        with open('last.txt','r') as f:
            last =  f.read()
            last = last.strip()
        print('Last account scraped was:',last)

        for profile in p:
            if last in profile and len(last)>2:
                print(last,profile)
                p.remove(profile)
         
        # input()
        print('Resuming from:',p[0])
        PROFILE = p[:]
        print(PROFILE)
        print('Total accounts:',len(PROFILE))

        for ind in range(len(PROFILE)):
            pro = PROFILE[ind]
            try:
                print('\n\nGetting followees from',pro)
                filename = 'downloads/'+pro+'.csv'
                with open(filename,'a',newline='',encoding="utf-8") as csvf:

                    csv_writer = csv.writer(csvf)
                    csv_writer.writerow(['username','is_verified'])


                profile = instaloader.Profile.from_username(self.insta.context, pro)
                main_followees = profile.followees
                count = 0
                total=0
                # Print list of followees
                for person in profile.get_followees():
                    try:
                        total+=1
                        username = person.username
                        is_verified = person.is_verified

                        print('Username:',username)
                        with open(filename,'a',newline='') as csvf:

                            csv_writer = csv.writer(csvf)
                            csv_writer.writerow([username,is_verified])
                        # os.system('clear')
                        # os.system('cls' if os.name == 'nt' else 'clear')

                        print('--------------------------------------------------------------------------------\nTotal followees scraped:',total,' out of',main_followees)
                        print('Time:',str(datetime.timedelta(seconds=(timer()-start))))
                        print('Current Account:',ind+1,'\t Remaining Accounts:',len(PROFILE)-ind-1 ,'\nAccount Name:',pro)


                    except Exception as e:
                        print(e)


                #saving the last account for resume
                f=open('last.txt','w+')
                f.write(pro)
                f.close()
                #log of completed account
                f=open('completed.txt','a+')
                f.write(pro+'\n')
                f.close()
                # (likewise with profile.get_followers())
            except Exception as e:
                print(e)
                print('Skipping',pro)
