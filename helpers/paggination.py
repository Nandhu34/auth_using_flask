

def pagination_setup (page_no):
    limit = 5
    start = (int(page_no)-1)*5
    end = start + limit 
    return (start,end )
