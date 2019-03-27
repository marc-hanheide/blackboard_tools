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


# Typical workflow

also very useful: https://github.com/hjalti/mossum for analysis

1. `ln -s submission_on_time.zip gradebook.zip`
1. `python blackboard_tools/extract_gradebook.py`
1. delete stupid stuff in submissions, e.g. `find submissions/ | grep '/devel/' | xargs rm -r -v`
1. run moss: `find -L submissions -name "*.py" -print0 | xargs -0 moss -l python`
1. run mossum: `mossum --show-loops  -o moss -p 60 -l 30 http://moss.stanford.edu/results/RESPONSECODEHERE/`
1. look at output: `open moss-1.png`

