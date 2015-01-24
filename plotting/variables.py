
def get_label(variable):
    label = variable['root']
    if 'units' in variable.keys():
        label += ' [{0}]'.format(variable['units'])
    return label


VARIABLES = {
    'lep1_pt': {
        'name': 'lep1_pt',
        'root': 'Leading p_{T}',
        'units': 'GeV',
        'scale': 0.001,
        'bins': 10,
        'range': (0, 200)
        },
    'lep2_pt': {
        'name': 'lep2_pt',
        'root': 'Subleading p_{T}',
        'units': 'GeV',
        'scale': 0.001,
        'bins': 10,
        'range': (0, 200)
        },
    'lep1_eta': {
        'name': 'lep1_eta',
        'root': 'Leading #eta',
        'units': 'GeV',
        'bins': 12,
        'range': (-3, 3)
        },
    'lep2_eta': {
        'name': 'lep2_eta',
        'root': 'Subleading #eta',
        'units': 'GeV',
        'bins': 12,
        'range': (-3, 3)
        },
}
