from graph import Graph, Edge, NetworkOptimizer
from onos_config import OnosConfigurator


def load_graph(file):
	graph = Graph()
	with open(file, "r") as f:
		for line in f.readlines():
			elements = [el.strip() for el in line.split(',')]
			src = int(elements[0])
			dst = int(elements[1])
			bw = int(elements[2])
			graph.add_edge(Edge(src, dst, bw))
	return graph


def load_sessions(file):
	result = []
	with open(file, "r") as f:
		for line in f.readlines():
			elements = [el.strip() for el in line.split(',')]
			src = int(elements[0])
			dst = int(elements[1])
			result.append((src, dst))
	return result


def get_device_id(id):
	return f"of:{format(id, 'x').rjust(16, '0')}"


def get_host_mac(id):
	text = f"{format(id, 'x').rjust(12, '0')}"
	mac = [text[i:i+2] for i in range(0, len(text), 2)]
	return ':'.join(mac)


if __name__ == "__main__":
	configurator = OnosConfigurator("http://192.168.16.46:8181/onos/v1", ('onos', 'rocks'))
	configurator.load_flows()
	configurator.load_devices()
	configurator.load_links()

	graph = load_graph("data/links.csv")
	sessions = load_sessions('data/sessions.csv')
	optimizer = NetworkOptimizer(graph, sessions)
	for path in optimizer.optimize().paths:
		print(f"Path: {path.path}, Bandwith: {path.weight} Mbps")
		configurator.configurate(
			[get_device_id(id) for id in path.path],
			get_host_mac(path.path[0]),
			get_host_mac(path.path[-1])
		)
