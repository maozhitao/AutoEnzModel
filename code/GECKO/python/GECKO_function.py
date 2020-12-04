import os
import shutil
import csv
import urllib2

################################################################################
# retrieveBRENDA
# Acces the web client and retrieves all EC data from BRENDA. Creates files with
# BRENDA output for all organisms and EC numbers for which there is data.
#
# Benjamin Sanchez. Last edited: 2018-04-10

#retrieveBRENDA: Function that extracts all BRENDA data from a specific field.
def retrieveBRENDA(field,last,output_path):

    #Construct list of EC numbers, based on the enzymes for which there is
    #data on BRENDA:
    if field == 'KM':
        ECstring = client.getEcNumbersFromKmValue(credentials)

    elif field == 'MW':
        ECstring = client.getEcNumbersFromMolecularWeight(credentials)

    elif field == 'PATH':
        ECstring = client.getEcNumbersFromPathway(credentials)

    elif field == 'SEQ':
        ECstring = client.getEcNumbersFromSequence(credentials)

    elif field == 'SA':
        ECstring = client.getEcNumbersFromSpecificActivity(credentials)

    elif field == 'KCAT':
        ECstring = client.getEcNumbersFromTurnoverNumber(credentials)
  
    EClist = ECstring.split('!')

    #Loop that retrieves data from BRENDA and saves it in txt files. Starts
    #from the last EC number queried:
    start = 0
    for ECnumber in EClist:
    
        #Detects the starting point (the last EC number queried):
        if not start and (ECnumber == last or last == ''):
            start = 1
        
        if start:
            #The code will retrieve data for all organisms:
            query  = credentials + ',ecNumber*' + ECnumber + '#organism*'
            succes = 0
            
            #The try/except block inside the while is to avoid timeout PROXY
            #and encoding errors:
            while succes < 10:
                try:
                    file_name = 'EC' + ECnumber + '_' + field
                    print file_name

                    if field == 'KM':
                        data = client.getKmValue(query)

                    elif field == 'MW':
                        data = client.getMolecularWeight(query)

                    elif field == 'PATH':
                        data = client.getPathway(query)

                    elif field == 'SEQ':
                        data = client.getSequence(query)

                    elif field == 'SA':
                        data = client.getSpecificActivity(query)

                    elif field == 'KCAT':
                        data = client.getTurnoverNumber(query)
                    
                    #Once the querie was performed succesfully, the data is
                    #copied in txt files:    
                    if data:
                        fid = open(output_path+file_name + '.txt','w')
                        fid.write(data.decode('ascii','ignore'))
                        fid.close()

                    succes = 10
                
                except:
                    #Let the server cool of for a bit. If after 10 times it
                    #still fails, the query is discarded:
                    time.sleep(1)
                    succes += 1

################################################################################

