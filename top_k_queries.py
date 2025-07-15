import copy

### Function to read the files and get the lower bound score or the final score
def seq_read(seq,R_list,S_dict,kc,DS_dict,DS_seq):
  
    seq=seq.replace('\n','')
    seq=seq.split(' ')
    ID_finder = seq[0]      ### keep the ID from the seq files
    seq = float(seq[1])     ### keep the score from the seq files
    kc_before=kc            ### keep the value of the kappa counter before it changes in check_existing_score function


    S_dict,  kc  =  check_existing_score(kc,S_dict,ID_finder,seq)
    ### S_dict: a dictionary with lower bound scores

    ### if the kappa counter hasn't changed "append" the lower bound score in the dictionary
    if(kc_before==kc):
        
        ### "append" the lower bound score in the dictionary
        down_score={ID_finder: R_list[int(ID_finder)]+seq} 
        DS_dict.update(down_score)
        S_dict.update(down_score)


        ### "append" the lower bound score in a dictionary for the different seq1 and seq2 files
        down_score={ID_finder: seq}  
        DS_seq.update(down_score)

        return kc,S_dict,seq,DS_dict,DS_seq
    
    ### if the kappa counter changed, keep the final score in the dictionary that you got from check_existing_score function
    else:
        down_score={ID_finder: seq}
        DS_seq.update(down_score)

        return kc,S_dict,seq,DS_dict,DS_seq
    


### Function to return the final score and raise the kappa counter
def check_existing_score(kc,S_dict,ID_finder,last_score):

    for key,val in S_dict.items():
        ### if you find the ID in the dictionary create the final score
        
        if ID_finder==key:
            S_dict[key]=S_dict[key]+last_score
            kc+=1
            return S_dict,kc
        
    ### else return the dictionary as it was before
    return S_dict,kc
    

### function to create the min heap
def create_min_heap(S_dict,kc):
    Wk={}
    copy_S_dict=copy.deepcopy(S_dict)

    while kc>0:

        max_value=max(copy_S_dict.values())
        max__value_key = next(key for key, value in copy_S_dict.items() if value == max_value)  ### keep the ID from the maximum value of the dictionary
            
        for_Wk={max__value_key : max_value}
        Wk.update(for_Wk)

        copy_S_dict.pop(max__value_key)  ### remove the ID and the value from the copied dictionary

        kc-=1
       
    return Wk


### Function to check if the values in the dictionary are lower or greater than the threshold 
def check_threshold(wk,big_T):
    for key,val in wk.items():
        if big_T >= val:
            return False

    return True


### Function to check if the values in the dictionary are lower or greater than the upper bound
def check_upper_bound(wk,S_dict,DS_dict,DS_seq1,DS_seq2):
    copy_DS_dict=copy.deepcopy(DS_dict)
    seq1=0   #last value that have been added from seq1.txt to S_dict and were a lower bound
    seq2=0   #last value that have been added from seq1.txt to S_dict and were a lower bound

    ## Find the last value that was added that is a down score in the seq1 down score dictionary
    for key1,val1 in DS_seq1.items():
        if copy_DS_dict[key1]==S_dict[key1]:
            seq1=val1

    ## Find the last value that was added that is a down score in the seq2 down score dictionary
    for key2,val2 in DS_seq2.items():
        if copy_DS_dict[key2]==S_dict[key2]:
            seq2=val2

    for key,val in copy_DS_dict.items():
    
        ### Check if the ID of the DS_dict dictionary is not in DS_seq1 and if it isn't find the upper bound score
        if key not in DS_seq1:
            copy_DS_dict[key]=copy_DS_dict[key]+seq1

        ### Check if the ID of the DS_dict dictionary is not in DS_seq1 and if it isn't find the upper bound score
        if key not in DS_seq2:
            copy_DS_dict[key]=copy_DS_dict[key]+seq2
        
        min_value=min(wk.values())
        ### Check if the ID of the wk dictionary is not in DS_seq1 and if it isn't and the upper bound score is greater than the minimum value of wk then do more sequential accesses
        if key not in wk:
            if copy_DS_dict[key] > min_value:
                return False
    return True


