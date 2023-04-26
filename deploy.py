from solcx import compile_standard, install_solc
import json


with open("./SuperContract.sol") as file:
    code = file.read()
    # print(code)

# Compilar
install_solc("0.8.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {
            "SuperContract.sol": {"content": code},
        },
        "settings": {
            "outputSelection": {
                "*": {
                    "*": ["abi", "metadata", "evm.bytecode", "evm.bytecode.sourceMap"]
                }
            }
        },
    },
    solc_version="0.8.0" "",
)

print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
    print("Codigo compilado guardado!")