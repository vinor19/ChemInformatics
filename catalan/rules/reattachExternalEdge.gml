rule [
	ruleID "Attatch Rs edges to A"
	context [
		node [ id 1 label "A" ]
		node [ id 2 label "R" ]
		node [ id 3 label "0" ]
		edge [ source 1 target 2 label "-" ]
	]
	left [
		edge [ source 2 target 3 label "-" ]
	]
	right [
		edge [ source 1 target 3 label "-" ]
	]
]