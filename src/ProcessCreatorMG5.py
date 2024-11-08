"""Simple classes for the construction of the mg5 script to initialize the folders"""

from collections import UserDict, UserList
from typing import Dict


class Model(UserDict):
    """
    Defines the model to be used.
    Stores the interaction order and respective Wilson coefficients.
    The key must contain the name of the Wilson coefficient and the value the respective
    interaction order.
    """

    def __init__(self, model_name: str, interaction_orders: Dict[str, str]):
        super().__init__(interaction_orders)
        self._model_name = model_name

    @property
    def model_name(self):
        """Returns the name of the model"""
        return self._model_name

    def build_interaction_orders(self, coefs):
        """
        Constructs the interaction orders given a specific set of Wilson coefficients.
        For the interference terms, only one Wilson coefficient must be passed.
        For the quadratic terms, two Wilson coefficients must be give.
        """
        # vanishing interaction order
        neglect_terms = " ".join([f"{int_order}=0" for coef, int_order in self.data.items() if coef not in coefs])

        # checks if all the coefs are among the ones defined by the model
        if not all([coef in self.data for coef in coefs]):
            return neglect_terms.strip()

        # if each wilson coefficient appears a single time their interaction order is 1, otherwise is two
        order_number = 1 if all([coefs.count(coef_name) == 1 for coef_name in set(coefs)]) else 2
        # sets the interaction orders for the coefficients
        coefs_int_orders = " ".join([f"{self.data[coef]}^2=={order_number}" for coef in set(coefs)])
        # full interaction order
        return f"{neglect_terms} {coefs_int_orders}".strip()


class Process(UserList):
    """
    Stores the list with all the process that must be generated.
    When iterating over the process, the first comes with 'generate' in front, while the others with
    'add process'.
    """
    def __iter__(self):
        for index, process in enumerate(self.data):
            yield f"generate {process}" if index == 0 else f"add process {process}"


class ProcessCreatorMG5:
    """
    Creates the script to generate the folders to stores the simulations to be run.
    A Model and a Process object must be passed.
    """

    def __init__(self, process: Process, model: Model, root_folder: str, definitions=None):
        self._process = process
        self._model = model
        self._root_folder_path = root_folder
        self._definitions = definitions

    def create_script(self,  eft_terms, create_bin_subfolder=False):
        """Creates the folder for each EFT term that one must simulate"""
        # transforms each term into a list of terms even if it's the interference with the SM
        eft_terms = [[term] if isinstance(term, str) else term for term in eft_terms]
        mg5_script = f"import model {self._model.model_name}\n\n"
        if self._definitions is not None:
            mg5_script += "\n".join([f"define {definition}" for definition in self._definitions]) + "\n\n"
        # builds each command for the creation of the folder
        for term in eft_terms:
            interaction_orders = self._model.build_interaction_orders(term)
            # accounts for all the process
            for process in self._process:
                mg5_script += f"{process} {interaction_orders}\n"
            subfolder = "/bin_1" if create_bin_subfolder else ""
            mg5_script += f"output {self._root_folder_path}/{'-'.join(term)}{subfolder}\n\n"
        return mg5_script.strip()
