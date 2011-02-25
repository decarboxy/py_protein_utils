import gzip

def universal_open(path,mode):
    """given a path and a mode, return a filehandle.
    allows you to open files regardless of whether they are gzipped"""
    extension = path.split(".")[-1]
    if(extension == "gz"):
        return gzip.open(path,mode)
    else:
        return open(path,mode)