import setuptools

# Check if ROOT is installed and raise error if not found
try:
    import ROOT
except ModuleNotFoundError:
    raise ImportError('ROOT not found. You need a full working installation of ROOT to install this package.\n' \
            'For more info, see: https://root.cern/install/')

def get_dependencies(env_yaml_file):
    import yaml
    with open(env_yaml_file, "r") as f:
        environment = yaml.safe_load(f)
    dependencies = []
    for dep in environment["dependencies"]:
        if dep != "root" and not dep.startswith("python"):
            dependencies.append(dep)
    return dependencies

setuptools.setup(
    name="flashgg",
    version="0.0.0",
    author="CMS",
    packages=["flashgg", "flashgg.helpers"],
    install_requires=get_dependencies("flashgg_env.yml"),
    python_requires=">=3.6",
)
