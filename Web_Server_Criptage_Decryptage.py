#!/usr/bin/python
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import cgi
import Queue

PORT_NUMBER = 8084

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
    def __init__(self, nsa_queue, *args):
        self.nsa_queue = nsa_queue
        BaseHTTPRequestHandler.__init__(self, *args)

    #Handler for the GET requests
    def do_GET(self):
        if self.path=="/":
            self.path="/index.html"

        try:
            #Check the file extension required and
            #set the right mime type

            sendReply = False
            if self.path.endswith(".html"):
                mimetype='text/html'
                sendReply = True
            if self.path.endswith(".jpg"):
                mimetype='image/jpg'
                sendReply = True
            if self.path.endswith(".gif"):
                mimetype='image/gif'
                sendReply = True
            if self.path.endswith(".js"):
                mimetype='application/javascript'
                sendReply = True
            if self.path.endswith(".css"):
                mimetype='text/css'
                sendReply = True

            if sendReply == True:
                #Open the static file requested and send it
                f = open(curdir + sep + self.path) 
                self.send_response(200)
                self.send_header('Content-type',mimetype)
                self.end_headers()
                self.wfile.write(f.read())
                f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)
    
    
    #Handler for the POST requests
    def do_POST(self):
        if self.path=="/send":
            form = cgi.FieldStorage(
                fp=self.rfile,
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })
            print form["le_texte"].value  
            encr_text = self.encrypt_cesar(form["le_texte"].value, 2)
            self.nsa_queue.put(encr_text)
            print "Le texte en clair: %s" % form["le_texte"].value
            self.send_response(200)
            self.end_headers()
            self.wfile.write(encr_text)
            return

        if self.path=="/send_scytal":
            form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                         'CONTENT_TYPE':self.headers['Content-Type'],
            })

            encr_text = self.encrypt_scytal(form["le_texte"].value, 2)
            self.nsa_queue.put(encr_text)
            print "Le texte en clair: %s" % form["le_texte"].value
            self.send_response(200)
            self.end_headers()
            self.wfile.write(encr_text)
            return

        if self.path=="/decrypt":
            le_texte = self.nsa_queue.get()
            print "Le texte en encode: %s" % le_texte
            self.send_response(200)
            self.end_headers()
            self.wfile.write("Le texte intercepte: %s.\r" % le_texte)
            self.wfile.write(" Le texte decode cesar: %s" % self.decrypt_cesar(le_texte , 2))
            self.wfile.write(" Le texte decode scytal: %s" % self.decrypt_scytal(le_texte , 2))
            return
            
    def encrypt_cesar(self, message, key):
        abc = "abcdefghijklmnopqrstuvwxyz"
        text_encrypted = ''
        for leter in message:
                sum = abc.find(leter) + key
                modulo = int(sum) % len(abc)
                text_encrypted = text_encrypted + str(abc[modulo])

        return text_encrypted
        
    def decrypt_cesar(self, message, key):
        abc = "abcdefghijklmnopqrstuvwxyz"
        text_decrypted = ''
        for leter in message:
                sum = abc.find(leter) - key
                modulo = int(sum) % len(abc)
                text_decrypted = text_decrypted + str(abc[modulo])
     
        return text_decrypted

    def encrypt_scytal(self, text, key):
        if len(text) % key == 0:
             rowLength = len(text) / key
        else:
            rowLength = len(text) / key + 1
        encryptMatrix = [[' ' for i in range(rowLength)] for j in range(key)]
        for y in range (0,key):
         for x in range (0, rowLength):
             if y * rowLength + x < len(text):
                 encryptMatrix[y][x] = text[y * rowLength + x]
        encryptedText = ''
        for x in range (0, rowLength):
          for y in range (0, key):
            encryptedText+=str(encryptMatrix[y][x])
        finalEncrypted = ''.join(encryptedText)
        return finalEncrypted
        
    def decrypt_scytal(self, text, key):
        if len(text) % key == 0:
             rowLength = len(text) / key
        else:
            rowLength = len(text) / key + 1
        encryptMatrix = [[' ' for i in range(rowLength)] for j in range(key)]
        for y in range (0,key):
         for x in range (0, rowLength):
             if y * rowLength + x < len(text):
                 encryptMatrix[y][x] = text[y * rowLength + x]
        encryptedText = ''
        for x in range (0, rowLength):
          for y in range (0, key):
            encryptedText+=str(encryptMatrix[y][x])
        finalEncrypted = ''.join(encryptedText)
        if len(text) % key == 0:
           rowLength = len(text) / key
        else: 
           rowLength = len(text) / key + 1
        decryptMatrix = [[' ' for i in range(rowLength)] for j in range(key)]
        for x in range (0, rowLength):
         for y in range (0,key):
           decryptMatrix[y][x] = finalEncrypted[x * key + y]
        decryptedText=''
        for x in range (0, rowLength):
          for y in range (0,key):
            decryptedText+=str(decryptMatrix[y][x])
        finalDecrypted = ''.join(decryptedText)
        return finalDecrypted


try:
    nsa_queue = Queue.Queue()

    def handler(*args):
        myHandler(nsa_queue, *args)

    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('', PORT_NUMBER), handler)
    print 'Started httpserver on port ' , PORT_NUMBER
    #Wait forever for incoming http requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
