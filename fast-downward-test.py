import glob
import sys
import os
from optparse import OptionParser
import fnmatch
from subprocess import check_output
from shutil import copyfile
from subprocess import CalledProcessError

import csv


def call_planner(domain_in, problem_in):

    from driver.main import main
    from tempfile import mkdtemp
    from shutil import rmtree
    from os import path

    tmpdir = mkdtemp()

    domain_file = path.join(tmpdir, 'domain.pddl')
    problem_file = path.join(tmpdir, 'problem.pddl')
    copyfile(domain_in, domain_file)
    copyfile(problem_in, problem_file)
    plan_file = path.join(tmpdir, 'plan.out')

    try:
        log = main(["--plan-file", plan_file, "--cwd", tmpdir, problem_file, "--search", "astar(ff)"])
        with open(plan_file, "r") as text_file:
            p = text_file.read()
        return True, log, p

    except (CalledProcessError) as e:
        return False, e.output, "no plan due to error. check logs"
    except (RuntimeError, OSError) as e:
        return False, str(e), "no plan due to error. check logs"
    finally:
        rmtree(tmpdir, ignore_errors=True)

    return False, "This contains the logs", "This shall be the plan"

def file_mime(f):
    return check_output(['file','-b', '--mime-type', f]).rstrip()


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("--glob", dest="glob_pattern", default="*_*_????????/actual-T2.pddl")
    parser.add_option("--problems", default=['move.pddl', 'move_rev.pddl', 'depot-01.pddl', 'depot-02.pddl'])
    parser.add_option("--planner", default="fast-downward.py")
    parser.add_option("--csv_output", default="output.csv")
    #parser.add_option("--to", dest="to_name")
    (options, args) = parser.parse_args(sys.argv[1:])

    files = glob.glob(options.glob_pattern)
    with open(options.csv_output, "w") as csv_file:
        csv_writer = csv.writer(csv_file, dialect='excel')
        csv_row=['surname', 'firstname','id','Filetype']
        for p in options.problems:
            csv_row.append(p)
            csv_row.append(p+" plan length/log")
        csv_writer.writerow(csv_row)

        files.sort()

        for f in files:
            f_name = os.path.abspath(f)
            dir_name = os.path.dirname(f_name)
            file_name = os.path.basename(f_name)
            user_dir = os.path.basename(dir_name)
            (first, sur, sid) = user_dir.split('_')

            csv_row=[sur, first, sid, file_mime(f_name)]
            for p in options.problems:
                (success, log, plan) = call_planner(f_name, p)
                if success:
                    print "%s:%s PLAN FOUND" % (f, p)
                    csv_row.append(True)
                    csv_row.append(plan.count('\n'))
                    with open(os.path.join(dir_name, p + ".plan"), "w") as text_file:
                        text_file.write(plan)
                else:
                    print "%s:%s NO PLAN FOUND" % (f, p)
                    csv_row.append(False)
                    csv_row.append(log)
                    with open(os.path.join(dir_name, p + ".noplan"), "w") as text_file:
                        text_file.write(log)
            csv_writer.writerow(csv_row)


