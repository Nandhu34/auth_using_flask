home_page_discount_based = [
    {
        '$match': {
            'price_drop': {
                '$regex': re.compile(r"[0-9]+%")
            }
        }
    }, {
        '$project': {
            'price_drop': 1, 
            'discount': {
                '$toInt': {
                    '$replaceAll': {
                        'input': {
                            '$arrayElemAt': [
                                {
                                    '$split': [
                                        {
                                            '$trim': {
                                                'input': '$price_drop'
                                            }
                                        }, ' '
                                    ]
                                }, 0
                            ]
                        }, 
                        'find': '%', 
                        'replacement': ''
                    }
                }
            }, 
            'root_data': '$$ROOT', 
            '_id': 0
        }
    }, {
        '$group': {
            '_id': '$root_data.category', 
            'category': {
                '$first': '$root_data.category'
            }, 
            'data': {
                '$addToSet': '$root_data'
            }
        }
    }, {
        '$project': {
            'data': {
                '$slice': [
                    '$data', 20
                ]
            }, 
            'category': 1, 
            '_id': 0
        }
    }
]