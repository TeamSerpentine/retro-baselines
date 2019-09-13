# retro_baselines
Machine Learning and Artificial Intelligence baseline algorithms applied to remastered retro games.

## Installation instructions
The repository is built for Python 3.7. Take a look at the requirements file for code dependencies.

For Windows the gym environment does not always work properly. A possible alternative for this is:

```
pip install --no-index -f https://github.com/Kojoley/atari-py/releases atari_py
```
## Repository management
When developing:
1. Define a feature that you would like to add. 
2. Branch off of a _dev/_ branch with the appropriate prefix. Examples are 
_feature/_, _bugfix/_ or _test/_.
3. When done with developing and testing a feature, request a pull from the branch into the _dev/_
branch. One review is needed. Please make sure to add unit tests and secure proper commit history.
4. Edit until satisfactory and let the reviewer approve the pull request.
5. Celebrate and start over with a new feature.

## Games
All games provided by the OpenAI Gym installation are available for experimentation. Additionally 
a custom snake game also exists in this repository.

## Playing a game
Run the _insertcoin.py_ script with default values through the command line as follows:
```
python insertcoin.py
```

For a list of options, type the following command:
```
python insertcoin.py --help
``` 

Games can be set, and you can choose which model you would like to run. An example of running a random 
model on the default game:
```
python insertcoin.py -m random_model
```
This runs the default game while choosing random actions available from the action space.

In order to run snake and render it you can also run it from the command prompt.
```
python insertcoin.py -g snake -r
```