################################################################################
# createECfiles
# Reads all data in kinetic_data and creates all EC files.
#
# Benjamin Sanchez. Last edited: 2018-04-10
def createECfiles(input_path,output_path):
    dir_files = os.listdir(input_path)
    dir_files.sort()    
    #Main loop: Adds each BRENDA file's info to the corresponding EC file.
    previous  = ''
    for i in dir_files:
        #Define EC number and variable name:
        sep_pos   = i.find('_')
        ec_number = i[0:sep_pos]
        var_name  = i[sep_pos+1:len(i)-4]

        #Read all data in BRENDA file:
        fid       = open(input_path+i,'r')
        data      = fid.read()
        fid.close()
        
        #Detect a change of EC number:
        if ec_number != previous:
            if previous != '':
                #Save previous ec_table in a EC file:
                fid = open(output_path+previous + '.txt','w')
                for j in ec_table:
                    fid.write(j)
                fid.close()
                print 'Succesfully constructed ' + previous + ' file.'

            #Reset ec_table (initialize it in the first iteration):    
            ec_table = []
        
        #Define query to find in string "data", according to the variable name:

        if var_name == 'KM':
            variable  = '#kmValue*'

        elif var_name == 'MW':
            variable  = '#molecularWeight*'

        elif var_name == 'PATH':
            variable  = '#pathway*'

        elif var_name == 'SEQ':
            variable  = '#sequence*'

        elif var_name == 'SA':
            variable  = '#specificActivity*'

        elif var_name == 'KCAT':
            variable  = '#turnoverNumber*'

        #Split the string in N+1 parts, where N is the number of values for the
        #given variable:
        options = data.split(variable)
        for k in options:
            #Find the end of the value of interest and save it as k_value:
            value_pos = k.find('#')
            if value_pos != -1:
                k_value = k[0:value_pos]
                #If there is a substrate, split will create 2 strings and the info
                #will be at the beginning of string 2. Applies to KM & KCAT.
                k_split = k.split('#substrate*')
                if len(k_split) == 1:
                    k_split     = k_split[0]
                    k_substrate = '*'
                else:
                    k_split     = k_split[1]
                    k_substrate = k_split[0:k_split.find('#')]
                    if k_substrate == '':
                        k_substrate = '*'          
                
                #If there is a commentary, split will create 2 strings and the info
                #will be at the beginning of string 2. Applies to all except PATH
                #and SEQ.
                k_split2 = k_split.split('#commentary')
                if len(k_split2) == 1:
                    k_split2  = k_split2[0]
                    k_comment = '*'

                else:
                    k_split2  = k_split2[1]
                    k_comment = k_split2[0:k_split2.find('#')]
                
                #If there is a organism, split will create 2 strings and the info
                #will be at the beginning of string 2. Applies to all except PATH.
                k_split = k.split('#organism*')
                if len(k_split) == 1:
                    k_org = '*'

                else:
                    k_split = k_split[1]
                    k_org   = k_split[0:k_split.find('#')]
                    if k_org == '':
                        k_org = '*'              
                
                #Append data to ec_table in the following format:
                #[variable   organism   value]
                ec_table.append(var_name + '\t' + k_org + '\t' + k_value + '\t')
                #[substrate(if any, otherwise '*') commentary(if any, otherwise '*')
                ec_table.append(k_substrate + '\t' + k_comment + '\n')

        #Update previous ec number:
        previous = ec_number

    #Write last EC file:
    fid = open(output_path+previous + '.txt','w')
    for j in ec_table:
        fid.write(j)
                
    fid.close()
    print 'Succesfully constructed ' + previous + ' file.'
################################################################################

################################################################################
# findMaxKcats
# Reads all EC files and finds the max value for each substrate for the chosen
# microorganism on the different enzymatic parameters [Kcat, KM, SA, MW]. 
# For each parameter Writes a table with the following columns:
#   * EC number
#   * substrate
#   * organism name//taxonomical classification (according to KEGG)
#   * Max value
#   * metabolic pathways
# Benjamin Sanchez. Last edited: 2015-08-26
# Ivan Domenzain.   Last edited: 2018-04-10

#sub_max_std: Recieves a list of substrates///organism_info///values, returns
#3 lists: substrates - max - std
def sub_max_std(data):
    #Sorts list, add a last empty line and initialize variables:
    data.sort()
    data.append('')
    #for every substrate gets the index of all its appearences in the rows
    #of the EC data
    substrates, org_strings_reps, values_reps, reps_indexes = substrate_repetitions(data)
    org_strings, values =\
    find_in_substrate(substrates, org_strings_reps, values_reps, reps_indexes)
    #get maximum kvalues
    values = maximum_values(values)

    return (substrates,org_strings,values)

#maximum_values: Gets the maximum Kvalue for each organism related
#to each substrate
def maximum_values(values):
    for subs_values in values:
        i = values.index(subs_values)
        for org_values in subs_values:
            j = subs_values.index(org_values)
            #org_values = max(org_values)
            values[i][j] = max(values[i][j])

    return(values)

#find_in_substrate: Finds the organisms and K values related to each substrate
def find_in_substrate(substrates, org_strings_reps, values_reps, reps_indexes):

    org_strings = []
    values      = []
    for i in range(len(substrates)):
        subs_orgs   = []
        subs_values = []
        
        for j in reps_indexes[i]:
            
            try:
                org_index = subs_orgs.index(org_strings_reps[j])
                subs_values[org_index].append(values_reps[j])
            
            except:
                subs_orgs.append(org_strings_reps[j])
                org_index = subs_orgs.index(org_strings_reps[j])
                subs_values.append([values_reps[j]])

        org_strings.append(subs_orgs)
        values.append(subs_values)

    return(org_strings, values)

