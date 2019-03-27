To use this implementation
First import db from model.py on python command line 
call create_all() to create the database
you create a user
Then  log in your user using the user username and password during creation
create a client
you can then add feature for each client using the add feature link on the homepage

function.py contains the order_priority function that reorders the priority for any any feature
It also ensures that no two features have the same priority for any given client
The function first selects the features for a given client
sorts all the feature
Then it looks for where a priority repeats and adds one to the first feature's priority
it then adds one the all following features for the client

This function is called after every new feature is created for a client
It takes the clients id as an argument

The web page can be tested using the user with the following credential

username: user
password: user

some clients has already been created already
