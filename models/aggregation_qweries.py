import re 

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

home_page_mrp_price = [
    {
        '$project': {
            'price': {
                '$convert': {
                    'input': {
                        '$replaceAll': {
                            'input': '$mrp_price', 
                            'find': '₹', 
                            'replacement': ''
                        }
                    }, 
                    'to': 'double', 
                    'onError': 0, 
                    'onNull': 0
                }
            }, 
            'category': '$category', 
            'total_data': '$$ROOT', 
            '_id': 0
        }
    }, {
        '$match': {
            'price': {
                '$gte': 1500, 
                '$lte': 3000, 
                '$ne': 0
            }
        }
    }, {
        '$sort': {
            'price': 1
        }
    }, {
        '$limit': 20
    }
]

home_page_actual_price = [
    {
        '$project': {
            'price': {
                '$convert': {
                    'input': {
                        '$replaceAll': {
                            'input': '$actual_price', 
                            'find': '₹', 
                            'replacement': ''
                        }
                    }, 
                    'to': 'double', 
                    'onError': 0, 
                    'onNull': 0
                }
            }, 
            'category': '$category', 
            'total_data': '$$ROOT', 
            '_id': 0
        }
    }, {
        '$match': {
            'price': {
                '$gte': 1500, 
                '$lte': 3000, 
                '$ne': 0
            }
        }
    }, {
        '$sort': {
            'price': 1
        }
    }, {
        '$limit': 20
    }
]