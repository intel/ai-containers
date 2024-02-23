import yaml
from py_markdown_table.markdown_table import markdown_table

LANDING_PAGE_URL = "README.md"
LP_DESCRIPTION = """This page provides overview of AI Containers for many Intel
optimized open-source frameworks such as PyTorch, TensorFlow, SciKit Learn,
XGBoost, Modin etc. Also provides containers for open-source deep learning models
optimized by Intel to run on Intel® Xeon® Scalable processors and Intel® Data Center GPUs."""


def generate_markdown_table(containers: list):
    """Generate markdown table from a list of containers.

    Args:
        containers (list(dict)): container metadata

    Returns:
        str: markdown table of container metadata
    """
    data = []
    for container in containers:
        row = {}
        row["Container"] = (
            f"[{container['_title']}]({container['url']})"
            if container["url"]
            else container["_title"]
        )
        row["Framework"] = container["framework"]
        row["Docker Pull Command"] = f"```{container['pull-cmd']}```"
        row["Compressed Size"] = container["compressed-size"]
        if "component-bom" in container:
            row["Components"] = "<br/>".join(container["components-bom"])
        data.append(row)
    return (
        markdown_table(data)
        .set_params(row_sep="markdown", padding_weight="centerleft", quote=False)
        .get_markdown()
    )


def generate_group_readme(cont_file: str, cont_group: str):
    """Generate the readme readme for a group.

    Args:
        cont_file (str): config file path
        cont_group (str): container group name
    """
    with open(cont_file, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)[cont_group]
        if len(yaml_data["containers"]) <= 3:
            return
        readme = f"# {yaml_data['_title']}\n\n{yaml_data['description']}\n\n{generate_markdown_table(yaml_data['containers'])}\n\n[Intel AI Containers]({LANDING_PAGE_URL})\n"
        with open(yaml_data["readme"], "w", encoding="utf-8") as file:
            file.write(readme)


def generate_main_readme(container_yaml: str, groups: list, readme_fname: str):
    """Generate the main readme for a group of containers.

    Args:
        container_yaml (str): config file path
        groups (list(str)): list of container group names
        readme_fname (str): name of output file to write
    """
    with open(container_yaml, "r", encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
        readme = f"# Intel AI Containers\n\n{LP_DESCRIPTION}\n\n"
        for group in groups:
            yaml_group = yaml_data[group]
            readme += f"## {yaml_group['_title']}\n\n{yaml_group['description']}\n\n{generate_markdown_table(yaml_group['containers'][:3])}\n\n"
            if len(yaml_group["containers"]) > 3:
                readme += f"[Complete list of Containers]({yaml_group['readme']})\n\n"
        with open(readme_fname, "w", encoding="utf-8") as file:
            file.write(readme)


GROUPS = [
    "intel-python",
    "cpu-base",
    "gpu-base",
    "cpu-models",
    "atsm-models",
    "pvc-models",
    "ai-tools",
    "preset",
    "ai-workflows",
]
CONTAINER_YAML = "ai-containers.yaml"

# Generate container groups readmes
for group in GROUPS:
    generate_group_readme(CONTAINER_YAML, group)

# Generate landing page
generate_main_readme(CONTAINER_YAML, GROUPS, "README.md")

print("Generated AI container landing page and container groups pages!")
