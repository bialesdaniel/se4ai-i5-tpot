import inspect

def get_class_attributes(c, skipped_fields):
    attributes = []
    for (name, value) in inspect.getmembers(c): 
        
        # to remove private and protected 
        # functions 
        if not name.startswith('_') and not name in skipped_fields: 
            
            # To remove other methods that 
            # doesnot start with a underscore 
            if not inspect.ismethod(value): 
                attributes.append((name,value))
    return attributes

