import glob
import sys
import os
from optparse import OptionParser
import fnmatch





if __name__ == "__main__":
    parser = OptionParser()
    parser.usage += " [TOPICs...]"
    parser.add_option("--dir", dest="dir_pattern", default="*_*_????????")
    parser.add_option("--from", dest="from_pattern")
    parser.add_option("--to", dest="to_name")
    (options, args) = parser.parse_args(sys.argv[1:])

    problems = []

    dirs = glob.glob(options.dir_pattern)
    for d in dirs:
    	search_pattern = d + "/" + options.from_pattern
    	#print "checking files in %s" % search_pattern

    	files = glob.glob(d + "/" + options.from_pattern)
    	if len(files) == 0:
    		print "no matching file found in %s" % d
    		problems.append(d)
    		continue
    	if len(files) > 1:
    		print "found too many ambigious files in %s: %s" % (d, files)
    		problems.append(d)
    		continue
    	if options.to_name is not None: 
    		dest_name = os.path.join(d, options.to_name)
    		print 'renaming "%s" to "%s"' % (files[0], dest_name)
    		os.rename(files[0], dest_name)

    print "problems: %s" % problems
    #print len(files)
