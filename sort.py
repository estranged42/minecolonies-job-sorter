from tabulate import tabulate
from progress.bar import IncrementalBar
import minecoloniesjobs

minecoloniesjobs.read_worker_types("workertypes.csv")
minecoloniesjobs.read_jobs("jobs.csv")
minecoloniesjobs.read_colonists("colonists.csv")

num_generations = 5000
num_trials = 20


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
        max=num_generations,
        suffix="%(index)d/%(max)d %(percent)d%%",
    )

    current_score = current_job_set.score()

    for n in range(num_generations):
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


max_score = 0
best_job_set = None
for n in range(num_trials):
    trial_result = run_trial()
    if trial_result["score"] > max_score:
        max_score = trial_result["score"]
        best_job_set = trial_result["job_set"]


print(tabulate(best_job_set.get_report_data(), headers="keys"))
