from solcx import compile_standard, install_solc
import json
from web3 import Web3
from termcolor import colored
from dotenv import load_dotenv
import os

load_dotenv()  # carga el ".env" al principio

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

# print(compiled_sol)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)
    print("Codigo compilado y guardado!")

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

    my_address = "0xdF9De2D0693037C194A4073D66f816aC1bdD3650"
    private_key = os.getenv("PRIVATE_KEY")  # to sign transactions

    # DEPLOY
    SuperContract = w3.eth.contract(
        abi=abi, bytecode=bytecode
    )  # crea una instancia del contrato
    #print(SuperContract)

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
    # print(tx, type(tx))

    # 2
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=private_key)
    # print(signed_tx)

    # 3
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print("Generating transaction, wait...")
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    print(tx_receipt.contractAddress)

    # ----- WORKING WITH DEPLOYED CONTRACTS
    super_contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
    ##funciones call y transact
    print(
        super_contract.functions.getNumber().call()
    )  # llama a la funcion "retrive()" del contrato con la función "call()"

    store_transaction = super_contract.functions.registerNumber(20).build_transaction(
        {
            "chainId": chain_id,
            "gasPrice": w3.eth.gas_price,  # no siempre es necesario
            "from": my_address,  # desde dónde envío la transacción
            "nonce": nonce + 1,  # contador de transaferencias de la address
        }
    )

    signed_store_tx = w3.eth.account.sign_transaction(
        store_transaction, private_key=private_key
    )
    print("Updating register number...")

    t_hash = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
    tx_receipt = w3.eth.wait_for_transaction_receipt(t_hash)
    print(super_contract.functions.getNumber().call())

except Exception as error:
    print(colored("\nHubo un error: ", "yellow"), colored(error, "red"))
