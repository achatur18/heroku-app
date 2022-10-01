def signal_given_st_indicator(st):
    st=st['Supertrend']
    signal=st[-1]
    count=1
    for i in range(1, len(st)):
        if st[i]==st[i-1]:
            count+=1
        else:
            count=1
    
    return {"signal": signal, "count": count}
