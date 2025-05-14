import requests
import datetime
import time
import sys, traceback
import json



##def add_timestamp(n,msg,sound,tor='',first=1,dl=0):
##
##      
##    if n==0:
##
##        if first==0 and n==0:
##            self.text.insert("end",'\n')
##            self.text.insert("end", f'          {tor}\n\n','bold' )
##     
##            
##    
##        
##        
##        
##
##    else:
##
##        
##
##
##
##        if dl==1: #usual word selection 
##
##            self.text.insert("end",msg,['usual','test'])
##        
##
##            
##        else:
##
##            self.text.insert("end",msg,['supa','test'])
## 
##



# Try to load previous message

# Load from file
##try:
##    with open("output.txt", "r", encoding="utf-8") as f:
##        messages = [line.strip() for line in f if line.strip()]
##except FileNotFoundError:
##    messages = []  # First run — no file yet


try:
    with open("data.json", "r", encoding="utf-8") as f:
        combined = json.load(f)
        kuits = combined.get("kuits", {})
        sits = combined.get("sits", {})
        messages = combined.get("messages", {})
except FileNotFoundError:
    kuits = {}
    sits = {}
    messages = []

except json.decoder.JSONDecodeError:
    kuits = {}
    sits = {}
    messages = []   

print("loaded kuits", kuits)
print("loaded sits", sits)
print("loaded messages", messages)

def core():
    global kuits, sits
    def connect(url):
        loop_counter=0
        check_url=url

        while 1==1:
            req=s.get(check_url)
            req=req.json()
            #print('loop counter is ',loop_counter)
            loop_counter+=1

            if loop_counter>10:
                return req
                
            if 'message' in req:
                if loop_counter%2:
                    check_url=url
                else:
                    check_url=url.replace('matches/?from','matches?from')
            else:
                return req

            time.sleep(1)


        
    def dummy():
        if req['matches'][0].get('MatchTimeStamp',99)==99:
            dat=req['matches'][-1].get('startdate')
            dat_day=int(dat.split('T')[0].split('-')[-1])
            if dat_day==from_to_oop_today.day:
                dummy_check=1
            else:
                dummy_check=0
        else:
            dummy_check=1
        return dummy_check

    def fill(): #add tor id to the list if no oop for today
        
        
        for che in torns:
            url=f'https://api.wtatennis.com/tennis/tournaments/{che[1]}/{year}/matches/?from={today_oop}&to={today_oop}'

            req=connect(url)

            if 'matches' in req and len(req['matches'])>0:
                if che[1] in temp_container:
                    del temp_container[che[1]]  
                
            else:
                
                temp_container.update({che[1]:today_oop}) 
                

    def info():
        

        url_det=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={yesterday}&to={from_to_oop}'
        det=connect(url_det)


        surface=det['tournament']['surface']         

        envionment=det['tournament']['inOutdoor']
        if envionment=='O':
            envionment='Outdoor'
        else:
            envionment='Indoor'

        city=det['tournament']['city'].lower()
        endD=det['tournament']['endDate']
        startD=det['tournament']['startDate']


        if city:
            spoc_city=city.capitalize()
        else:
            spoc_name=det['tournament']['tournamentGroup']['name']
            spoc_city=spoc_name.replace('125','')
            spoc_city=spoc_city.lower().capitalize()

        if '125' in det['tournament']['tournamentGroup']['name']:
            spoc_name=f'{year} WTA {spoc_city} 125K Series{slovar2.get(eventTypeCode)}'
            
        else:
            spoc_name=f'{year} WTA {spoc_city}{slovar2.get(eventTypeCode)}'
        
        
        msg_info=f'       {spoc_name}\n'
        sur_enf=f'       Surface: {surface}\n       Environment: {envionment}\n'
        tor_date=f'       From: {startD} To: {endD}\n\n'

 


        
    
    dc={}
    n_dc_old={}
    n_dc={}
    name_dc_old={}
    name_dc={}

    seq={}
    
    seq_old={}

    #sits={}
    #kuits={}

    repl={}
    
    now=datetime.datetime.now()
    
    old_day=now.day

    year=now.year
    future_date = now+datetime.timedelta(days=5)

    if year != future_date.year:
       year = future_date.year


    from_oop_repl=now-datetime.timedelta(1)
    from_oop_repl=from_oop_repl.strftime('%Y-%m-%d') #yesterday
    to_oop_repl=now+datetime.timedelta(1)
    to_oop_repl=to_oop_repl.strftime('%Y-%m-%d') #from_to_oop    
    
    from_=now.strftime('%Y-%m-%d')
    to_=now+datetime.timedelta(4)
    to_=to_.strftime('%Y-%m-%d')
    url=f'https://api.wtatennis.com/tennis/tournaments/?page=0&pageSize=100&excludeLevels=ITF&from={from_}&to={to_}'
    ids=s.get(url).json()

    torns=[]
    torns_string=''

    temp_container={}

    oop_containter={} #for walkovers
    all_matches_container={}
    walkovers_id=[]


    from_to_oop_today=now+datetime.timedelta(1)
    today_oop=now.strftime('%Y-%m-%d')

    from_to_oop=from_to_oop_today.strftime('%Y-%m-%d')

    yesterday=now-datetime.timedelta(1)
    yesterday=yesterday.strftime('%Y-%m-%d')

    slovar={'LS':'SINGLES','LD':'DOUBLES','RS':'QUALS','QD':'DOUBLES QUALS','RD':'DOUBLES QUALS'}
    slovar2={'LS':'','LD':' Doubles','RS':' Qualification','QD':' Doubles Qualification','QS':' Qualification','MDS':'','MDD':' Doubles'}
    
    first_change=0

    if (len(messages) == 0):
        n=0
        flag=0
    else:
        n=1
        flag=1        

    change_draw=0

    torns_header_prev=[]

    #messages = []

    while (1==1):
        print("starting")
        try:


                
    

            now=datetime.datetime.now()
            time_of_last_check = now
            
            if n!=0 and now-time_of_last_check>datetime.timedelta(minutes=15):

                text='No updates for 15 min. Is something wrong?\n'

                time_of_last_check=now

            day=now.day
            old_day = day
            
            if day!=old_day:
                from_=now.strftime('%Y-%m-%d')

                to_=now+datetime.timedelta(4)
                to_=to_.strftime('%Y-%m-%d')
