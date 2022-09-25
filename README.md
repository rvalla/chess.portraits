![logo](https://gitlab.com/azarte/chessportraits/-/raw/themoststable/assets/img/icon.png)

# azarte: chessboard portraits

This is the code I use to make my series of **chessboard portraits**. Some of my photography work inspired
by chess...  
The idea is to take fragments of a set of images and build a *chess board*. A *heat map* created using
a chess game moves introduce noise in some of the squares.  

![example](https://gitlab.com/azarte/chessportraits/-/raw/themoststable/assets/img/example.jpg)

## running the code

To create an image you need a set of square images and a chessgame in *pgn* format. First you need to
load your configuration in a *json* file:  

```
{
	"name": "test",
	"sq_size": 128, //the size of each square in pixels
	"size": 1024,	//the size of input images (note that 8 * sq_size = size)
	"noise": true, //you can set this to false, but that's boring
	"noise_width": 30, //maximum noise width (to change color's channels (0-255))
	"input_path": "input/img/test", //the folder with input images
	"output_path": "output/img/test", //the output folder
	"output_file": "test_1", //you need an output name
	"game_path": "input/pgn/pgn_source_00643.pgn", //path to the chessgame
	"piece_weight": "1,3,3,5,9,9" //relative pieces weight to calculate the heatmap
}
```

And then you simply run something like:  

```
from chessboard_portrait import Portrait
p = Portrait("input/test.json")
```

## standing upon the shoulders of giants

This little project is possible thanks to a lot of work done by others in the *open-source* community. Particularly in
this case I need to mention:

- [**Python**](https://www.python.org/): the programming language I used.  
- [**python-chess**](https://github.com/niklasf/python-chess): the library which helps me to process chess moves.  

Feel free to contact me by [mail](mailto:rodrigovalla@protonmail.ch) or reach me in
[telegram](https://t.me/rvalla) or [mastodon](https://fosstodon.org/@rvalla).