#substrate_repetitions: Finds from each EC file the organism and K values related
#to each substrate
def substrate_repetitions(data):
    
    substrates       = []
    org_strings_reps = []
    values_reps      = []
    reps_indexes = []

    for row in data:
        if row != '':
            row_index = data.index(row)
            #gets index if row substrate is repeated
            try:
                subs_indx = substrates.index(row[0:row.find('///')])
            #if new substrate
            except:
                substrates.append(row[0:row.find('///')])
                subs_indx = substrates.index(row[0:row.find('///')])
                reps_indexes.append([])
            #list with the indexes of the rows with repeated substrates
            reps_indexes[subs_indx].append(row_index)
            #organisms for related to each substrate
            org_strings_reps.append(row[row.find('///')+3:row.find('////')])
            #values found for each organism
            values_reps.append(float(row[row.find('////')+4:len(row)]))
    return(substrates, org_strings_reps, values_reps, reps_indexes)

#create_orgs_list: Finds all the organism names for which data is available in
#BRENDA database. As an output a list with all found names is created.
def brenda_orgs_list(input_path,dir):
    brenda_orgs=[]
    for ec in dir:
        fid     = open(input_path+ec,'r')
        csv_fid = csv.reader(fid,delimiter='\t')    
        try:
            for row in csv_fid:
                if row != '' and row[0] != 'SEQ' and row[0] != '*':       
        #Uncomment and indent properly if you want to exclude any name longer
        #two words (mutants for example, but not exclusively) 
                    #second_blank = row[1].find(' ',row[1].find(' ')+1)
                    #if second_blank == -1:
                    org_name = row[1].lower()
                    #else:
                    #    org_name=row[1][0:second_blank]               
                    if brenda_orgs.count(org_name)==0:
                        brenda_orgs.append(org_name)
        except:
            pass#brenda_orgs.append(org_name)
    return (brenda_orgs)

#KEGG_orgs_list: Creates a list with all the organisms available at KEGG, as an
#output  a table with the fields: name, KEGG code and Taxonomy is created.
def KEGG_orgs_list():
    #URL that returns available data of the gene entry on KEGG
    url = 'http://rest.kegg.jp/list/organism'
    #Try/except for avoiding timeout exceedings
    try:
        query = urllib2.urlopen(url, timeout=20).read()
    except:
        query=''

    entries   = query.split('\n')
    KEGG_list = []
    tax_kegg  = []
    codes     = []
    for row in entries:
        if row != '':
            row_list = row.split('\t')
            if len(row_list)>1:
                row_list=[row_list[2],row_list[3],row_list[1]]
                if row_list[0].find('(') != -1:
                    row_list[0]=row_list[0][0:row_list[0].find('(')-1]
       
                #Saves only organisms with specific taxonomic classifications
                taxonomy=row_list[1].lower()
                if taxonomy.find('eukaryotes')!= -1 or taxonomy.find('prokaryotes')!= -1:
                    KEGG_list.append(row_list[0].lower())
                    tax_kegg.append(taxonomy)
                    codes.append(row_list[2])
    return(KEGG_list, tax_kegg, codes)

#orgs_list: Two possible options 1) Merges BRENDA and KEGG organisms lists
# creates a list with only coincidences between lists.
def orgs_list(input_path,dir):
    KEGG_orgs, info_KEGG, codes = KEGG_orgs_list()
    print(KEGG_orgs)
    brenda_orgs = brenda_orgs_list(input_path,dir)
    #print brenda_orgs
    organism_list = []
    taxonomy      = []
    org_codes     = []
    #i=0
    counter=0 
    for B_org in brenda_orgs:
        flag = False
        if B_org != '*':
            i=0        
            while (i < len(KEGG_orgs) and flag == False):
                K_org = KEGG_orgs[i]
                if K_org.find(B_org)!= -1:               
                    flag    = True
                    counter = counter+1
                    organism_list.append(B_org)
                    taxonomy.append(info_KEGG[i])
                    org_codes.append(codes[i])
                i = i +1  
            if flag == False:
                organism_list.append(B_org)
                taxonomy.append('*')
                org_codes.append('*')

    return(organism_list,taxonomy,org_codes)

