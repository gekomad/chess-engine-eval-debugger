
chess-engine-eval-debugger
======
<img src="https://raw.githubusercontent.com/gekomad/chess-engine-eval-debugger/site/img/img.gif">

#### Version
v.1.0

## Run local web server


`server.py`

## Open web page

[http://127.0.0.1:8385](http://127.0.0.1:8385)

or with bookmarks

ht<span>tp</span>://127.0.0.1:8385/?exe1=c:\path\engine1.exe&proto1=uci&eval1=score&exe2=Stockfish&proto2=uci&eval2=eval&regex2=.*Total evaluation:.* (.*) \(.*&exe3=Crafty&proto3=xboard&eval3=score&regex3=.*total..........(.*).*


### Debbugging engine

1. Set one or more engines.
2. Set eval command, example stockfish uses **eval**, crafty uses **score**.
3. Set pieces on chessboard and automatically the evaluate value will appear below.
4. Can generate random positions.
5. Passing a list of `fen string`, can generate a `csv file` with score.

### How it works

These commands will be send to **UCI** engine
```
position fen <fen>
<eval command>
quit
```

these commands will be send to **XBOARD** engine

```
position fen <fen>
<eval command>
quit
```
and the stdout will be show in text area


### Use your engine

Engines (uci or xboard) have to manage the command `<eval command>` to print information, Stockfish uses `eval`, Crafty uses `score`

### Requirements
Python 3

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
