def filter_element(objectList: list, attr_name: str, value: any):
    for item in objectList:
        valueA = getattr(item, attr_name)
        if(valueA == value):
            return item
        
    return None