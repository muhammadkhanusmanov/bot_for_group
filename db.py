import json

class DB:
    def __init__(self, db_path):
        #Initialize the database
        #Open the database file if it exists, otherwise create a new database file
        self.db_path = db_path
        try:
            with open(db_path, 'r') as f:
                self.db = json.load(f)
        except FileNotFoundError:
            self.db = {}
            #Save the database to the database file
            with open(db_path, 'w') as f:
                json.dump(self.db, f, indent=4)
    def save(self):
        with open(self.db_path, 'w') as f:
            json.dump(self.db, f, indent=4)
        return None
    def add_group(self, group1, group2):
        self.db['admin']['group']["1"]=group1
        self.db['admin']['group']["2"]=group2
        return None
    def get_user(self,chat_id):
        return self.db['Users'][str(chat_id)]
    def add_actives(self,chat_id,date):
        self.db['admin']['actives'][str(chat_id)]={'date':date}
        return None
    def get_date(self,user_id):
        return self.db['Users'][str(user_id)]['date']
    def get_statistic(self):
        return self.db['admin']
    def add_cost(self,a,b,c):
        self.db['admin']['date']['7'] = a
        self.db['admin']['date']['15'] = b
        self.db['admin']['date']['30'] = c
        return None
    def add_cart(self,cart):
        self.db['admin']['cart'] = cart
        return None
    def add_current(self,user_id):
        if not (str(user_id) in self.db['admin']['current_active']):
            self.db['admin']['current_active'].append(str(user_id))
            return None
        return None
    def del_current(self,user_id):
        if str(user_id) in self.db['admin']['current_active']:
            self.db['admin']['current_active'].remove(str(user_id))
        return None
    def add_til(self, user_id,til):
        self.db['Users'][str(user_id)]['til'] = til
        return None
    def starting(self,user_id):
        if not (user_id in self.db['Users']):
            stc=self.get_statistic()
            if (str(user_id) in stc['admins']) or (str(user_id) in stc['superadmins']):
                self.db['Users'][user_id] = {'til':'','date':'admin'}
            else:
                self.db['Users'][user_id] = {'til':'','date':''}
        return None
    def add_superadmin(self,user_id):
        
        if not (user_id in self.db['admin']['superadmins']):
            self.db['admin']['superadmins'].append(str(user_id))
        return None
    def del_superadmin(self,user_id):
        if user_id in self.db['admin']['superadmins']:
            self.db['admin']['superadmins'].remove(str(user_id))
            return True
        return False
    def del_admin(self, user_id):
        if user_id in self.db['admin']['admins']:
            self.db['admin']['admins'].remove(str(user_id))
            return True
        return False
    def del_activ(self, user_id):
        del self.db['admin']['actives'][str(user_id)]
        return None
    def del_current(self, user_id):
        self.db['admin']['current_active'].remove(str(user_id))
        return None
    def add_name(self,name):
        self.db['admin']['cart_name'] = name
        return None
    def add_admin(self,admin):
        self.db['admin']['admins'].append(admin)
        return None
    def add_xabar(self,user_id):
        self.db['admin']['xabar'][str(user_id)] = True
        return None
    def del_xabar(self,user_id):
        self.db['admin']['xabar'][str(user_id)] = False
        return None
    def add_check(self,user_id):
        if not (str(user_id) in self.db['admin']['check']):
            self.db['admin']['check'].append(str(user_id))
            return None
        return None
    def del_check(self,user_id):
        self.db['admin']['check'].remove(str(user_id))
        return None
            

    