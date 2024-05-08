import toml
import versioningit

data = toml.load("./pyproject.toml")
print(data['project']['name'], end=" ")

version = versioningit.get_version(".",)
print(version)
