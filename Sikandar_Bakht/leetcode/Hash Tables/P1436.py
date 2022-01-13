def destCity(paths):
    d = dict(paths)
    
    for v in d.values():
        
        if v not in d:
            return v