import datetime
import pymongo

client = pymongo.MongoClient("mongodb+srv://Admin:AdminHackBot@hackbot.g1uz8.mongodb.net/HackBot?retryWrites=true&w=majority")
db = client["HackBot"]


fetch_hackathons = db['Hackathons'].find()
for hackathon in fetch_hackathons:
    fetchStart = hackathon['start']
    fetchEnd = hackathon['end']
    try:
        date_time_start = datetime.datetime.strptime(fetchStart, '%B %d, %Y')
        date_time_end = datetime.datetime.strptime(fetchEnd, '%B %d, %Y')
        db['Hackathons'].update_one({'_id':hackathon['_id']},{'$set':{'dateTimeStart':date_time_start,'dateTimeEnd':date_time_end}})
    except:
        pass

