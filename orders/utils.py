import datetime

def generate_order_number(pk):
    current_datetime=datetime.datetime.now().strftime('%Y%m%d%H%M%S') #20241208141833 +pk
    order_number=current_datetime + str(pk)   #aapan ordernumber year month date hr sec chya format madhe create keli ani PK tyala concat keli
    return order_number
