def trilaterate(og):
    arr= []
    avg = 0
    for x in range(len(og)):
        arr.append(og[x].get(u'signal'))
    for i in range(len(arr)):
        avg = avg + arr[i]
    for i in range(len(arr)):
        arr[i] = arr[i] / avg
    return(arr.index(min(arr)))


def printarray(arr):
    for i in range(len(arr)):
        print(arr[i])
