from flashgg import Dataset
from flashgg import Tagger
from flashgg import Cut
from flashgg import NTupleDumper
from flashgg import Task
from flashgg import RunManager



def main():

    # Create Dataset from local .root files (i.e. no Dasgoclient)
    file_names = ["file1.root", "file2.root"]
    tree_name = "my_tree"
    dataset = Dataset("my_dataset", file_names, tree_name)

    # Create Dataset from json file using Dasgoclient
    # TODO

    # Instances of transformations we want to apply
    tagger = Tagger(
            regressor="path_to_regressor",
            variables=["a", "b"],
            systematics=["Up", "Down"],
            predicted_name="y"
            )

    cuts = [Cut("cut1", "expression1"), Cut("cut2", "expression2")]

    # Instances of final actions we want to perform on the dataset (?)
    dumper = NTupleDumper("path_to_output_file")

    # Create Tasks
    task = Task(
            dataset=dataset,
            transformations=[tagger, *cuts],
            action=dumper
            )
    tasks = [task]

    # Start computation

    run_manager = RunManager(tasks=tasks)

    # Locally - single_thread (for debugging), multiprocessing or multithreading
    run_manager.run_locally(
            parallelization_type="multiprocessing",
            )

    # Distributed - choose batch queuing system and parallelization library
    # batch_queuing_system = HTCondor, SLURM
    # backend = Dask, Ray, Celery (default to Celery for robustness?)
    run_manager.run_on_cluster(
            batch_queuing_system="HTCondor",
            backend="Dask",
            )



if __name__ == "__main__":
    main()
