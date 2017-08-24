# BEA

This Simple application is tested using Postman
Database : MongoDb - on a virtual machine with address of 192.168.100.210 and port : 27017
framework : flask with flask-restful
libraries : pymongo , flask_httpauth

REST.py        : contain all functions required to communicate with database , and serve the requests.
ServerApp.py   : run the script to start the application

Database   : bank_db
Collection : accounts
document example : 
{
    "_id" : ObjectId("599e478b23049f39eb0ccc4c"),
    "AccountNumber" : "123",
    "CurrentAccBalance" : "3000",
    "ClientDoB" : "12/12/1970",
    "ClientAddress" : "no where",
    "AccountType" : "debit",
    "ClientName" : "name",
    "ClientFirstName" : "firstName"
}

Requests are tested using Postman , with basic Auth 
users     |     psw
-------------------
agent     |     123
client    |     321

The Application runs on the machine IP address
port : 5000

Example requests : 
    GET - PUT - DELETE - POST
    ----------------------------------------------------------------------------------
    GET Client Address  : http://192.168.100.125:5000/api/v1/client/get/address/123
    GET Client name     : http://192.168.100.125:5000/api/v1/client/get/name/123
    GET Client firstname: http://192.168.100.125:5000/api/v1/client/get/firstname/123
    GET Client fullname : http://192.168.100.125:5000/api/v1/client/get/fullname/123
    GET Account type    : http://192.168.100.125:5000/api/v1/account/get/type/123

The usage of the Requests is explained in the code.




