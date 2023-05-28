# frozen-lake

## An implementation of the Frozen Lake game and application of Genetic Algorithms to learn and solve it

### Play Modes
The game is designed to be played by a human or by an automatic agent
- For Human, it works with the keyboard arrows
- For an agent, with a list of inputs. E.g: ["u", "d", "l", "r"]

The Genetic Algorithms are based on the GeneticAlgorithm Base Class. 
- Subsequently, we implement three different versions. Using Elitism, FPS, and Tournament Selection. Being the last notoriously more efficient. 
Results for a sample of 1000 games
![image](https://github.com/lucarso120/frozen-lake/assets/45951783/eb02ce2e-21e4-4424-b3fb-2288838a956f)
