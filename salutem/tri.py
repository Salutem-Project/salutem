def trilaterate(og):
    mean([item.get(u'signal') for item in og])


    # arr= []
    # avg = 0
    # for x in range(len(og)):
    #     arr.append(og[x].get(u'signal'))
    # for i in range(len(arr)):
    #     avg = avg + arr[i]
    # for i in range(len(arr)):
    #     arr[i] = arr[i] / avg
    # return(arr.index(min(arr)))