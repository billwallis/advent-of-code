class Node:
    def __init__(self, name: str):
        self.name = name
        self.from_nodes: list[Node] = []
        self.to_nodes: list[Node] = []

    def __str__(self):
        return f"'{self.name}'"

    def __repr__(self):
        return self.__str__()


class Nodes:
    def __init__(self):
        self.nodes: list[Node] = []

    def __iter__(self):
        yield from self.nodes

    def __getitem__(self, item: str | Node):
        name = item.name if isinstance(item, Node) else item
        for node in self.nodes:
            if node.name == name:
                return node
        raise ValueError(f"Node '{name}' not found")

    def append(self, item: Node):
        self.nodes.append(item)


class Edge:
    def __init__(self, node_from: Node, node_to: Node):
        self.node_from = node_from
        self.node_to = node_to


class Graph:
    def __init__(self):
        self.nodes: Nodes = Nodes()
        self.edges: list[Edge] = []

    def add_node(self, node: Node):
        self.nodes.append(node)

    def add_edge(self, edge: Edge):
        self.edges.append(edge)
        self.nodes[edge.node_from].to_nodes.append(edge.node_to)
        self.nodes[edge.node_to].from_nodes.append(edge.node_from)


def main() -> None:
    graph = Graph()
    node_a = Node("AA")
    node_b = Node("BB")
    node_c = Node("CC")
    graph.add_node(node_a)
    graph.add_node(node_b)
    graph.add_node(node_c)
    graph.add_edge(Edge(node_a, node_b))
    graph.add_edge(Edge(node_b, node_c))
    graph.add_edge(Edge(node_c, node_a))

    for node in graph.nodes:
        print(node, node.from_nodes, node.to_nodes)
