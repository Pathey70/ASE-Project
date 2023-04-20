
- To view all command line options run 
    ```python3 Main.py --help True ```

- To Run 
    
    ```python3 Main.py --go get_results```
 

```
Here are the list of options

OPTIONS:
  -b  --bins    initial number of bins       = 16
  -c  --cliffs  cliff's delta threshold      = .147
  -d  --d       different is over sd*d       = .35
  -f  --file    data file                    = ../etc/data/auto93.csv
  -F  --Far     distance to distant          = .95
  -g  --go      start-up action              = nothing
  -h  --help    show help                    = False
  -H  --Halves  search space for clustering  = 102400
  -m  --min     size of smallest cluster     = .5
  -M  --Max     numbers                      = 512
  -p  --p       dist coefficient             = 1.1
  -r  --rest    how many of rest to sample   = 4
  -R  --Reuse   child splits reuse a parent pole = True
  -s  --seed    random number seed           = 937162211