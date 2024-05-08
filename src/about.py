import toml
import versioningit

data = toml.load("./pyproject.toml")
print(data['project']['title'], end=" ")

version = versioningit.get_version(".",)
print(version)
