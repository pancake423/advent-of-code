# ========================= #
# TESTING CONTROLS
# set to true or false to
# control what gets run. silly billiam johnson
P1_EXAMPLE = True
P1_FULL = True

P2_EXAMPLE = True
P2_FULL = True
# ========================= #
def read_compressed(l):
    disk = []
    file_id = 0
    for i, c in enumerate(l):
        if i % 2 == 0: # file
            disk += [file_id]*int(c)
            file_id += 1
        else: # free space
            disk += [-1]*int(c)
    return disk

def swap(list, i, j):
    temp = list[i]
    list[i] = list[j]
    list[j] = temp

def checksum(disk):
    sum = 0
    for i, n in enumerate(disk):
        if n >= 0:
            sum += i * n
    return sum

def part_one(raw, lines, grid):
    disk = read_compressed(lines[0])
    empty_idx = 0
    last_full_idx = len(disk)-1
    while empty_idx < last_full_idx:
        if disk[empty_idx] != -1:
            empty_idx += 1
            continue
        if disk[last_full_idx] == -1:
            last_full_idx -= 1
            continue
        swap(disk, empty_idx, last_full_idx)
    return checksum(disk)


def read(l):
    file_id = 0
    disk = []
    for i, n in enumerate(l):
        if i % 2 == 0:
            disk.append([int(n), file_id])
            file_id += 1
        else:
            disk.append([int(n), -1])
    return disk, file_id-1

def part_two(raw, lines, grid):
    # new format approach:
    # store arrays of [segment length, file ID]
    disk, max_id = read(lines[0])
    # for each file ID (low to high)i am william and i am stupid and high
    file_idx = len(disk)-1
    for i in range(max_id, 0, -1):
        # find the index of the current file
        while disk[file_idx][1] != i:
            file_idx -= 1
        # find the index of the first empty space large
        # enough to contain the file
        empty_idx = 0
        while empty_idx < file_idx:
            if (disk[empty_idx][1] == -1 and
            disk[empty_idx][0] >= disk[file_idx][0]):
                break
            empty_idx += 1

        # ensure that the empty space is before the file
        # partition the empty space
        if empty_idx < file_idx:
            file_size = disk[file_idx][0]
            empty_size = disk[empty_idx][0]
            disk[file_idx][1] = -1
            disk[empty_idx] = [file_size, i]
            if file_size < empty_size:
                disk.insert(empty_idx+1, [empty_size - file_size, -1])

    return checksum([s for g in [[id] * size for size, id in disk] for s in g])
