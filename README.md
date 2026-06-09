# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20602446.svg)](https://doi.org/10.5281/zenodo.20602446)

---

## Origem

Este repositório nasceu como subproduto da série
[Motor de Herança Estrutural](https://github.com/tiagobandeira/conjectura-de-goldbach),
um projeto independente sobre a Conjectura de Goldbach. Durante a investigação
das âncoras do operador $W_i(C)$ e das sequências hierárquicas $L(P_n)$, surgiu
a necessidade de extrair primoriais sem depender de um crivo externo. A tentativa
de resolver esse problema operacional levou a um resultado mais amplo: a estrutura
primorial está codificada na geometria de produtos de inteiros consecutivos e é
recuperável por análise espectral, sem conhecimento prévio dos primos e sem os
zeros da função zeta de Riemann.

Os resultados aqui documentados têm vida própria — interessam a qualquer pessoa
que estude distribuição de primos, análise harmônica em teoria dos números, ou
testes de primalidade — mas a motivação original e as conexões com o Motor estão
explicitadas em cada nota.

---

## O resultado central

Para um primo $p$ com $n = \lfloor \log_2 p \rfloor$, define-se:

$$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$$

Este produto é construído a partir de inteiros consecutivos, sem qualquer
conhecimento de quais são primos. A observação central, verificada
computacionalmente para $p \in \{37, 41, 53\}$:

> *A FFT de $\log|Z_Q(\tfrac{1}{2}+it)|$ — onde $Z_Q$ é o produto de Euler
> truncado sobre o intervalo $[2^{n-1}, p-1]$ — exibe picos nas frequências
> exatas $\log(q)/(2\pi)$ de todos os primos $q < p$. A estrutura primorial
> está codificada na geometria do intervalo binário e é recuperável
> espectralmente.*

Isso coloca o método em uma posição distinta das abordagens clássicas:

| Abordagem | Entrada | Saída | Requer |
|---|---|---|---|
| Produto de Euler | primos conhecidos | $\zeta(s)$ | lista de primos |
| Fórmula explícita de Riemann | zeros de $\zeta$ | contagem de primos | zeros de $\zeta$ |
| **Este método** | inteiros consecutivos | primos via FFT | nada além de aritmética |

---

## Estrutura do repositório

```
analise-espectral-primos/
├── README.md                         ← este arquivo
├── notas/
│   ├── nota_16_espectral_bloco_binario_primorial.md
│   └── nota_17_ferramenta_espectral_Qp.md
└── codigo/
    ├── extracao_espectral.py         ← pipeline de dois estágios
    └── sequencias_L_espectrais.py    ← sequências L(P_n) via candidatos espectrais
```

---

## Notas

### Nota 16 — Conexão Espectral entre Blocos Binários e a Hierarquia Primorial

Mostra que $Q(p)$ contém, como divisores, todos os primos menores que $p$ — uma
consequência do Teorema 1 do
[repositório de blocos binários](https://github.com/tiagobandeira/primalidade-blocos-binarios).
Introduz a análise de $Z_Q/\zeta$ e identifica o efeito de cancelamento: a
divisão por $\zeta$ remove os primos diretamente no intervalo $[2^{n-1}, p-1]$,
recuperando apenas os primos menores que $2^{n-1}$.

### Nota 17 — Ferramenta Espectral via $Q(p)$: Fundamentação e Validação

Resolve o problema de cancelamento com um pipeline de dois estágios:

- **Etapa 1** — $R_1(t) = \log|Z_Q/Z_{\text{comp}}|$: recupera os primos
  diretamente no intervalo $[2^{n-1}, p-1]$, cancelando os compostos.
- **Etapa 2** — $R_2(t) = \log|Z_Q/\zeta/Z_{\mathcal{P}_>}|$: recupera os
  primos menores que $2^{n-1}$, usando os primos da Etapa 1 para desfazer o
  cancelamento de $\zeta$.

Valida o método para $p \in \{37, 41, 53\}$ (acertos: 11/11, 12/12, 15/15).
Aplica os candidatos extraídos para construir as sequências $L(P_n)$ da
hierarquia primorial, obtendo taxas de primos idênticas à referência nos níveis
verificados. Discute a posição do método na literatura e caminhos futuros,
incluindo a comparação com fatorial e a questão de uma função interpoladora
de $Q$.

---

## Código

### `extracao_espectral.py`

Implementação do pipeline de dois estágios. Uso:

```python
from extracao_espectral import recuperar_primos

primos = recuperar_primos(p=53, t_max=300, t_step=0.02)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```
>Devido a limitações de resolução e precisão nos cálculos, alguns números compostos podem surgir e alguns primos podem ser omitidos durante a extração. Contudo, para o estudo dos primoriais e sequências $L_p$, essa variação pode ser levada em consideração. No teste, esses valores são identificados por meio de um teste simples de primalidade para facilitar a visualização.

Parâmetros principais:

| Parâmetro | Padrão | Efeito |
|---|---|---|
| `t_max` | 300 | Aumentar melhora resolução para primos próximos |
| `t_step` | 0.02 | Diminuir aumenta resolução FFT (mais lento) |
| `altura_rel` | 0.03 | Limiar de detecção de picos (fração do máximo) |

**Nota de desempenho:** o cálculo de $\zeta(\tfrac{1}{2}+it)$ via mpmath é o
gargalo (~8–15s para 3000 pontos). O cache automático por parâmetros garante
que chamadas subsequentes com os mesmos parâmetros sejam instantâneas.
$Z_Q$ em numpy é ~150× mais rápido que $\zeta$ em mpmath.

### `sequencias_L_espectrais.py`

Constrói sequências $L(P_n)$ usando os candidatos extraídos espectralmente como
universo de trabalho, sem crivo externo. Compara com a referência usando primos
reais. Uso:

```python
# No final do script, descomente:
# experimento(67, indices=(2,3,4,5,6))
```

---

## Dependências

```
numpy
scipy
mpmath
```

```bash
pip install numpy scipy mpmath
```

---

## Conexões

- **Motor de Herança Estrutural** — série de 12 artigos sobre Goldbach que
  motivou este trabalho. As sequências $L(P_n)$ (Nota 14) e as classes
  residuais módulo primoriais (Nota 15) estão nessa série.
- **Primalidade por Blocos Binários** — repositório independente com o Teorema 1
  (caracterização por MDC) e a Proposição 2 (divisibilidade por $P(N)$), cujos
  resultados sobre $A_{n-1}$ fundamentam a Proposição da Nota 16.



---

## Citação

```
T. Bandeira, "Análise Espectral de Primos via Produtos de Intervalos Binários",
notas de pesquisa independente, 2026.
DOI: 10.5281/zenodo.20602446
```



---

## Licença

- Documentação, notas matemáticas e artigos: [CC BY 4.0](LICENSE.txt)
- Código-fonte: [MIT License](LICENSE-MIT.txt)