# Can remove this once we get to python 3.10
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from enum import Enum, auto
import copy
import random
import config


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class Skill(AutoNameEnum):
    Athletics = auto()
    Dexterity = auto()
    Strength = auto()
    Agility = auto()
    Stamina = auto()
    Mana = auto()
    Adaptability = auto()
    Focus = auto()
    Creativity = auto()
    Knowledge = auto()
    Intelligence = auto()


@dataclass
class WorkerType:
    name: str
    primary: Skill
    secondary: Skill
    weight: float


@dataclass
class Colonist:
    Name: str
    Athletics: int
    Dexterity: int
    Strength: int
    Agility: int
    Stamina: int
    Mana: int
    Adaptability: int
    Focus: int
    Creativity: int
    Knowledge: int
    Intelligence: int

    def get_skill_value(self, skill: Skill):
        return getattr(self, skill.name)


@dataclass
class Job:
    type: WorkerType
    colonist: Optional[Colonist]

    def __init__(self, type_string) -> None:
        global worker_types
        self.colonist = None
        valid_type = False
        for t in worker_types:
            if t.name == type_string:
                self.type = t
                valid_type = True
                break
        if valid_type == False:
            raise Exception(f"Invalid Worker Type: {type_string}")

    def __repr__(self) -> str:
        if self.colonist is None:
            colonist_description = "None"
        else:
            colonist_description = f"Colonist({self.colonist.Name})"
        description = (
            f"type=WorkerType({self.type.name}), colonist={colonist_description})"
        )
        return description


@dataclass
class JobSet:
    jobs: list[Job]
    _current_index: int = 0

    def __init__(self, jobs: list[Job]) -> None:
        global primary_skill_weight
        global secondary_skill_weight
        self.jobs = jobs
        self.unassigned_jobs = copy.copy(jobs)
        self.primary_weight = config.primary_skill_weight
        self.secondary_weight = config.secondary_skill_weight

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.jobs) > 0 and self._current_index < len(self.jobs):
            job = self.jobs[self._current_index]
            self._current_index = self._current_index + 1
            return job

        self._current_index = 0
        raise StopIteration

    def copy(self):
        new_job_list = []
        for job in self.jobs:
            new_job_list.append(copy.copy(job))

        new_job_set = JobSet(jobs=new_job_list)
        return new_job_set

    def init_random_colonist(self, colonist: Colonist):
        # If we're out of unassigned colonists, return False
        if len(self.unassigned_jobs) > 0:
            # Select a random job from those that are still unassigned
            random_inx = random.randrange(len(self.unassigned_jobs))
            selected_job = self.unassigned_jobs[random_inx]
            # Assign our colonist
            selected_job.colonist = colonist
            # Remove this job from the unassigned list
            self.unassigned_jobs.remove(selected_job)
            return True
        else:
            return False

    def score(self):
        # Go through each job, and add up the primary and secondary attributes
        # of the assigend colonist
        total_score = 0
        for job in self.jobs:
            # If no one is assigned, skip it
            if job.colonist == None:
                continue

            primary_skill_score = (
                job.colonist.get_skill_value(job.type.primary) * self.primary_weight
            )
            secondary_skill_score = (
                job.colonist.get_skill_value(job.type.secondary) * self.secondary_weight
            )
            # print(
            #     f"{job.colonist.Name}: {job.type.primary.name}({primary_skill_score}) {job.type.secondary.name}({secondary_skill_score})"
            # )
            job_score = (primary_skill_score + secondary_skill_score) * job.type.weight
            total_score = total_score + job_score

        return round(total_score, 1)

    def swap(self):
        """
        Select a colonist from an assigned job, and then swap that colonist with another one.
        The first colonist needs to be from an assigned job, but the second one can be randomly one
        who has a current job, or an unemployed colonist.
        """
        global colonists
        available_colonists = copy.copy(colonists)
        # Pick a random job
        random_job_idx = random.randrange(len(self.jobs))
        first_job = self.jobs[random_job_idx]
        # The first job picked might be empty. That's OK.
        if first_job.colonist != None:
            # Remove this colonist from the available_colonists
            available_colonists.remove(first_job.colonist)
        # Select a second colonist
        second_idx = random.randrange(len(available_colonists))
        second_colonist = available_colonists[second_idx]
        second_job = None
        for job in self.jobs:
            if job.colonist == second_colonist:
                # If the second colonist has a job, swap jobs.
                second_job = job
                first_colonist = first_job.colonist
                first_job.colonist = second_colonist
                second_job.colonist = first_colonist
        if second_job is None:
            # If the second colonist was unemployed, just assign them to the first job
            first_job.colonist = second_colonist

    def get_report_data(self):
        @dataclass
        class JobReportRow:
            JobName: str
            Worker: str
            Primary: str
            Secondary: str

        report_data = []
        for job in self.jobs:
            if job.colonist is None:
                worker_string = "None"
                primary_string = f"{job.type.primary.name} 0"
                secondary_string = f"{job.type.secondary.name} 0"
            else:
                worker_string = job.colonist.Name
                primary_string = f"{job.type.primary.name} {job.colonist.get_skill_value(job.type.primary)}"
                secondary_string = f"{job.type.secondary.name} {job.colonist.get_skill_value(job.type.secondary)}"

            new_job_row = JobReportRow(
                JobName=job.type.name,
                Worker=worker_string,
                Primary=primary_string,
                Secondary=secondary_string,
            )
            report_data.append(new_job_row)
        return report_data


worker_types: list[WorkerType] = []
available_jobs: Optional[JobSet] = None
colonists: list[Colonist] = []
