#!/bin/bash

i=1
grep E\ [0-9] levels.txt | while read level; do
	echo "Level $i"
	file="level_$i.gml"
	nodes=( $(echo $level | sed "s/.*|//") )
	numNodes=${#nodes[@]}

	echo "graph [" > $file
	let n=numNodes-1
	for j in $(seq 0 $n); do
		echo -e "\tnode [ id $j label \"0\" ]" >> $file
	done;

	edges=$(echo $level | sed -e "s/|.*//" -e "s/E//") 
	for e in $edges; do
		source=$(echo $e | sed "s/,.*//")
		target=$(echo $e | sed "s/.*,//")
		echo -e "\tedge [ source $source target $target label \"-\" ]" >> $file
	done
	echo "]" >> $file
	let i=i+1
done;
