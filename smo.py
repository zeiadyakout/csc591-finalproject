from itertools import chain
from SMO.data import DATA
from datetime import datetime
from SMO.row import ROW
import SMO.eg as eg
import random
import SMO.stats as stats


def std(data):
    sum = 0
    mid = data.mid().d2h(data)
    for i in data.rows:
        sum += (i.d2h(data) - mid) ** 2
    return (sum / len(data.rows)) ** .5



def part1(filename, seed, repeats):
    random.seed(seed)
    data = DATA(filename)
    # something ova here
    print("date :", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("file :", filename)
    print("repeats  :", repeats)
    print("seed :", seed)
    print("rows :", len(data.rows))
    print("cols :", len(data.cols.all))

    print("{:<30} {:<50} {:>23}".format("names", "{:<3}".format(str(data.cols.names).replace(',', '    ')), "D2h-"))

    print(f"{'mid':<30} [", end="")
    for cell in data.mid().cells:
        print(f"{cell:<13.2f}", end="")
    print(f"]     {data.mid().d2h(data):.2f}")
    
    print(f"{'div':<30} [", end="")
    for cell in data.div().cells:
        print(f"{cell:<13.2f}", end="")
    print(f"]     {std(data):.2f}")

    print("#")

    for i in range(repeats):
        stats, bests = data.gate(budget0=4, budget=9, some=0.5)
        best = bests[-1]
        print(f"{'smo9':<30} [", end="")
        for cell in best.cells:
            print(f"{cell:<13}", end="")
        print(f"]     {best.d2h(data):.2f}") 

    print("#")

    for i in range(repeats):
        selectRows = random.sample(data.rows, 50)
        minRow = min(selectRows, key=lambda row:row.d2h(data))

        print(f"{'any50':<30} [", end="")
        for cell in minRow.cells:
            print(f"{cell:<13}", end="")
        print(f"]     {minRow.d2h(data):.2f}")
    
    print("#")

    globalMin = min(data.rows, key=lambda row: row.d2h(data))
    print(f"{'100%':<30} [", end="")
    for cell in globalMin.cells:
        print(f"{cell:<13}", end="")
    print(f"]     {globalMin.d2h(data):.2f}")


def part2(filename, seed, repeats):
    random.seed(seed)
    data = DATA(filename)

    print("date :", datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
    print("file :", filename)
    print("repeats  :", repeats)
    print("seed :", seed)
    print("rows :", len(data.rows))
    print("cols :", len(data.cols.all))
    print("best :", round(min(data.rows, key=lambda row: row.d2h(data)).d2h(data), 2))
    print("tiny: ", round(std(data) * 0.35,2))

    print("#base", end =" ")
    #base
    base_d2h = [x.d2h(data) for x in data.rows]
    # sample = stats.SAMPLE(base_d2h)
    # print(sample.bar(sample))
    print("#bonr9", end =" ")
    #bonr9
    bonr9_d2h = [x.d2h(data) for x in chain.from_iterable(data.gate(4, 5, 0.5))]

    print("#rand9", end =" ")
    #rand9
    rand9_d2h = []
    for i in range(9):
        orig = data.rows
        data.rows = random.sample(data.rows, int(len(data.rows) * 0.1))
        rand9_d2h.append(min([x.d2h(data) for x in data.rows]))
        data.rows = orig
    print("#bonr15", end =" ")
    #bonr15
    bonr15_d2h = [x.d2h(data) for x in chain.from_iterable(data.gate(4, 11, 0.5))]
    print("#rand15", end =" ")
    #rand15
    rand15_d2h = []
    for i in range(15):
        orig = data.rows
        data.rows = random.sample(data.rows, int(len(data.rows) * 0.1))
        rand15_d2h.append(min([x.d2h(data) for x in data.rows]))
        data.rows = orig
    print("#bonr20", end =" ")
    #bonr20
    bonr20_d2h = [x.d2h(data) for x in chain.from_iterable(data.gate(4, 16, 0.5))]
    print("#rand20", end =" ")
    #rand20
    rand20_d2h = []
    for i in range(20):
        orig = data.rows
        data.rows = random.sample(data.rows, int(len(data.rows) * 0.1))
        rand20_d2h.append(min([x.d2h(data) for x in data.rows]))
        data.rows = orig
    print("#rand358", end =" ")
    #rand358
    rand358_d2h = []
    for i in range(358):
        orig = data.rows
        data.rows = random.sample(data.rows, int(len(data.rows) * 0.1))
        rand358_d2h.append(min([x.d2h(data) for x in data.rows]))
        data.rows = orig
    # putting in stat samples
    samples = [stats.SAMPLE(base_d2h, "base"),
               stats.SAMPLE(bonr9_d2h, "#bonr9"),
               stats.SAMPLE(rand9_d2h, "#rand9"),
               stats.SAMPLE(bonr15_d2h, "#bonr15"),
               stats.SAMPLE(rand15_d2h, "#rand15"),
               stats.SAMPLE(bonr20_d2h, "#bonr20"),
               stats.SAMPLE(rand20_d2h, "#rand20"),
               stats.SAMPLE(rand358_d2h, "#rand358")]
    
    # output stuff
    print("#report8")
    stats.eg0(samples)
# kmeans
# paths = ["clusteredData\kmeans\pom3d\kmeans_pom3d0.csv", "clusteredData\kmeans\pom3d\kmeans_pom3d1.csv", "clusteredData\kmeans\pom3d\kmeans_pom3d2.csv"]
# gaussmix
# paths = ["clusteredData\gaussmix\pom3d\gaussmix_pom3d0.csv", "clusteredData\gaussmix\pom3d\gaussmix_pom3d1.csv", "clusteredData\gaussmix\pom3d\gaussmix_pom3d2.csv"]
# kmedoids
paths = ["clusteredData\kmedoids\pom3d\kmedoids_pom3d0.csv", "clusteredData\kmedoids\pom3d\kmedoids_pom3d1.csv", "clusteredData\kmedoids\pom3d\kmedoids_pom3d2.csv"]
for idx, path in enumerate(paths):
    print("Part", idx + 1)
    part1(path, 31210, 20)
    part2(path, 31210, 20)
    print()

# filename = "data/wineQuality/wineQuality.csv"
# repeats = 20
# seed = 31210
# part1(filename, seed, repeats)
# part2(filename, seed, repeats)