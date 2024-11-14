"""Generates the scripts for ditau production recast"""

from ProcessCreatorMG5.src.ProcessCreatorMG5 import Process, Model, ProcessCreatorMG5
import subprocess

if __name__ == "__main__":
    # UFO model configurations

    # For the tildas variables
    # model = Model(model_name="TildeT_DY_UFO",
    #               interaction_orders={
    #                   "cphi1T": "TILCPHI1T", "D4FT": "TILD4FT", "cBWT": "TILDcBWT", "c3W2H4T": "TILDc3W2H4T"
    #               })

    # For the effective operators
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
    processes = Process(["p p > e- ve~", "p p > e+ ve"])
    root_folder = "/home/martines/work/MG5_aMC_v3_1_1/PhD/DY/cms-monoe-13TEV/UniversalSMEFT_d8"

    eft_terms = [
        # ["SM"],
        # interference with the SM
        # ["cphi1T"], ["D4FT"], ["cBWT"], ["c3W2H4T"],
        # # pure BSM terms
        # ["cphi1T", "cphi1T"], ["cphi1T", "D4FT"], ["cphi1T", "cBWT"], ["cphi1T", "c3W2H4T"],
        # ["D4FT", "D4FT"], ["D4FT", "cBWT"], ["D4FT", "c3W2H4T"],
        # ["cBWT", "cBWT"], ["cBWT", "c3W2H4T"],
        # ["c3W2H4T", "c3W2H4T"]
        # dim-6 operators
        ["c2JW"], ["c2JW", "c2JW"],
        # dim-6 x dim-6 renorm
        ["c2JW", "cphi1"],
        # dim-8
        ["c2psi2H2D3"], ["c5psi4H2"], ["c3psi4D2"]
    ]

    mg5script_builder = ProcessCreatorMG5(model=model)
    mg5script_builder.add_simulations(process=processes, eft_terms=eft_terms, root_folder=root_folder,
                                      create_bin_subfolder=True)

    print(mg5script_builder.mg5_script)
    # save file
    file_ = open("cms_monoe_eft.txt", "w")
    file_.write(mg5script_builder.mg5_script)
    file_.close()

    # launch mg5
    subprocess.Popen(["/bin/bash", "-i", "-c", "mg5 cms_monoe_eft.txt"])
