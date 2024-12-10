import database.database as db

def req(user, password): 
    return db.check_user_passw(users, password)

def new_user(user, password):
    db.create_new_user(user, password)
