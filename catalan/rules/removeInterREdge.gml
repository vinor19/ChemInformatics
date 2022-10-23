rule [
	ruleID "Remove inter R edges"
	context [
		node [ id 1 label "R"]
		node [ id 2 label "R"]
	]
	left [
		edge [source 1 target 2 label "-"]
	]
	right [
	]		
]