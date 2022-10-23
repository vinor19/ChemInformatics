dgPrinter = DGPrinter()
dgPrinter.withGraphImages = False # be careful, the derivation graphs can become quite large
flowPrinter = FlowPrinter()
flowPrinter.printUnfiltered = False
config.io.useOpenBabelCoords = False

goal = graphDFS("[0]", "Goal")
level = graphGML(levelFile, "Start")
postSection("Loaded Graphs")
for a in inputGraphs: a.print()

include("rules.py")

postSection("Loaded Rules")
for a in inputRules: a.print()



# You have to provide a strategy and the rules. I will later (approx begin of October)
# provide a stratgey for you to use, in case you find this too challenging.

"""
Available rules (their variable names)
mark
removeInterR
reattachExternal
reattachExternal
removeR
unmark
"""
strategy = (addSubset(level) >> repeat[steps](
	mark
	>> repeat(revive(removeInterR))
	>> repeat(revive(reattachExternal))
	>> repeat(revive(removeAttached))
	>> repeat(revive(removeR))
	>> unmark
))
dg = DG(graphDatabase=[goal, level])
dg.build().execute(strategy)

dg.print(dgPrinter)
postSection("Product Graphs")
for a in dg.products: a.print() # this can take a while in the post processing

def doFlow(dg):
	flow = Flow(dg)
	# flow.objectiveFunction = FlowLinExp() # important, otherwise the default function will min. #edgesUsed which may take a long time
	flow.addSource(level)
	flow.addSink(goal)
	flow.addConstraint(inFlow[level] == 1)
	flow.findSolutions(verbosity=2)
	flow.solutions.print(flowPrinter)
doFlow(dg)

# sys.exit()

# The below code is an attempt to contract the above derivation graph
# 

postChapter("Contracted")
realStates = set([dg.findVertex(level)])
for e in dg.edges:
	assert e.numSources == 1
	assert e.numTargets == 1
	if unmark in e.rules:
		realStates.add(next(iter(e.targets)))
print("Real States finding done")

sources = {}
marked = set()
for v in dg.vertices:
	sources[v] = set()
qNext = [dg.findVertex(level)]
marked.add(dg.findVertex(level))
while len(qNext) != 0:
	print("while1 ")
	q = qNext
	qNext = []
	for v in q:
		for eOut in v.outEdges:
			vOut = next(iter(eOut.targets))
			if not (vOut in marked): 
				qNext.append(vOut)
				marked.add(vOut)
			if v in realStates:
				sources[vOut].add(v)
			else:
				sources[vOut] |= sources[v]


dgContracted = DG()
with dgContracted.build() as b:
	for v in realStates:
		for s in sources[v]:
			d = Derivation()
			d.left.append(s.graph)
			d.right.append(v.graph)
			b.addDerivation(d)
dgContracted.print(dgPrinter)
doFlow(dgContracted)
