import uuid
import json

class User():
    def __init__(self, name, password,role="user", id = None, packs = []) -> None:
        self.name = name
        self.password = password
        self.role = role
        self.id = id or str(uuid.uuid4())
        self.packs = packs or [] 
    def to_json(self):        
        return {"name": self.name}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)
    
    def newUser(name:str,password:str,role:str = "user"):
        with open("users.json","r") as f:
            users = json.loads(f.read())
        users.append(User(name,password,role = role).__dict__)
        with open("users.json",'w') as f:
            f.write(json.dumps(users))





