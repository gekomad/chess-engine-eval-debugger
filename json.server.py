#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import tempfile
import os
import subprocess
from subprocess import Popen
import urllib
import os  

class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/text')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        try:
            self.send_response(200)
            page=self.path.rsplit('?',1)[0]
            if page.endswith(".html"):               
                self.send_header('Content-type',    'text/html')               
            elif page.endswith(".css"):               
                self.send_header('Content-type',    'text/css')
            
            f = open("./"+page, 'rb')
            
            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

        except IOError:
            self.send_error(404,'File Not Found: %s' % self.path)

    # POST echoes the message adding a JSON field
    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.getheader('content-length'))
        message = json.loads(self.rfile.read(length))

        fen = message['fen']
        exe = urllib.unquote(message['exe'])
        remove_line = int(message['remove_line'])
        eval_command = message['eval_command']
        protocol = message['protocol']
        set_board = 'position fen'

        if protocol == 'xboard':
            set_board = 'setboard'

        # write command file
        new_file, filename = tempfile.mkstemp()
        print(filename)

        os.write(new_file, set_board + ' ' + fen + "\n" + eval_command + "\n")
        os.close(new_file)

        input = open(filename, 'r').read()

        outfile = Popen([exe], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = outfile.communicate(input=input)
        res = out.decode()
        res = '\n'.join(res.split('\n')[remove_line:])
        os.remove(filename)
        # send the message back
        self._set_headers()
        #new_file1, filename1 = tempfile.mkstemp()
        #os.write(new_file1,res)
        #os.close(new_file1)
        self.wfile.write(res)


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print
    'Starting httpd on port %d...' % port
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv
    run()
