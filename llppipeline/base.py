import igraph


class Pipeline:

    def __init__(self):
        self.modules = []
        self.targets = set()

    def register_module(self, module):
        self.modules.append(module)
        self.targets = self.targets.union(module.prerequisites())
        self.targets = self.targets.union(module.targets())

    def make(self, targets):
        # build dependency graph
        graph = igraph.Graph(directed=True)

        for target in self.targets:
            graph.add_vertex(target=target)

        for module in self.modules:
            graph.add_vertex(module=module)
            v = graph.vs[graph.vcount()-1]
            for prereq in module.prerequisites():
                p = graph.vs.find(target=prereq)
                graph.add_edge(p, v)
            for target in module.targets():
                t = graph.vs.find(target=target)
                graph.add_edge(v, t)

        # compute relevant subgraph
        required_nodes = set()
        for t in targets:
            try:
                v = graph.vs.find(target=t)
            except ValueError as e:
                raise ValueError("Could not find module to make target %s" % t) from e

            required_nodes = required_nodes.union(set(graph.bfs(v.index, mode=igraph.IN)[0]))

        subgraph = graph.vs[required_nodes].subgraph()

        # compute evaluation order, e.g. topological sorting
        evaluation = subgraph.vs[subgraph.topological_sorting()]

        print('Evaluation order:')
        for node in evaluation:
            if not node['module']:
                continue
            print('\t' + str(node['module']))
        print()


        results = {}
        for node in evaluation:
            if not node['module']:
                continue

            module = node['module']
            print('Evaluating ' + str(module))
            prerequisites = {key:results[key] for key in module.prerequisites()}
            targets_data = module.make(prerequisites)
            results.update(targets_data)

        return {key:results[key] for key in targets}


class PipelineModule:

    def targets(self):
        raise NotImplementedError

    def prerequisites(self):
        raise NotImplementedError

    def make(self, prerequisite_data):
        raise NotImplementedError
