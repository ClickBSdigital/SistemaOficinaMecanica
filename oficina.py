# -*- coding: utf-8 -*-
import os
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

# ==================== Funções auxiliares ====================

def verificar_existencia(arquivo):
    if not os.path.exists(arquivo):
        with open(arquivo, 'w', encoding='utf-8') as f:
            pass

def ler_arquivo(arquivo):
    verificar_existencia(arquivo)
    with open(arquivo, 'r', encoding='utf-8') as f:
        return f.readlines()

def escrever_arquivo(arquivo, linhas):
    with open(arquivo, 'w', encoding='utf-8') as f:
        f.writelines(linhas)

def buscar_linha_por_campo(arquivo, campo, valor):
    linhas = ler_arquivo(arquivo)
    for linha in linhas:
        dados = linha.strip().split(";")
        if dados[campo] == valor:
            return linha.strip()
    return None

def remover_linhas(arquivo, condicao):
    linhas = ler_arquivo(arquivo)
    novas_linhas = [linha for linha in linhas if not condicao(linha)]
    escrever_arquivo(arquivo, novas_linhas)

def validar_cpf(cpf: str) -> bool:
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False
    if cpf == cpf[0] * 11:
        return False

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        return False

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(cpf[10]):
        return False

    return True

def validar_telefone(telefone: str) -> bool:
    telefone = telefone.strip()
    padrao = r'^\(?\d{2}\)?[\s-]?(\d{4,5})[\s-]?(\d{4})$'
    return bool(re.match(padrao, telefone))

# ==================== Cadastro ====================

def cadastrar_cliente():
    cpf = input("CPF (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido! Digite um CPF válido.")
        return
    if buscar_linha_por_campo("clientes.txt", 0, cpf):
        print("❌ CPF já cadastrado!")
        return
    nome = input("Nome completo: ")
    telefone = input("Telefone (com DDD, ex: (11) 91234-5678): ")
    if not validar_telefone(telefone):
        print("❌ Telefone inválido! Digite no formato correto, ex: (11) 91234-5678")
        return
    with open("clientes.txt", "a", encoding='utf-8') as f:
        f.write(f"{cpf};{nome};{telefone}\n")
    print("✅ Cliente cadastrado com sucesso!")

