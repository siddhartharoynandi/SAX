import numpy as np
import math
import scipy.stats as st

def standardize(num,glob_mean,glob_sd):
    num_standard = []
    for i in num:
        num_standard.append((i-glob_mean)/glob_sd)
    return num_standard

def SAX(num,word_length,alphabet_size):
    glob_mean = np.mean(num)
    glob_sd = np.std(num)
    #print glob_mean,glob_sd
    standard_num = standardize(num,glob_mean,glob_sd)
    #print standard_num
    ############# This Part is for Alphabet Assignment ########################
    each_alphabet_segment_area = 1.0/alphabet_size
    i= 0.0
    word_range_dict = {}
    count = 65
    while (i<1.0):
        #print i,i+increment_value
        #print chr(count)
        word_range_dict.update({chr(count): [i, i + each_alphabet_segment_area]})
        count +=1
        i += each_alphabet_segment_area
    #print word_range_dict

    ############# This Part is for Breaking the Signal And Calculating Local Minima ##################
    size_of_each_window = math.ceil((len(standard_num)*1.0)/word_length)
    #print size_of_each_window
    br_num = []
    i = 0.0
    while (i<len(standard_num)):
        if (int(i+size_of_each_window) >len(standard_num)):
            br_num.append(standard_num[int(i):])
        else:
            br_num.append(standard_num[int(i):int(i+size_of_each_window)])
        i += size_of_each_window
    #print br_num
    br_num_mean = []
    for i in br_num:
        br_num_mean.append((sum(i)*1.0)/len(i))
    #print br_num_mean
    br_num_mean_prob = []
    for i in br_num_mean:
        if i < glob_mean:
            br_num_mean_prob.append(1.0 - (st.norm(glob_mean, glob_sd).pdf(i)))
        else:
            br_num_mean_prob.append(st.norm(glob_mean, glob_sd).pdf(i))
    #print br_num_mean_prob
    ############## This Part is for String Generation of the Segmented Signal ##########################
    SAX_String = ''
    for i in br_num_mean_prob:
        for j in word_range_dict.keys():
            if (word_range_dict[j][0]<= i < word_range_dict[j][1]):
                SAX_String += j
                break
    return SAX_String

if __name__ == '__main__':
    num = np.array([-8.0, -7.0, -6.0, -5.0, -4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0])
    word_length = 5
    alphabet_size = 4
    f = open('/Users/siddhartharoynandi/Desktop/ADM/CIS563_HW3/SAX_Output.txt', 'w')
    f.write('Input Array: ' +str(num))
    f.write('\n')
    f.write('String Size: '+str(word_length))
    f.write('\n')
    f.write('Word Vocabulary Size: '+str(alphabet_size))
    f.write('\n')
    f.write('SAX output stream: '+SAX(num,word_length,alphabet_size))
    f.close()
    exit(0)

