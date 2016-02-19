import threading

def tosql(df, *args, **kargs):
    CHUNKSIZE = 1000
    INITIAL_CHUNK = 100
    if len(df) <= CHUNKSIZE:
        df.to_sql(*args, **kargs)
        print('added: smaller than or same as chunksize', len(df), args[0])
        return
    if len(df) > CHUNKSIZE:
        df.iloc[:INITIAL_CHUNK, :].to_sql(*args, **kargs)
    if kargs['if_exists'] == 'replace':
        kargs['if_exists'] = 'append'
    workers = []
    for x in range((len(df) - INITIAL_CHUNK)//CHUNKSIZE):
        t = threading.Thread(target=lambda: df.iloc[INITIAL_CHUNK+x*CHUNKSIZE:INITIAL_CHUNK+(x+1)*CHUNKSIZE, :].to_sql(*args, **kargs))
        t.start()
        workers.append(t)
    print('total number of threads:', x, 'for', args[0])
    df.iloc[INITIAL_CHUNK+(x+1)*CHUNKSIZE:, :].to_sql(*args, **kargs)
    [t.join() for t in workers]
    print('added data:', len(df), 'to', args[0])