#-----------------------------------walkover-----------
                yesterday=now-datetime.timedelta(1)
                yesterday=yesterday.strftime('%Y-%m-%d')                
#--------------------------------------------------------                
                today_oop=now.strftime('%Y-%m-%d')
                from_to_oop_today=now+datetime.timedelta(1)
                from_to_oop=from_to_oop_today.strftime('%Y-%m-%d')

                from_oop_repl=now-datetime.timedelta(1)
                from_oop_repl=from_oop_repl.strftime('%Y-%m-%d')
                to_oop_repl=now+datetime.timedelta(1)
                to_oop_repl=to_oop_repl.strftime('%Y-%m-%d')                

                n=0
                old_day=day
    
            old_day=day
            time_=now.strftime('%H:%M')
            print("n -",n)
            if n==0:
                torns=[]
                torns_header=[]
                
                kuits={}
                torns_string=''
                url=f'https://api.wtatennis.com/tennis/tournaments/?page=0&pageSize=100&excludeLevels=ITF&from={from_}&to={to_}'
                
                ids=s.get(url).json()
                for id_ in ids['content']:
                    
                        
                        tor_name=id_['tournamentGroup']['name']
                        tor_name=tor_name.split(' ')
                        tor_name='-'.join(tor_name)
                        torns.append((tor_name,id_['tournamentGroup']['id']))
                        torns_string+=id_['tournamentGroup']['name']+' '
                        torns_header.append(tor_name)

                        all_matches_container.update({tor_name:[]})
                        
                        kuits.update({tor_name:[[0,0],[0,'none'],[0,'none'],[0,'none'],[0,'none']]})
                        
                        if flag==0:
                            sits.update({tor_name:[[0,0,{'players':[]}],[1,0,{'players':[]}],[2,0,{'players':[]}],[3,0,{'players':[]}],[4,0,{'players':[]}],'nothing']})
                            repl.update({tor_name:[]})
                            sits[tor_name][5]='nothing'

                        elif tor_name not in torns_header_prev:
                            sits.update({tor_name:[[0,0,{'players':[]}],[1,0,{'players':[]}],[2,0,{'players':[]}],[3,0,{'players':[]}],[4,0,{'players':[]}],'nothing']})
                            
                        else:
                            pass

                torns_header_prev=torns_header.copy()
                header=''
                header=(', ').join(torns_header)


            
