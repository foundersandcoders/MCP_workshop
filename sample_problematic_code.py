# Problematic Python code for testing code review tools
# This file intentionally contains various code smells and anti-patterns

import os,sys,json,re,time # Bad: multiple imports on one line

# Magic numbers throughout the code
def CalculateScore(data):  # Bad: CamelCase function name, no docstring
    total=0 # Bad: no spaces around operator
    for item in data:
        if item>100: # Bad: no spaces around operator, magic number
            total+=item*2 # Bad: no spaces, magic number
        elif item>50 and item<=100: # Bad: magic numbers, complex condition
            total+=item*1.5 # Bad: magic number
        elif item>25:
            total+=item
        elif item>10:
            total+=item*0.5
        elif item>5:
            total+=item*0.25
        elif item>1:
            total+=item*0.1
        else:
            total+=0

    if total>1000: # Magic number
        return total*1.2
    elif total>500: # Magic number
        return total*1.1
    elif total>200: # Magic number
        return total*1.05
    else:
        return total

class DataManager: # Manager pattern (good to detect)
    def __init__(self):
        self.data=[]
        self.cache={}
        self.settings={}
        self.users=[]
        self.logs=[]
        self.stats={}
        self.temp_data=[]
        self.processed_items=[]
        self.failed_items=[]
        self.success_count=0
        self.error_count=0
        self.last_updated=None
        self.is_dirty=False
        self.lock_status=False # Too many instance variables (God object)

    def processData(self,input_data,mode,options,filters,validators,transformers): # Bad: CamelCase, too many parameters
        if not input_data:
            return []

        result=[]
        errors=[]

        for i,item in enumerate(input_data):
            if mode=='strict':
                if options and 'validate' in options:
                    if validators:
                        for validator in validators:
                            if validator=='email':
                                if '@' not in str(item) or '.' not in str(item):
                                    errors.append(f"Invalid email at index {i}")
                                    continue
                            elif validator=='phone':
                                if len(str(item))!=10: # Magic number
                                    errors.append(f"Invalid phone at index {i}")
                                    continue
                            elif validator=='age':
                                if int(item)<18 or int(item)>120: # Magic numbers
                                    errors.append(f"Invalid age at index {i}")
                                    continue

                if transformers:
                    for transformer in transformers:
                        if transformer=='uppercase':
                            item=str(item).upper()
                        elif transformer=='lowercase':
                            item=str(item).lower()
                        elif transformer=='trim':
                            item=str(item).strip()

                if filters:
                    skip=False
                    for filter_rule in filters:
                        if filter_rule=='empty':
                            if not item or str(item).strip()=='':
                                skip=True
                                break
                        elif filter_rule=='numeric':
                            try:
                                float(item)
                            except:
                                skip=True
                                break
                    if skip:
                        continue

                result.append(item)

            elif mode=='lenient':
                try:
                    if transformers:
                        for transformer in transformers:
                            if transformer=='clean':
                                item=str(item).replace('  ',' ').strip()
                    result.append(item)
                except:
                    errors.append(f"Error processing item at index {i}")

        return result,errors # Long function with high complexity

def create_user_factory(user_type): # Factory pattern (good to detect)
    if user_type=='admin':
        return {'type':'admin','permissions':['read','write','delete']}
    elif user_type=='user':
        return {'type':'user','permissions':['read']}
    else:
        return {'type':'guest','permissions':[]}

class ConfigBuilder: # Builder pattern (good to detect)
    def __init__(self):
        self.config={}

    def build_database_config(self):
        self.config['database']={'host':'localhost','port':5432} # Magic number
        return self

    def build_cache_config(self):
        self.config['cache']={'ttl':3600,'max_size':1000} # Magic numbers
        return self

    def build(self):
        return self.config

# Singleton pattern (good to detect)
class Logger:
    _instance=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance=super().__new__(cls)
        return cls._instance

# Very long line that exceeds the recommended 79 character limit and should be flagged by the style checker as a violation
x = "This is an extremely long string that goes way beyond the recommended line length limit and should definitely be broken into multiple lines for better readability and maintainability"

def process_everything(data,mode,settings,cache,logs,users,permissions,filters,validators,transformers,handlers): # Too many parameters
    pass # Empty function

if(__name__=="__main__"): # Bad: missing space, should be if __name__ == "__main__":
    data=[1,2,3,42,100,1000] # Magic numbers
    score=CalculateScore(data)
    print(f"Score: {score}")

    manager=DataManager()
    result,errors=manager.processData(data,'strict',None,None,None,None)
    print(f"Processed: {len(result)} items")