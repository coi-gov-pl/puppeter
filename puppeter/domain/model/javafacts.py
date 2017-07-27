from enum import Enum


class JavaVersion(Enum):
    NOT_INSTALLED = 1
    JRE6 = 2
    JRE7 = 3
    JRE8 = 4
    JRE9 = 5

    def has_permgen_space(self):
        return self in (JavaVersion.JRE7, JavaVersion.JRE7)
