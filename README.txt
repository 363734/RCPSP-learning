

- chuffed:
    contains binaries from chuffed solver to solve things using shuffed

- datas:
    contains initial files from PSPLIB, classed by category

- graphs:
    contains scripts to generate plots and the plots


- results:
    contains raw files of results

- scripts:
    contains the scripts to run everything

    * GNN:
        * dglGraph.py: create DGL graphs with node features

    * Instances:
        * PrecedenceGraph.py: data structure to represent a precedence graph
        * PrecedenceParser.py: parser and logger for precedence files
        * RCPSPinstance.py: datastructure containing an RCPSP instance
        * RCPSPparser.py: contains all the things related to parsing RCPSP files
        * RCPSPstats.py: basic stats about an instance (lazy computation)


WARNING: because of variable DIR_PROJECT within the parameter file, all path should be written as from the root
         of the project and each read/write within a file should concatene this var to the relative path from the root of the project