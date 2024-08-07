import dotenv
import shutil
from copy import copy
from pathlib import Path
import subprocess
import json
import os
import platform

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from ccds.hook_utils.custom_config import write_custom_config
from ccds.hook_utils.dependencies import basic, scaffold, write_dependencies

packages = [
    "black",
    "flake8",
    "isort",
    "pip",
    "python-dotenv",
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "numpy",
    "pandas",
    "scikit-learn",
    "mkdocs",
    "mkdocs-material",
    "mkdocstrings[python]",
]

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages_to_install = copy(packages)

# {% if cookiecutter.dataset_storage.s3 %}
packages_to_install += ["awscli"]
# {% endif %} #

# {% if cookiecutter.include_code_scaffold == "Yes" %}
packages_to_install += scaffold
# {% endif %}

# {% if cookiecutter.pydata_packages == "basic" %}
packages_to_install += basic
# {% endif %}

# track packages that are not available through conda
pip_only_packages = [
    "awscli",
    "python-dotenv",
]

# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
# {% if cookiecutter.docs != "none" %}
packages_to_install += ["{{ cookiecutter.docs }}"]
pip_only_packages += ["{{ cookiecutter.docs }}"]
docs_subpath = docs_path / "{{ cookiecutter.docs }}"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))
# {% endif %}

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  POST-GENERATION FUNCTIONS
#

write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages_to_install,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
)


write_custom_config("{{ cookiecutter.custom_config }}")

# Remove LICENSE if "No license file"
if "{{ cookiecutter.open_source_license }}" == "No license file":
    Path("LICENSE").unlink()

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))

# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
for generated_path in Path("{{ cookiecutter.module_name }}").iterdir():
    if generated_path.is_dir():
        shutil.rmtree(generated_path)
    elif generated_path.name != "__init__.py":
        generated_path.unlink()
    elif generated_path.name == "__init__.py":
        # remove any content in __init__.py since it won't be available
        generated_path.write_text("")
# {% endif %}

# Setup .env file
env_file_path = Path(".env")
env_file_path.touch(mode=0o600, exist_ok=True)

# Add Snowflake credentials to .env
dotenv.set_key(
    dotenv_path=env_file_path,
    key_to_set="SNOWFLAKE_URL",
    value_to_set="{{ cookiecutter.env_snowflake_url }}",
)

# Add data path to .env
dotenv.set_key(
    dotenv_path=env_file_path,
    key_to_set="DATA_PATH",
    value_to_set="{{ cookiecutter.env_data_path }}",
)

# Initiate git repo
# NOTE: Can this be done in one command?
# subprocess.run("git init")
os.system("git init")

# Add git submodules
# NOTE: This will fail without clear warning
# NOTE: This might need to be modified to allow specifying a branch
# subprocess.run(
#     "git submodule add %s" % "{{ cookiecutter.env_git_url_shared_library_submodule }}"
# )
if (
    "{{ cookiecutter.env_git_url_shared_library_submodule }}"
    != "Github URL of shared library (leave blank if undesired)"
):
    os.system(
        "git submodule add %s"
        % "{{ cookiecutter.env_git_url_shared_library_submodule }}"
    )
    # Add git submodules to PYTHONPATH
    # NOTE: Additional directories can be added to PYTHONPATH using ';' as a delimiter (NO SPACES!)
    dotenv.set_key(
        dotenv_path=env_file_path,
        key_to_set="PYTHONPATH",
        value_to_set="{{ cookiecutter.env_git_url_shared_library_submodule }}".split(
            "/"
        )[-1],
    )

# Intiate venv
# NOTE: This might not work on MacOS?
if "windows" in platform.platform().lower():
    subprocess.run("py -0p")
    subprocess.run("py -%s -m venv .venv" % "{{ cookiecutter.python_version_number }}")

    # Install dependencies
    subprocess.run(".venv\Scripts\python -m pip install -r requirements.txt")

    # Complete first commit
    subprocess.run("git add .")
    subprocess.run('git commit -m "[AUTOGENERATED] First commit"')
elif "macos" in platform.platform().lower():
    os.system("python%s -m venv .venv" % "{{ cookiecutter.python_version_number }}")

    # Install dependencies
    os.system(".venv/bin/python -m pip install -r requirements.txt")

    # Complete first commit
    os.system("git add .")
    os.system('git commit -m "[AUTOGENERATED] First commit"')
