# blackboard_tools

Some scripts and tools I found useful for dealing with blackboard

# useful bash scripts

## Find missing files:

```
for d in submissions/*; do if [ ! -r $d/swish.pl ]; then echo "$d doesn't contain swish.pl, but `ls $d`"; fi; done
```
## rename files

```
mmv "submissions/*/*.pl.pl" "submissions/#1/#2.pl"
```

