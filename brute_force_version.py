###### MAIN_PROGRAM ######
R={}



## Fill the R list with the scores from rnd.txt
with open('rnd.txt','r') as rnd:
    linereader=rnd.readlines()
    for row in linereader:
        row=row.replace('\n','')
        row=row.split(' ')
        score={int(row[0]): float(row[1])} 
        R.update(score)


with open('seq1.txt','r') as seq_1:
    linereader=seq_1.readlines()
    for row in linereader:
        row=row.replace('\n','')
        row=row.split(' ')
        R[int(row[0])]+=float(row[1])


with open('seq2.txt','r') as seq_2:
    linereader=seq_2.readlines()
    for row in linereader:
        row=row.replace('\n','')
        row=row.split(' ')
        R[int(row[0])]+=float(row[1])
print(R[22652])

R=dict(sorted(R.items(), key=lambda x: x[1]))


for key, value in R.items():
        print(key, value)