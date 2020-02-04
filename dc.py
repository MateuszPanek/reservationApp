from dataclasses import dataclass


class MyClass:

    def __init__(self, name, surname, age, weight):
        self.name = name
        self.surname = surname
        self.age = age
        self.weight = weight

    def __repr__(self):
        return f'name={self.name} surname={self.surname} age={self.age} weight={self.weight}'

    # def __eq__(self, other): #Porównanie instancji klas (domyślnie nie sprawdza atrybutów i nawet jeśli są identyczne zwróci false - możemy ją jednak nadpisać
    #     if self.name == other.name:
    #         return True
    #     return False
@dataclass
class SuperClass:
    name: str
    surname: str
    age: int
    weight: float


person = MyClass('Jan', 'Kowalski', 42, 85)
person_duplicate = MyClass('Jan', 'Kowalski', 42, 85)
print(person)
print(person == person_duplicate) #Porównanie dwóch instancji klas

person1 = SuperClass('Marian', 'Kowalski', 54, 125)
person1_duplicate = SuperClass('Marian', 'Kowalski', 54, 125)
print(person1)
print(person1 == person1_duplicate)
