
from datetime import datetime
from typing import Optional
from fastapi import FastAPI,HTTPException
import pymongo
from bson.objectid import ObjectId


client = pymongo.MongoClient("mongodb+srv://Admin:AdminHackBot@hackbot.g1uz8.mongodb.net/HackBot?retryWrites=true&w=majority")
db = client["HackBot"]

# from .db import read, read_one, create, update, delete 

app = FastAPI()


@app.get("/")
def home():
    return {"Let's": "Go"}
@app.get("/devpost")
def getDevpostHackathons(q:Optional[str] = None, page:int = 0, per_page: int = 10):
    result = {'meta':{}, 'data':[]}
    result['meta']['query'] = q
    result['meta']['page'] = page
    result['meta']['per_page'] = per_page
    query = {'website':'DEVPOST'}
    if q:
        query['name'] = {'$regex': q}
    fetch_query = db['Hackathons'].find(query)
    fetch_count = db['Hackathons'].count_documents(query)
    if not fetch_count:
        raise HTTPException(status_code=404, detail = 'No Hackathons Found' )
    
    result['meta']['total'] = fetch_count
    result['meta']['total_pages'] = fetch_count // per_page+1
    result['data'] = list(fetch_query.skip(page * per_page).limit(per_page))
    for i in result['data']:
        i['_id'] = str(i['_id'])
    return result
@app.get("/mlh")
def getMLHHackathons(q:Optional[str] = None, page:int = 0, per_page: int = 10):
    result = {'meta':{}, 'data':[]}
    result['meta']['query'] = q
    result['meta']['page'] = page
    result['meta']['per_page'] = per_page
    query = {'website':'MLH'}
    if q:
        query['name'] = {'$regex': q}
    fetch_query = db['Hackathons'].find(query)
    fetch_count = db['Hackathons'].count_documents(query)
    if not fetch_count:
        raise HTTPException(status_code=404, detail = 'No Hackathons Found' )
    
    result['meta']['total'] = fetch_count
    result['meta']['total_pages'] = fetch_count // per_page+1
    result['data'] = list(fetch_query.skip(page * per_page).limit(per_page))
    for i in result['data']:
        i['_id'] = str(i['_id'])
    return result
@app.get("/hackathon/{id}")
def getHackathon(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail = 'Invalid ObjectId')
    result = db['Hackathons'].find_one({'_id': ObjectId(id)})
    if not result:
        raise HTTPException(status_code=404, detail = 'Hackathon Not Found' )
    result['_id'] = str(result['_id'])
    return result
@app.get('/devfolio')
def getDevfolioHackathons(q:Optional[str] = None, page:int = 0, per_page: int = 10):
    result = {'meta':{}, 'data':[]}
    result['meta']['query'] = q
    result['meta']['page'] = page
    result['meta']['per_page'] = per_page
    query = {'website':'DEVFOLIO'}
    if q:
        query['name'] = {'$regex': q}
    fetch_query = db['Hackathons'].find(query)
    fetch_count = fetch_query.count()
    if not fetch_count:
        raise HTTPException(status_code=404, detail = 'No Hackathons Found' )
    
    result['meta']['total'] = fetch_count
    result['meta']['total_pages'] = fetch_count // per_page+1
    result['data'] = list(fetch_query.skip(page * per_page).limit(per_page))
    for i in result['data']:
        i['_id'] = str(i['_id'])
    return result
@app.get('/new')
def getNewHackathons(q:Optional[str] = None, page:int = 0, per_page: int = 10,ongoing = False):
    result = {'meta':{}, 'data':[]}
    result['meta']['query'] = q
    result['meta']['page'] = page
    result['meta']['per_page'] = per_page
    query = {'datetimeStart':{'$gte':datetime.now()}}
    if ongoing:
        query['datetimeStart'] = {'$lte':datetime.now()}
        query['datetimeEnd'] = {'$gte':datetime.now()}
    if q:
        query['name'] = {'$regex': q}
    fetch_query = db['Hackathons'].find(query)
    fetch_count = db['Hackathons'].count_documents(query)
    if not fetch_count:
        raise HTTPException(status_code=404, detail = 'No Hackathons Found' )
    result['meta']['total'] = fetch_count
    result['meta']['total_pages'] = fetch_count // per_page+1
    result['data'] = list(fetch_query.sort("datetimeStart").skip(page * per_page).limit(per_page))
    for i in result['data']:
        i['_id'] = str(i['_id'])
    return result
@app.get('/all')
def getAllHackathons(q:Optional[str] = None, page:int = 0, per_page: int = 10):
    result = {'meta':{}, 'data':[]}
    result['meta']['query'] = q
    result['meta']['page'] = page
    result['meta']['per_page'] = per_page
    query = {}
    if q:
        query['name'] = {'$regex': q}
    fetch_query = db['Hackathons'].find(query)
    fetch_count = db['Hackathons'].count_documents(query)
    if not fetch_count:
        raise HTTPException(status_code=404, detail = 'No Hackathons Found' )
    result['meta']['total'] = fetch_count
    result['meta']['total_pages'] = fetch_count // per_page+1
    result['data'] = list(fetch_query.skip(page * per_page).limit(per_page))
    for i in result['data']:
        i['_id'] = str(i['_id'])
    return result
