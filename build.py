import os
import yaml
import json
from util import hash_file, get_key
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
    
    file_name_parts = file_name.split(".")
    file_name_parts[0] = file_name_parts[0] + "-" + hash_file(file_path)
    
    dest_name = ".".join(file_name_parts)
    file_dest = os.path.join(temp_dir, dest_name)
    
    shutil.copyfile(file_path, file_dest)

    files.append(dest_root + "/" + dest_name)

  build_data[key]["files"] = files

def load_flag(problem, data, key):
  # Exactly one must be true
  assert ("flag" in data) ^ ("flag_file" in data)
  
  if "flag" in data:
    build_data[key]["flag"] = data["flag"]
  
  if "flag_file" in data:
    with open(os.path.join(problem, data["flag_file"]), "r") as f:
      build_data[key]["flag"] = f.read().strip()

if __name__ == "__main__":
  baseDir = config["problemDirectory"]

  cats = [(baseDir + "/" + x) for x in os.listdir(baseDir) if not x.startswith(".") and os.path.isdir(baseDir + "/" + x)]
  cats.sort()
 
  for ci in range(len(cats)):
    cat = cats[ci]

    problems = [(cat + "/" + x) for x in os.listdir(cat) if not x.startswith(".") and os.path.isdir(cat + "/" + x)]
    problems.sort()

    for pi in range(len(problems)):
      problem = problems[pi]
      
      key = get_key(problem, baseDir)
      
      print("Loading " + key)

      with open(problem + "/config.yml", 'r') as stream:
        try:
          data = yaml.safe_load(stream)

          if "binary" in data:
            generate_xinetd(problem, data)
          generate_docker(problem, data)

          ret = {}
          ret["name"] = data["name"]
          ret["author"] = data["author"]
          ret["description"] = data["description"]
          ret["points"] = {
            "min": config["points"]["min"],
            "max": config["points"]["max"]
          }
          ret["id"] = key
          ret["port"] = config["ports"]["base"] + config["ports"]["mod"] * ci + ((config["ports"]["A"] * pi) % config["ports"]["mod"])
          build_data[key] = ret

          load_flag(problem, data, key)
          save_files(problem, data, key)
        except Exception as exc:
          print(exc)
          print("Failed to build " + problem)
  
  export_dir = config["exportDirectory"]
  
  shutil.rmtree(export_dir)
  os.makedirs(export_dir)
  
  shutil.copytree(temp_dir, os.path.join(export_dir, config["fileDirectory"]))
  with open(os.path.join(export_dir, "config.json"), "w") as f:
    arr = []
    for key, value in build_data.iteritems():
      arr.append(value)

    json.dump(arr, f)
  shutil.rmtree(temp_dir)
