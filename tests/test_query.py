EXAMPLE_REQUEST = {
    'patient': {
        'id': '1',
        'label': 'patient 1',
        'contact': {
            'name': 'First Last',
            'institution': 'Contact Institution',
            'href': 'mailto:first.last@example.com',
        },
        'ageOfOnset': 'HP:0003577',
        'inheritanceMode': 'HP:0000006',
        'features': [
            {
                'id': 'HP:0000252',
                'label': 'Microcephaly',
            },
            {
                'id': 'HP:0000522',
                'label': 'Alacrima',
                'ageOfOnset': 'HP:0003593',
            },
        ],
        'genomicFeatures': [{
            "gene": {
              "id": "EFTUD2",
            },
            "type": {
              "id": "SO:0001587",
              "label": "STOPGAIN",
            },
            "variant": {
              "alternateBases": "A",
              "assembly": "GRCh37",
              "end": 42929131,
              "referenceBases": "G",
              "referenceName": "17",
              "start": 42929130,
            },
            "zygosity": 1,
        }],
        'disorders': [{
            "id": "MIM:610536",
        }],
    }
}
