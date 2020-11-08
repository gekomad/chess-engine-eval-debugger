
chess-engine-eval-debugger
======
<img src="http://cinnamonchess.altervista.org/web_evaluate4.gif">

#### Version
v.0.3

## Run local server

`server_python2.py`

or

`server_python3.py`

## Open web page

[http://127.0.0.1:8080/index.html](http://127.0.0.1:8080/index.html)

or

[http://127.0.0.1:8080/index.html?exe1=c:\path\engine1.exe&proto1=uci&eval1=score&exe2=c:\path\engine2.exe&proto2=uci&eval2=score&exe3=c:\path\engine3.exe&proto3=xboard&eval3=eval&exe4=c:\path\engine4.exe&proto4=uci&eval4=score](http://127.0.0.1:8080/index.html?exe1=c:\path\engine1.exe&proto1=uci&eval1=score&exe2=c:\path\engine2.exe&proto2=uci&eval2=score&exe3=c:\path\engine3.exe&proto3=xboard&eval3=eval&exe4=c:\path\engine4.exe&proto4=uci&eval4=score)


### Debbugging engine

1. Set one or more engines
2. Set eval command, example stockfish 8 uses **eval**, crafty uses **score**
3. Select protocol (uci or xboard)
4. Set pieces on chessboard and automatically the evaluate value will appear below.

### How it works

These commands will be send to **UCI** engine
```
position fen <fen>
<eval command>
quit
```

and the stdout will be show in text area

example for stockfish:
```
position fen rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR w KQkq - 0 1
eval
quit
```
these commands will be send to **XBOARD** engine

```
position fen <fen>
<eval command>
quit
```

example for crafty:
```
setboard rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR w KQkq - 0 1
score
quit
```

### Use your engine

Engines (uci or xboard) have to manage the command `<eval command>` to print eval information

### Requirements
Python (2 or 3)

## Bugs and Feedback
For bugs, questions and discussions please use [Github Issues](https://github.com/gekomad/chess-engine-eval-debugger/issues).

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance
with the License. You may obtain a copy of the License at

[http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an
"AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.


## Special thanks to

[https://chessboardjs.com](https://chessboardjs.com)
