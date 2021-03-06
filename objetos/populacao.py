from objetos.cromossomo import Cromossomo
import numpy as np
import copy as cp
import bitstring


class Populacao:
    def __init__(self, numero_cromossomos, parametros):
        self.numero_cromossomos = numero_cromossomos
        self.parametros = parametros
        self.cromossomos = self.cria_cromossomos()

    def cria_cromossomos(self):
        return [Cromossomo() for _ in range(self.numero_cromossomos)]

    def gera_posicoes_aleatorias(self):
        for cromossomo in range(0, self.numero_cromossomos):
            self.cromossomos[cromossomo].bits = bitstring.BitArray(bin='')
            colunas = np.arange(0, 8)
            np.random.shuffle(colunas)
            for linha_rainha in range(0, 8):
                coluna_rainha = colunas[linha_rainha]
                bits = format(coluna_rainha, "#005b")
                self.cromossomos[cromossomo].bits.insert(bits, 3 * linha_rainha)
                self.cromossomos[cromossomo].tabuleiro[linha_rainha, coluna_rainha] = 1
            self.cromossomos[cromossomo].calcular_fitness()

    def ordena_populacao(self):
        self.cromossomos = sorted(self.cromossomos, key=Cromossomo.get_fitness)

    def seleciona_cromossomos(self):
        numero_cromossomos = self.numero_cromossomos
        if numero_cromossomos % 2 != 0:
            numero_cromossomos += 1
        nova_populacao = Populacao(numero_cromossomos, self.parametros)
        for i in range(nova_populacao.numero_cromossomos):
            chance_escolha = np.random.uniform(0, 1)
            candidatos = np.random.choice(self.cromossomos, 2, replace=False)
            if candidatos[0].fitness <= candidatos[1].fitness:
                cromossomo_melhor = candidatos[0]
                cromossomo_pior = candidatos[1]
            else:
                cromossomo_melhor = candidatos[1]
                cromossomo_pior = candidatos[0]

            if chance_escolha <= 0.80:
                nova_populacao.cromossomos[i] = cp.deepcopy(cromossomo_melhor)
            else:
                nova_populacao.cromossomos[i] = cp.deepcopy(cromossomo_pior)
        return nova_populacao

    def cruza_cromossomos(self):
        for cromossomo in range(0, self.numero_cromossomos, 2):
            if np.random.uniform(0, 1) <= self.parametros.taxa_crossover:
                filho_1 = Cromossomo()
                filho_2 = Cromossomo()
                ponto = np.random.randint(1, 8)
                pai = self.cromossomos[cromossomo]
                mae = self.cromossomos[cromossomo+1]
                filho_1.posicao_baseada_nos_pais(pai, mae, ponto)
                filho_2.posicao_baseada_nos_pais(mae, pai, ponto)
                self.cromossomos[cromossomo] = filho_1
                self.cromossomos[cromossomo+1] = filho_2

    def mutacao_cromossomos(self):
        for cromossomo in range(self.numero_cromossomos):
            chance_escolha = np.random.uniform(0, 1)
            if chance_escolha <= self.parametros.taxa_mutacao:
                ponto_1 = np.random.randint(0, 7)
                ponto_2 = np.random.randint(0, 7)
                while ponto_2 == ponto_1:
                    ponto_2 = np.random.randint(0, 7)
                bits_1 = self.cromossomos[cromossomo].bits[3*ponto_1:(3*ponto_1)+3]
                bits_2 = self.cromossomos[cromossomo].bits[3*ponto_2:(3*ponto_2)+3]
                self.cromossomos[cromossomo].bits[3*ponto_1:(3*ponto_1)+3] = bits_2
                self.cromossomos[cromossomo].bits[3*ponto_2:(3*ponto_2)+3] = bits_1
                self.cromossomos[cromossomo].tabuleiro[ponto_1][int(bits_1.bin, 2)] = 0
                self.cromossomos[cromossomo].tabuleiro[ponto_2][int(bits_2.bin, 2)] = 0
                self.cromossomos[cromossomo].tabuleiro[ponto_1][int(bits_2.bin, 2)] = 1
                self.cromossomos[cromossomo].tabuleiro[ponto_2][int(bits_1.bin, 2)] = 1
                self.cromossomos[cromossomo].calcular_fitness()

    def selecao_natural(self, filhos):
        populacao_final = Populacao(self.numero_cromossomos, self.parametros)
        filhos.ordena_populacao()
        for cromossomo in range(self.numero_cromossomos):
            if self.cromossomos[cromossomo].fitness <= filhos.cromossomos[cromossomo].fitness:
                populacao_final.cromossomos[cromossomo] = self.cromossomos[cromossomo]
            else:
                populacao_final.cromossomos[cromossomo] = filhos.cromossomos[cromossomo]
        return populacao_final
