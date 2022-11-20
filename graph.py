import math


class Edge:
	def __init__(self, source, target, weight):
		self.source = source
		self.target = target
		self.weight = weight


class Graph:
	def __init__(self, edges=None):
		if edges is None:
			edges = []
		self.edges = edges

	def add_edge(self, edge):
		self.edges.append(edge)

	def get_vertices(self):
		vertices = set()
		for edge in self.edges:
			vertices.add(edge.source)
			vertices.add(edge.target)
		return vertices

	def widest_path(self, src, dst):
		vertices = self.get_vertices()
		visited = {v: False for v in vertices}
		weights = {v: -math.inf for v in vertices}
		weights[src] = math.inf
		paths = {v: (v,) for v in vertices}

		queue = [src]
		while queue:
			current = queue.pop(0)
			if visited[current]:
				continue

			for e in self.edges:
				if e.target == current:
					neighbour = e.source
				elif e.source == current:
					neighbour = e.target
				else:
					continue
				queue.append(neighbour)
				w = min(weights[current], e.weight)
				if weights[neighbour] < w:
					visited[neighbour] = False
					weights[neighbour] = w

					current_path = list(paths[current])
					current_path.append(neighbour)
					paths[neighbour] = tuple(current_path)
			visited[current] = True
		return Path(paths[dst], weights[dst])

	def use_path(self, path):
		vertices = path.path
		for i in range(len(vertices) - 1):
			for e in self.edges:
				if (e.source == vertices[i] and e.target == vertices[i + 1]) or (e.source == vertices[i + 1] and e.target == vertices[i]):
					e.weight = e.weight - path.weight

	def copy(self):
		return Graph([Edge(e.source, e.target, e.weight) for e in self.edges])


class Path:
	def __init__(self, path, weight):
		self.path = path
		self.weight = weight

	def __repr__(self):
		return f"Path(path={self.path},weight={self.weight})"


class NetworkConfiguration:
	def __init__(self, paths):
		self.paths = paths

	def sum_weight(self):
		avg = 0
		for path in self.paths:
			avg = avg + path.weight
		return avg


class NetworkOptimizer:
	def __init__(self, graph, streams):
		self.graph = graph
		self.streams = streams

	def permutation(self):
		n = len(self.streams)
		result = []
		x = [0] * n

		while x:
			if x[len(x)-1] < n:
				while len(x) < n:
					x.append(0)
			else:
				x.pop()
			if len(x) == 0:
				break
			elif len(set(x)) == n:
				result.append([self.streams[i] for i in x])

			x[len(x) - 1] = x[len(x) - 1] + 1
		return result

	def optimize(self):
		configurations = []
		for configuration in self.permutation():
			paths = []
			g = self.graph.copy()
			for hosts in configuration:
				path = g.widest_path(hosts[0], hosts[1])
				g.use_path(path)
				paths.append(path)
			configurations.append(NetworkConfiguration(paths))
		return sorted(configurations, key=lambda item: item.sum_weight(), reverse=True)[0]
