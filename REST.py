from flask_restful import Resource
from flask_restful import reqparse
from flask import request
from pymongo import MongoClient
from flask_httpauth import HTTPBasicAuth
from bson.json_util import dumps

#USERS username and password
USERS_DATA = {
    "agent" : "123",
    "client": "321"
}
dbName = 'bank_db'

# MongoDB is running on virual machine
# Connect to database
client = MongoClient('192.168.100.210', 27017)
# Select the database
db = client[dbName]

parser = reqparse.RequestParser()

auth = HTTPBasicAuth()

@auth.verify_password
def verify(username, password):
    #make sure that client cannot access to update his account balance
    if 'agent' in request.url_rule.rule and username == 'client':
        return False

    if not (username and password):
        return False
    return USERS_DATA.get(username) == password

# Users can get there account type
class AccoutType(Resource):
    @auth.login_required
    def get(self, accountNumber):
        return dumps(db.accounts.find({'AccountNumber': accountNumber}, {'AccountType': 1, '_id': 0}))


# users can get there account balance
class CurrentAccBalance(Resource):
    @auth.login_required
    def get(self, accountNumber):
        return dumps(db.accounts.find({'AccountNumber': accountNumber}, {'CurrentAccBalance': 1, '_id': 0}))


# get the full name
class accClientFullName(Resource):
    @auth.login_required
    def get(self, accountNumber):
        result = db.accounts.find(
            {'AccountNumber': accountNumber},
            {'ClientName': 1, 'ClientFirstName': 1, '_id': 0}
        )
        return dumps({"fullName": result[0]['ClientFirstName'] + " " + result[0]['ClientName']})

# Server/client/(get | add | update | delete)choice/accountnumber , choice < name | firstname | DateOfBirth | ClientAddress | fullname >
class ClientInfo(Resource):
    @auth.login_required
    # get informations about the client
    def get(self, choice, accountNumber):
        # query to select only ClientName,ClientFirstName,ClientDoB,ClientAddress by giving accountNumber
        result = db.accounts.find(
            {'AccountNumber': accountNumber},
            {'ClientName': 1, 'ClientFirstName': 1, 'ClientDoB': 1, 'ClientAddress': 1, '_id': 0}
        )
        # serve the request depending on choice value
        if choice == 'name':
            return dumps({'name': result[0]['ClientName']})
        elif choice == 'firstname':
            return dumps({'firstname': result[0]['ClientFirstName']})
        elif choice == 'dateofbirth':
            return dumps({"DateOfBirth": result[0]['ClientDoB']})
        elif choice == 'address':
            return dumps({'ClientAddress': result[0]['ClientAddress']})
        elif choice == 'fullname':
            return dumps({'fullName': result[0]['ClientFirstName'] + ' ' + result[0]['ClientName']})

#operations accessible for regular users
class ClientUpdate(Resource):
    @auth.login_required
    # Update Client Info
    def put(self, choice, accountNumber):

        parser.add_argument('newname')
        parser.add_argument('newfirstname')
        parser.add_argument('newaddress')
        parser.add_argument('newdateofbirth')
        args = parser.parse_args()

        if choice == 'name':

            result = db.accounts.update_one(
                {'AccountNumber': accountNumber},
                {
                    '$set': {
                        'ClientName': args['newname']
                    }
                }
            )
        elif choice == 'firstname' :
            result = db.accounts.update_one(
                {'AccountNumber': accountNumber},
                {
                    '$set': {
                        'ClientFirstName': args['newfirstname']
                    }
                }
            )
        elif choice == 'address' :
            result = db.accounts.update_one(
                {'AccountNumber': accountNumber},
                {
                    '$set': {
                        'ClientAddress': args['newaddress']
                    }
                }
            )
        elif choice == 'dateofbirth' :
            result = db.accounts.update_one(
                {'AccountNumber': accountNumber},
                {
                    '$set': {
                        'ClientDoB': args['newdateofbirth']
                    }
                }
            )

        return result.matched_count, 201

#operations for a bank agent using a username and password
class BankAgentUpdate(Resource):
    @auth.login_required
    #update accountNumber of a client
    def put(self, choice, accountNumber):
        parser.add_argument('newaccbalance')
        args = parser.parse_args()

        result = db.accounts.update_one(
                {'AccountNumber': accountNumber},
                {
                    '$set': {
                        'CurrentAccBalance': args['newaccbalance']
                    }
                }
            )
        return result.matched_count , 201


#operations for a bank agent using a username and password
class BankAgentDelete(Resource):
    @auth.login_required
    #delete a client
    def delete(self, choice ,accountNumber):
        if choice == 'client' :
            result = db.accounts.deleted_many({'AccountNumber' : accountNumber})
            return result.deleted_count , 204
        elif choice == 'account' :
            result = db.accounts.update_one(
                     {'AccountNumber': accountNumber},
                     {
                          '$set': {
                                    'CurrentAccBalance': 0,
                                    'AccountType'  : '',
                                    'AccountNumber': ''
                                }
                     }
                    )
            return result.matched_count , 204

        return -1 , 404

class BankAgentCreate(Resource):
    @auth.login_required
    #add new client with account
    def post(self):

        parser.add_argument('AccountNumber')
        parser.add_argument('AccountType')
        parser.add_argument('CurrentAccBalance')
        parser.add_argument('ClientFirstName')
        parser.add_argument('ClientName')
        parser.add_argument('ClientDoB')
        parser.add_argument('ClientAddress')
        args = parser.parse_args()

        result = db.accounts.insert_one(
            {
                'AccountNumber' : args['AccountNumber'],
                'AccountType' : args['AccountType'],
                'CurrentAccBalance': args['CurrentAccBalance'],
                'ClientFirstName': args['ClientFirstName'],
                'ClientName': args['ClientName'],
                'ClientDoB': args['ClientDoB'],
                'ClientAddress': args['ClientAddress']
            }
        )

        return dumps(result.inserted_id) , 201