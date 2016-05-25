"""
The following code opens the binary file and creates an
array of 6 columns that are the [o]event, [1]channel, [2]something,
[3]trigger time, [4]energy, and a [5]boolean variable to indicate if
this is a coincidence event. In order to understand the bitwise
operations that are performed, refer to section 4 of the Pixie-4
user manual. (4.2)
"""

import sys
import time
import chanCheck
import numpy as np

def binaryRead(det):
    print('BinaryRead method')
    print("binary file processing...please wait...")
    with open(det.fileLoc, "rb") as f: #fileLoc = det.fileLoc = location of file #opens the files for reading (rb=binary mode)
        dt=np.dtype('u2') #dt is datatype u2 (unsigned int)
        detectRes=np.fromfile(f, dt) #reads file and sets contents in as detectRes

    bufferHeader=np.zeros(6,dtype=np.int) #array os 6, zeroed, int
    listHold=[]
    channel=[]
    size=np.size(detectRes) # of the rows read from binary file
    z=0    
    temp=[]
    while z<size: #run while z is less than size of total rows in binfile
        bufferHeader.fill(0) #fill buffer header array with 0s
        np.copyto(bufferHeader,detectRes[z:z+6]) #copy in bufferheader array with the 6 rows of contents
        bufferHeader[2]-=0x2000 #take number in slot two and remove 10000000000000 in binary, 8192 in decimal
        if(bufferHeader[2]==256 or bufferHeader[2]==257): #next three conditions specify what chLen will equal (based on runtype/task)
            chLen=9 #(List mode standard and list mode compression 1)

        elif(bufferHeader[2]==258): #list mode compress 2 type
            chLen=4

        elif(bufferHeader[2]==259): # #list mode compress 3 (energy and time only)* usually what is used
            chLen=2

        temp+=list(detectRes[z+6:z+bufferHeader[0]]) #add the items in list format to the temp array (from end of first buffer header+6 to end of word size as indicated by 0'th col of buffer header)
        #I.E if z= 0 , bufferheader[0]= 10, then temp copies detectRes[6:10] (header + ch blocks)      
        z+=bufferHeader[0] #increment z by first buffer block

    detVal=np.array(temp) #take the event header + channel header blocks and create an array
    com=3 #size of event header block
    tskLen=com+chLen #length of total blocks to work with per event
    hold=np.zeros(tskLen+1,dtype=np.int) #zero out an array of size chLen+3(+1for coincidence check)
    x=0
    while x<np.size(detVal): #while x is less then size of the total event+ch header blocks (detVal)
        hold.fill(0) #empty temporary list
        coinChan=0 #
        np.copyto(hold[:tskLen],detVal[x:x+tskLen]) #copy current event + ch header block to temp list
        x+=tskLen #increment x
        oldChanPat=hold[0]&0xf #bitwise operation AND logic test between hold[0] and 1111 binary (strips the event header's hit pattern 4 bit info)
        
								#above line basically compares last 4 bits of hold[0] (Event header word #0) to binary: 1111 using AND logic to determine what channels are valid in the event
								#hold[0] = event_header block's 1st 16 bit word
        hold[0]=chanCheck.chanCheck(oldChanPat,channel,hold[0]) #does something with chanCheck , for coincidence analysis, returns CurChan value from chancHECK
        for i in range(0,4):
            if oldChanPat&(0b1<<i): #if a coincidence is recorded
                coinChan+=1 #increase number of coincidence

        if coinChan>1: #if coincidence exists 
            hold[-1]=1 #make the last entry in hold = 1 (coincidence =true)
            for i in range(1,coinChan):
                listHold.append(list(hold)) #append current 5 blocks + 1 of data for each instance of coin
                oldChanPat=(oldChanPat&(~hold[0])) #bitwise operators & = AND, ~ = binary ones complement
                hold[0]=oldChanPat
                np.copyto(hold[com:tskLen],detVal[x:x+chLen]) #copy 2 more ch header blocks per additinal coincidence (up to 4)
                x+=chLen #increase counter by the ch's block amount

        listHold.append(list(hold))

    det.resInfo.append(list(channel)) #here is where resInfo is set 
    det.res=np.array(listHold) #here is where det.res is set. It gets the list and makes it work