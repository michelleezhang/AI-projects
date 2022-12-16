# Search
Notes:
The A\* function will be given two routing maps as inputs. 
The first map specifies the straight-line distance between two landmarks -- this is the **distance map**.
The second map is based on the data from the Archive traffic survey. It specifies the expected time it takes a driver to go from one landmark to a neigbhoring landmark; this is the **time map**. 

For all three implementations (BFS, DFS, and A\*), we use the time differences between places as the main metric, not distance. However, for A\*, we use the distances between places as the **heuristic** (how far you are from the destination). In other words, for A\*, the distance from the start to your current location will be time-based, but the distance from your current location to the destination will be distance-based.

With A\*, if two or more nodes have the same f(n), we use h(n) to break the tie, i.e., pick the node that has the smallest h(n). If two or more nodes have the same h(n), then pick the node that entered the open list first when returned/yielded by expand().

When passed to your A\* implementation, both the distance map and the time map are stored in the same format (a Python dictionary). The following is an example time map.

```python
Time_map = {
'Campus':
	{'Campus':None,'Whole_Food':4,'Beach':3,'Cinema':None,'Lighthouse':1,'Ryan Field':None,'YWCA':None},
'Whole_Food':
	{'Campus':4,'Whole_Food':None,'Beach':4,'Cinema':3,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Beach':
	{'Campus':4,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':None},
'Cinema':
	{'Campus':None,'Whole_Food':4,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':None,'YWCA':2},
'Lighthouse':
	{'Campus':1,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':None,'Ryan Field':1,'YWCA':None},
'Ryan Field':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':None,'Lighthouse':2,'Ryan Field':None,'YWCA':5},
'YWCA':
	{'Campus':None,'Whole_Food':None,'Beach':None,'Cinema':3,'Lighthouse':None,'Ryan Field':5,'YWCA':None}}
```

In this example, the traffic time between Campus and Beach is `3`. `None` indicates that there is no road which directly connects the two landmarks. Off-road driving is prohibited by local law, so drivers must only take the roads marked on the diagram above. Combining this legal requirement and with the volatile traffic pattern of Heavanston, it is certain that the distance map can only be used as a heuristic for the A\* algorithm. It is also noteworthy that the time it takes traveling on the two sides of the same road is most likely different. 