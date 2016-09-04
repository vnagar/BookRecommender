#!/bin/sh

#Get the api token
curl -u pam:pam -i -X GET http://127.0.0.1:5000/api/token

#send the token as part of the request. Note the "unused" at the end of token 
#since the password is not used.
curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ3MzAwNDYyMywiaWF0IjoxNDczMDA0MDIzfQ.eyJpZCI6MX0.NG49rMlFqc0NFHThtjcouJrUoPRo1fSTeVyULNgUbrc:unused -i -X GET http://127.0.0.1:5000/api