###### MAIN_PROGRAM ######
R=[]
dict_of_scores={}           ## Dictionary that contains the ID, the lower bound scores and final scores from seq1 and seq2
dict_of_downscores={}       ## Dictionary that contains the ID and the lower bound scores from seq1 and seq2
dict_of_downscores_seq1={}  ## Dictionary that contains the ID, the lower bound scores and final scores from seq1
dict_of_downscores_seq2={}  ## Dictionary that contains the ID, the lower bound scores and final scores from seq2
k=0                         ## Input k from command line
kappa_counter=0             ## Counter to check if equal with k
access_counter=0            ## Counter to count the sequential accesses
checking=True


## While k is negative continue to ask for input
while k<=0:
    k=int(input("Give a positive number for k: "))

## Fill the R list with the scores from rnd.txt
with open('rnd.txt','r') as rnd:
    linereader=rnd.readlines()
    for row in linereader:
        row=row.replace('\n','')
        row=row.split(' ')
        R.append(float(row[1]))


## Read both seq1.txt and seq2.txt and do sequential accesses until the conditions are met
with open('seq1.txt','r') as seq_1, open('seq2.txt','r') as seq_2:
    for i,j in zip(seq_1,seq_2):
        ### Read line of seq1 
        if i:

            ## while the counter is lower than the k continue to do sequential accesses
            if kappa_counter<k:
                kappa_counter,  dict_of_scores,  threshold1,  dict_of_downscores, dict_of_downscores_seq1  =  seq_read(i,R,dict_of_scores,kappa_counter,dict_of_downscores,dict_of_downscores_seq1)
                access_counter+=1

            ## when we get the False from the checks bellow continue to do sequential accesses
            elif checking == False and kappa_counter>=k:
                    kappa_counter,  dict_of_scores,  threshold1,  dict_of_downscores, dict_of_downscores_seq1  =  seq_read(i,R,dict_of_scores,kappa_counter,dict_of_downscores,dict_of_downscores_seq1)
                    access_counter+=1
      
            ## If the counter is equal or greater than the input k, check the conditions for the min heap
            if kappa_counter>=k:
               
                Wk = create_min_heap(dict_of_scores,k)  ## Create the min heap

                final_threshold  =  threshold1 +threshold2 +5.0     ## Calculate or update the final threshold
                
                checking = check_threshold(Wk,final_threshold)   ## Check if the values in Wk are lower than the threshold
                
                ## Check if the values in Wk are lower than the upperbound
                if checking == True:
                    checking = check_upper_bound(Wk,dict_of_scores,dict_of_downscores,dict_of_downscores_seq1,dict_of_downscores_seq2)
               
                ## break the loop if the conditions have been met
                if checking==True:
                    break

        ### Read line of seq2 
        if j:
              
            ## while the counter is lower than the k continue to do sequential accesses
            if kappa_counter<k:
                kappa_counter,  dict_of_scores,  threshold2,  dict_of_downscores,  dict_of_downscores_seq2  =  seq_read(j,R,dict_of_scores,kappa_counter,dict_of_downscores,dict_of_downscores_seq2)
                access_counter+=1

            ## when we get the False from the checks bellow continue to do sequential accesses
            elif checking == False and kappa_counter>=k:
                kappa_counter,  dict_of_scores,  threshold2,  dict_of_downscores,  dict_of_downscores_seq2  =  seq_read(j,R,dict_of_scores,kappa_counter,dict_of_downscores,dict_of_downscores_seq2)
                access_counter+=1

            ## If the counter is equal or greater than the input k, check the conditions for the min heap
            if kappa_counter>=k:
                Wk = create_min_heap(dict_of_scores,k)  ## Create the min heap

                final_threshold  =  threshold1 +threshold2 +5.0     ## Calculate or update the final threshold

                checking = check_threshold(Wk,final_threshold)   ## Check if the values in Wk are lower than the threshold

                ## Check if the values in Wk are lower than the upperbound
                if checking == True:
                    checking = check_upper_bound(Wk,dict_of_scores,dict_of_downscores,dict_of_downscores_seq1,dict_of_downscores_seq2)
                       
                ## break the loop if the conditions have been met
                    if checking==True:
                        break


print("Number of sequential accesses:",access_counter)
print("Top k objects:")

for i in Wk:
    print(i,":",Wk[i])


