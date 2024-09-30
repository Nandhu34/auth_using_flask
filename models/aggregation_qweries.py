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

normal_aggregation=[
    {
        '$addFields': {
            'mrp_price': {
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
            'actual_price': {
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
            'price_drop': {
                '$convert': {
                    'input': {
                        '$replaceAll': {
                            'input': {
                                '$arrayElemAt': [
                                    {
                                        '$split': [
                                            '$price_drop', ' '
                                        ]
                                    }, 0
                                ]
                            }, 
                            'find': '%', 
                            'replacement': ''
                        }
                    }, 
                    'to': 'double', 
                    'onError': 0, 
                    'onNull': 0
                }
            }
        }
    }, {
        '$project': {
            'category': '$category', 
            '_id': 0, 
            'data': '$$ROOT'
        }
    }, {
        '$sample': {
            'size': 20
        }
    }
]

get_all_category= [
    {
        '$group': {
            '_id': {
                'category': '$category', 
                'sub_category': '$sub_category'
            }, 
            'inner_category': {
                '$addToSet': '$inner_category'
            }
        }
    }, {
        '$group': {
            '_id': '$_id.category', 
            'inner_category': {
                '$addToSet': {
                    'sub_category': '$_id.sub_category', 
                    'inner_category': '$inner_category'
                }
            }
        }
    }, {
        '$project': {
            '_id': 0, 
            'category': '$_id', 
            'inner_category': {
                '$arrayToObject': {
                    '$map': {
                        'input': '$inner_category', 
                        'as': 'ic', 
                        'in': {
                            'k': '$$ic.sub_category', 
                            'v': '$$ic.inner_category'
                        }
                    }
                }
            }
        }
    }
]



get_filter_by_all_category =[
    {
        '$match': {
            'category': 'kitchen, garden & pets', 
            'sub_category': 'electronics & devices ', 
            'inner_category': 'audio & accessories'
        }
    }, {
        '$group': {
            '_id': 'null', 
            'brand_name': {
                '$addToSet': '$brand_name'
            }
        }
    }
]

