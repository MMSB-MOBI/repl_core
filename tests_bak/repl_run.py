#from ..repl_core import run
import uvicorn



if __name__ == "__main__":
    uvicorn.run("test_server:app", host="127.0.0.1", port=5000, log_level="info")

"""
command_pool_example = {
                "clist" : {
                    "_target" : clist,
                    "paramTypes" : None,
                    "help" : f"List database content\nUsage: clist tree|all|culled|vector"
                },
                "connect" : {
                    "_target"    : connect,
                    "paramTypes" : [str, int],
                    "runningParams" : True,
                    "help" : f"Connect to database\nUsage: connect <i>hostname</i> <i>port</i>"
                },
                "load"    :  {
                    "_target"    : load,
                    "paramTypes" : [str, str],
                    "runningParams" : True,
                    "help" : f"Insert any number of triplets of GO trees in the database\nUsage: load <i>owl_file proteome_file_1, ...</i>"
                },
                'exit'    :  {
                    "_target"    : _exit,
                    "paramTypes" : None,
                    "help" : f"Close the interface\nUsage: exit"
                },
                "delete"    :  {
                    "_target"    : delete,
                    "paramTypes" : [str],
                    "runningParams" : True,
                    "help" : f"Delete any number of triplets of GO trees in the database\nUsage: delete <i>taxid_1, ...</i>"
                },
                "build"    :  {
                    "_target"    : build,
                    "paramTypes" : None,               
                    "help" : f"Build all missing triplets of <u>GO vectors</u> in the database\nUsage: build"
                }
            }
run()

"""

