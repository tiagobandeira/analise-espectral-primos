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
conhecimento de quais são primos. A observação central, validada
computacionalmente para $p \in \{37, 41, 53, 59, 67\}$:

> *A FFT de $\log|Z_Q(\tfrac{1}{2}+it)|$ — onde $Z_Q$ é o produto de Euler
> truncado sobre o intervalo $[2^{n-1}, p-1]$ — exibe picos nas frequências
> exatas $\log(q)/(2\pi)$ de todos os primos $q < p$. A estrutura primorial
> está codificada na geometria do intervalo binário e é recuperável
> espectralmente.*

O estado atual do método (Nota 20): o pipeline opera sem verificador externo
de primalidade. A classificação primo/composto é feita pelo critério de
irredutibilidade logarítmica $\rho(m \mid \mathcal{P}_{<})$, cuja exatidão
no bloco é garantida pelo Teorema 1 dos
[blocos binários](https://github.com/tiagobandeira/primalidade-blocos-binarios).

| Abordagem | Entrada | Saída | Requer |
|---|---|---|---|
| Produto de Euler | primos conhecidos | $\zeta(s)$ | lista de primos |
| Fórmula explícita de Riemann | zeros de $\zeta$ | contagem de primos | zeros de $\zeta$ |
| **Este método (Notas 16–17)** | inteiros consecutivos | primos via FFT | $\zeta$ na Etapa 2 |
| **Este método (Nota 20)** | inteiros consecutivos | primos via FFT | nada além de aritmética |

> **Nota honesta:** $\zeta$ ainda é usada na Etapa 2 como referência de
> normalização. A Nota 20 elimina o verificador externo de primalidade
> (`isprime`), não $\zeta$. A questão de substituir $\zeta$ por uma referência
> intrinsecamente espectral está em aberto e documentada na Seção 7 da Nota 20.

---

## Estrutura do repositório

```
analise-espectral-primos/
├── README.md
├── notas/
│   ├── nota_16_espectral_bloco_binario_primorial.md
│   ├── nota_17_ferramenta_espectral_Qp.md
│   ├── nota_18_benchmark_espectral.md
│   ├── nota_19_detector_espectral.md
│   └── nota_20_crivo_espectral_sem_oraculo.md
└── notebooks/
    ├── benchmark_espectral.ipynb        ← comparação Q(p) vs primorial vs fatorial
    ├── crivo_espectral_v2.ipynb         ← crivo por subtração iterativa de compostos
    ├── crivo_sem_oraculo.ipynb          ← crivo sem isprime(), classificador ρ
    └── detector_frequencia_3.ipynb      ← irredutibilidade logarítmica de log(m)
```

---

## Notas

### Nota 16 — Conexão Espectral entre Blocos Binários e a Hierarquia Primorial

Mostra que $Q(p)$ contém, como divisores, todos os primos menores que $p$ —
consequência do Teorema 1 do
[repositório de blocos binários](https://github.com/tiagobandeira/primalidade-blocos-binarios).
Introduz a análise de $Z_Q/\zeta$ e identifica o efeito de cancelamento: a
divisão por $\zeta$ remove os primos do intervalo $[2^{n-1}, p-1]$,
recuperando apenas os primos menores que $2^{n-1}$.

### Nota 17 — Ferramenta Espectral via $Q(p)$: Fundamentação e Validação

Resolve o problema de cancelamento com um pipeline de dois estágios:

- **Etapa 1** — $R_1(t) = \log|Z_Q/Z_{\text{comp}}|$: recupera os primos
  diretamente no intervalo $[2^{n-1}, p-1]$, cancelando os compostos.
- **Etapa 2** — $R_2(t) = \log|Z_Q/\zeta/Z_{\mathcal{P}_{>}}|$: recupera os
  primos menores que $2^{n-1}$, usando os primos da Etapa 1.

Validado para $p \in \{37, 41, 53\}$. Aplica os candidatos extraídos para
construir as sequências $L(P_n)$ da hierarquia primorial.

### Nota 18 — Benchmark Espectral: Primorial, Fatorial e $Q(p)$

Compara as três funções como base para extração espectral. Resultados para
$p \in \{37, 41, 53\}$:

| Função | Taxa média | Tempo médio | $\vert I \vert$ médio |
|--------|-----------|-------------|-------------|
| Primorial $P\#$ | 92,0% | 0,12 s | 13 |
| $Q(p)$ | **97,8%** | **0,08 s** | 28 |
| Fatorial $(p-1)!$ | 31,3% | 5,46 s | 42 |

$Q(p)$ supera inclusive o primorial em taxa média, com zero falsos positivos.
Documenta a observação qualitativa principal: na faixa $f \in [0.4, 0.6]$,
correspondente ao bloco binário, $Q(p)$ exibe picos quase periódicos de alta
nitidez ausentes nos outros extratores — o recorte binário atua como filtro
natural de banda passante. Inclui três questões abertas sobre comportamento
assintótico do método.

### Nota 19 — Detector Espectral de Primalidade: da Razão $R(k)$ à Irredutibilidade Logarítmica

Documenta três abordagens progressivas para detecção do próximo primo sem
oráculo. A formulação final: $m$ é primo $\iff$ $\log m$ é irredutível no
reticulado $\mathbb{Z}$-gerado por $\{\log p_i : p_i < m\}$. Resultados:

- Critério exato (divisibilidade): 100% — equivalente à definição de primo
- Resíduo contínuo $\rho(m)$ sem aritmética inteira: **80,1%** de separação
- Correlação negativa inesperada: $\rho(m) \times \text{dist\_primo} = -0.45$
  (Spearman) — compostos próximos de primos têm resíduo maior, não menor

Evidência empírica de que $t_{\max} \sim O(p)$ para primos gêmeos.

### Nota 20 — Crivo Espectral sem Oráculo de Primalidade

Elimina `isprime()` do pipeline substituindo-o pelo critério
$\rho(m \mid \mathcal{P}_{<}) > \rho^*$, onde $\mathcal{P}_{<} = \{q \text{
primo} : q < 2^{n-1}\}$. O critério é exato no bloco pelo Corolário do
Teorema 1: todo composto em $[2^{n-1}, p-1]$ tem todos os seus fatores primos
em $\mathcal{P}_{<}$, portanto $\rho = 0$ exatamente para compostos e $\rho >
0.009$ para primos.

O pipeline resultante inverte a ordem das etapas (Etapa 2 → Etapa 1):
$\mathcal{P}_{<}$ é extraída primeiro e fornece a base para o classificador
$\rho$ na Etapa 1. Validado para $p \in \{37, 41, 53, 59, 67\}$, com taxas
idênticas à versão com `isprime()` para $p \leq 59$.

---

## Notebooks

### `benchmark_espectral.ipynb`

Comparação sistemática de primorial, fatorial e $Q(p)$ como bases para
extração espectral. Métricas: taxa de acertos, falsos positivos, primos
perdidos, tempo de cálculo, tamanho do intervalo, eficiência $\eta =
|\text{acertos}|/|I|$, e amplitude espectral nos picos primos. Gera tabela
LaTeX pronta para inserção em nota.

### `crivo_espectral_v2.ipynb`

Crivo espectral por subtração iterativa: em vez de suprimir picos no espectro
bruto, subtrai $S_m(t) = \log|(1 - m^{-1/2-it})^{-1}|$ do sinal residual a
cada candidato não aceito. Emula $R_1 = \log|Z_Q/Z_{\text{comp}}|$ sem lista
prévia de compostos.

### `crivo_sem_oraculo.ipynb`

Versão final do pipeline sem verificador externo. Substitui `isprime(m)` pelo
critério $\rho(m \mid \mathcal{P}_{<})$. Inclui calibração do limiar $\rho^*$,
comparação com a versão de referência e análise dos casos de divergência.

### `detector_frequencia_3.ipynb`

Investigação da irredutibilidade logarítmica: $\rho(m)$ como distância de
$\log m$ ao reticulado dos $\log p_i$. Inclui distribuição dos resíduos para
primos e compostos em $[4, 149]$, limiar ótimo de separação (80,1% sem
aritmética inteira), e análise de correlação $\rho \times$ distância ao primo
mais próximo.

---

## Código

### `extracao_espectral.py`

Implementação do pipeline de dois estágios original (Nota 17). Uso:

```python
from extracao_espectral import recuperar_primos

primos = recuperar_primos(p=53, t_max=300, t_step=0.02)
# [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

> Devido a limitações de resolução, alguns primos podem ser omitidos e alguns
> compostos podem emergir. Para $t_{\max} = 300$, o método recupera todos os
> primos testados. O parâmetro `isprime` nos scripts de validação é usado apenas
> para facilitar a visualização — não faz parte do método.

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

Constrói sequências $L(P_n)$ usando os candidatos extraídos espectralmente
como universo de trabalho, sem crivo externo. Compara com a referência usando
primos reais.

---

## Dependências

```
numpy
scipy
mpmath
sympy
```

```bash
pip install numpy scipy mpmath sympy
```

---

## Estado atual e questões abertas

O pipeline sem oráculo (Nota 20) é o estado atual do método. As questões em
aberto documentadas nas notas são:

1. **Substituição de $\zeta$** — existe referência espectral construída a
   partir de $Z_Q$ sem $\zeta$? Blocos binários e suas uniões foram testados
   e falharam (Nota 20, Seção 7). Em aberto.

2. **Escala de $t_{\max}$** — para primos gêmeos, $t_{\min} \sim O(p/\log p)$.
   Evidência empírica na Nota 19. Questão analítica em aberto.

3. **SNR assintótico** — o SNR dos picos de primos no bloco de $Q(p)$ cresce
   com $p$? Testável computacionalmente estendendo o benchmark a $p$ maiores.

4. **Crivo espectral autônomo completo** — existe operador espectral que, a
   partir dos picos irredutíveis de $Z_{Q(p)}$, produz o próximo primo sem
   aritmética inteira? (Questão 4, Nota 19.)

---

## Conexões

- **Motor de Herança Estrutural** — série de 12 artigos sobre Goldbach que
  motivou este trabalho. As sequências $L(P_n)$ (Nota 14) e as classes
  residuais módulo primoriais (Nota 15) estão nessa série.
- **Primalidade por Blocos Binários** — repositório independente com o Teorema 1
  (caracterização por MDC) e a Proposição 2 (divisibilidade por $P(N)$), cujos
  resultados sobre $A_{n-1}$ fundamentam a Proposição da Nota 16 e o
  classificador $\rho$ da Nota 20.

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