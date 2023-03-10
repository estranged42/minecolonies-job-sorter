import config
import argparse
from tabulate import tabulate
from progress.bar import IncrementalBar
import minecoloniesjobs


def run_trial():
    # Perform initial random assignment of colonists to job
    current_job_set = minecoloniesjobs.available_jobs.copy()
    for colonist in minecoloniesjobs.colonists:
        # Assign colonists to random jobs until we're out or all the
        # available jobs are taken and init_random_colonist returns False
        if current_job_set.init_random_colonist(colonist):
            continue
        else:
            break

    bar = IncrementalBar(
        "Score 0",
        max=config.num_generations,
        suffix="%(index)d/%(max)d %(percent)d%%",
    )

    current_score = current_job_set.score()

    for n in range(config.num_generations):
        new_job_set = current_job_set.copy()
        new_job_set.swap()
        new_score = new_job_set.score()
        if new_score > current_score:
            current_job_set = new_job_set
            current_score = new_score
            bar.message = f"Score {new_score}"

        bar.next()

    bar.finish()
    return {"score": current_score, "job_set": current_job_set}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-t",
        "--typesfile",
        default="workertypes.csv",
        help="Worker Types input CSV file",
    )
    parser.add_argument(
        "-j", "--jobsfile", default="jobs.csv", help="Jobs input CSV file"
    )
    parser.add_argument(
        "-c",
        "--colonistsfile",
        default="colonists.csv",
        help="Colonists input CSV file",
    )
    parser.add_argument(
        "-n",
        "--numtrials",
        default=config.num_trials,
        help="Number of Trials to run",
    )
    parser.add_argument(
        "-g",
        "--generations",
        default=config.num_generations,
        help="Number of Generations per Trial",
    )
    parser.add_argument(
        "-p",
        "--primaryweight",
        default=config.primary_skill_weight,
        help="Weight of the Primary Skill",
    )
    parser.add_argument(
        "-s",
        "--secondaryweight",
        default=config.secondary_skill_weight,
        help="Weight of the Secondary Skill",
    )
    args = parser.parse_args()

    minecoloniesjobs.read_worker_types(args.typesfile)
    minecoloniesjobs.read_jobs(args.jobsfile)
    minecoloniesjobs.read_colonists(args.colonistsfile)

    config.num_generations = int(args.generations)
    config.num_trials = int(args.numtrials)
    config.primary_skill_weight = float(args.primaryweight)
    config.secondary_skill_weight = float(args.secondaryweight)

    max_score = 0
    best_job_set = None
    for n in range(config.num_trials):
        trial_result = run_trial()
        if trial_result["score"] > max_score:
            max_score = trial_result["score"]
            best_job_set = trial_result["job_set"]

    print(tabulate(best_job_set.get_report_data(), headers="keys"))
