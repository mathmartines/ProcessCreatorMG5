"""Generates the scripts for ditau production recast"""

from src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess

if __name__ == "__main__":
    # UFO model configurations
    model = Model(model_name="HeavyScalar", interaction_orders={"cHgg": "LOOPGG"})
    # process with all the possible tau decay channels
    processes = Process([
        # fully leptonic
        "g g > hh > vt l+ vl vt~ l- vl~",
        # tau_lep x # tau_had
        "g g > hh > vt j j vt~ l- vl~",
        "g g > hh > vt l+ vl vt~ j j",
        # tau_had x tau_had
        "g g > hh > vt j j vt~ j j",
    ])
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/DY/ditau-ATLAS13TEV/recast"
    definitions = [
        "vl = ve vm", "vl~ = ve~ vm~", "j = g u c d s b u~ c~ d~ s~ b~"
    ]
    mg5script_builder = ProcessCreatorMG5(process=processes, model=model, root_folder=root_folder,
                                          definitions=definitions)
    mg5_script = mg5script_builder.create_script(eft_terms=[["cHgg", "cHgg"]])

    # save file
    file_ = open("recast_ditau.txt", "w")
    file_.write(mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 recast_ditau.txt"])
