# != Diferente
# == Igual
# > Maior
# < Menor
# >= Maior ou Igual
# <= Menor ou Igual

mediaAluno = int(input("Qual a media do aluno: \nR: "))
freqAluno = int(input("Qual a frequencia do aluno: \nR: "))
mediaCorte = 7
freqCorte = 70

if mediaAluno >= mediaCorte and freqAluno >= freqCorte :
    print("Aprovado")
else :
    print("Reprovado")