import hashlib
import re
import os
import shutil
from SOAPpy import SOAPProxy#python 2.7
#create file
def create_file(store_path):
    if os.path.exists(store_path):
        print("path exists")
        shutil.rmtree(store_path)
        os.mkdir(store_path)        
    else:      
        os.mkdir(store_path)
        print(store_path) 

# search brenda
def query_brenda(outFile,search_function):
    #parameters = "mao_zt@tib.cas.cn,"+password+",ecNumber*%s#organism*Escherichia coli"%term
    password = hashlib.sha256("jxphmzt258").hexdigest()
    parameters = "mao_zt@tib.cas.cn,"+password
    #print parameters
    endpointURL = "https://www.brenda-enzymes.org/soap/brenda_server.php"
    client = SOAPProxy(endpointURL)  
    #resultString = client.search_function(parameters)
    method_to_call = getattr(client, search_function)
    try:
        resultString = method_to_call(parameters)    
        resultValue=resultString.split("!")
    except:
        pass
    else:
        for eachdata in resultValue:
            if eachdata: 
                outFile.write(eachdata.encode('utf-8', 'ignore'))
                outFile.write("\n")
            else:
                break                       

def query_brenda_by_ec(outFile,search_key,search_function):
    #parameters = "mao_zt@tib.cas.cn,"+password+",ecNumber*%s#organism*Escherichia coli"%term
    password = hashlib.sha256("jxphmzt258").hexdigest()
    parameters = "mao_zt@tib.cas.cn,"+password+",ecNumber*%s"%search_key
    #print parameters
    endpointURL = "https://www.brenda-enzymes.org/soap/brenda_server.php"
    client = SOAPProxy(endpointURL)  
    method_to_call = getattr(client, search_function)
    try:
        resultString = method_to_call(parameters)    
        resultValue=resultString.split("!")
    except:
        pass
    else:
        for eachdata in resultValue:
            if eachdata: 
                outFile.write(eachdata.encode('utf-8', 'ignore'))
                outFile.write("\n")
            else:
                break

def query_brenda_by_ec_org(outFile,search_key1,search_key2,search_function):
    #parameters = "mao_zt@tib.cas.cn,"+password+",ecNumber*%s#organism*Escherichia coli"%term
    password = hashlib.sha256("jxphmzt258").hexdigest()
    parameters = "mao_zt@tib.cas.cn,"+password+",ecNumber*%s#organism*%s"%(search_key1,search_key2)
    #print parameters
    endpointURL = "https://www.brenda-enzymes.org/soap/brenda_server.php"
    client = SOAPProxy(endpointURL)  
    method_to_call = getattr(client, search_function)
    try:
        resultString = method_to_call(parameters)    
        resultValue=resultString.split("!")
    except:
        pass
    else:
        for eachdata in resultValue:
            if eachdata: 
                outFile.write(eachdata.encode('utf-8', 'ignore'))
                outFile.write("\n")
            else:
                break
