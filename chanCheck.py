"""
chanCheck is a function that is used by binaryRead. It takes in the
old channel pattern of the binary signal, the array of already known channels,
and the current channel binary pattern (necessary for identifying and adding channels
in coincidence events)
"""

def chanCheck(oldChanPat,channel,curChan): #used for coincidence event analysis
    #print('chanCheck Method called') <this method gets called alot during calibration
    k=0
    for i in range(0,4):
        if curChan&(0b1<<i)!=0b0: #0b1 << i = shift 0001 to make cmbination of 0001, 0010, 0100, 1000 then AND logic compare to current event's channels, 0b0 = 0000
            k=i #current ch (from evt header's 1st word's 4 bits)
            break

    curChan=oldChanPat&(0b1<<k)#previous header's 4bit and logic test with current
    if channel:
        for i in range(0,len(channel)+1):
            if channel[i]==curChan: #if previous channel = current ch
                k=i
                break

            if i==len(channel)-1: #end of list correction
                channel.append(curChan)
    
    else:
        channel.append(curChan)  #append to channel in binaryread.py   (tracks total # of ch's) up to 4
    
    return curChan