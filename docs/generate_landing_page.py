import yaml
from py_markdown_table.markdown_table import markdown_table

LANDING_PAGE_URL = "README.md"

LP_DESCRIPTION="""This page provides overview of AI Containers for many Intel 
optiomized open-source frameworks such as PyTorch, TensorFlow, SciKit Learn, 
XGBoost, Modin etc. Also provides containers for open-source deep learning models 
optimized by Intel to run on Intel® Xeon® Scalable processors and Intel® Data Center GPUs."""


def generate_group_readme(cont_file, cont_group):
    data = []
    readme = ""
    with open(cont_file, 'r') as file:
        yaml_data = yaml.safe_load(file)[cont_group]
        readme_fname = yaml_data['readme']
        readme = "# "+ yaml_data['_title'] + "\n"
        readme += yaml_data['description'] + "\n"
        if len(yaml_data['containers']) <=3:
            return
        for container in yaml_data['containers']:
            row = {}
            if not container['url']:
                row['Container'] = container['_title']
            else:
                row['Container'] = "["+ container['_title']+"]("+container['url']+")"
            row['Framework'] = container['framework']
            row['Docker Pull Command'] = "```" + container['pull-cmd'] + "```"
            row['Compressed Size'] = container['compressed-size']
            if "component-bom" in container:
                components = container['components-bom']
                components = "<br/>".join(components)
                row['Components'] = components
            data.append(row)
        markdown = markdown_table(data).set_params(row_sep = 'markdown',
                                                   padding_weight = 'centerleft', 
                                                   quote = False).get_markdown()
        readme += markdown
        readme += "\n\n"
        readme += "[Intel AI Containers](" + LANDING_PAGE_URL + ")\n"
        with open(readme_fname, "w") as file:
            file.write(readme)
        return 

# TODO: this menthod is pretty much copy-pasta of above menthod, merge it soon!
def generate_main_readme(container_yaml, groups, readme_fname):
    readme = "# Intel AI Containers\n"
    readme += LP_DESCRIPTION + "\n"
    with open(container_yaml, 'r') as file:
        yaml_data = yaml.safe_load(file)
        for group in groups:
            data = []
            yaml_group = yaml_data[group]
            readme += "## "+ yaml_group['_title'] + "\n"
            readme += yaml_group['description'] + "\n"
            count = 0
            for container in yaml_group['containers']:
                if count > 2:
                    break
                count += 1
                row = {}
                if not container['url']:
                    row['Container'] = container['_title']
                else:
                    row['Container'] = "["+ container['_title']+"]("+container['url']+")"
                row['Framework'] = container['framework']
                row['Docker Pull Command'] = "```" + container['pull-cmd'] + "```"
                row['Compressed Size'] = container['compressed-size']
                if "component-bom" in container:
                    components = container['components-bom']
                    components = "<br/>".join(components)
                    row['Components'] = components
                data.append(row)
            markdown = markdown_table(data).set_params(row_sep = 'markdown',
                                                    padding_weight = 'centerleft', 
                                                    quote = False).get_markdown()
            readme += markdown
            if len(yaml_group['containers']) >3:
                readme += "\n\n\n"
                readme += "[Complete list of Containers]("+ yaml_group['readme']+")\n"
            readme += "\n"
    with open(readme_fname, "w") as file:
        file.write(readme)
    return  

groups = ['intel-python', 'cpu-base', 'gpu-base', 'cpu-models', 'atsm-models', 'pvc-models', 'ai-tools', 'preset', 'ai-workflows']
container_yaml = 'ai-containers.yaml'

# Generate container groups readmes
for group in groups:
    generate_group_readme(container_yaml, group)

# Generate landing page
main_readme_name = "README.md"
generate_main_readme(container_yaml, groups, main_readme_name)

print("Generated AI container landing page and container groups pages!")
