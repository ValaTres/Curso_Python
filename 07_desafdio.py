executar = True
while executar :
    nome = input("Digite seu nome: ")
    anoAtual = int(input("Digite o ano atual: "))
    anoNasc = int(input("Digite o ano de nascimento: "))
    idade = anoAtual - anoNasc
    print("Olá " + nome + ", vocLê tem " + str(idade) + "anos")
    opcao = input("Você deseja testar novamente? \n[1] sim ou [2]não?")
    if opcao == "2" or "Não" or "não" or "nao" or "Nao":
        executar = False