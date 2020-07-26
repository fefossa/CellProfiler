"""
Run pipelines on imagesets to produce measurements.
"""

import os
import os.path
import sys
import threading

import cellprofiler

from cellprofiler_core.analysis._analysis import Analysis
from cellprofiler_core.analysis._runner import Runner
from cellprofiler_core.analysis.reply._image_set_success import ImageSetSuccess
from cellprofiler_core.utilities.zmq.communicable.reply.upstream_exit._upstream_exit import (
    UpstreamExit,
)

use_analysis = True

DEBUG = "DEBUG"
ANNOUNCE_DONE = "DONE"


def find_python():
    if hasattr(sys, "frozen"):
        if sys.platform == "darwin":
            app_python = os.path.join(os.path.dirname(os.environ["ARGVZERO"]), "python")
            return app_python
    return sys.executable


def find_worker_env(idx):
    """Construct a command-line environment for the worker

    idx - index of the worker, e.g., 0 for the first, 1 for the second...
    """
    newenv = os.environ.copy()
    root_dir = os.path.abspath(
        os.path.join(os.path.dirname(cellprofiler.__file__), "..")
    )
    added_paths = []
    if "PYTHONPATH" in newenv:
        old_path = newenv["PYTHONPATH"]
        if not any([root_dir == path for path in old_path.split(os.pathsep)]):
            added_paths.append(root_dir)
    else:
        added_paths.append(root_dir)

    if hasattr(sys, "frozen"):
        if sys.platform == "darwin":
            # http://mail.python.org/pipermail/pythonmac-sig/2005-April/013852.html
            added_paths += [p for p in sys.path if isinstance(p, str)]
    if "PYTHONPATH" in newenv:
        added_paths.insert(0, newenv["PYTHONPATH"])
    newenv["PYTHONPATH"] = os.pathsep.join([x for x in added_paths])
    if "CP_JDWP_PORT" in newenv:
        del newenv["CP_JDWP_PORT"]
    if "AW_JDWP_PORT" in newenv:
        port = str(int(newenv["AW_JDWP_PORT"]) + idx)
        newenv["CP_JDWP_PORT"] = port
        del newenv["AW_JDWP_PORT"]
    for key in newenv:
        if isinstance(newenv[key], str):
            newenv[key] = newenv[key]
    return newenv


def find_analysis_worker_source():
    # import here to break circular dependency.
    import cellprofiler_core.worker  # used to get the path to the code

    return os.path.join(
        os.path.dirname(cellprofiler_core.worker.__file__), "__init__.py"
    )


def start_daemon_thread(target=None, args=(), kwargs=None, name=None):
    thread = threading.Thread(target=target, args=args, kwargs=kwargs, name=name)
    thread.daemon = True
    thread.start()
    return thread


###############################
# Request, Replies, Events
###############################


class ServerExited(UpstreamExit):
    pass


if sys.platform == "darwin":
    import fcntl

    def close_all_on_exec():
        """Mark every file handle above 2 with CLOEXEC

        We don't want child processes inheret anything
        except for STDIN / STDOUT / STDERR. This should
        make it so in a horribly brute-force way.
        """
        try:
            maxfd = os.sysconf("SC_OPEN_MAX")
        except:
            maxfd = 256
        for fd in range(3, maxfd):
            try:
                fcntl.fcntl(fd, fcntl.FD_CLOEXEC)
            except:
                pass


if __name__ == "__main__":
    # This is an ugly hack, but it's necesary to unify the Request/Reply
    # classes above, so that regardless of whether this is the current module,
    # or a separately imported one, they see the same classes.
    import cellprofiler_core.analysis

    globals().update(cellprofiler_core.analysis.__dict__)

    Runner.start_workers(2)
    Runner.stop_workers()
