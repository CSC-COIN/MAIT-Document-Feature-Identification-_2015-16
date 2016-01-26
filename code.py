#Import Library Files

import sys
import nltk
import operator
import shutil
from nltk.tokenize import word_tokenize
from nltk.corpus import brown

path = ['files/input_files/Gravity (film).txt','files/input_files/Minions (film).txt',
'files/input_files/java(tech).txt','files/input_files/reboot(science_friction).txt',
 'files/input_files/Python (programming language).txt',
 'files/input_files/GreatestMysteries(science_friction).txt']

for pid in path:
    #Read input file
    inpfile = open(pid).read() 

    reload(sys)  
    sys.setdefaultencoding('Cp1252')

    #Tokenize
    inpwords=word_tokenize(inpfile);

    #POS
    tagged=nltk.pos_tag(inpwords)
    
    #Extracting Nouns using Chunking
    chunkGram = r"""Chunk: {<NN.?.?>}"""
    chunkParser = nltk.RegexpParser(chunkGram)

    #Get Parse Tree
    chunked = chunkParser.parse(tagged)

    #Initialise
    inpfinal=[]
    scifi_top=[]
    content_top=[]
    pl_top=[]

    #Append Nouns to Array
    for subtree in chunked.subtrees():
       if subtree.label() == 'Chunk':
            inpfinal.append(subtree[0][0])

    #Frequency Distribution
    freqn = nltk.FreqDist(w.lower() for w in inpfinal)
    
    #Get top 500 words from Content
    content_topf=freqn.most_common(500)
    for i in content_topf:
        content_top.append(i[0])

    #Get top 500 words from Science Fiction
    scifi = brown.words(categories='science_fiction')
    scifi_freq = nltk.FreqDist(w.lower() for w in scifi)
    scifi_topf=scifi_freq.most_common(500)
    for i in scifi_topf:
       scifi_top.append(i[0])
    
    #Get top 500 words from Programming Language   
    plfile = open("PL_corpora.txt").read()
    plwords=word_tokenize(plfile);
    pl_freq = nltk.FreqDist(w.lower() for w in plwords)
    pl_topf=pl_freq.most_common(500)
    for i in pl_topf:
       pl_top.append(i[0])

    scifi_count=0
    pl_count=0
    default=17 #Threshold value
    
    #Print File Name
    print ("Processing: " + pid)

    #Searching
    for i in content_top:
       if i in scifi_top:
          #print "Matched word: "+i
          scifi_count+=1
       if i in pl_top:
          #print "Matched word: "+i
          pl_count+=1
    
    #Print each probability
    #print ("SciFi Count: "+str(scifi_count))
    #print ("PL Count: "+str(pl_count))
    
    #Get MAX of count from dictionary of counts
    countd={'SciFi': scifi_count,'PL': pl_count,'Other': default}
    maxkey=max(countd.iteritems(), key=operator.itemgetter(1))[0]
    
    #Classify
    if(maxkey=='SciFi'):
        shutil.move(pid, 'files/categories/fiction')
    elif(maxkey=='PL'):
        shutil.move(pid, 'files/categories/technologies and PL')
    elif(maxkey=='Other'):
        shutil.move(pid, 'files/categories/movies')
    
    #Print highest probability
    #print countd[maxkey] #for verification