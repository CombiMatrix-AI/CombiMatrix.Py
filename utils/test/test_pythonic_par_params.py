import json
import pytest

from utils.par import PAR
from utils.ui_utils import ROOT_DIR


@pytest.fixture
def test_pythonic_create_parameters():
    # Assuming the PAR class is already defined in scope
    par_instance = PAR()

    # Assuming the `test.cv.vcfg` file contains a JSON-like structure
    with open(ROOT_DIR / "vcfgs" / "test.cv.vcfg", 'r') as file:
        vcfg_data = json.load(file)

    ecc_params = par_instance.create_parameters(vcfg_data)

    print(ecc_params)

if __name__ == "__main__":
    pytest.main()
