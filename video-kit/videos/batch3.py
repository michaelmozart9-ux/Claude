import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "lib"))
from formats2 import *
which = sys.argv[1:] or ["all"]
fns = {"f1": plan6, "g1": bar_one, "g2": hands_sep, "g3": chunks, "h1": speed_test, "i1": pov_kid, "i2": teacher_week, "i3": returner, "j1": missed_day, "k1": thirty_min}
for k, f in fns.items():
    if "all" in which or k in which:
        f()
