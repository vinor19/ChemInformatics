include("grammar.py")

flowPrinter = FlowPrinter()
flowPrinter.printUnfiltered = False

postSection("Loaded Graphs")
for a in inputGraphs: a.print()
postSection("Loaded Rules")
for a in inputRules: a.print()

dg = DG(graphDatabase=inputGraphs)
dg.build().execute(
	addSubset(inputGraphs)
	>> rightPredicate[
		lambda d: all(g.vLabelCount("C") <= 5 for g in d.right)
	](
		repeat(inputRules)
	)
)
dg.print()
postSection("Product Graphs")
for a in dg.products: a.print()

flowAutocata = Flow(dg)
flowAutocata.overallAutocatalysis.enable()
for a in {formaldehyde, glycolaldehyde}: flowAutocata.addSource(a)
flowAutocata.addSink(glycolaldehyde)
flowAutocata.findSolutions()
flowAutocata.solutions.list()
flowAutocata.solutions.print(flowPrinter)


sys.exit(0)

rc = rcEvaluator(inputRules)
for dRef in dg.derivations:
	der = dRef.derivation
	educt = rcId(der.left[0])
	for i in range(1, len(der.left)):
		educt = educt *rcParallel* rcId(der.left[i])
	product = rcId(der.right[0])
	for i in range(1, len(der.right)):
		product = product *rcParallel* rcId(der.right[i])
	rcExp = educt *rcSuper(allowPartial=False)* der.rule *rcSuper(allowPartial=False)* product
	res = rc.eval(rcExp)
	dRef.print()
	for a in res:
		a.print()
		a.printGML()