#!/usr/bin/env python
# -*- coding: utf-8 -*-
     
abc = 'abcdefghijklmnopqrstuvwxyz'
     
def encrypt(message, key):
     
    text_encrypted = ''
     
    for leter in message:
	    sum = abc.find(leter) + key
	    modulo = int(sum) % len(abc)
	    text_encrypted = text_encrypted + str(abc[modulo])
     
    return text_encrypted
     
def decrypt(message, key):
     
    text_encrypted = ''
     
    for leter in message:
	    sum = abc.find(leter) - key
	    modulo = int(sum) % len(abc)
	    text_encrypted = text_encrypted + str(abc[modulo])
     
    return text_encrypted
     
def main():
    ms = str(raw_input('message a encrypt: ')).lower()
    n = int(raw_input('key numerica: '))
    print encrypt(ms,n)
    cms = str(raw_input('message a decrypt: ')).lower()
    cn = int(raw_input('key numerica: '))
    print decrypt(cms,cn)	
     
if __name__ == '__main__':
    main()
