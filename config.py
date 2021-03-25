import configparser
DEFAULT_SETTINGS = {'silence': 0, 'autorun_hk':'num minus', 'dwarfglitch_hk':'ctrl+j', 'autorun_state':1, 'dwarfglitch_state':1}
BOOL_KEYS = ['silence', 'autorun_state', 'dwarfglitch_state']

SETTINGS = DEFAULT_SETTINGS

def save():
    config = configparser.ConfigParser()
    config['SETTINGS'] = SETTINGS
    with open('params.ini', 'w') as configfile:
        config.write(configfile)

def load():
    global SETTINGS
    res = DEFAULT_SETTINGS
    config = configparser.ConfigParser()
    try:
        config.read('params.ini')
        res.update(config['SETTINGS'])
        for key in BOOL_KEYS:
            if res[key] in ['True', 'true']:
                res[key] = True
            elif res[key] in ['False', 'false']:
                res[key] = False
            else:
                res[key] = int(res[key])

        SETTINGS.update(res)
    except Exception as e:
        print(e)
    return  res

def set_param(key, value):
    global SETTINGS
    if type(value) is bool:
        SETTINGS[key] = int(value)
    else:
        SETTINGS[key] = value
    save()

def get_param(key):
    if key in SETTINGS:
        return SETTINGS[key]
    else:
        return None