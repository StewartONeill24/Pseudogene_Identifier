from Bio import Entrez
from pybedtools import BedTool
import os, glob, pybedtools, subprocess, pandas as pd, re
from tkinter import *
from mysite.settings import BASE_DIR

def retrieve_input():
    global geneNames
    inputValue=textBox.get("1.0","end-1c")
    geneNames = inputValue.splitlines()
    root.destroy()
    return geneNames

bedGraphFile = BASE_DIR+"/script/static_files/wgEncodeCrgMapabilityAlign75mer.bedGraph"

#With gene name as input, obtain all the accession IDs associated with this query gene, using e-utils.
#Return a list of all accession IDs found.
def get_Accessions(query_genes):
    dictionary = {}
    #Obtain accession IDs using entrez utils.
    for query_gene in query_genes:
        print('....getting accessions....')
        print(query_gene)
        Entrez.email = "stewart.o'neill@nhs.net"
        handle = Entrez.esearch(db="nucleotide", term= "Homo sapiens[ORGN] AND %s [GENE]" % query_gene, idtype="acc")
        record =Entrez.read(handle)
        handle.close()
        accessionIDs_1 = record['IdList']
        dictionary[query_gene.upper()] = accessionIDs_1
    print(dictionary)
    return dictionary

#Retain only those accession IDs with NM prefix.
#Uses list of accession IDs as input.
#Returns a list of only those accession IDs that contain the string "NM" as output.
def get_NM_Accessions_Only(accessionID_DICT):
    dictionary_filtered = {}
    print('....getting NM accessions....')
    for gene, accession_list in accessionID_DICT.items():
        acc_trim = []
        for acc in accession_list:
            if "NM" in acc:
                head, sep, tail = acc.partition('.')
                new_acc = head + sep
                acc_trim.append(new_acc)
        dictionary_filtered[gene] = acc_trim
    print(dictionary_filtered)
    return dictionary_filtered

#Retrieve the BED file for each transcript.
#Uses list of transcripts containing string "NM" as input.
#Creates a BED file for each item in this list by searching whether the transcript ID is present in each line of refseq_Exons.bed.
#If so, print line to file.
def create_BEDs(ACC_FILTERED_DICT):
    print('....getting BEDs....')
    for gene, accession_list in ACC_FILTERED_DICT.items():
        print(gene)
        print(accession_list)

        for acc in accession_list:
            with open(BASE_DIR+"/script/static_files/refseq_Exons.bed") as f:
                with open(gene + "_" + (acc.rsplit(".", 1)[0]) + ".bed", "w") as output_file:
                    for line in f:
                        if acc in line:
                            print('.....line is......')
                            print(line)
                            output_file.write(line)

#Intersect a given bed file with that containing the alignment mappability of the entire genome.
#Uses a BED file and the alignment mappability BED file as inputs.
#Output is a BED file containing intersecting rows between the two files.
def intersect(bedA, bedB):
    print('....intersecting....')
    print('....bedA is....')
    print(bedA)
    print('....bedB is....')
    print(bedB)
    a = pybedtools.BedTool(bedA)
    b = pybedtools.BedTool(bedB)
    intersectFile = a.intersect(b, wb=True, sorted=True, output="%s.intersect" % bedA)
    os.remove(os.path.abspath(bedA))

def create_PNG(bed_intersect_file, ACC_FILTERED_DICT):
    #Instantiate local variables
    list_of_dfs = []
    row_list = []
    print('....creating PNGs ....')
    print(bed_intersect_file)
    
    #Split file name. Store NM ID as 'transcript'
    head, sep, tail = bed_intersect_file.partition('.')
    transcript = head
    
    #Convert bed_intersect_file to a dataframe.
    #Remove unnecessary columns.
    #Calculate the number of bases the alignment score applies to for each row.
    #Remove original bed_intersect_file
    df = pd.read_csv(bed_intersect_file,sep="\t",header=None)
    df.drop(df.columns[[4,5,6,7,8]], axis =1, inplace = True)
    span_df= df[2] - df[1]
    os.remove(os.path.abspath(bed_intersect_file))

    #Append each row, according to its corresponding span, to row_list
    for i in range((df.shape[0])):
        for _ in range(span_df[i]):
            row_list.append(list(df.iloc[i, :]))

    #Convert row_list to dataframe. Delete row_list
    df = pd.DataFrame.from_records(row_list)
    row_list.clear()

    #Parse the entries of the transcript/exon column to a new dataframe set to remove duplicates.
    unique_entries = df[3].unique()
    sorted(unique_entries)

    #Iterate and split the dataframes when they have the desired value.
    #Append to a new list of dataframes, each entry containing rows pertaining to only one exon of the transcript.
    for i in unique_entries:
        df_temp = df[df[3] == i]
        list_of_dfs.append(df_temp)

    for index,df in enumerate(list_of_dfs, 1):

        #Save the new dataframes into tsv files.
        for i in range((df.shape[0])):
            df.iloc[i,0] = i    
        df.drop(df.columns[[1,2,3]], axis =1, inplace = True)
        tsvFile = "{transcript}_exon_{index}.tsv".format(transcript=transcript, index=index)
        df.to_csv(tsvFile,header=None,sep="\t",index=False)

        #Plot tsvFile and save as png. Remove tsvFile.
        subprocess.call(["Rscript", BASE_DIR+"/script/plot_repeat.R", tsvFile])
        os.remove(os.path.abspath(tsvFile))

    list_of_dfs.clear()
    
    try:
        os.makedirs(transcript)
    except FileExistsError:
        pass
    for file in glob.glob("*.png"):
        if transcript in file:
            new_location = transcript + "/" + file
            os.rename(file, new_location)
"""
root=Tk()
root.title("Mappability")
w = Label(root, text="Please enter the genes of which you wish to calculate the mappability")
w.pack()
textBox=Text(root, height=10, width=50)
textBox.bind('<Return>', lambda x: retrieve_input())
textBox.pack()
buttonCommit=Button(root, height=1, width=18, text="Calculate Mappability", command=lambda: retrieve_input())
buttonCommit.pack()
mainloop()

acc_dict = get_Accessions(geneNames)
acc_trimmed = get_NM_Accessions_Only(acc_dict)
create_BEDs(acc_trimmed)

#For every BED file, remove those that are empty, and intersect those that aren't empty with the bedGraph file. The remove the original bed file.
for file in glob.glob("*.bed"):
    if os.stat(os.path.abspath(file)).st_size == 0:
        os.remove(os.path.abspath(file))
    else:
        intersect(file,bedGraphFile)

for file in glob.glob("*.bed.intersect"):
    create_PNG(file, acc_trimmed)
"""
