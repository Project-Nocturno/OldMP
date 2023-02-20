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
    
    def clear(self):
        
        exist=False
        for i in self.session:
            if i==self.ip:
                exist=True
        
        if not exist:
            pass
        
        else:
            self.session.pop(self.ip)