"""Generates the scripts for ditau production recast"""

from src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess

if __name__ == "__main__":
    # UFO model configurations
    model = Model(model_name="HeavyVector", interaction_orders={"gl": "ANOGL", "gq": "ANOGQ"})
    # process with all the possible tau decay channels
    processes = Process([
       "p p > e+ e-"
    ])
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/DY/cms-dielectron-13TEV/recast"
    definitions = [
        "vl = ve vm", "vl~ = ve~ vm~", "j = g u c d s b u~ c~ d~ s~ b~"
    ]
    mg5script_builder = ProcessCreatorMG5(process=processes, model=model, root_folder=root_folder,
                                          definitions=definitions)
    mg5_script = mg5script_builder.create_script(eft_terms=[["gl", "gl", "gq", "gq"]])

    # save file
    file_ = open("recast_dielectron.txt", "w")
    file_.write(mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 recast_dielectron.txt"])
