Python version of [zevv/lsofgraph](https://github.com/zevv/lsofgraph)

A small utility to convert Unix `lsof` output to a graph showing FIFO and UNIX interprocess communication.

Generate graph:

````shell
sudo lsof -n -F | python lsofgraph.py | dot -Tjpg > /tmp/a.jpg
    OR
sudo lsof -n -F | python lsofgraph.py | dot -T svg > /tmp/a.svg
````
or add `unflatten` to the chain for a better layout:

````shell
sudo lsof -n -F | python lsofgraph.py | unflatten -l 1 -c 6 | dot -T jpg > /tmp/a.jpg
    OR
sudo lsof -n -F | python lsofgraph.py | unflatten -l 1 -c 6 | dot -T svg > /tmp/a.svg
````
Note: In cases of handling large datasets, you might encounter a "maximum recursion depth exceeded" error. To work around this, you can increase the recursion limit in your Python environment by adding `sys.setrecursionlimit(15000)` in the `lsofgraph.py` script.

![example output](/example.jpg)

# Install and use on MacOS

Graphviz contains utilities dot and unflatten
````shell
brew install Graphviz
git clone https://github.com/akme/lsofgraph-python.git
cd lsofgraph-python
lsof -n -F | python lsofgraph.py | unflatten -l 1 -c 6 | dot -T jpg > /tmp/a.jpg && open /tmp/a.jpg
lsof -n -F | python lsofgraph.py | unflatten -l 1 -c 6 | dot -T svg > /tmp/a.jpg && open -a Safari.app '/tmp/a.svg'
````
