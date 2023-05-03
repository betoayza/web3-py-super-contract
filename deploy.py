from solcx import compile_standard, install_solc
import json
from web3 import Web3
from termcolor import colored
from dotenv import load_dotenv
import os

load_dotenv() # carga el ".env" al principio

# Extraer el codigo del contrato
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

# Para desplegar necesito:
## 1- Bytecode
## 2- ABI

# PREPARING DEPLOY...
bytecode = compiled_sol["contracts"]["SuperContract.sol"]["SuperContract"]["evm"][
    "bytecode"
]["object"]
abi = json.loads(
    compiled_sol["contracts"]["SuperContract.sol"]["SuperContract"]["metadata"]
)["output"]["abi"]

# print({"bytecode": bytecode, "abi": abi}, "Listo para hacer el deploy!")

chain_id = 1337  # id de la blockchain
try:
    w3 = Web3(
        Web3.HTTPProvider("http://127.0.0.1:7545")
    )  # client w3 to cpnnect to ganache

    my_address = "0x08a4134686c9c0a422c3eED336b63a7844A77876"
    private_key = os.getenv("PRIVATE_KEY")  # to sign transactions

    # DEPLOY
    SuperContract = w3.eth.contract(abi=abi, bytecode=bytecode) # crea una instancia del contrato
    print(SuperContract)

    nonce = w3.eth.get_transaction_count(my_address)
    print("Nonce:", nonce)
    ## Condiciones del deployeo:
    ### 1 Construir la transaccion
    ### 2 Firmar la transaccion
    ### 3 Enviar la transaccion

    # 1
    tx = SuperContract.constructor().build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,  # no siempre es necesario
            "from": my_address,  # desde dónde envío la transacción
            "nonce": nonce,  # contador de transaferencias de la address
        }
    )
    # Contract.constructor() crea una instancia nueva del contrato en la red de ETH, necesaria para el deploy
    print(tx, type(tx))
 
    # 2
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    print(signed_tx)

    # 3
    # sended_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    # print(signed_tx)


except Exception as error:
    print(colored("\nHubo un error: ", "yellow"), colored(error, "red"))
