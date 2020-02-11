from lib.deploy import deploy
from lib.build import build
import argparse

parser = argparse.ArgumentParser(description='rDeploy: A CTF deployment script')
parser.add_argument("opt", help="subcommand to run", choices=["start", "stop", "build"])
args = parser.parse_args()

opt = args.opt
if opt == "start":
  deploy(True)
elif opt == "stop":
  deploy(False)
elif opt == "build":
  build()
else:
  print("Invalid option: " + opt)
