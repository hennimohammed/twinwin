import sys


def read_file(filename=None):
    '''Parses file into list of edges 

    Arges: 
        filename (str): file name, None for stdin

    Returns:
        n (int): number of vertices
        m (int): number of edges
        edges (list): list of edges, each edge of the form (int, int)
    '''

    file = sys.stdin if filename is None else open(filename)

    lines = file.readlines()

    #filter comment lines
    filtered_lines = list(filter(lambda line: not line.lower().startswith('c'), lines))

    #first line
    _, _, n, m = filtered_lines.pop(0).split()

    n, m = int(n), int(m)

    if len(filtered_lines) != m:
        print(f"ERROR reading input, m={m} but {len(filtered_lines)} non-comment lines found.")
        exit()

    edges = [tuple(map(int, line.split())) for line in filtered_lines]

    if filename is not None:
        file.close()

    return n, m, edges