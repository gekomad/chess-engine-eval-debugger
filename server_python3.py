#!/usr/bin/env python3

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import cgi
import tempfile
import os
import subprocess
from subprocess import Popen
import urllib.request, urllib.parse, urllib.error
import os
import platform

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


    def do_PUT(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        if platform.system()=="Linux" :
            exe = './engines/cinnamon_2.4_x64-INTEL'
        elif platform.system()=="Windows" :
            exe = './engines/cinnamon_2.4_x64-INTEL.exe'
        elif platform.system()=="Darwin" :
            exe = './engines/cinnamon_mac_2.4'

        new_file, filename = tempfile.mkstemp()

        puzzle = message['puzzle']

        input = open(filename, 'r').read()

        outfile = Popen([exe,"-puzzle_epd", "-t", puzzle], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = outfile.communicate(input=bytes(input,"utf-8"))
        res = out.decode()
        print(res[:10])
        #os.remove(filename)

        # send the message back
        self._set_headers()
        #new_file1, filename1 = tempfile.mkstemp()
        #os.write(new_file1,res)
        #os.close(new_file1)
        self.wfile.write(bytes(res, "utf-8") )

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))

        # refuse to receive non-json content
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        fen = message['fen']
        exe = urllib.parse.unquote(message['exe'])

        if exe == "Crafty" :
            if platform.system()=="Linux" :
                exe = './engines/crafty-linux64'
            elif platform.system()=="Windows" :
                exe = './engines/crafty25.3.exe'
            elif platform.system()=="Darwin" :
                exe = './engines/crafty_25.2_mac'
        elif exe == "Stockfish" :
            if platform.system()=="Linux" :
                exe = './engines/stockfish_20011801_x64_linux'
            elif platform.system()=="Windows" :
                exe = './engines/stockfish_20011801_x64.exe'
            elif platform.system()=="Darwin" :
                exe = './engines/stockfish-11-64_mac'

        eval_command = message['eval_command']
        protocol = message['protocol']
        set_board = 'position fen'
        disable_ponder = 'setoption name ponder value false'
        if protocol == 'xboard':
            set_board = 'setboard'
            disable_ponder = 'ponder off'
        # write command file
        new_file, filename = tempfile.mkstemp()

        os.write(new_file, bytes(disable_ponder + '\n' + set_board + ' ' + fen + "\n" + eval_command + "\nquit\n","utf-8"))
        os.close(new_file)

        input = open(filename, 'r').read()

        outfile = Popen([exe], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)

        out, err = outfile.communicate(input=bytes(input,"utf-8"))
        res = out.decode()
        os.remove(filename)

        # send the message back
        self._set_headers()
        #new_file1, filename1 = tempfile.mkstemp()
        #os.write(new_file1,res)
        #os.close(new_file1)
        self.wfile.write(bytes(res, "utf-8") )


def run(server_class=HTTPServer, handler_class=Server, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)

    print("\nopen http://127.0.0.1:8080/\n")
    'Starting httpd on port %d...' % port
    httpd.serve_forever()


if __name__ == "__main__":
    from sys import argv
    run()
