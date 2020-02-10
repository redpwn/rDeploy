import os, yaml

config = eval(open("config/config.json", "r").read().strip())
xinetd_template = open("config/ctf.xinetd.sample", "r").read().strip()
compose_template = open("config/docker-compose.yml.sample", "r").read().strip()

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
            f = open(problem + "/ctf.xinetd", "w")
            xinted = xinetd_template.replace("[BINARY]", data["binary"])

            f.write(xinted)
            f.close()

          if not os.path.exists(problem + "/docker-compose.yml"):
            if os.path.exists(problem + "/Dockerfile"):
              f = open(problem + "/docker-compose.yml", "w")
              compose = compose_template.replace("[PORT]", str(data["port"]))
            
              f.write(compose)
              f.close()

              print("Successfully built " + problem)
            else:
              print("Skipping build for " + problem)
        except Exception as exc:
          print("Failed to build " + problem)

