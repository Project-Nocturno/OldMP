class Session():
    def __init__(self, session, sock):
        self.session=session
        self.ip, self.port=sock.getpeername()
        
    def put(self, key: str, value):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
                
        if not exist:
            self.session.update({
                self.ip: {}
            })
            
        self.session[self.ip][key]=value
        
    def get(self, key: str):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
                
        if not exist:
            self.session.update({
                self.ip: {}
            })
            
        try: return self.session[self.ip][key]
        except: 
            print(f'\nbadinfos-{key}\n')
            return ""
    
    def exist(self):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
        
        return exist
    
    def len(self):
        
        return len(self.session)
    
    def list(self, key: str):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
        
        if not exist:
            self.session.update({
                self.ip: {}
            })
            
        try: return [self.session[i][key] for i in self.session]
        except: 
            print(f'\nbadinfos key-{key}\n')
            return []
        
    def found(self, key: str):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
        
        if not exist:
            self.session.update({
                self.ip: {}
            })
        
        for i in self.session:
            if self.session[i][key]=='':
                return self.session[i]
        
        print(f'\nkey not found-{key}')
        return {}
    
    def clear(self):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
        
        if not exist:
            pass
        
        else:
            self.session.pop(self.ip)