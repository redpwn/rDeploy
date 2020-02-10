import os, yaml, subprocess

config = eval(open("config/config.json", "r").read().strip())

def deploy(up=False):
  baseDir = config["problemDirectory"]

  cats = [(baseDir + "/" + x) for x in os.listdir(baseDir) if not x.startswith(".") and os.path.isdir(baseDir + "/" + x)]
 
  for cat in cats:
    problems = [(cat + "/" + x) for x in os.listdir(cat) if not x.startswith(".") and os.path.isdir(cat + "/" + x)]

    for problem in problems:
      p = subprocess.Popen(["docker-compose", "up" if up else "down"], cwd=problem)
      
      stdout, stderr = p.communicate()
      
      if p.returncode == 0:
        print("Successfully deployed " + problem)
      else:
        print("Error when deploying " + problem)

if __name__ == "__main__":
  deploy()
