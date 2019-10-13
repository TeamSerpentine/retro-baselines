**When developing the genetic model, the following changes were made step by step.**
1. Base run
No graph, but scores are logged in text

2. Decreased standard deviation used to 1/3 instead of 1
![plot run 2](https://i.imgur.com/TOrR3h6.png)

3. Changed mutation to add to the current values instead of overwriting them and crossover to take a sequential part of the first parent and the sequential remainder of the second (basically cutting them at only one point and then glueing them together) instead of taking a random one of the two parent's values for each value.
![plot run 3](https://i.imgur.com/IvVctqU.png)

4. Changed the board size to 21 by 16 instead of 42 by 32
![plot run 4](https://i.imgur.com/s779yAO.png)

5. Increased population size to 2000
![plot run 5](https://i.imgur.com/JZBCzWd.png)

6. Give snake 500 start lives with 250 extra per step
![plot run 6](https://i.imgur.com/UO6IG78.png)

7. Change reward from 1 per apple to 1 per step + 1000 per apple
![plot run 7](https://i.imgur.com/OjcdXJL.png)

**Tried eventually (not exactly documented):**
* Decrease model size to [x,x]: Bad results, reverted
* Make crossbred children also mutate: Tried in multiple configurations with repeated bad results: reverted
![plot cross mutate](https://i.imgur.com/wrEAilM.png)
* Add [-1, 1] clipping to the weights and biases
* Apply clipping only to the weights
* Increased population size to 20.000
![plot_population_20000](https://i.imgur.com/lsnPDCt.png)
* Run multiple games per weightset per generation to get a better average scoring per generation (and more meaningfully select actually good weightsets, not just lucky ones)
* Decrease population size to 500 & increase network to [18,18,16]

**Plots belonging to above attempts (altho order unknown)**
![plot unknown 1](https://i.imgur.com/NwsE0kH.png)
![plot unknown 2](https://i.imgur.com/O6hTa3u.png)
![plot unknown 3](https://i.imgur.com/gU9478e.png)
![plot unknown 4](https://i.imgur.com/JWMzOqH.png)
![plot unknown 5](https://i.imgur.com/CgPhSy5.png)

**Eventually we reached the following settings**
* Standard deviation for random weights generation of 1/3
* Mutation adds the generated values to the current values
* Crossover takes a sequential part of the first parent and the sequential remainder of the second (basically cutting them at only one point and then glueing them together)
* Board size 21x16
* Rewards: 1000 per apple, 1 per step lived
* Lives at start: 200 steps
* Extra lives per apple eaten: 200 steps
* Maximum buffer of lives left: 500.000
* Weights clipped to [-1,1] (but biases unclipped)
* Population size: 500
* Elite fraction: 0.05
* Crossover fraction: 0.80
* Mutation probability: 0.01
* Network: (input 32)[18,18,16](4 output) fully connected neural network
![plot_top_snake](https://i.imgur.com/lO20AfE.png)
![gif_top_snake](https://i.imgur.com/L2oQTRc.gifv)
