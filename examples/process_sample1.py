from flashgg import Dataset
from flashgg import Tagger
from flashgg import NTupleDumper
from flashgg import Task
from flashgg import RunManager
from flashgg import setup_logging

def main():
    logger = setup_logging("process_sample1.log")

    # Create Dataset from local .root files (i.e. no Dasgoclient)
    tree_name = "Events"
    file_names = ["data/sample1.root"]
    df_variables = [
            "Muon_pt_1", "Muon_pt_2",
            "Electron_pt_1", "Electron_pt_2",
            "PV_x", "PV_y", "PV_z"
            ]
    dataset = Dataset("sample1", tree_name, file_names, df_variables)

    # Instances of transformations we want to apply
    tagger = Tagger(
            name="ExampleTagger",
            regressor_name="data/classifier.pkl",
            variables=["Muon_pt_1", "Muon_pt_2", "Electron_pt_1", "Electron_pt_2"],
            systematics=["Up", "Down"],
            predicted_variable="y"
            )

    # Instances of final actions we want to perform on the dataset (?)
    dumper = NTupleDumper("data/sample1_output.root")

    # Create Tasks
    task = Task(
            dataset=dataset,
            transformations=[tagger],
            action=dumper
            )
    tasks = [task]

    # Start computation
    run_manager = RunManager(tasks=tasks)
    run_manager.run_locally()

if __name__ == "__main__":
    main()
