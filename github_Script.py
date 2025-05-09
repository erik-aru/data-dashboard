import requests
import datetime
import time

n = 0
now=datetime.datetime.now()


if n!=0 and now-time_of_last_check>datetime.timedelta(minutes=15):

    text='No updates for 15 min. Is something wrong?\n'

    time_of_last_check=now

day=now.day


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

    print(sits)



msg=f'-Checking for updates in {header}\n-Last checked: {time_}\n\n'

time_of_last_check = now
