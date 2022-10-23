include("grammar.py")


randmols=[smiles("OCC(O)C(C(O)CO)=O", "random1"),
		  smiles("OCC(O)C(O)C(CO)=O", "random2"),
		  smiles("OCC(O)C(O)=C(O)CO", "random3"),
		  smiles("OCC(O)C(O)C(O)=CO", "random4"),
		  smiles("OCC(O)C(O)C(O)C=O", "random5"),
		  smiles("OCC(O)(CO)C(O)C=O", "random6"),
		  smiles("OCC(O)(CO)C(O)=CO", "random7"),
		  smiles("OCC(C(O)(CO)CO)=O", "random8")]

randmols=[smiles("OCC(O)C(O)C=O"),
		  smiles("OCC(O)C(O)=CO"),
		  smiles("OCC(O)C(CO)=O"),
		  smiles("OCC(O)=C(O)CO")]


flowPrinter = FlowPrinter()
flowPrinter.printUnfiltered = False

postSection("Loaded Graphs")
for a in inputGraphs: a.print()
postSection("Loaded Rules")
for a in inputRules: a.print()

dg = DG(graphDatabase=inputGraphs)
dg.build().execute(
	addSubset(inputGraphs)
	>> leftPredicate[
		lambda d: not all(g.vLabelCount("C") == 2 for g in d.left)
	](
		rightPredicate[
			lambda d: all(g.vLabelCount("C") <= 7 for g in d.right) and all(g.vLabelCount("C") >= 2 for g in d.right)
		](
			repeat(inputRules)
		)
	)
)
dg.print()
postSection("Product Graphs")
print("Products")
for a in dg.products:
	if a.smiles.count("C") == 4:
		print(a.smiles)


# look for autocatalysis
for randmol in randmols:
	postSection("Trying "+randmol.smiles)
	flowAutocata = Flow(dg)
	flowAutocata.overallAutocatalysis.enable()
	for a in {glycolaldehyde,  randmol}: flowAutocata.addSource(a)
	flowAutocata.addSink(randmol)
	# TODO: remove the enumeration at some point
	# this is to make sure the old and new enumeration give the same results.
	# There are only a few solutions, so it's reasonably fast.
	flowAutocata.absGap = 0
	flowAutocata.findSolutions(maxNumSolutions=1337)
	flowAutocata.solutions.list()
	flowAutocata.solutions.print(flowPrinter)


# look for a pathway
for randmol in randmols:
	flow = Flow(dg)
	flow.addSource(glycolaldehyde)
	flow.addConstraint(inFlow[glycolaldehyde] == 2 )
	flow.addSink(randmol)
	flow.addConstraint(outFlow[randmol] >= 1)
	flow.objectiveFunction = -outFlow[randmol]
	for v in dg.vertices: flow.addSink(v.graph)
	# There are way too many optimal soltuions to compare old and new.
	config.flow.doSolutionAsserts = False
	flow.findSolutions()
	config.flow.doSolutionAsserts = True
	flow.solutions.list()
	flowPrinter = FlowPrinter()
	flowPrinter.printUnfiltered = False
	flow.solutions.print()
