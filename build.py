import os, yaml
import hash_file from util

config = eval(open("config/config.json", "r").read().strip())
xinetd_template = open("config/ctf.xinetd.sample", "r").read().strip()
compose_template = open("config/docker-compose.yml.sample", "r").read().strip()

def generate_xinted(problem, data):
  f = open(problem + "/ctf.xinetd", "w")
  xinted = xinetd_template.replace("[BINARY]", data["binary"])

  f.write(xinted)
  f.close()

def generate_docker(problem, data):
  if not os.path.exists(problem + "/docker-compose.yml"):
    if os.path.exists(problem + "/Dockerfile"):
      f = open(problem + "/docker-compose.yml", "w")
      compose = compose_template.replace("[PORT]", str(data["port"]))
    
      f.write(compose)
      f.close()

      print("Successfully generated docker-compose.yml for " + problem)
    else:
      print("Skipping docker for " + problem)

if __name__ == "__main__":
  baseDir = config["problemDirectory"]

  cats = [(baseDir + "/" + x) for x in os.listdir(baseDir) if not x.startswith(".") and os.path.isdir(baseDir + "/" + x)]
 
  for cat in cats:
    problems = [(cat + "/" + x) for x in os.listdir(cat) if not x.startswith(".") and os.path.isdir(cat + "/" + x)]

    for problem in problems:
      with open(problem + "/config.yml", 'r') as stream:
        try:
          data = yaml.safe_load(stream)

          if "binary" in data:
            generate_xinetd(problem, data)
          generate_docker(problem, data)

        except Exception as exc:
          print("Failed to build " + problem)