def cadastrar_veiculo():
    cpf = input("CPF do proprietário (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    if not buscar_linha_por_campo("clientes.txt", 0, cpf):
        print("❌ Cliente não encontrado.")
        return
    placa = input("Placa: ")
    if buscar_linha_por_campo("veiculos.txt", 0, placa):
        print("❌ Placa já cadastrada!")
        return
    modelo = input("Modelo: ")
    ano = input("Ano: ")
    with open("veiculos.txt", "a", encoding='utf-8') as f:
        f.write(f"{placa};{modelo};{ano};{cpf}\n")
    print("✅ Veículo cadastrado com sucesso!")

def cadastrar_ordem_servico():
    cpf = input("CPF do cliente (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    if not buscar_linha_por_campo("clientes.txt", 0, cpf):
        print("❌ Cliente não encontrado.")
        return
    placa = input("Placa do veículo: ")
    if not buscar_linha_por_campo("veiculos.txt", 0, placa):
        print("❌ Veículo não encontrado.")
        return
    numero = input("Número da OS: ")
    if buscar_linha_por_campo("ordens_servico.txt", 0, numero):
        print("❌ OS já cadastrada!")
        return
    descricao = input("Descrição do serviço: ")
    valor = input("Valor: ")
    with open("ordens_servico.txt", "a", encoding='utf-8') as f:
        f.write(f"{numero};{descricao};{valor};{cpf};{placa}\n")
    print("✅ OS cadastrada com sucesso!")

# ==================== Consulta ====================

def listar_arquivo(arquivo, titulo):
    print(f"\n--- {titulo} ---")
    for linha in ler_arquivo(arquivo):
        print(linha.strip())
    print("--------------------------")

def consultar_veiculos_por_cpf():
    cpf = input("CPF do cliente (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    for linha in ler_arquivo("veiculos.txt"):
        dados = linha.strip().split(";")
        if dados[3] == cpf:
            print(linha.strip())

def consultar_os_por_cpf():
    cpf = input("CPF do cliente (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    for linha in ler_arquivo("ordens_servico.txt"):
        if cpf in linha:
            print(linha.strip())

def consultar_os_por_numero():
    numero = input("Número da OS: ")
    linha = buscar_linha_por_campo("ordens_servico.txt", 0, numero)
    if linha:
        print(linha)
    else:
        print("❌ OS não encontrada.")

# ==================== Edição ====================

def editar_cliente():
    cpf = input("CPF do cliente a editar (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    linha = buscar_linha_por_campo("clientes.txt", 0, cpf)
    if not linha:
        print("❌ Cliente não encontrado.")
        return
    nome = input("Novo nome: ")
    telefone = input("Novo telefone (com DDD, ex: (11) 91234-5678): ")
    if not validar_telefone(telefone):
        print("❌ Telefone inválido! Digite no formato correto, ex: (11) 91234-5678")
        return
    remover_linhas("clientes.txt", lambda l: l.startswith(cpf))
    with open("clientes.txt", "a", encoding='utf-8') as f:
        f.write(f"{cpf};{nome};{telefone}\n")
    print("✅ Cliente atualizado.")

def editar_veiculo():
    placa = input("Placa do veículo: ")
    linha = buscar_linha_por_campo("veiculos.txt", 0, placa)
    if not linha:
        print("❌ Veículo não encontrado.")
        return
    modelo = input("Novo modelo: ")
    ano = input("Novo ano: ")
    cpf = linha.split(";")[3]
    remover_linhas("veiculos.txt", lambda l: l.startswith(placa))
    with open("veiculos.txt", "a", encoding='utf-8') as f:
        f.write(f"{placa};{modelo};{ano};{cpf}\n")
    print("✅ Veículo atualizado.")

def editar_os():
    numero = input("Número da OS: ")
    linha = buscar_linha_por_campo("ordens_servico.txt", 0, numero)
    if not linha:
        print("❌ OS não encontrada.")
        return
    descricao = input("Nova descrição: ")
    valor = input("Novo valor: ")
    _, _, _, cpf, placa = linha.split(";")
    remover_linhas("ordens_servico.txt", lambda l: l.startswith(numero))
    with open("ordens_servico.txt", "a", encoding='utf-8') as f:
        f.write(f"{numero};{descricao};{valor};{cpf};{placa}\n")
    print("✅ OS atualizada.")

# ==================== Exclusão ====================

def excluir_cliente():
    cpf = input("CPF do cliente (apenas números): ")
    if not validar_cpf(cpf):
        print("❌ CPF inválido!")
        return
    if not buscar_linha_por_campo("clientes.txt", 0, cpf):
        print("❌ Cliente não encontrado.")
        return
    remover_linhas("clientes.txt", lambda l: l.startswith(cpf))
    remover_linhas("veiculos.txt", lambda l: l.split(";")[3] == cpf)
    remover_linhas("ordens_servico.txt", lambda l: l.split(";")[3] == cpf)
    print("✅ Cliente e dados vinculados removidos.")

def excluir_veiculo():
    placa = input("Placa do veículo: ")
    remover_linhas("veiculos.txt", lambda l: l.startswith(placa))
    remover_linhas("ordens_servico.txt", lambda l: l.split(";")[4] == placa)
    print("✅ Veículo e OSs vinculadas removidos.")

def excluir_os():
    numero = input("Número da OS: ")
    remover_linhas("ordens_servico.txt", lambda l: l.startswith(numero))
    print("✅ OS removida.")

# ==================== Menu ====================

def menu():
    while True:
        print("""
====== Menu Oficina Mecânica ======
1. Cadastrar Cliente
2. Cadastrar Veículo
3. Cadastrar Ordem de Serviço
4. Listar Clientes
5. Listar Veículos
6. Listar OS
7. Consultar Veículos por CPF
8. Consultar OS por CPF
9. Consultar OS por Número
10. Editar Cliente
11. Editar Veículo
12. Editar OS
13. Excluir Cliente
14. Excluir Veículo
15. Excluir OS
0. Sair
""")
        op = input("Escolha: ")

        try:
            if op == '1':
                cadastrar_cliente()
            elif op == '2':
                cadastrar_veiculo()
            elif op == '3':
                cadastrar_ordem_servico()
            elif op == '4':
                listar_arquivo("clientes.txt", "Clientes")
            elif op == '5':
                listar_arquivo("veiculos.txt", "Veículos")
            elif op == '6':
                listar_arquivo("ordens_servico.txt", "Ordens de Serviço")
            elif op == '7':
                consultar_veiculos_por_cpf()
            elif op == '8':
                consultar_os_por_cpf()
            elif op == '9':
                consultar_os_por_numero()
            elif op == '10':
                editar_cliente()
            elif op == '11':
                editar_veiculo()
            elif op == '12':
                editar_os()
            elif op == '13':
                excluir_cliente()
            elif op == '14':
                excluir_veiculo()
            elif op == '15':
                excluir_os()
            elif op == '0':
                print("Encerrando o sistema...")
                break
            else:
                print("Opção inválida.")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# ==================== Execução ====================
if __name__ == "__main__":
    menu()
