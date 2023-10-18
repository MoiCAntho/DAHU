from giacpy import *
print(chromatic_number(graph('"petersen"')) == 3)
print(graph_automorphisms(cycle_graph(3)) == 'list[list[[1,2]],list[[0,1]]]')
print(canonical_labeling(path_graph(3)) == [0,2,1])
print(is_isomorphic(graph(trail(1,2,3,4,5,6,1,5)),graph(trail(1,2,3,4,5,6,1,3))))
