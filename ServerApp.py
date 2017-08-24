import REST as R
from flask import Flask
from flask_restful import Api

# create flask app
app = Flask(__name__)
api = Api(app, prefix='/api/v1')

#user : client , password : 321
#user : agent  , password : 123


# get the account type
api.add_resource(R.AccoutType, '/account/get/type/<accountNumber>')

# get the Current Balance
api.add_resource(R.CurrentAccBalance, '/account/get/balance/<accountNumber>')

# get the client info
# choice can be : name , firstname , dateofbirth , address
api.add_resource(R.ClientInfo, '/client/get/<choice>/<accountNumber>')

# update the client info
# choice can be : name , firstname , address or dateofbirth
# the body of request should have 'newname' for choice == name ,
# 'newfirstname' for choice == firstname ,
# 'newaddress' for choice == address,
# 'newdateofbirth' for choice == dateofbirth
# the return is 1 if updated
api.add_resource(R.ClientUpdate, '/client/update/<choice>/<accountNumber>')

# operations for bank agent as app user
# choice can be : accbalance ;  pass also the agent 'username' and 'password'
# Request body should have attribute of newaccbalance
# the connected user should be agent , if not : Unauthorized access message
api.add_resource(R.BankAgentUpdate, '/agent/update/<choice>/<accountNumber>')

# choice can be : client , account .
# deleting  a client means deleting also the account (full document), the opposit is false
api.add_resource(R.BankAgentDelete, '/agent/delete/<choice>/<accountNumber>')

#create new client
#arguments :
#'AccountNumber'
#'AccountType'
#'CurrentAccBalance'
#'ClientFirstName'
#'ClientName'
#'ClientDoB'
#'ClientAddress'
api.add_resource(R.BankAgentCreate, '/agent/create/client')

if __name__ == '__main__':
    #Run the server on the machine IP address
    #to be visible across the network
    #Set debug to True for more debugging information
    app.run(host='0.0.0.0', debug=False)