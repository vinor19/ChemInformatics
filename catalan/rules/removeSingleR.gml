rule [
	ruleID "Remove R nodes"
	context [
		node [id 1 label "A"]
	]
	left [
		node [id 2 label "R"]
		node [id 3 label "R"]
		node [id 4 label "R"]
		edge [source 1 target 2 label "-"]
		edge [source 1 target 3 label "-"]
		edge [source 1 target 4 label "-"]
	]
	right [
	]
]
