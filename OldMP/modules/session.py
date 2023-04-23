from flask import request

class Session():
    def __init__(self, session: dict={}, req: request=request):
        self.session=session
        self.request=req
        
    def put(self, key: str, value):
        
        exist=False
        for i in self.session:
            if i==self.request.remote_addr:
                exist=True
                
        if not exist:
            self.session.update({
                self.request.remote_addr: {}
            })
            
        self.session[self.request.remote_addr][key]=value
        
    def get(self, key: str):
        
        exist=False
        for i in self.session:
            if i==self.request.remote_addr:
                exist=True
                
        if not exist:
            self.session.update({
                self.request.remote_addr: {}
            })
            
        try: return self.session[self.request.remote_addr][key]
        except: 
            print(f'\nbadinfos-{key}\n')
            return ""
    
    def exist(self):
        
        exist=False
        for i in self.session:
            if i==self.request.remote_addr:
                exist=True
        
        return exist
    
    def len(self):
        
        return len(self.session)
    
    def kill(self):

        exist=False
        for i in self.session:
            if i==self.request.remote_addr:
                exist=True
                
        if not exist:
            pass
        else:
            self.clear()
            self.put('kill', True)

    def clear(self):
        
        exist=False
        for i in self.session:
            if i==self.request.remote_addr:
                exist=True
        
        if not exist:
            pass
        
        else:
            self.session.pop(self.request.remote_addr)