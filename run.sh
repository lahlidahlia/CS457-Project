run_pdb=""
if [[ "$1" == "-i" ]] ; then
    run_pdb="-m pdb -c continue"
fi

python $run_pdb main.py
