#This parser converts the packet to a single X feature vector based on user input.
#6-28-19
#This version runs like all of the others: using the first hex character through the
#number of features requested.
#This parser also uses packet_types.py along with the newer datasets based on 2500 packets
#for each protocol/type for training. For ex. 2500 ARP messages 

#from packet_types import *
import numpy as np
from datetime import datetime
import time
import os
import statmaker



def num_rows(X_outfile):
    X_rows=0
    Y_rows=0
    with open(X_outfile) as data:
        for line in data:
            X_rows=X_rows+1
            Y_rows=Y_rows+1
    return X_rows, Y_rows

def numpy_X_Y(X_rows, X_cols, X_outfile, Y_rows, Y_cols):
    X=np.zeros((X_cols,X_rows))
    Y=np.zeros((Y_rows,Y_cols))
    i=0
    print("numpy_X_Y shapes:",X.shape, Y.shape)

    with open(X_outfile) as traffic:
        for line in traffic:
            for j in range(X_cols):
                #print(i,j,line)
                X[j][i]=int(line[j],16)  #This is a problem with odd nos. due to '/n'
            i=i+1
    #X=X/16           #Normalizes X
    #print(X[:,0])
    return X,Y

def mean_normalize(X, features):
    X_normalized=np.zeros((X.shape[0],X.shape[1]))
    #ctr=0
    for i in range(X.shape[1]):
        X_sum=np.sum(X[:,i])
        X_mean=X_sum/features
        for j in range (X.shape[0]):
            X_normalized[j,i]=X[j,i]-X_mean
        #Y[i]=Y[ctr]/16
        #ctr=ctr+1
    return X_normalized

def fields_and_labels(X_outfile, Y):
    icmp_req_ctr =0
    icmp_reply_ctr =0
    arp_req_ctr = 0
    arp_reply_ctr = 0
    ctr = 0

    #read the file and classify

    with open(X_outfile, 'r') as file:
        lines = file.readlines()

    for i in range(0, len(lines), 1):
        packet_hex = lines[i].strip()  # Second line is the hex data
        
        classic = statmaker.classifier(packet_hex)        #get the packet class

        #["ICMP Reply", "ICMP Request", "ARP Request", "ARP Reply"]:

        if classic == 'ICMP Request':
            traffic_class_int = 1
            icmp_req_ctr +=1
        if classic == 'ICMP Reply':
            traffic_class_int = 2
            icmp_reply_ctr += 1
        if classic == 'ARP Request':
            traffic_class_int = 3
            arp_req_ctr += 1
        if classic == 'ARP Reply':
            arp_reply_ctr +=1
            traffic_class_int = 4
   
        traffic_class_int=str(traffic_class_int)
        Y[ctr]=traffic_class_int                             #Places the value of the ground truth into the proper Y index
        ctr=ctr+1
  
    print("Some label ctrs:",icmp_req_ctr, icmp_reply_ctr, arp_req_ctr, arp_reply_ctr)
    return Y
    

def preprocessor_main(features,cleaned_file_list,X_test_file_list,Y_test_file_list):


    #print()
    #Step one - obtain source file and create clean version of each named for the kind of capture file.
    #features=150 #X_cols
    X_rows=0
    Y_rows=0
    Y_cols=1
    X_cols=features
   
   
    for i in range(len(cleaned_file_list)):
        X_source_file=cleaned_file_list[i]
        X_features_file=X_test_file_list[i]
        Y_labels_file=Y_test_file_list[i]

        print()
        print("Input file             :",X_source_file)
        print("Normalized feature file:",X_features_file)
        print("Output label file      :",Y_labels_file)
        print()

        #print("Calling num_rows")
        X_rows, Y_rows=num_rows(X_source_file)              #Used to help build numpy arrays

        #print("Calling numpy_X_Y")
        X,Y=numpy_X_Y(X_rows, X_cols, X_source_file, Y_rows, Y_cols)

        #print("Calling mean_normalized")
        X_normalized=mean_normalize(X, features)    #Currently not called for CNN    6-4-19 

        # if "w" in X_source_file:
        #     print("Calling wireshark fields and labels for:", X_source_file)
        #     Y=fields_and_labels(X_source_file, Y) #Processes source data to establish ground truth values.

        # else:
        #     print("Unknown file type.")

        Y = fields_and_labels(X_source_file, Y)
            
        np.save(Y_labels_file,Y)
        np.save(X_features_file,X_normalized)

# cleaned_file_list = []
# cleaned_file_list.append('megacleanfoobar.txt')
# X_test_file_list = []
# X_test_file_list.append('x_test.npy')
# Y_test_file_list = []
# Y_test_file_list.append('y_test.npy')


#preprocessor_main(128,cleaned_file_list,X_test_file_list,Y_test_file_list)



