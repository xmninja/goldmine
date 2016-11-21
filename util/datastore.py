"""Functions for handling the Data Store."""
import os
import json
from properties import command_prefix as cmdfix

orig_store = {
    'version': 2,
    'date_format': '{0}/{1}/{2}',
    'quote_format': '**#{0}**: *"{1}"* \u2014 `{2}` [{3}]',
    'quotes': [
        {
            'id': 0,
            'quote': 'Haaaaaaaaahn!',
            'author': 'Frisky Turtle, MrXarous',
            'author_ids': ['000000000000000000', '141246933359394816'],
            'date': [11, 7, 2016]
        },
        {
            'id': 1,
            'quote': 'Living well is the best revenge.',
            'author': 'George Herbert',
            'author_ids': ['000000000000000000'],
            'date': [4, 3, 1593]
        },
        {
            'id': 2,
            'quote': 'Change your thoughts and you change your world.',
            'author': 'Norman Vincent Peale',
            'author_ids': ['000000000000000000'],
            'date': [5, 31, 1898]
        }
    ]
}

async def dump():
    """Dump the entire data store's contents.'"""
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'storage.json'), 'r') as storefile:
        return json.loads('' + storefile.read())

async def write(newstore):
    """Write a new dictionary as the data store."""
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'storage.json'), 'w') as storefile:
        storefile.write(json.dumps(newstore, indent=1, separators=(',', ':')))

async def reset():
    """Reset the data store to the stock values."""
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'storage.json'), 'w') as storefile:
        storefile.write(json.dumps(orig_store, indent=1, separators=(',', ':')))

async def read(*depths):
    """Read a specific entry or entry hierarchy from the data store."""
    pass

def initialize():
    """Initialize the data store, if needed."""
#    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', 'storage.json'), 'w+') as storefile:
#        try:
#            json.loads('' + storefile.read())
#        except json.decoder.JSONDecodeError:
#            storefile.write(json.dumps(orig_store, indent=1, separators=(',', ':')))
    pass

async def get_props_s(msg):
    """Get the server properties of a message."""
    rs = await dump()
    try:
        return rs['properties']['by_server'][str(msg.server.id)]
    except (KeyError, AttributeError):
        rs['properties']['by_server'][str(msg.server.id)] = {}
        await write(rs)
        return {}

async def get_props_p(msg):
    """Get the user properties of a message."""
    rs = await dump()
    try:
        return rs['properties']['by_user'][str(msg.author.id)]
    except (KeyError, AttributeError):
        rs['properties']['by_user'][str(msg.author.id)] = {}
        await write(rs)
        return {}

async def get_prop(msg, prop: str):
    """Get the final property referenced in msg's scope."""
    try:
        thing = await get_props_p(msg)
        return thing[prop]
    except (KeyError, AttributeError):
        try:
            thing = await get_props_s(msg)
            return thing[prop]
        except (KeyError, AttributeError):
            rs = await dump()
            return rs['properties']['global'][prop]

async def get_cmdfix(msg):
    """Easy method to retrieve the command prefix in current scope."""
    return await get_prop(msg, 'command_prefix')