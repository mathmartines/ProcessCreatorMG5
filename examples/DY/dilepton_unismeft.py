"""Generates the scripts for ditau production recast"""

from src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess

if __name__ == "__main__":
    # UFO model configurations
    model = Model(model_name="Direct_and_4ferm_DY_UFO",
                  interaction_orders={
                      # dim-6 coefficients
                      # operators entering through renormalization
                      "cBW": "ANOBW", "cWW": "ANOWW", "cBB": "ANOBB", "cphi1": "ANOPHI1", "c2JWrenorm": "ANO2JWrenorm",
                      "c2JW": "ANO2JW", "c2JB": "ANO2JB",  # 4-fermion ops
                      # dim-8 coefficients
                      "c1psi2H2D3": "ANO1PSI2H2D3", "c2psi2H2D3": "ANO2PSI2H2D3",  # momentum dependent ops
                      "c5psi4H2": "ANO5PSI4H2", "c4psi4H2": "ANO4PSI4H2",  "c7psi4H2": "ANO7PSI4H2",  # 4-fermion
                      "c2psi4D2": "ANO2PSI4D2", "c3psi4D2": "ANO3PSI4D2"  # 4-fermion-momentum dep.
                  })
    # DY process
    processes = Process([
        "p p > e+ e-"
    ])
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/DY/cms-dielectron-13TEV/UniversalSMEFT_d8"

    eft_terms = [
        # ["c2JB"], ["c2JW"],
        # ["c2JB", "c2JB"], ["c2JB", "c2JW"], ["c2JW", "c2JW"]
        ["c2JB", "c2JWrenorm"], ["c2JB", "cphi1"], ["c2JB", "cBW"],
        # ["c2JW", "c2JWrenorm"], ["c2JW", "cphi1"], ["c2JW", "cBW"],
        # ["c1psi2H2D3"], ["c2psi2H2D3"], ["c5psi4H2"], ["c4psi4H2"], ["c7psi4H2"]
    ]

    mg5script_builder = ProcessCreatorMG5(process=processes, model=model, root_folder=root_folder)
    mg5_script = mg5script_builder.create_script(eft_terms=eft_terms, create_bin_subfolder=True)

    # save file
    file_ = open("cms_dielectron_eft.txt", "w")
    file_.write(mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 cms_dielectron_eft.txt"])
