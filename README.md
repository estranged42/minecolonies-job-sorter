# Minecolonies Job Sorter

This project aims to assist with sorting your colonists into a better set of available jobs.

You will supply a list of which jobs your colony has available, and a list of your colonists. The program will then run several iterations of assigning them to various jobs and coming up with a pretty good set of assignments.

## Prerequisites

This project depends on at least python 3.8, and the modules in `requirements.txt`. To install the required modules, you should be able to run:

```
# Mac/Linux
python -m pip install -r requirements.txt

# Windows
py -m pip install -r requirements.txt
```

## Input Files

### Worker Types List

The `workertypes.csv` file contains the different types of jobs available in MineColonies, with the exception of Library Student and Pupil. Because the sole purpose of those jobs is to raise that particular stat, it would not be a good idea to optomize for putting a highly skilled person into that job. :) Raise your colonists skills at the Library or School separately from this sorting.

The current job list was scraped from the [MineColonies worker system page](https://wiki.minecolonies.ldtteam.com/source/systems/worker) on the wiki 1.19.2 version.

#### Worker Type Weights

I've felt that some worker types are more important than others, so there is a weight component for each type. Set these all to 1.0 if you want to treak each type the same. For example Archers and Builders have the same skill requirements, but I would rather have highly skilled builders. So I weight Builders a little higher, and Archers lower. Feel free to adjust these weights in `workertypes.csv`.

### Jobs List

The input for the Jobs list is a simple CSV file with just two columns, "Jobname" and "Count". List each type of job you have available in your colony along with the count. You don't have to specify every job if you don't have one, or you can set the count to zero. See the example `jobs.csv` file.

### Colonists List

The input file your your colonists is a CSV file with the following column names. Order does not matter.
    - Name
    - Athletics
    - Dexterity
    - Strength
    - Agility
    - Stamina
    - Mana
    - Adaptability
    - Focus
    - Creativity
    - Knowledge
    - Intelligence

## Running

If you have your three input files, and you don't want to change any defaults, you can run the program with the following:

```bash
~/mcsort $ python sort.py
Score 370.4 |████████████████████████████████| 5000/5000 100%
Score 370.4 |████████████████████████████████| 5000/5000 100%
Score 370.4 |████████████████████████████████| 5000/5000 100%
Score 367.4 |████████████████████████████████| 5000/5000 100%
Score 370.4 |████████████████████████████████| 5000/5000 100%
JobName     Worker             Primary          Secondary
----------  -----------------  ---------------  ---------------
Blacksmith  Samuel Q Ashton    Strength 27      Focus 20
Builder     Ellianna W Jones   Adaptability 27  Athletics 20
Builder     Hana H Gedding     Adaptability 26  Athletics 19
Carpenter   Kiaan C Andrews    Knowledge 28     Dexterity 22
Cook        Remi P Greene      Adaptability 25  Knowledge 19
Courier     Bo A Gisborne      Agility 27       Adaptability 25
Courier     Kasem N Collard    Agility 25       Adaptability 31
Forester    Gloria G Addicock  Strength 30      Focus 17
~/mcsort $ 
```

That will kick off the trials and show you the best score from all the trials.

## How it Works

This program uses a simplistic version of an [evolutionary algorithm](https://en.wikipedia.org/wiki/Evolutionary_algorithm) to sort colonists in to jobs in an attempt to find a 'pretty good' set of assignments where the overall skills of the colonists are well utilized. I don't say 'best' in any case here, as the randomized nature of the algorithm makes it difficult to say and given set og job assignments is the abolute 'best'. And 'best' is highly subjective for each player and set of colony restrictions.

The basic steps are this:

### A Trial

#### Assignment

One trial consists of first assigning your available colonists to random jobs. It does't matter if you have more colonists than jobs, or more jobs than colonists. It should do the best it can with what's available. A given set of jobs with colonists assigned I call a Job Set. 

#### Scoring

Once the initial Job Set has been generated, it is scored. The scoring function is pretty basic. It goes through all the jobs in the Job Set, and adds up the weighted skill values for the primary and secondary skills of that Worker Type. Because the Primary Skill for a given Worker Type is more important, it has a weight of 1.0, and the secondary skill has a weight of 0.7. The skill of the colonist assigned to the job is multiplied by the weight of that skill, then are added up across all job/skill/colonist combinations. The result is the score for this Job Set.

#### Generation Mutations

Once the initial score is found, a set of swapping iterations happens. One occupied job is randomly selected, and then a different colonist is randomly selected. If both colonists are employed, then their jobs are swapped. If the second colonist was unemployed, then that colonist is assigned to the frist job.

Once a swap has happened, the new Job Set is scored. If this Job Set has a higher score than the previous one, it is promoted to the 'current best' Job Set, and the iterations continue.

By default each trial runs 5000 generations.

### Final Scoring

Through emperical testing, I have found that about 5000 generations seems to arive at the best score that trial is going to get. Running it out to hundreds of thousands of generations doesn't seem to budge the score. However due to the randomized nature of the initial Job Set, successive trials can result in measurable improvements in the final score. Therefore I have chosen to run multiple full trials, picking the best out of all the trial results. By default there are 20 trials run.

## Command Line Options

Many of the defaults can be changed with command line options. See `python sort.py --help` for details.

```bash
usage: sort.py [-h] [-t TYPESFILE] [-j JOBSFILE]
               [-c COLONISTSFILE] [-n NUMTRIALS]
               [-g GENERATIONS] [-p PRIMARYWEIGHT]
               [-s SECONDARYWEIGHT]

optional arguments:
  -h, --help            show this help message and exit
  -t TYPESFILE, --typesfile TYPESFILE
                        Worker Types input CSV file
  -j JOBSFILE, --jobsfile JOBSFILE
                        Jobs input CSV file
  -c COLONISTSFILE, --colonistsfile COLONISTSFILE
                        Colonists input CSV file
  -n NUMTRIALS, --numtrials NUMTRIALS
                        Number of Trials to run
  -g GENERATIONS, --generations GENERATIONS
                        Number of Generations per Trial
  -p PRIMARYWEIGHT, --primaryweight PRIMARYWEIGHT
                        Weight of the Primary Skill
  -s SECONDARYWEIGHT, --secondaryweight SECONDARYWEIGHT
                        Weight of the Secondary Skill
```
