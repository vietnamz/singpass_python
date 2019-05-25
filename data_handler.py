from google.cloud import datastore
from datetime import datetime
from pprint import pprint as pp
from security import security
import uuid
import sys

test =  {
            "name":"TAN XIAO HUI",
            "sex": "F",
            "race": "CN",
            "nationality": "SG",
            "dob":"1970-05-17",
            "email": "myinfotesting@gmail.com",
            "mobileno": "+97399245",
            "regadd": "SG, 128 street BEDOK NORTH AVENUE 4 block 102 postal 460102 floor 09 building PEARL GARDEN", 
            "hdbtype":"113",
            "marital": "1",
            "edulevel": "3",
            "assessableincome": "1456789.00",
            "uinfin":"S9812381D"
        }
def validateUserLogin(userName, password):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    query = datastore_client.query(kind='users', namespace='MyInfoApp')
    query.add_filter('password', '=', password)
    query.add_filter('userName', '=', userName)
    users = list(query.fetch())
    pp(users)
    for user in users:
        if user['userName'] == userName and user['password'] == password:
            return True
    return False
def generateSessionEntity(requester):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # Fetch the current date / time.
    current_datetime = datetime.now()

    # The kind for the new entity.
    kind = 'Sessions'

    # The name/ID for the new entity.
    session = uuid.uuid4().hex
    pp(session)

    # Create the Cloud Datastore key for the new entity.
    key = datastore_client.key(kind, str(session), namespace='MyInfoApp')

    # Construct the new entity using the key. Set dictionary values for entity
    # keys blob_name, requester, requetee, timestamp, nonce.
    entity = datastore.Entity(key)
    entity['requester'] = requester
    entity['requestee'] = ""
    entity['timestamp'] = current_datetime
    entity['data'] = dict()
    entity['nonce'] = security.generate_nonce(15)

    # Save the new entity to Datastore.
    datastore_client.put(entity)
    return session
def updateSessionEntity(session, requester, requestee, data):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    key = datastore_client.key(kind, str(session), namespace="MyInfoApp")
    entity = datastore_client.get(key)
    if entity is None:
        return None
    if requester is not None:
        entity['requester'] = requester
    if requestee is not None:
        entity['requestee'] = requestee
    if data is not None:
        entity['data'] = data
    datastore_client.put(entity)
    __delete_previous_session__(session, entity['requester'], entity['requestee'])
    return session

def getSessionEntity(session):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    key = datastore_client.key(kind, str(session), namespace="MyInfoApp")
    entity = datastore_client.get(key)
    if entity is None:
        return None
    return entity

def __delete_previous_session__(current_session, requester, requestee):
        # Create a Cloud Datastore client.
    datastore_client = datastore.Client()

    query = datastore_client.query(kind='Sessions', namespace='MyInfoApp')
    query.add_filter('requester', '=', requester)
    query.add_filter('requestee', '=', requestee)
    sessions = list(query.fetch())
    kind = 'Sessions'
    if sessions is not None:
        for session in sessions:
            name = session.key.name
            pp(name)
            if name != current_session:
                key = datastore_client.key(kind, str(name), namespace="MyInfoApp")
                datastore_client.delete(key)
    return True

def query_data(requester):
    # Create a Cloud Datastore client.
    datastore_client = datastore.Client()
    # The kind for the new entity.
    kind = 'Sessions'
    query = datastore_client.query(kind=kind, namespace='MyInfoApp')
    query.add_filter('requester', '=', requester)
    requesters = list(query.fetch())
    if requesters is None:
        return None
    data = []
    for request in requesters:
        if bool(request['data']) == True and request['requestee'] != '':
            data.append(request['data'])
    return data

if __name__ == "__main__":
    sess = generateSessionEntity("abc")
    print(sess)
    entity = getSessionEntity(sess)
    if entity is None:
        sys.exit()
    if entity['requester'] is None:
        pp("requester is none")
    if entity['requester'] == "":
        pp("requester is empty")
    if entity['requestee'] is None:
        pp("requestee is none")
    if entity['requestee'] == "":
        pp("requestee is empty")
    if not entity['data']:
        pp("data is empty")
    sess = updateSessionEntity(sess, "abc", "efg", test)
    print(sess)
    entity = getSessionEntity(sess)
    if entity['requester'] is None:
        pp("requester 2 is none")
    if entity['requester'] != "":
        pp("requester 2 is not empty")
    if entity['requestee'] is None:
        pp("requestee 2 is none")
    if entity['requestee'] != "":
        pp("requestee 2 is not empty")
    if entity['data']:
        pp("data 2 is empty")
    pp(entity)