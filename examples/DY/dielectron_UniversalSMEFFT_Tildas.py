"""Generates the scripts for ditau production recast"""

from src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess

if __name__ == "__main__":
    # UFO model configurations
    model = Model(model_name="TildeT_DY_UFO",
                  interaction_orders={
                      "cphi1T": "TILCPHI1T", "D4FT": "TILD4FT", "cBWT": "TILDcBWT", "c3W2H4T": "TILDc3W2H4T"
                  })
    # DY process
    processes = Process([
       "p p > e+ e-"
    ])
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/DY/cms-dielectron-13TEV/UniversalSMEFT_d8"

    eft_terms = [
        # interference with the SM
        ["cphi1T"], ["D4FT"], ["cBWT"],
        # pure BSM terms
        ["cphi1T", "cphi1T"], ["cphi1T", "D4FT"], ["cphi1T", "cBWT"],
        ["D4FT", "D4FT"], ["D4FT", "cBWT"],
        ["cBWT", "cBWT"]
    ]

    mg5script_builder = ProcessCreatorMG5(process=processes, model=model, root_folder=root_folder)
    mg5_script = mg5script_builder.create_script(eft_terms=eft_terms, create_bin_subfolder=True)

    # save file
    file_ = open("cms_dielectron_eft.txt", "w")
    file_.write(mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 cms_dielectron_eft.txt"])
