import csv
import random
from .types import (
    WorkerType,
    Skill,
    Job,
    JobSet,
    Colonist,
    worker_types,
    available_jobs,
    colonists,
)


def read_csv(filename, headers=None):
    # utf-8-sig encoding skips the stupid BOM stuff excel sticks in when exporting CSVs
    with open(filename, encoding="utf-8-sig") as csv_file:
        if headers is None:
            reader = csv.DictReader(csv_file)
        else:
            reader = csv.DictReader(csv_file, headers)

        items = []
        for i in reader:
            items.append(dict(i))

    return items


def read_worker_types(filename):
    global worker_types
    worker_data = read_csv(filename)
    for worker_type_data in worker_data:
        new_worker_type = WorkerType(
            name=worker_type_data["Worker"],
            primary=Skill(worker_type_data["Primary"]),
            secondary=Skill(worker_type_data["Secondary"]),
            weight=float(worker_type_data["Weight"]),
        )
        worker_types.append(new_worker_type)


def read_jobs(filename):
    global available_jobs
    temp_job_list = []
    jobs_data = read_csv(filename)
    for job_row in jobs_data:
        worker_type = job_row["Worker"]
        count = int(job_row["Count"])
        for n in range(count):
            new_job = Job(worker_type)
            temp_job_list.append(new_job)
    available_jobs = JobSet(temp_job_list)


def read_colonists(filename):
    global colonists
    colonists_data = read_csv(filename)
    for colonist_row in colonists_data:
        new_colonist = Colonist(
            Name=colonist_row["Name"],
            Athletics=int(colonist_row["Athletics"]),
            Dexterity=int(colonist_row["Dexterity"]),
            Strength=int(colonist_row["Strength"]),
            Agility=int(colonist_row["Agility"]),
            Stamina=int(colonist_row["Stamina"]),
            Mana=int(colonist_row["Mana"]),
            Adaptability=int(colonist_row["Adaptability"]),
            Focus=int(colonist_row["Focus"]),
            Creativity=int(colonist_row["Creativity"]),
            Knowledge=int(colonist_row["Knowledge"]),
            Intelligence=int(colonist_row["Intelligence"]),
        )
        colonists.append(new_colonist)


def get_random_colonist():
    global colonists
    idx = random.randrange(len(colonists))
    return colonists[idx]
