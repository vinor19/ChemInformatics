rule [
	ruleID "Keto-enol isomerization ->"
	context [
		node [ id 1 label "H" ]
		node [ id 2 label "C" ]
		node [ id 3 label "C" ]
		node [ id 4 label "O" ]
	]
	left [
		edge [ source 1 target 2 label "-"]
		edge [ source 2 target 3 label "-"]
		edge [ source 3 target 4 label "="]
	]
	right [
		edge [ source 2 target 3 label "="]
		edge [ source 3 target 4 label "-"]
		edge [ source 1 target 4 label "-"]
	]
	constrainAdj [
		id 3
		op "="
		count 1
		nodeLabels [ label "O" ]
	]
]	
