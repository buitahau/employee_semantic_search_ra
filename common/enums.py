from enum import StrEnum


class Gender(StrEnum):
    MALE   = "Male"
    FEMALE = "Female"


class ContractType(StrEnum):
    FULLTIME  = "Full time"
    PART_TIME = "Part time"
    INTERN    = "Intern"


class Position(StrEnum):
    ADMIN   = "Admin"
    DEV     = "Dev"
    HR      = "HR"
    MANAGER = "Manager"
    QA      = "QA"


class Level(StrEnum):
    EXPERT = "Expert"
    INTERN = "Intern"
    JUNIOR = "Junior"
    MIDDLE = "Middle"
    SENIOR = "Senior"
