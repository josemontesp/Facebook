import urllib.request
import json
from datetime import datetime

######facebook target user data#####
token = 'CAACEdEose0cBAFmXZAv8Oh0OLYDbwCCe3UubQSZAktIQlZC8dbt3ZCI430WjOWmjZAZCnkeySUMPVagyF0mDAQHZAUuKtWOz6r9GsFK9GtIIca5ZAgBomG19gP4MHTdus3DpwKyQbVOZBZAr4ws36nAopCdIpZAemYnzgZCcFPdGHAHM7M0tgJ0Csq3cYQtZCPKiC2UQZD'
_id = '815626504'
####################################

def load_facebook_page(facebook_id, token):
    url = 'https://graph.facebook.com/' + facebook_id + '?fields=friends.fields(id,name,birthday,gender,hometown,languages,relationship_status),name,last_name,picture.width(300).height(300)&method=GET&format=json&suppress_http_code=1&access_token=' + token
    #print (url)
    return (urllib.request.urlopen(url)).read().decode("utf-8")


data =  (load_facebook_page(_id,token))
j = json.loads(data)
#print (j['friends']['data'][0])


age = []
gender = {'female':0 , 'male':0}
hometown = {}
languages = {}
relationship_status = {'complicated':0, 'divorced':0, 'engaged':0, 'in_a_relationship':0, 'married':0, 'open_relationship':0, 'separated':0, 'single':0, 'widowed':0}

# gathering data
for i in j['friends']['data']:
    if ('gender' in i):
        d = i['gender']
        gender[d] += 1
    if ('birthday' in i):
        c = i['birthday']
        if c.count('/') == 2:
            c = 2014 - int(c[-4:])
            if c < 100:
                age.append(c)

    if ('hometown' in i):
        e = i['hometown']['name']
        if e in hometown:
            hometown[e] += 1
        else:
            hometown[e] = 1
    if ('languages' in i):
        g = i['languages']
        for k in g:
            a = k['name']
            if a in languages:
                languages[a] += 1
            else:
                languages[a] = 1
    if ('relationship_status' in i):
        f = i['relationship_status'].replace(' ', '_').lower()
        if f == "it's_complicated":
            f = 'complicated'
        if f != 'in_a_civil_union':
            relationship_status[f] += 1

        
print ('Successfully processed ' + str (len(j['friends']['data'])) + ' friends.')


ageaverage = 0
for i in age:
    ageaverage += i
ageaverage /= len(age)
ageaverage = (ageaverage.__round__(2))

#creating file

file = {}
file['friends'] = {}
file['friends']['age'] = {}
file['friends']['age']['average'] =  ageaverage
file['friends']['age']['oldest'] =  max(age)
file['friends']['age']['youngest'] =  min(age)
file['friends']['count'] = len(j['friends']['data'])
file['friends']['gender'] = {}
file['friends']['gender']['male'] = gender['male']
file['friends']['gender']['female'] = gender['female']
file['friends']['hometown'] = []
for key in hometown:
    file['friends']['hometown'].append({'town': key, 'count': hometown[key]})
file['friends']['languages'] = []
for key in languages:
    file['friends']['languages'].append({'language': key, 'count': languages[key]})
file['friends']['relationship_status'] = relationship_status
file['name'] = j['name']
file['picture'] = {'height': j['picture']['data']['height'], 'width':j['picture']['data']['width'], 'url':j['picture']['data']['url']}


#Exporting the created file
if j['last_name'].find(' ') == -1:
    name = file['name'][0] + j['last_name']
else:
    name = file['name'][0] + j['last_name'][:j['last_name'].find(' ')]
f = open(name + '.json', 'w')
f.write(json.dumps(file, indent=4))
f.close()



        
        
        
        
