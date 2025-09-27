import random, os


# function to be called everytime the fame loads

def generante_map_file(width, height, filename="assets/map.txt"):
    lines = []
    for y in range(height):
        row = []
        for x in range(width):
            my_list = ['a','b','n']
            weights = [20,20,60]
            tile = random.choices(my_list, weights=weights, k=1)[0]
            row.append(tile)
        lines.append(";".join(row))
    
    with open(filename, "w") as f:
        f.write("\n".join(lines))


# generante_map_file(4,4)

     
 

                        
    