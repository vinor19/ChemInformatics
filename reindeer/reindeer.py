s = "SAAAEBBBT"
t = "TAAAEBBBS"
g = graphDFS("".join("[%s]" % a for a in s))
g.print()
goal = graphDFS("".join("[%s]" % a for a in t))
goal.print()

aJump = ruleGMLString("""rule [
	ruleID "A Jump"
	context [
		node [ id 2 label "B"]
		edge [ source 1 target 2 label "-"]
		edge [ source 2 target 3 label "-"]
	]
	left [
		node [ id 1 label "A"]
		node [ id 3 label "E"]
	]
	right [
		node [  id 1 label "E"]
		node [  id 3 label "A"]
	]
]""")
bJump = ruleGMLString("""rule [
	ruleID "B Jump"
	context [
		node [ id 2 label "A"]
		edge [ source 1 target 2 label "-"]
		edge [ source 2 target 3 label "-"]
	]
	left [
		node [ id 1 label "E"]
		node [ id 3 label "B"]
	]
	right [
		node [ id 1 label "B"]
		node [ id 3 label "E"]
	]
]""")
aMove = ruleGMLString("""rule [
	ruleID "A Move"
	context[
		edge [ source 1 target 2 label "-"]
	]
	left [
		node [ id 1 label "A"]
		node [ id 2 label "E"]
	]
	right [
		node [ id 1 label "E"]
		node [ id 2 label "A"]
	]
]""")
bMove = ruleGMLString("""rule [
	ruleID "B Move"
	context[
		edge [source 1 target 2 label "-"]
	]
	left [
		node [ id 1 label "E"]
		node [ id 2 label "B"]
	]
	right [
		node [ id 1 label "B"]
		node [ id 2 label "E"]
	]
]""")
for a in inputRules: a.print()

dg = DG(graphDatabase=inputGraphs)
dg.build().execute(addSubset(g) >> repeat(inputRules))

p = DGPrinter()
p.graphvizPrefix=' layout = "dot"; '

def setPrinter(p):
	p.withRuleName = True
	p.pushVertexColour(lambda a: "blue" if a.graph == g else "")
	p.pushVertexColour(lambda a: "red" if a.graph == goal else "")
setPrinter(p)
dg.print(p)

# The following is a rather brutal sledgehammer-approach.
#
# You could also use, e.g., networkx to find a shortest path
# in the derivation graph, as the derivation graph is very
# likely a directed graph (i.e., not a hyper.graph)
flow = Flow(dg)
flow.addSource(g)
flow.addSink(goal)
flow.addConstraint(inFlow(g) == 1)
flow.setSolverEnumerateBy(absGap=0)
flow.calc()
fp = FlowPrinter()
setPrinter(fp.dgPrinter)
for s in flow.solutions:
	s.print(fp)