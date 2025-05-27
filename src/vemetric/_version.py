from importlib import metadata

try:
    __version__ = metadata.version("vemetric")
except:
    __version__ = "dev"