import pickle

import dgl


def load_pickel(filename: str):
    with open(filename, 'rb') as file:
        obj = pickle.load(file)
        print('Load pickle ({})'.format(filename))
        return obj


if __name__ == "__main__":
    graph1 = load_pickel("graph1.pkl")
    graph2 = load_pickel("graph2.pkl")
    print(graph1)
    print(graph2)

    batch_graph = dgl.batch([graph1,graph2])
    print(batch_graph)

