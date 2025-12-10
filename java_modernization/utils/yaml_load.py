import yaml
import os

def load_yaml_file(relative_path):
    """Loads a YAML file from a relative path to the current script."""
    # print(f"load_yaml_file script_dir:{relative_path}")
    script_dir = os.path.dirname(os.path.abspath(__file__)) #absolute path is better
    # print(f"load_yaml_file script_dir:{script_dir}")
    # print(f"load_yaml_file relative_path:{relative_path}")

    absolute_path = os.path.join(script_dir, relative_path)
    try:
        with open(absolute_path, 'r', encoding='utf-8') as file:
                return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: File not found at {absolute_path}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

#Loading specific topics 
def load_topics(relative_path, program_type="batch_programs"):
    script_dir = os.path.dirname(os.path.abspath(__file__)) #absolute path is better
    absolute_path = os.path.join(script_dir, relative_path)
    try:
        with open(absolute_path, 'r', encoding='utf-8') as file:
            all_topics=yaml.safe_load(file)
            if program_type == "batch_programs":
                return all_topics.get("batch_programs", [])
            elif program_type == "non_batch_programs":
                return all_topics.get("non_batch_programs", [])
            else:
                return []  # Return empty if program_type is invalid
    except FileNotFoundError:
        print(f"Error: File '{absolute_path}' not found.")
        return []
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return []


# prompts = load_yaml_file(f"..\\prompts_template\\agent_fs_prompts.yaml") #replace with your yaml file name.
# relative_path=f"prompts_template\\agent_fs_prompts_list.yaml"
# topics = load_topics(relative_path=relative_path,program_type="non_batch_programs")
# print(f"topics:{topics}")
# if prompts:
#     # print(f"prompts:{prompts}")
#     system_message = prompts["code2functionalspec"]["system_message"]
#     system_message = prompts["code2functionalspec"]["user_message"]
#     system_message = prompts["code2functionalspec"]["user_message"]
#     print(f"system_message:{system_message}")
#     data = yaml.safe_load(yaml_data)

# if "code2functionalspec" in prompts:
#     fs_prompts = prompts["code2functionalspec"]
#     if fs_prompts["name"] == "extract_programoverview" and fs_prompts["version"] == "1.0":
#             system_message = fs_prompts["system_message"]
#             user_message = fs_prompts["user_message"]
#             print("Name:", fs_prompts["name"])
#             print("Version:", fs_prompts["version"])
#             print("System Message:", system_message)
#             print("User Message:\n", user_message)