#EC_string: Receives the information in the EC file and builds a string with
#substrates, related organisms and Kvalues
def EC_string(csv_fid, organism_list, organism_code, taxonomy, feature_name):
    data_string = []
    ec_pathways = ''
    for row in csv_fid:
        if row[0] != '':
            row[4] = row[4].lower()
            mutant = max(row[4].find('mutant'),row[4].find('mutated'))
            #Ignore invalid values:
            if row[2] != '-999' and mutant == -1:
                #Only allow Kcats <= 1e7 [Bar-Even et al. 2011]
                if row[0] == feature_name and float(row[2]) <= 1e7:
                    #Looks for the organism in the organism merged list
                    #in order to include taxonomical info if available
                    try:
                        org_index  = organism_list.index(row[1].lower())
                        org_string = organism_list[org_index]+'//'+\
                                     taxonomy[org_index]+ '//'+ organism_code[org_index]
                            
                        data_string.append(row[3].lower() + '///' +\
                                            org_string + '////' + row[2])
                    except:
                        print 'Organism not found in KEGG or BRENDA'
        
            #Gets the associated not engineered pathways to the
            #EC number if present
            if row[0] == 'PATH' and row[2].lower() != 'metabolic pathways':
                if row[2].find('(engineered)') == -1:
                    ec_pathways = ec_pathways + row[2].lower() + '///'
    #If path not found an asterisk is added to the field
    if ec_pathways == '' or ec_pathways == ' ' or ec_pathways == '\0':
        ec_pathways = '*'
    if len(ec_pathways) > 3 and ec_pathways[-3] == '/':
        ec_pathways = ec_pathways[:-3]

    return(data_string, ec_pathways)

################################################################################

################################################################################
# retrieveKEGG
# Access the KEGG API and retrieves all data available for each protein-coding
# gene of the "n" organisms specified. Creates a file for each succesful query.
#retrieve_org_genesData: Function that extracts all data available
#in KEGG database for the organism in turn.
# Ivan Domenzain. Last edited: 2018-04-10

def retrieve_org_genesData(organism, last_entry):
    
    #URL that returns the entire genes list for the organism
    url        = 'http://rest.kegg.jp/list/' + organism
    genes_list = []
    
    #Try/except for avoiding execution abortions ending in case of
    #querying timeout exceeded
    try:
        #Stores the queried genes list as a string
        data_str = urllib2.urlopen(url, timeout=20).read()
        
        #String division into substrings for each gene. Just the entry names are
        #saved on a list. Previously queried genes, if any, are removed from the list.
        separator  = organism + ':'
        substrings = data_str.split(separator)

        for i in substrings:
            if i[0:i.find('\t')]!=(' ' and '\0'and ''):
                genes_list.append(i[0:i.find('\t')])

        if last_entry!='':
            genes_list=genes_list[genes_list.index(last_entry):]
        
        #Retrieves gene data, if sucessfuly queried and a UniProt code is found
        #then a file .txt is created, otherwise, a warning is displayed
        for gene in genes_list:
            gene_query, gene_string = extract_geneEntry_data(organism, gene)
            
            if gene_query.find('UniProt:')!=-1:
                if gene_query!='':
                    fid = open(gene + '.txt','w')
                    fid.write(gene_query.decode('ascii','ignore'))
                    fid.close()
                    print 'Succesfully constructed ' + gene_string + '.txt'
                else:
                    print 'Unsuccesful query for gene ' + gene_string
            else:
                print 'No UniProt code for ' + gene_string
    except:
        print organism + ' not found or timeout exceeded'

#extract_geneEntry_data: Function that retrieves specific
#gene entries from KEGG
def extract_geneEntry_data(organism, gene):
    #URL that returns available data of the gene entry on KEGG
    gene_string = organism+ ':' + gene
    url         = 'http://rest.kegg.jp/get/' + gene_string
    
    #Try/except for avoiding timeout exceedings
    try:
        gene_query = urllib2.urlopen(url, timeout=20).read()
    except:
        gene_query=''

    return(gene_query, gene_string)

################################################################################