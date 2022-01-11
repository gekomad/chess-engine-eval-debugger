#!/usr/bin/env python3

import json
import tempfile
import subprocess
from subprocess import Popen
import urllib.request, urllib.parse, urllib.error
import os
import re
import platform
import shutil
import stat
from urllib.parse import unquote
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
import os.path
import sys

class Handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/text')
        self.end_headers()

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        try:
            self.send_response(200)
            page = self.path.rsplit('?', 1)[0]
            if page == "/":
                page = "index.html"

            if page.endswith(".html"):
                self.send_header('Content-type', 'text/html')
            elif page.endswith(".css"):
                self.send_header('Content-type', 'text/css')

            f = open("./" + page, 'rb')

            self.end_headers()
            self.wfile.write(f.read())
            f.close()
            return

        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def get_score(self, exe, set_board, fen, eval_command):
        input = bytes(
            "ponder off" + '\n' + "log off" + '\n' + "setoption name ponder value false" + '\n' + set_board + ' ' + fen + '\n' + eval_command + '\n' + "quit" + '\n',
            "utf-8")
        outfile = Popen([exe], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = outfile.communicate(input)
        res = out.decode()
        res2 = ""
        for line in res.splitlines():
            if "White(1): " != line and "Black(1): " != line and "Unknown command" not in line and "Illegal move" not in line and "unable to open book file" not in line and "book is disabled" not in line and "pondering disabled" not in line and "machine has" not in line:
                res2 += f"{line}\n"
        return res2

    def do_PUT(self):

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        if platform.system() == "Linux":
            exe = './engines/cinnamon_2.4_x64_linux'
        elif platform.system() == "Windows":
            exe = './engines/cinnamon_2.4_x64.exe'
        elif platform.system() == "Darwin":
            exe = './engines/cinnamon_mac_2.4'

        puzzle = message['puzzle']

        outfile = Popen([exe, "-puzzle_epd", "-t", puzzle], stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                        stderr=subprocess.PIPE)

        out, err = outfile.communicate(input=bytes("", "utf-8"))
        res = out.decode()

        self._set_headers()
        self.wfile.write(bytes(res, "utf-8"))

    def get_engine(self, exe):
        if exe == "Crafty":
            if platform.system() == "Linux":
                return './engines/crafty_25.2_linux'
            elif platform.system() == "Windows":
                return './engines/crafty25.2.exe'
            elif platform.system() == "Darwin":
                return './engines/crafty_25.2_mac'
        elif exe == "Stockfish":
            if platform.system() == "Linux":
                return './engines/stockfish_20011801_x64_linux'
            elif platform.system() == "Windows":
                return './engines/stockfish_20011801_x64.exe'
            elif platform.system() == "Darwin":
                return './engines/stockfish-11-64_mac'
        else:
            return exe

    def setboard(self, protocol):
        set_board = 'position fen'
        if protocol == 'xboard':
            set_board = 'setboard'
        return set_board

    def get_engine_protocol(self, engine):
        input =  bytes("uci\nquit\n", "utf-8")
        outfile = Popen([engine], stdout=subprocess.PIPE, stdin=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = outfile.communicate(input=input)
        res = out.decode()
        try:
            re.compile(".*id name (.*).*").search(res).group(1)
            return "uci"
        except:
            return "xboard"

    def do_PATCH(self):

        length = int(self.headers.get('content-length'))

        message = json.loads(self.rfile.read(length))
        print(message)
        exe1 = self.get_engine(urllib.parse.unquote(message['exe1']))
        exe2 = self.get_engine(urllib.parse.unquote(message['exe2']))
        exe3 = self.get_engine(urllib.parse.unquote(message['exe3']))
        exe4 = self.get_engine(urllib.parse.unquote(message['exe4']))

        engine1 = False
        engine2 = False
        engine3 = False
        engine4 = False
        protocol1 = ""
        protocol2 = ""
        protocol3 = ""
        protocol4 = ""
        tempdir = tempfile.mkdtemp(prefix="chess-engine-eval-debugger-")
        os.mkdir(f"{tempdir}/engines")
        if exe1.strip():
            engine1 = True
            protocol1 = self.get_engine_protocol(exe1)
            shutil.copy(exe1, f"{tempdir}/engines/")
            exe1 = f"./engines/{os.path.basename(exe1)}"

        if exe2.strip():
            engine2 = True
            protocol2 = self.get_engine_protocol(exe2)
            shutil.copy(exe2, f"{tempdir}/engines/")
            exe2 = f"./engines/{os.path.basename(exe2)}"

        if exe3.strip():
            engine3 = True
            protocol3 = self.get_engine_protocol(exe3)
            shutil.copy(exe3, f"{tempdir}/engines/")
            exe3 = f"./engines/{os.path.basename(exe3)}"

        if exe4.strip():
            engine4 = True
            protocol4 = self.get_engine_protocol(exe4)
            shutil.copy(exe4, f"{tempdir}/engines/")
            exe4 = f"./engines/{os.path.basename(exe4)}"

        eval_command1 = message['eval_command1']
        eval_command2 = message['eval_command2']
        eval_command3 = message['eval_command3']
        eval_command4 = message['eval_command4']

        regex1 = unquote(message['regex1'])
        regex2 = unquote(message['regex2'])
        regex3 = unquote(message['regex3'])
        regex4 = unquote(message['regex4'])

        fen_list = unquote(message['fen_list'])
        fen_file = f"{tempdir}/fen.epd"
        ff = open(fen_file, 'w+')
        ff.write(fen_list)
        ff.close()
        set_board1 = self.setboard(protocol1)
        set_board2 = self.setboard(protocol2)
        set_board3 = self.setboard(protocol3)
        set_board4 = self.setboard(protocol4)

        template_file = open("generate_csv.py.template", "r")
        script_file = f"{tempdir}/generate_csv.py"
        script = open(script_file, 'w+')
        st = os.stat(script_file)
        os.chmod(script_file, st.st_mode | stat.S_IEXEC)
        for line in template_file:
            line = line.replace("$ENGINE1$", "True") if engine1 == True else line.replace("$ENGINE1$", "False")
            line = line.replace("$ENGINE2$", "True") if engine2 == True else line.replace("$ENGINE2$", "False")
            line = line.replace("$ENGINE3$", "True") if engine3 == True else line.replace("$ENGINE3$", "False")
            line = line.replace("$ENGINE4$", "True") if engine4 == True else line.replace("$ENGINE4$", "False")
            if engine1 == True:
                line = line.replace("$EXE1$", exe1)
                line = line.replace("$POSITION1$", set_board1)
                line = line.replace("$SCORE1$", eval_command1)
                line = line.replace("$REGEX1$", regex1)
            if engine2 == True:
                line = line.replace("$EXE2$", exe2)
                line = line.replace("$POSITION2$", set_board2)
                line = line.replace("$SCORE2$", eval_command2)
                line = line.replace("$REGEX2$", regex2)
            if engine3 == True:
                line = line.replace("$EXE3$", exe3)
                line = line.replace("$POSITION3$", set_board3)
                line = line.replace("$SCORE3$", eval_command3)
                line = line.replace("$REGEX3$", regex3)
            if engine4 == True:
                line = line.replace("$EXE4$", exe4)
                line = line.replace("$POSITION4$", set_board4)
                line = line.replace("$SCORE4$", eval_command4)
                line = line.replace("$REGEX4$", regex4)
            script.write(f"{line}")
        template_file.close()
        script.close()

        shutil.make_archive("generate_csv", 'zip', tempdir)
        self.send_response(200)
        self.end_headers()

    def do_POST(self):

        length = int(self.headers.get('content-length'))
        message = json.loads(self.rfile.read(length))

        fen = message['fen']
        if fen.count('/') != 7 or "k" not in fen or "K" not in fen:
            self._set_headers()
            self.wfile.write(bytes(f"malformed fen {fen}", "utf-8"))
        else:

            exe = urllib.parse.unquote(message['exe'])
            exe = self.get_engine(exe)
            self._set_headers()
            if os.path.isfile(exe) and os.access(exe, os.X_OK):
                eval_command = message['eval_command']
                protocol = self.get_engine_protocol(exe)
                set_board = self.setboard(protocol)
                res = self.get_score(exe, set_board, fen, eval_command)
                self.wfile.write(bytes(res, "utf-8"))
            else:
                if(os.access(exe, os.X_OK)):
                    self.wfile.write(bytes("error on loading engine " + exe, "utf-8"))
                else:
                    self.wfile.write(bytes(f"file {exe} is not executable", "utf-8"))



class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


def run(port=8385):
    server = ThreadingSimpleServer(('0.0.0.0', port), Handler)
    print(f"\nopen http://127.0.0.1:{port}\n")
    server.serve_forever()


if __name__ == "__main__":
    run()