##            msg=f'-Checking for updates in {header}\n-Last checked: {time_}\n\n'
##
##            messages.append(msg)

            time_of_last_check = now

            for x in torns:
                
                req=s.get(f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/players')


                

                try:
                    discp=len(req.json()['events'])
                    skip=0

                except:

                    skip=1


                 

                if skip==0:
                    old_situation=[[0,0],[1,0],[2,0],[3,0],[4,0]]
                    situation=[]
                    for ii,y in enumerate(req.json()['events']):
                            ids_list = []

                            eventTypeCode=y.get("eventTypeCode")

                            if eventTypeCode=='RS':
                                i=0
                            elif eventTypeCode=='LS':
                                i=1
                            elif eventTypeCode=='LD':
                                i=2
                            elif eventTypeCode=='RD':
                                i=3
                            elif eventTypeCode:
                                i=4
                            else:
                                continue

                            real_players=[]
                            spocota=[]

                            kolvo=len(y['eventPlayers'])

                            for full_name in y['eventPlayers']:
                                
                                if y["eventTypeCode"]=='LD':
                                    name1=full_name['players'][0]['fullName']
                                    id_1_1=str(full_name['players'][0]['id'])
                                    
                                    name2=full_name['players'][1]['fullName']
                                    id_1_2=str(full_name['players'][1]['id'])

                                    spoc1L=full_name['players'][0]['lastName']
                                    spoc2L=full_name['players'][1]['lastName']

                                    name=name1+' / '+name2

                                    ids=[id_1_1,id_1_2]

                                    if spoc1L==None or spoc2L==None:
                                        
                                        spoc1L=(' ').join(name1.split()[1:])
                                        spoc1F=name1.split()[0][0]
                                        spoc2L=(' ').join(name2.split()[1:])
                                        spoc2F=name2.split()[0][0]
                                    else:
                                        spoc1L=full_name['players'][0]['lastName']
                                        try:
                                            spoc1F=full_name['players'][0]['firstName'][0]
                                        except:
                                            print('\n',full_name['players'][0])
                                            continue

                                        spoc2L=full_name['players'][1]['lastName']
                                        spoc2F=full_name['players'][1]['firstName'][0]

                                    spocota_format=f"{spoc1L}, {spoc1F}/{spoc2L}, {spoc2F}"    
                                    
                                
                                else:
                                    name=full_name['players'][0]['fullName']
                                    ids=[str(full_name['players'][0]['id'])]

                                    
                                    spoc1L=full_name['players'][0]['lastName']
                                    if spoc1L==None:
                                        spoc1L=(' ').join(name.split()[1:])
                                        spoc1F=name.split()[0][0]
                                    else:
                                        try:
                                            spoc1F=full_name['players'][0]['firstName'][0]
                                        except:
                                            print('\n',full_name['players'][0])
                                            continue

                                    spocota_format=f"{spoc1L}, {spoc1F}"
                                
                          
                                real_players.append(name)
                                ids_list.append(ids)
                                spocota.append(spocota_format)
                       
                            if sits[x[0]][i][1]!=len(y['eventPlayers']) and kolvo>0:
                                
                                event_type=slovar.get(y["eventTypeCode"])
                               
                                
                                if n==0:
                                    
                                    msg=f'{time_}  {x[0]} {event_type} draw    \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/draws\n\n'
                                    #frame.add_timestamp(n,msg,0,x[0],first_change)
                                    messages.append(msg)
                                    
                                    
                                elif sits[x[0]][i][1]==0:
                                    msg=f'{time_}  NEW draw in {x[0]} {event_type} ★    \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/draws\n\n'

                                    print(msg)
                                    messages.append(msg)
                                    #frame.add_timestamp(n,msg,1,x[0],first_change)
                                    info()



                                else:
                                    msg=f'{time_}  change in {x[0]} {event_type} ★   \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/draws\n\n'
                                    #frame.add_timestamp(n,msg,1,x[0],first_change)

                                    print(msg)
                                    messages.append(msg)

                                change_draw=1

                                
                                

                   
                                first_change=1
                                

                            if  n!=0 or (n==0 and flag==1): #
                                if sits[x[0]][i][2]['players']!=real_players and kolvo>0:

                                    


                                    event_type=slovar.get(y["eventTypeCode"])
                                    
                                    if change_draw==1:
                                        msg=f'       Players added to the draw in {x[0]} {event_type}:    \n\n'
                                        
                                    else:
                                        msg=f'{time_}  change in {x[0]} {event_type} ★   \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/draws\n\n       Players added to the draw in {x[0]} {event_type}:    \n\n'

                                    print(msg)
                                    messages.append(msg)
                                    
                                    #frame.add_timestamp(n,msg,1) #?

                                    p_idx=1

                                    for idx,p in enumerate(real_players):

                                        if p not in sits[x[0]][i][2]["players"]:
                                            is_found=0

                                            if x[0] not in repl:
                                                repl.update({x[0]:[]})

                                            for sub in repl[x[0]]:
                                                if sub == ids_list[idx]:
                                                    is_found=1 

                                            if p_idx<10:
                                                msg1_1=f'       {p_idx}. {p} \n'
                                                msg1_2=f'          {spocota[idx]}\n\n'
                                            else:
                                                msg1_1=f'       {p_idx}. {p} \n'
                                                msg1_2=f'           {spocota[idx]}\n\n'

                                            #frame.add_timestamp(n,msg1_1,0,dl=1)
                                            #frame.add_timestamp(n,msg1_2,0)

                                            print(msg1_1)
                                            messages.append(msg1_1)                                                
                                            
                                            print(msg1_2)
                                            messages.append(msg1_2)

                                            repl[x[0]].append(ids_list[idx])

                                            p_idx+=1

                                    
                                    
                                    p_idx=1
                                    if_found=1

                                    for idx,p in enumerate(sits[x[0]][i][2]["players"]):

                                        if p not in real_players:

                                            if p_idx<10:
                                                msg=f'       {p_idx}. {p} \n\n'
                                            else:
                                                msg=f'       {p_idx}. {p} \n\n'

                                            if if_found==1:
                                                msg2=f'       Players removed from the draw in {x[0]} {event_type}:    \n\n'

                                                #frame.add_timestamp(n,msg2,1)

                                                print(msg2)
                                                messages.append(msg2)                                                

                                                if_found=0

                                            #frame.add_timestamp(n,msg,0)

                                            print(msg)
                                            messages.append(msg)                                                

                                            p_idx+=1
                                        
                              
                            dc_players={'players':real_players}
                            sits[x[0]][i]=[i,kolvo,dc_players]

                            change_draw=0

                            

                if n==0 and flag==0:
                    url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={today_oop}&to={today_oop}'
                    req=connect(url)

                    if 'matches' in req and len(req['matches'])>0:
                        msg=f"{time_}  Today's OOP of {x[0]}  \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n"

                        messages.append(msg)
                        
                        #frame.add_timestamp(n,msg,0,x[0],first_change)
                        
                        first_change=1

                    url=f'http://wtafiles.wtatennis.com/pdf/draws/{year}/{x[1]}/OP.pdf'
                    req=requests.get(url)

                    if req.status_code!=404 and req.status_code!=kuits[x[0]][0][0]:

                        msg=f'{time_}  OOP of {x[0]} (pdf)   \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,0)
                        print(msg)
                        messages.append(msg)

                        first_change=1


                #url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={from_to_oop}&to={from_to_oop}'
                url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={today_oop}&to={from_to_oop}'


                req=connect(url)

                if n==0:
                    fill()

                try:
                    if len(req['matches'])>0 and n==0 and flag==0:
                        print('tut')
                        last_date=(req['matches'][-1]['MatchTimeStamp']).split('T')[0]
                        print(last_date)

                                
                        if dummy()==1 and last_date==from_to_oop:    
                            
                            msg=f'{time_}  Tomorrow\'s OOP of {x[0]}  \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n'
                            
                            #frame.add_timestamp(n,msg,0)
                            #frame.add_timestamp(n,msg,0,x[0],first_change)

                            #sits[x[0]][-1]=last_date

                            messages.append(msg)

                            print(last_date)
                            first_change=1

                            if x[1] in temp_container:
                                del temp_container[x[1]]
                        sits[x[0]][-1]=last_date
            
##                    if n==0:
##                        url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={today_oop}&to={from_to_oop}'
##
##                        req=connect(url)
##
##                        if len(req['matches'])>0 and n==0 and flag==0:
##                            print('tut')
##                            last_date=(req['matches'][-1]['MatchTimeStamp']).split('T')[0]
##                            print(last_date)
##
##                                    
##                            if dummy()==1:    
##
##                                sits[x[0]][-1]=last_date
##                                print(last_date)
##                                first_change=1
##
##                                if x[1] in temp_container:
##                                    del temp_container[x[1]] 

                    elif len(req['matches'])>0 and flag==1:
                        last_date=(req['matches'][-1]['MatchTimeStamp']).split('T')[0]
                        print(last_date)
                        if sits[x[0]][-1]!=last_date:
                            if dummy()==1:  
                                
                                msg=f'{time_}  OOP in {x[0]} appeared ★\n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n'


                                print(msg)
                                messages.append(msg)                                

                                #frame.add_timestamp(n,msg,1)
                                sits[x[0]][-1]=last_date
                                first_change=1

                                if x[1] in temp_container:
                                    del temp_container[x[1]]                              

                        
                    else:
                        pass
                except:
                      
                    pass

#----------------------------------------------
                url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={today_oop}&to={to_oop_repl}'
                oop_containter.update({x[0]:[]})
                req=connect(url)

                if 'matches' in req:
                    for last_n in req['matches']:
                        
                        #print(last_n)
                        try:
                            a=last_n['PlayerNameLastA']
                        except:
                            break
                        
                        a_firstName=last_n['PlayerNameFirstA']
                        a_id=last_n['PlayerIDA']

                        a2=last_n.get('PlayerNameLastA2','None')
                        a2_firstName=last_n.get('PlayerNameFirstA2')
                        a2_id=last_n.get('PlayerIDA2','None')

                        b=last_n['PlayerNameLastB']
                        b_firstName=last_n['PlayerNameFirstB']
                        b_id=last_n['PlayerIDB']

                        b2=last_n.get('PlayerNameLastB2','None')
                        b2_firstName=last_n.get('PlayerNameFirstB2','None')
                        b2_id=last_n.get('PlayerIDB2','None')

                        wolkover_test=last_n.get('ScoreString','None')        
                        wolkover_test2=last_n.get('ResultString','None')

                        matchID=last_n['MatchID']
                        eventID=last_n['EventID']
                        #stamp=last_n['MatchTimeStamp'][:10]

                        if 'W/O' in wolkover_test or 'W/O' in wolkover_test2:
                            if last_n['MatchID'] not in walkovers_id:
                                print(f' walkerover1 is {wolkover_test} and walkerover2 is {wolkover_test2}')
                                if a2:
                                    msg=f'{time_}  Walkover in {x[0]} \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n       {a}/{a2} vs {b}/{b2}\n\n'
                                    #msg=f'{time_}  Walkover in {a}/{a2} vs {b}/{b2} in {x[0]} \n\n'
                                else:
                                    msg=f'{time_}  Walkover in {x[0]} \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n       {a} vs {b}\n\n'
                                    #msg=f'{time_}  Walkover in {a} vs {b} match in {x[0]} \n\n'                            

                                if  n==0 and flag==0:
                                    pass#frame.add_timestamp(n,msg,1,x[0],first_change)
                                else:
                                    #frame.add_timestamp(n,msg,1,x[0],first_change)
                                    pass
                                walkovers_id.append(last_n['MatchID'])

                        if a2=='':
                            a2='None'

                        if b2=='':
                            b2='None'

                        if a2=='None':
                            teamA=[a_id, a_firstName, a, matchID]
                            teamB=[b_id, b_firstName, b, matchID]
                        else:
                            teamA=[a_id,a2_id,a_firstName,a,a2_firstName,a2,matchID]
                            teamB=[b_id,b2_id,b_firstName,b,b2_firstName,b2,matchID]

                        oop_containter[x[0]].append([teamA,teamB])


                if n!=0:                    
                    for names in oop_containter[x[0]]:
                        if names not in all_matches_container[x[0]]: #names = [teamA,teamB]
                            
                            #print(f'\n repl is {repl[x[0]]}')
                            teamA = names[0]
                            teamB = names[1]

                            for index,prev_names in enumerate(all_matches_container[x[0]]):

                                if teamA in prev_names:
                                    # means teamB - replacement

                                    if len(teamB)>4:
                                        this_id=teamA[6]
                                        that_id=all_matches_container[x[0]][index][prev_names.index(teamA)][6]

                                        added_team = [names[1][0],names[1][1]]
                               
                                    else:
                                        this_id=teamA[3]
                                        that_id=all_matches_container[x[0]][index][prev_names.index(teamA)][3]

                                        added_team = [names[1][0]]
                           
                                    if this_id==that_id:
                                        is_found=0

                                        if  x[0] not in repl:
                                            repl.update({x[0]:[]})

                                        for sub in repl[x[0]]:
                                            if sub == added_team:
                                                is_found=1

                                        if is_found==0 or is_found==1: # hcanged
##                                            if is_found==0: ##
##                                                frame.add_timestamp(n,'real\n',1)
##                                            else: ##
##                                                frame.add_timestamp(n,'fake\n',1)

                                            msg=f'{time_}  change in {x[0]} ★   \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n'          
                                            msg=msg+f'       Players added to OOP in {x[0]}:    \n\n'
                                            #frame.add_timestamp(n,msg,1)
                                            
                                            print(msg)
                                            messages.append(msg)

                                            if len(teamB)>4:
                                                msg=f'       1. {teamB[2]} {teamB[3]} / {teamB[4]} {teamB[5]} \n'
                                                msg2=f'          {teamB[3]}, {teamB[2][0]} / {teamB[5]}, {teamB[4][0]}\n\n'
                                            else:
                                                msg=f'       1. {teamB[1]} {teamB[2]} \n'
                                                msg2=f'          {teamB[2]}, {teamB[1][0]}\n\n'

                                            #frame.add_timestamp(n,msg,0,dl=1)
                                            #frame.add_timestamp(n,msg2,0)

                                            print(msg)
                                            messages.append(msg)

                                            print(msg2)
                                            messages.append(msg2)
                                            

                                            msg=f'       Players removed from OOP in {x[0]} {event_type}:    \n\n'
                                            #frame.add_timestamp(n,msg,0)

                                            print(msg)
                                            messages.append(msg)

                                            if len(teamB)>4:                                                
                                                msg=f'       1. {all_matches_container[x[0]][index][1][2]} {all_matches_container[x[0]][index][1][3]} / {all_matches_container[x[0]][index][1][4]} {all_matches_container[x[0]][index][1][5]} \n'
                                                msg2=f'          {all_matches_container[x[0]][index][1][3]}, {all_matches_container[x[0]][index][1][2][0]} / {all_matches_container[x[0]][index][1][5]}, {all_matches_container[x[0]][index][1][4][0]}\n\n'
                                            else:
                                                msg=f'       1. {all_matches_container[x[0]][index][1][1]} {all_matches_container[x[0]][index][1][2]} \n'
                                                msg2=f'          {all_matches_container[x[0]][index][1][2]}, {all_matches_container[x[0]][index][1][1][0]}\n\n'

                                            #frame.add_timestamp(n,msg,0,dl=1)
                                            #frame.add_timestamp(n,msg2,0)
                                            print(msg)
                                            messages.append(msg)

                                            
                                            print(msg2)
                                            messages.append(msg2)

                                            repl[x[0]].append(added_team)

                                elif teamB in prev_names:
                                    # means teamA - replacement

                                    if len(teamA)>4:
                                        this_id=teamB[6]
                                        that_id=all_matches_container[x[0]][index][prev_names.index(teamB)][6]

                                        added_team = [names[0][0],names[0][1]]
                                    else:
                                        this_id=teamB[3]
                                        that_id=all_matches_container[x[0]][index][prev_names.index(teamB)][3]

                                        added_team = [names[0][0]]
                                    #print(f'\n \n this_id is {this_id} and that_id is {that_id}\n\n')
                                    if this_id==that_id:
                                        is_found=0

                                        if  x[0] not in repl:
                                            repl.update({x[0]:[]})

                                        for sub in repl[x[0]]:
                                            if sub == added_team:
                                                is_found=1

                                        if is_found==0 or is_found==1: # changed

##                                            if is_found==0:
##                                                frame.add_timestamp(n,'real\n',1)
##                                            else:
##                                                frame.add_timestamp(n,'fake\n',1)

                                            msg=f'{time_}  change in {x[0]} ★   \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n'          
                                            msg=msg+f'       Players added to OOP in {x[0]}:    \n\n'
                                            #msg=f'       Players added to OOP in {x[0]} {event_type}:    \n\n'
                                            #frame.add_timestamp(n,msg,1)

                                            print(msg)
                                            messages.append(msg)
                                            

                                            if len(teamA)>4:
                                                msg=f'       1. {teamA[2]} {teamA[3]} / {teamA[4]} {teamA[5]} \n'
                                                msg2=f'          {teamA[3]}, {teamA[2][0]} / {teamA[5]}, {teamA[4][0]}\n\n'
                                            else:
                                                msg=f'       1. {teamA[1]} {teamA[2]} \n'
                                                msg2=f'          {teamA[2]}, {teamA[1][0]}\n\n'

                                            #frame.add_timestamp(n,msg,0,dl=1)
                                            #frame.add_timestamp(n,msg2,0)

                                            msg=f'       Players removed from OOP in {x[0]} {event_type}:    \n\n'
                                            frame.add_timestamp(n,msg,0)

                                            if len(teamA)>4:                                                
                                                msg=f'       1. {all_matches_container[x[0]][index][0][2]} {all_matches_container[x[0]][index][0][3]} / {all_matches_container[x[0]][index][0][4]} {all_matches_container[x[0]][index][0][5]} \n'
                                                msg2=f'          {all_matches_container[x[0]][index][0][3]}, {all_matches_container[x[0]][index][0][2][0]} / {all_matches_container[x[0]][index][0][5]}, {all_matches_container[x[0]][index][0][4][0]}\n\n'
                                            else:
                                                msg=f'       1. {all_matches_container[x[0]][index][0][1]} {all_matches_container[x[0]][index][0][2]} \n'
                                                msg2=f'          {all_matches_container[x[0]][index][0][2]}, {all_matches_container[x[0]][index][0][1][0]}\n\n'

                                            #frame.add_timestamp(n,msg,0,dl=1)
                                            #frame.add_timestamp(n,msg2,0)

                                            print(msg)
                                            messages.append(msg)

                                            print(msg2)
                                            messages.append(msg2)                                            

                                            repl[x[0]].append(added_team)

                                else:
                                    pass

                            all_matches_container[x[0]].append(names)  # add new name if it wasnt before

                else: # n==0
                   all_matches_container[x[0]]=all_matches_container[x[0]] + oop_containter[x[0]]
#----------------------------------------------------------------------------------------
                
                if x[1] in temp_container:
                    
                    
                    
                    
                    url=f'https://api.wtatennis.com/tennis/tournaments/{x[1]}/{year}/matches/?from={today_oop}&to={today_oop}'

                    req=connect(url)
                    if 'matches' in req and len(req['matches'])>0:
                        if flag!=0:
                            msg=f'{time_}  OOP in {x[0]} appeared ★   \n       https://www.wtatennis.com/tournament/{x[1]}/{x[0]}/{year}/order-of-play\n\n'
                            
                            #frame.add_timestamp(n,msg,1)
                            print(msg)
                            messages.append(msg)
                        
                        del temp_container[x[1]]
                        
                    
                    


                
                url=f'http://wtafiles.wtatennis.com/pdf/draws/{year}/{x[1]}/MDS.pdf'
                req=s.get(url)
                try:
                    modi=req.headers['Last-Modified']
                except:
                    modi=0
                if req.status_code!=404 and (req.status_code!=kuits[x[0]][1][0] or modi!=kuits[x[0]][1][1]) and int(req.headers['Content-Length'])>10000:
                    if  n==0 and flag==0:
                        
                        msg=f'{time_}  MDS of {x[0]} (pdf)    \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,0,x[0],first_change)

                    elif n>1 and flag==1 and req.status_code!=kuits[x[0]][1][0]:

                        eventTypeCode='MDS'
                        msg=f'{time_}  NEW MDS of {x[0]} detected (pdf) ★    \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,1,x[0],first_change)
                        info()

                        print(msg)
                        messages.append(msg)

                    else:
                        pass

                    kuits[x[0]][1][0]=req.status_code
                    
                    



                    kuits[x[0]][1][1]=modi

                    first_change=1
                    

                if kuits[x[0]][2][1]!='done':
                    url=f'http://wtafiles.wtatennis.com/pdf/draws/{year}/{x[1]}/MDD.pdf'
                    req=s.get(url)
                    try:
                        modi=req.headers['Last-Modified']
                    except:
                        modi=0
                    if req.status_code!=404 and req.status_code!=kuits[x[0]][2][0] and int(req.headers['Content-Length'])>10000:
                        if  n==0 and flag==0:
                            msg=f'{time_}  MDD of {x[0]} (pdf)     \n       {url}\n\n'
                            #frame.add_timestamp(n,msg,0,x[0],first_change)
     
                            
                        elif n>1 and flag==1 and req.status_code!=kuits[x[0]][2][0]:

                            eventTypeCode='MDD'
                            msg=f'{time_}  NEW MDD of {x[0]} detected (pdf) ★   \n       {url}\n\n'
                            #frame.add_timestamp(n,msg,1,x[0],first_change)
                            info()

                            print(msg)
                            messages.append(msg)

                        else:
                            pass
                        first_change=1

                        kuits[x[0]][2][0]=req.status_code
                        kuits[x[0]][2][1]='done'
                    



                    #kuits[x[0]][2][1]=modi
                    
                kuits[x[0]][3]
                url=f'http://wtafiles.wtatennis.com/pdf/draws/{year}/{x[1]}/QS.pdf'
                req=s.get(url)
                try:
                    modi=req.headers['Last-Modified']
                except:
                    modi=0
                if req.status_code!=404 and (req.status_code!=kuits[x[0]][3][0] or modi!=kuits[x[0]][3][1]) and int(req.headers['Content-Length'])>10000:
                    if  n==0 and flag==0:
                        msg=f'{time_}  QS of {x[0]} (pdf)    \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,0,x[0],first_change)

                    elif n>1 and flag==1 and req.status_code!=kuits[x[0]][3][0]:

                        eventTypeCode='QS'
                        msg=f'{time_}  NEW QS of {x[0]} detected (pdf) ★    \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,1,x[0],first_change)
                        print(msg)
                        messages.append(msg)


                        info()
                        
                    else:
                        pass
                    

                    kuits[x[0]][3][0]=req.status_code
                    
                    



                    kuits[x[0]][3][1]=modi

                    first_change=1
                kuits[x[0]][4]
                url=f'http://wtafiles.wtatennis.com/pdf/draws/{year}/{x[1]}/QD.pdf'
                req=s.get(url)
                try:
                    modi=req.headers['Last-Modified']
                except:
                    modi=0
                
                if req.status_code!=404 and (req.status_code!=kuits[x[0]][4][0] or modi!=kuits[x[0]][4][1]) and int(req.headers['Content-Length'])>10000:
                    if  n==0 and flag==0:
                        msg=f'{time_}  QD of {x[0]} (pdf)     \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,0,x[0],first_change)

                    elif n>1 and flag==1 and req.status_code!=kuits[x[0]][4][0]:
                        eventTypeCode='QD'
                        msg=f'{time_}  NEW QD of {x[0]} detected (pdf) ★     \n       {url}\n\n'
                        #frame.add_timestamp(n,msg,1,x[0],first_change)
                        print(msg)
                        messages.append(msg)

                        
                        info()
                    
                    else:
                        pass                
                    kuits[x[0]][4][0]=req.status_code
                    

                    kuits[x[0]][4][1]=modi

                if n==0 and flag==0:
                    first_change=0
            
            
            
            
##            if n==0:
##                
##                
##
##                if first_change==0:
##                    
##                    #frame.add_timestamp(0,'',0,'Waiting for updates...',first_change)
##                    first_change=1

            n+=1
            flag=1

            print(messages)

            html_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Draws Info</title>
                <meta charset="UTF-8">
                <style>
                    body { font-family: Arial, sans-serif; padding: 20px; }
                    li { margin-bottom: 1em; white-space: pre-wrap; }
                </style>
            </head>
            <body>
                <h1>Draws and Links</h1>
                <ul>
            """

            for item in messages:
                html_content += f"        <li>{item.strip()}</li>\n"

            html_content += """
                </ul>
            </body>
            </html>
            """

            with open("index.html", "w", encoding="utf-8") as f:
                f.write(html_content)

            # Save to file
            #messages_dict = {"messages":messages}
            


##            with open("output.txt", "w", encoding="utf-8") as f:
##                for message in messages:
##                    f.write(message + "\n")
            
            # Wrap into one structure
            combined = {
                "kuits": kuits,
                "messages": messages,
                "sits": sits
            }

            # Save to a file
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(combined, f, indent=2)
            

            break

            #time.sleep(300) 



        except:
            print("error")
            exc_type, exc_value, exc_traceback = sys.exc_info()
            var = traceback.format_exc()
            print(datetime.datetime.now().strftime("%H:%M:%S"))
            print('skip1 error')
            print("Exception type : %s " % exc_type.__name__)
            print("Exception message : %s" %exc_value)
            print(f' Var is {var}')
            print(f'\n sits is {sits}')

            break

            #time.sleep(300) 
            


var=0




s=requests.Session()

zoomed=0

core()



