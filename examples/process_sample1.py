from flashgg import Dataset
from flashgg import NTupleDumper
from flashgg import Task
from flashgg import RunManager
from flashgg import setup_logging

log = setup_logging("process_sample1.log")



def main():

    # Create Dataset from local .root files (i.e. no Dasgoclient)
    tree_name = "Events"
    file_names = ["data/sample1.root"]
    dataset = Dataset("sample1", tree_name, file_names)

    # Instances of final actions we want to perform on the dataset (?)
    dumper = NTupleDumper("data/sample1_output.parquet")

    # Create Tasks
    task = Task(
            dataset=dataset,
            action=dumper
            )
    tasks = [task]

    # Start computation
    run_manager = RunManager(tasks=tasks)
    run_manager.run_locally()

if __name__ == "__main__":
    main()
