def remove_loopback(lst):
    for chainlen in range(int((len(lst) + 1) / 2), 1, -1):
        print()
        for j in range(len(lst) - chainlen + 1):
            a = (str(lst[j:j + chainlen])[1:-1])
            if (str(lst).count(a)) > 1:
                print(a)


a = [{"name": "boy", "methods": [
    {"name": "__destruct", "modifiers": "public", "funcs": [{"name": "echo", "params": [[]]}],
     "methods": [{"name": "make_friends", "variable": ["$this", "like"]}], "params": []},
    {"name": "__toString", "modifiers": "public",
     "funcs": [{"name": "echo", "params": [[]]}, {"name": "return", "params": [["string", "like", "$this"]]}],
     "methods": [], "params": []}], "variables": [{"name": "$like", "modifiers": ["public"], "initial": None}],
      "calls": None, "evils": []}, {"name": "girl", "methods": [{"name": "__call", "modifiers": "public",
                                                                 "funcs": [{"name": "echo", "params": [[]]},
                                                                           {"name": "isset",
                                                                            "params": [["name", "boyname", "$this"]]}],
                                                                 "methods": [], "params": ["$func", "$args"]}],
                                    "variables": [{"name": "$boyname", "modifiers": ["private"], "initial": None}],
                                    "calls": None, "evils": []}, {"name": "helper", "methods": [
    {"name": "__construct", "modifiers": "public", "funcs": [], "methods": [], "params": ["$string"]},
    {"name": "__isset", "modifiers": "public",
     "funcs": [{"name": "echo", "params": [[]]}, {"name": "echo", "params": [["name", "$this"]]}], "methods": [],
     "params": ["$val"]}, {"name": "__get", "modifiers": "public", "funcs": [{"name": "echo", "params": [[]]}],
                           "methods": [{"name": ["$name", "$var"]}], "params": ["$name"]}], "variables": [
    {"name": "$name", "modifiers": ["private"], "initial": None},
    {"name": "$string", "modifiers": ["private"], "initial": None}], "calls": None, "evils": []}, {"name": "love_story",
                                                                                                   "methods": [
                                                                                                       {"name": "love",
                                                                                                        "modifiers": "public",
                                                                                                        "funcs": [{
                                                                                                                      "name": "echo",
                                                                                                                      "params": [
                                                                                                                          []]},
                                                                                                                  {
                                                                                                                      "name": "array_walk",
                                                                                                                      "params": []},
                                                                                                                  {
                                                                                                                      "name": "echo",
                                                                                                                      "params": [
                                                                                                                          []]},
                                                                                                                  {
                                                                                                                      "name": "echo",
                                                                                                                      "params": [
                                                                                                                          [
                                                                                                                              "$flag"]]}],
                                                                                                        "methods": [],
                                                                                                        "params": []}],
                                                                                                   "variables": [],
                                                                                                   "calls": None,
                                                                                                   "evils": []}]
