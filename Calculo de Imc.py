print("Estaremos calculando o seu IMC")

Nome = input("Qual seria o seu nome?")
Altura = float (input("Poderia informar sua altura?"))
Peso = float (input("Para fecharmos, poderia informar seu peso?"))

IMC= Peso / (Altura*Altura)

print(Nome, "O seu IMC sera", IMC)

print("De acordo com o imc base confira se esta tudo ok")

Imc_Base = ( "Menos de 18,5 abaixo do peso","18,5 a 24,9 peso saudável", "25 a 29,9 sobrepeso", "30 a 39,9 obeso", "+ de 40 muito obeso também conhecido como obeso mórbido")
for Resultado in Imc_Base:
    print(Resultado)