
chess-engine-eval-debugger
======
<img src="http://cinnamonchess.altervista.org/web_evaluate.gif">

#### Version
v0.1-alpha

## Run local server
`./json.server.py`  
  
## Open web page  
  
[http://127.0.0.1:8080/index.html](http://127.0.0.1:8080/index.html)
or
[http://127.0.0.1:8080/index.html?exe1=stockfish&exe2=crafty&proto1=uci&proto2=xboard&eval1=eval&eval2=score&rem1=0&rem2=4](http://127.0.0.1:8080/index.html?exe1=stockfish&exe2=crafty&proto1=uci&proto2=xboard&eval1=eval&eval2=score&rem1=0&rem2=4)


## Debbugging engine

1. Select one or two engine (exe)
2. Select eval command, for example for stockfish is eval, for crafty is score
3. Select protocol (uci or xboard)
4. Set pieces on chessboard, automatically the evaluate will appear below

### Use your engine
the two commands will be send to **UCI** engine
`position fen <fen>`  
`<eval command>`  

example for stockfish:
`position fen rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR w KQkq - 0 1`
`eval`

the two commands will be send to **XBOARD** engine
`position fen <fen>`  
`<eval command>`  

example for crafty:
`setboard rnbqkbnr/pppppppp/8/8/8/6P1/PPPPPP1P/RNBQKBNR w KQkq - 0 1`
`score`

so your engine have to manage the command `<eval command>` 

  
### Requirement
Python 2

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
