# encoding:utf-8
import struct,sys,os,binascii

class rc4:

    def __init__(self,key = None):
        self.key = key or 'default_key'

    def encode(self,data):
        if(type(data) is type("string")):
            tmpData=data
            data=[]
            for tmp in tmpData:
                data.append(ord(tmp))
        if(type(self.key) is type("string")):
            tmpKey=self.key
            self.key=[]
            for tmp in tmpKey:
                self.key.append(ord(tmp))
        x = 0
        box= list(range(256))
        for i in range(256):
            x = (x + box[i] + self.key[i % len(self.key)]) % 256
            box[i], box[x] = box[x], box[i]
        x = 0
        y = 0
        out = []
        for c in data:
            x = (x + 1) % 256
            y = (y + box[x]) % 256
            box[x], box[y] = box[y], box[x]
            out.append(c ^ box[(box[x] + box[y]) % 256])
     
        result=""
        printable=True
        for tmp in out:
            if(tmp<0x21 or tmp>0x7e):
                printable=False
                break
            result += chr(tmp)
            
        if(printable==False):
            result=""
            for tmp in out:
                result += "{0:02X}".format(tmp)
            
        return result

    def decode(self,data):
        data=[int(('0x')+data[i:i+2],16) for i in range(0,len(data),2)]
        x = 0
        box= list(range(256))
        for i in range(256):
            x = (x + box[i] + self.key[i % len(self.key)]) % 256
            box[i], box[x] = box[x], box[i]
        x = 0
        y = 0
        out = []
        for c in data:
            x = (x + 1) % 256
            y = (y + box[x]) % 256
            box[x], box[y] = box[y], box[x]
            out.append(c ^ box[(box[x] + box[y]) % 256])
     
        result=""
        printable=True
        for tmp in out:
            if(tmp<0x21 or tmp>0x7e):
                printable=False
                break
            result += chr(tmp)
            
        if(printable==False):
            result=""  
            for tmp in out:
                result += "{0:02X}".format(tmp)
        return result

        pass

if __name__ == '__main__':
    rc4=rc4('foo')
    encoded_key=rc4.encode('bar')
    print(encoded_key)
    decoded_key=rc4.decode(encoded_key)
    print(decoded_key)
