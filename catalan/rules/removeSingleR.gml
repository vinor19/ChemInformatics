rule [
	ruleID "Remove a single R node"
	context [
		node [id 1 label "A"]
	]
	left [
		node [id 2 label "R"]
		edge [source 1 target 2 label "-"]
	]
	right [
	]
]
