# sets-card-game
Implementation of the [game sets](https://www.setgame.com/file/set-english). Doesn't quite follow the rules as laid out but works ok. May blow up in the rare case where you have 15 cards on the table and still no sets.

Only been tested with python3.7  May work with lower versions of python3.x but probably will not work with python2.

To setup/run, clone/dowload this repo. cd to sets-card-game directory.  
`virtualenv venv -p python3.7`  
You may need to put a more complete path to the python binary. If virtualenv is not installed you unchecked a box somewhere while installing python.

Activate the virtualenv you just created.  
On windows:  
`venv\Scripts\activate`  
On not windows:  
`source venv/bin/activate`  
Prompt should now be prepended with (venv) while virtualenv is active.

Install required modules  
`pip install -r requirements.txt`

To play, be sure virtualenv is active, then run:  
`python game.py`  
You can also pass the argument `mute` to silence the ding sound effect.
