"""Generates the scripts for ditau production recast"""

from src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess


if __name__ == "__main__":
    # UFO model configurations
    model = Model(
        model_name="Semi_Leptonic_SMEFT_dim6_UFO_c1ql_c3ql",
        interaction_orders={wc: f"O{wc}" for wc in ["C1lq", "C3lq"]}
    )

    # initial partons
    # same flavor
    # initial_partons = {"uubar": "u u~", "ccbar": "c c~", "ddbar": "d d~", "ssbar": "s s~", "bbar": "b b~"}
    # different flavor
    initial_partons = {
        # up quarks combinations
        "ucbar": "u c~", "cubar": "c u~",
        # down quarks combinations
        "dsbar": "d s~", "dbbar": "d b~", "sdbar": "s d~", "sbbar": "s b~", "bdbar": "b d~", "bsbar": "b s~"
    }

    # terms that we need to simulate and their respective final states
    terms = {
        # "int-gamma": "ta+ ta- / z h",
        # "int-Z": "ta+ ta- / a h",
        "reg-reg": "ta+ ta-"
    }

    # main folder to store the simulations
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/HighPT/atlas-ditau-13TEV"

    # builds the script
    mg5script_builder = ProcessCreatorMG5(model=model)

    # creates all the folders we need
    for partons_label, initial_states in initial_partons.items():
        for term_name, final_state in terms.items():
            # defining the process
            process = Process([f"{initial_states} > {final_state}"])
            wcoefs = [["C1lq", "C1lq"]] if term_name == "reg-reg" else ["C1lq"]
            # builds the script
            mg5script_builder.add_simulations(
                process=process,
                eft_terms=wcoefs,
                root_folder=f"{root_folder}/{partons_label}_{term_name}",
                create_bin_subfolder=True
            )

    # save file
    file_ = open("atlas-ditau.txt", "w")
    file_.write(mg5script_builder.mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 atlas-ditau.txt"])
