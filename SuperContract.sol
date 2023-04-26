// SPDX-License-Identifier: MIT
pragma solidity >= 0.8.0;

//@custom:dev-run-script hipotheticScript
contract SuperContract {
    uint256 numero;
    Person public Employeer =
        Person({dni: 36592920, name: "Alberto", lastname: "Ayza"});
    Person[] public persons;

    mapping(string => uint256) public lastnameToDNI; // definición -> lastnameToDNI es el nombre del mapping

    function registerNumber(uint256 _nro) public {
        numero = _nro;
    }

    // view es un identificador para llamadas a la blockchain
    function getNumber() public view returns (uint256) {
        return numero;
    }

    // pure es otro identificador, pero para cálculos
    function triple(uint256 _numb) public pure returns (uint256) {
        return _numb * 3;
    }

    struct Person {
        uint256 dni;
        string name;
        string lastname;
    }

    function addPerson(
        uint256 _dni,
        string memory _name,
        string memory _lastname
    ) public {
        persons.push(Person(_dni, _name, _lastname));

        lastnameToDNI[_lastname] = _dni;
    }
}
