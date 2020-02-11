import os
import yaml
import json
from util import hash_file
import tempfile
import shutil

temp_dir = tempfile.mkdtemp()
build_data = {}

config = eval(open("config/config.json", "r").read().strip())
xinetd_template = open("config/ctf.xinetd.sample", "r").read().strip()
compose_template = open("config/docker-compose.yml.sample", "r").read().strip()

def generate_xinetd(problem, data):
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

def save_files(problem, data, key):
  files = []

  dest_root = config["fileDirectory"]
  for f in data["provide"]:
    file_path = os.path.join(problem, f)
    file_name = os.path.basename(file_path)
    
    file_name_head = file_name.split(".")[0]
    file_name_tail = ".".join(file_name.split(".")[1:])
    dest_name = file_name_head + "-" + hash_file(file_path) + "." + file_name_tail
    file_dest = os.path.join(temp_dir, dest_name)
    
    shutil.copyfile(file_path, file_dest)

    files.append(dest_root + "/" + dest_name)

  build_data[key]["files"] = files
if __name__ == "__main__":
  baseDir = config["problemDirectory"]

  cats = [(baseDir + "/" + x) for x in os.listdir(baseDir) if not x.startswith(".") and os.path.isdir(baseDir + "/" + x)]
 
  for cat in cats:
    problems = [(cat + "/" + x) for x in os.listdir(cat) if not x.startswith(".") and os.path.isdir(cat + "/" + x)]

    for problem in problems:
      assert problem.startswith(baseDir)

      key = problem[len(baseDir):]

      if key[0] == '/':
        key = key[1:]
      
      print("Loading " + key)

      with open(problem + "/config.yml", 'r') as stream:
        try:
          data = yaml.safe_load(stream)

          if "binary" in data:
            generate_xinetd(problem, data)
          generate_docker(problem, data)

          build_data[key] = data

          save_files(problem, data, key)
        except Exception as exc:
          print(exc)
          print("Failed to build " + problem)
  
  export_dir = config["exportDirectory"]
  
  shutil.rmtree(export_dir)
  os.makedirs(export_dir)
  
  shutil.copytree(temp_dir, os.path.join(export_dir, config["fileDirectory"]))
  with open(os.path.join(export_dir, "data.json"), "w") as f:
    json.dump(build_data, f)
  shutil.rmtree(temp_dir)
