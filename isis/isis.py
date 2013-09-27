import re
import string
import socket
import time
import telnetlib
from struct import pack,unpack

def getSocket(chal):
    '''chal is a 2-tuple with an address and a port  ex: ('127.0.0.1',111)'''
    s=socket.socket()
    s.settimeout(5)
    s.connect(chal)
    return s

def shell(sock):
    '''pass to this function a socket object with a listening shell(socket reuse)'''
    command=''
    while(command != 'exit'):
        command=raw_input('$ ') 
        sock.send(command + '\n\0')#raw_input won't grab a newline
        time.sleep(.5)
        print sock.recv(0x10000)
    return

def telnet_shell(sock):
    '''pass to this function a socket object with a listening shell(socket reuse)'''
    tc = telnetlib.Telnet()  
    tc.sock = sock
    tc.interact() 
    return 

def lei(*nums):
    '''
    wrapper for pack, will guess integer size and type
    takes a variable number of arguments
    '''
    if(len(nums)==1):
        num=nums[0]
        if(num>0):
            if(num<0xffffffff):
                return pack("<I",num)
            else:
                return pack("<Q",num)
        else:
            return pack("<i",num)
    else:
        return ''.join(map(lei,nums))

''' 
utilities
'''
def chunk(iterable, chunkSize):
    for i in range(0,len(iterable),chunkSize):
        yield iterable[i:i+chunkSize]

#def alphabet():
#    return map (chr, [(lambda x: x+ord('a'))(x) for x in range(0,26)])
    

def patternString(): 
    for x in list(string.ascii_lowercase): 
        for y in list(string.ascii_lowercase): 
            for z in range(10): 
                yield ''.join([x.upper(), y, str(z)])


def dipstick(n): 
    limit = 0 
    ret = ''
    for i in patternString(): 
        if limit < n: 
            limit = limit + 1 
            ret = ret + i 
        else: 
            break 
    return ret 

maxPat=''.join(patternString())

def rDipstick(offset):
    '''
    will accept an int of the form 0x12345678 or a string
    that looks like '12345678'
    '''
    if(type(offset)==type(999)):
        offset=hex(offset)[2:].zfill(8)
    findMe=reduce(lambda a,b:b+a,chunk(offset,2)).decode('hex')
    return maxPat.index(findMe)

