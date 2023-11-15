from jsonschemacodegen import python as pygen
from yaml import load, dump
try:
  from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
  from yaml import Loader, Dumper

with open('schema/level.yaml') as fp:
  data = load(fp, Loader=Loader)
  generator = pygen.GeneratorFromSchema('output_dir')
  generator.Generate(data, None, 'Example', 'example')