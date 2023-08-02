
def Quote(string):
    return ("\"" + string + "\"").replace("\\", "\\\\")

def delta(original,new):
    return (new / original) - 1.0

def mean(json):
    acc = 0.0
    count = 0
    for key, value in json.items():
        count = count + 1
        acc = acc + value
    return acc / count