# Análise Espectral de Primos via Produtos de Intervalos Binários

**T. Bandeira · 2026**

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20648983.svg)](https://doi.org/10.5281/zenodo.20648983)

---

## O resultado central

Para um primo $p$ com $n = \lfloor \log_2 p \rfloor$, define-se o produto sobre o bloco binário:

$$Q(p) = \prod_{x=2^{n-1}}^{p-1} x$$

construído a partir de inteiros consecutivos, sem qualquer conhecimento de quais são primos. A observação central, validada computacionalmente:

> A FFT de $\log|Z_Q(\frac{1}{2}+it)|$ — onde $Z_Q$ é o produto de Euler truncado sobre $[2^{n-1}, p-1]$ — exibe picos nas frequências $\log(q)/(2\pi)$ de todos os primos $q < p$. A estrutura primorial está codificada na geometria do intervalo binário e é recuperável espectralmente, **sem conhecimento prévio dos primos e sem os zeros de $\zeta$**.

O fundamento teórico (Nota 21): um inteiro $m$ é *logaritmicamente irredutível* — i.e., $\log m$ não pode ser escrito como combinação inteira $\sum e_i \log p_i$ com $p_i < m$ — se e somente se $m$ é primo. O crivo remove iterativamente as contribuições redutíveis do sinal; os picos sobreviventes são exatamente os primos. A correção do filtro segue do Teorema de Invariância: as funções $t \mapsto \cos(t \log m)$ são assintoticamente ortogonais, então remover a contribuição de um composto não contamina a de nenhum primo.

| Abordagem | Entrada | Requer |
|---|---|---|
| Produto de Euler | primos conhecidos | lista de primos |
| Fórmula explícita de Riemann–Mangoldt | zeros de $\zeta$ | zeros de $\zeta$ |
| **Este método (versão final)** | inteiros consecutivos | **nenhum** (autônomo) |

O método atual (Notas 23–24) é completamente autônomo:
- **Etapa A (recursão):** constrói $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$ usando apenas divisibilidade e o critério $\rho_B$, bloco a bloco.
- **Pré-limpeza:** subtrai de uma só vez todos os compostos do bloco, identificados por $\rho_B(m \mid \mathcal{P}_<)=0$, simulando o efeito de $\log|Z_Q| - \log|Z_{\text{compostos}}|$ sem $\zeta$.
- **Crivo iterativo:** sobre o sinal já limpo, extrai os primos do bloco usando $\rho_B(m \mid \mathcal{P}_<) > 10^{-6}$ como classificador.

Nenhuma dependência analítica ($\zeta$) ou oráculo de primalidade (`isprime`) permanece.

### Complementaridade das duas etapas

As duas etapas do pipeline exploram estruturas distintas e se complementam:

- **Etapa A (recursão aritmética)** — opera sobre primos pequenos, onde a base $\mathcal{S}_k$ é densa e a aritmética inteira é ótima: o teste `m % p == 0` resolve em $O(|\mathcal{S}_k|)$ o que qualquer critério contínuo resolveria em $O(|\mathcal{S}_k|^2 \cdot k)$ (Nota 26).
- **Crivo iterativo (domínio espectral)** — opera sobre primos grandes do bloco, onde as frequências $\log(q)/(2\pi)$ são bem separadas e a ortogonalidade das funções de Dirichlet garante que remover um composto não contamina nenhum primo. Não requer divisibilidade: a separação emerge da geometria do sinal.

Cada etapa é ótima exatamente onde a outra seria custosa. A recursão resolve o que o espectro não resolve bem (primos pequenos, frequências próximas); o crivo espectral resolve o que a aritmética inteira não aproveita (primos grandes, estrutura multiplicativa codificada em $Z_Q$).

---

## Origem

Este repositório nasceu como subproduto da série [Motor de Herança Estrutural](https://github.com/tiagobandeira/conjectura-de-goldbach), um projeto independente sobre a Conjectura de Goldbach. Durante a investigação das âncoras do operador $W_i(C)$ e das sequências hierárquicas $L(P_n)$, surgiu a necessidade de extrair primoriais sem depender de um crivo externo — o que levou ao método documentado aqui.

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
│   ├── nota_20_crivo_espectral_sem_oraculo.md
│   ├── nota_21_formalizacao.md
│   ├── nota_22_metodo.md
│   ├── nota_23_recursao_blocos.md          ← substitui ζ por recursão
│   ├── nota_24_prelimpeza.md               ← pré-limpeza + equivalência com versão ζ
│   ├── nota_25_rho_continuo.md             ← critério ρ sem aritmética inteira; limites de escala
│   ├── nota_26_rho_adapt.md                ← ρ_adapt com expoente e*(p,k); equivalência e otimalidade
│   └── nota_27_cota_rho_min.md             ← cota assintótica para ρ_min(k); limiar adaptativo
└── notebooks/
    ├── benchmark_espectral.ipynb
    ├── crivo_espectral_v2.ipynb
    ├── crivo_sem_oraculo.ipynb
    ├── detector_frequencia_3.ipynb
    ├── fundamentos_teoricos_v2.ipynb
    ├── exp_c_recursao.ipynb                 ← validação da recursão (substituto de ζ)
    ├── exp_d_rho_continuo.ipynb             ← separabilidade de ρ_cont para k=2..8; falha para k≥6
    ├── exp_e_rho_adapt.ipynb                ← ρ_adapt com e*(p,k); separação restaurada; recursão sem aritmética inteira
    └── exp_f_rho_min.ipynb                  ← cota assintótica de ρ_min(k); padrão estrutural; extrapolação do limiar
```

---

## Notas

### Nota 16 — Conexão Espectral entre Blocos Binários e a Hierarquia Primorial

$Q(p)$ contém todos os primos menores que $p$ como divisores — consequência do Teorema 1 dos [blocos binários](https://github.com/tiagobandeira/primalidade-blocos-binarios). Introduz a análise de $Z_Q/\zeta$ e identifica o efeito de cancelamento: a divisão por $\zeta$ remove os primos do intervalo $[2^{n-1}, p-1]$, recuperando apenas os primos menores que $2^{n-1}$. Motivação para o pipeline de dois estágios da Nota 17.

### Nota 17 — Ferramenta Espectral via $Q(p)$: Fundamentação e Validação

Resolve o cancelamento com o pipeline de dois estágios. Validado para $p \in \{37, 41, 53\}$, com recuperação de 100% dos primos para $p \leq 41$ e 93% para $p = 53$ (primo 41 recuperável com $t_{\max} = 300$).

### Nota 18 — Benchmark Espectral: Primorial, Fatorial e $Q(p)$

Compara as três funções como base para extração espectral ($p \in \{37, 41, 53\}$):

| Função | Taxa média | Tempo médio |
|--------|-----------|-------------|
| $Q(p)$ | **97,8%** | **0,08 s** |
| Primorial P# | 92,0% | 0,12 s |
| Fatorial $(p-1)!$ | 31,3% | 5,46 s |

$Q(p)$ supera inclusive o primorial. Na faixa $f \in [0.4, 0.6]$ (bloco binário), exibe picos quase periódicos de alta nitidez ausentes nos outros extratores — o recorte binário atua como filtro natural de banda passante.

Resultados do `fundamentos_teoricos_v2.ipynb` (Exp 3 e 4b) respondem as questões assintóticas: o SNR da Etapa 1 é estável em $[0.72, 0.98]$ para $p \leq 499$; o SNR da Etapa 2 é o gargalo (cai com $p$, requer $t_{\max}$ crescente). O valor mínimo de $\rho$ entre primos do bloco decai com $p$ mas permanece acima de $3{,}3 \times 10^{-4}$ para $p \leq 499$.

### Nota 19 — Detector Espectral de Primalidade: da Razão $R(k)$ à Irredutibilidade Logarítmica

Três abordagens progressivas para detecção do próximo primo sem oráculo. A formulação final: $m$ é primo $\iff$ $\log m$ é irredutível no reticulado inteiro gerado por $\{\log p_i : p_i < m\}$. O resíduo contínuo $\rho(m)$ atinge 80,1% de separação sem aritmética inteira. Resultado inesperado: correlação negativa entre $\rho(m)$ e distância ao primo mais próximo (Spearman $-0.45$) — compostos próximos de primos têm resíduo *maior*, não menor.

Contém tabela empírica de $t_{\min}$ para pares gêmeos até $(461, 463)$, confirmando crescimento $\sim p / \log p$.

### Nota 20 — Crivo Espectral sem Oráculo de Primalidade (versão original)

Elimina `isprime()` substituindo-o pelo critério $\rho(m \mid \mathcal{P}_<) > \rho^*$, onde $\mathcal{P}_< = \{q \text{ primo} : q < 2^{n-1}\}$. O pipeline inverte a ordem das etapas (Etapa 2 → Etapa 1). **Ainda usava $\zeta$ na Etapa 2.** Validado para $p \in \{37, 41, 53, 59, 67\}$. A versão final, que elimina $\zeta$, é documentada nas Notas 23 e 24.

### Nota 21 — Formalização do Crivo Espectral Oracle-Free

Formaliza a teoria a partir de uma definição central — Redutibilidade Logarítmica — da qual todos os resultados derivam. Estrutura:

- **Proposição:** $m$ é logaritmicamente irredutível $\iff$ $m$ é primo (prova via TFA)
- **Lema $\rho$:** $\rho(m \mid \mathcal{P}_<) = 0 \iff m$ é composto no bloco (corolário do Teorema 1 da Nota MDC)
- **Teorema de Invariância:** $\mathcal{R}_m$ remove a contribuição de $m$ sem afetar nenhum primo $q \neq m$, no limite $T \to \infty$ (prova via ortogonalidade das funções de Dirichlet)
- **Corolário:** após eliminação iterativa dos redutíveis, os sobreviventes são exatamente os primos do bloco

A FFT não é objeto da teoria — é o instrumento que implementa o Corolário na prática.

### Nota 22 — Método do Crivo Espectral Oracle-Free

Descrição reproduzível e agnóstica de linguagem do algoritmo. Contém pseudocódigo completo, tabela de parâmetros com justificativas, checklist de verificação da implementação, e documentação das limitações conhecidas com soluções. Parâmetros recomendados: $t_{\max} > 2\pi/(\log q_2 - \log q_1)$ para o par mais próximo no bloco; $\rho^* = 10^{-6}$ (robusto para $p \leq 499$).

### Nota 23 — Extração Recursiva de Primos via Blocos Binários: Substituição de $\zeta$ na Etapa 2

**Elimina completamente $\zeta$.** A Etapa 2 (extração de $\mathcal{P}_<$) é substituída por uma recursão sobre os blocos $A_k = [2^k, 2^{k+1}-1]$, que constrói $\mathcal{P}_<$ indutivamente usando apenas o critério $\rho_B$ e divisibilidade. A correção é provada por indução a partir do Teorema 1 da Nota MDC. Validado para $n \in \{5,6,7,8\}$ (primos até $511$) com 100% de acerto. O pipeline resultante opera inteiramente sem dependências analíticas externas.

### Nota 24 — Pré-limpeza e Equivalência com a Versão com $\zeta$

**Completa a autonomia do método.** A pré-limpeza — passo explícito antes do crivo iterativo — subtrai de uma só vez todos os compostos do bloco (identificados por $\rho_B(m \mid \mathcal{P}_<)=0$), replicando o efeito de $\log|Z_Q| - \log|Z_{\text{compostos}}|$ que antes era obtido via $\zeta$. O sinal residual inicial contém apenas os primos do bloco, maximizando o SNR desde o início. A correção é garantida pelo Lema $\rho$ (Nota 20). A versão final do pipeline (Nota 23 + Nota 24) é **autônoma**: sem $\zeta$, sem `isprime()`, sem qualquer referência analítica externa.

### Nota 25 — Critério $\rho$ sem Aritmética Inteira: Separabilidade Logarítmica e Limites de Escala

Investiga se o teste de divisibilidade `m % b == 0` dentro de $\rho_B$ pode ser eliminado, substituindo-o pela versão puramente contínua $\rho_{\text{cont}}$, que mede a distância de $\log m$ ao reticulado gerado por $\{\log b\}$. Os experimentos (Exp D) mostram separação perfeita para $k \leq 5$ e colapso para $k \geq 6$: compostos com muitas potências de primos pequenos (ex: $96 = 2^5 \cdot 3$) produzem $\rho_{\text{cont}}$ da mesma ordem que primos do bloco quando o teto de expoentes é fixo. A causa é identificada: compostos exigem expoentes crescentes com $k$, enquanto a implementação usava teto fixo $e \leq 4$. Conclui que a aritmética inteira é o algoritmo ótimo para o critério quando a base é inteira — não uma dependência conceitual — e propõe $\rho_{\text{adapt}}$ com expoente adaptativo como questão aberta.

### Nota 26 — Equivalência entre Divisibilidade e Irredutibilidade Logarítmica Adaptativa

**Fecha as questões abertas das Notas 23 e 25.** Introduz o critério $\rho_{\text{adapt}}$ com expoente máximo adaptativo por bloco:

$$e^*(p, k) = \left\lfloor \frac{k \log 2}{\log p} \right\rfloor$$

**Proposição (demonstrada):** com esse expoente, $\rho_{\text{adapt}}(m) = 0$ exato para todo composto $m \in A_k$, e $\rho_{\text{adapt}}(q) > 0$ para todo primo $q \in A_k$ — separação perfeita para todo $k$. O Exp E confirma: zero FP, zero FN para $k = 2, \ldots, 9$; a recursão $C_1$ com $\rho_{\text{adapt}}$ reproduz exatamente o resultado com divisibilidade pura para $n_{\text{alvo}} = 5, \ldots, 10$.

Conclusão dupla:
- **Conceitualmente:** o critério de irredutibilidade logarítmica é genuinamente contínuo — a separação existe no domínio dos logaritmos sem aritmética inteira, dado que a profundidade de busca seja adaptada ao bloco. A dependência da aritmética inteira nas Notas 20–24 não era conceitual.
- **Algoritmicamente:** `m % p == 0` é o algoritmo ótimo — resolve em $O(|\mathcal{S}_k|)$ o que $\rho_{\text{adapt}}$ resolve em $O(|\mathcal{S}_k|^2 \cdot k^2)$, aproveitando a estrutura da divisão euclidiana para eliminar a busca de expoentes.

### Nota 27 — Cota Assintótica para $\rho_{\min}(k)$ e Limiar Adaptativo

**Fecha a Questão 1 da Nota 26.** Determina o comportamento assintótico de $\rho_{\min}(k)$ — o menor valor de $\rho_{\text{adapt}}$ entre primos do bloco $A_k$ — e a escala em que o limiar $\rho^* = 10^{-6}$ se torna insuficiente.

O Exp F revela um padrão estrutural preciso: o primo que realiza $\rho_{\min}(k)$ é sempre o **maior primo do bloco**, e a combinação logarítmica mais próxima é sempre o vizinho composto imediato $q \pm 1$. Isso reduz o problema a uma questão sobre gaps de primos:

$$\rho_{\min}(k) \approx \frac{1}{q_{\max} \cdot \log q_{\max}} \gtrsim \frac{1}{2^{k+1}(k+1)\log 2}$$

A razão observado/cota converge para $1$ conforme $k$ cresce (razão $= 1{,}005$ para $k = 10$) — a cota é assintoticamente tight. A rota via Baker, investigada e descartada, é frouxa por $10^{20}$–$10^{95}$: o problema é de distribuição de primos, não de teoria transcendente.

Consequências práticas:

| $\rho^*$ | $k$ seguro | Escala de primos |
|---|---|---|
| $10^{-6}$ (atual) | $k \leq 15$ | $p \lesssim 32768$ |
| $10^{-8}$ | $k \leq 21$ | $p \lesssim 4 \times 10^6$ |
| $10^{-10}$ | $k \leq 27$ | $p \lesssim 10^8$ |

Para escalas além de $k \approx 16$, o limiar adaptativo $\rho^*(k) = c\,/\,(2^{k+1}(k+1)\log 2)$ com $c = 0{,}1$ garante margem de $10\times$ em qualquer bloco.

---

## Notebooks

| Notebook | Conteúdo |
|---|---|
| `benchmark_espectral.ipynb` | Comparação $Q(p)$ vs primorial vs fatorial; métricas de precisão, tempo e eficiência |
| `crivo_espectral_v2.ipynb` | Crivo por subtração iterativa de $S_m(t)$ sem lista prévia de compostos (versão original com $\zeta$) |
| `crivo_sem_oraculo.ipynb` | Pipeline sem `isprime()`, com $\rho$ e recursão (pré-limpeza incluída na versão final) |
| `detector_frequencia_3.ipynb` | Irredutibilidade logarítmica; distribuição de $\rho(m)$; correlação com distância ao primo |
| `fundamentos_teoricos_v2.ipynb` | SNR como função de $p$ até 499; estabilidade de $\rho_{\min}$; $t_{\min}$ para pares gêmeos |
| `exp_c_recursao.ipynb` | Validação da extração recursiva de primos via blocos binários (substituto de $\zeta$). Cobre níveis até $2^8$, confirmando 100% de acerto sem falsos positivos |
| `exp_d_rho_continuo.ipynb` | Separabilidade de $\rho_{\text{cont}}$ (teto fixo) para $k=2,\ldots,8$. Mostra colapso para $k \geq 6$ e identifica os compostos escapados e sua causa estrutural |
| `exp_e_rho_adapt.ipynb` | $\rho_{\text{adapt}}$ com $e^*(p,k)$ adaptativo: separação restaurada para $k=2,\ldots,9$; recursão $C_1$ sem aritmética inteira com 100% de acerto até $n=10$ |
| `exp_f_rho_min.ipynb` | Cota assintótica de $\rho_{\min}(k)$: padrão estrutural (maior primo do bloco), cota tight $\sim 1/(2^{k+1}(k+1)\log 2)$, comparação com Baker, limiar adaptativo |

---

## Dependências

```bash
pip install numpy scipy mpmath sympy
```

O cálculo de $\zeta(1/2 + it)$ via mpmath **não é mais necessário** na versão final (Notas 23–24). Permanece apenas para comparação histórica nos notebooks originais.

---

## Estado atual da série

As Notas 16–27 constituem um corpo completo e autocontido:

- **Teoria** (Notas 21, 23, 26): Proposição de equivalência primo/irredutível, Teorema de Invariância, Proposição de extração recursiva, Proposição de equivalência $\rho_{\text{adapt}}$/divisibilidade — todas com demonstrações.
- **Método** (Notas 22, 23, 24): pipeline reproduzível, autônomo, sem $\zeta$, sem `isprime()`, com parâmetros justificados.
- **Validação** (Notas 17–20, Exp C, D, E): cobertura empírica de $p \leq 499$ para o crivo espectral; primos até $2^{10}$ para a recursão; separabilidade de $\rho_{\text{adapt}}$ verificada para $k \leq 9$.
- **Escala** (Nota 27, Exp F): cota assintótica tight para $\rho_{\min}(k)$; limiar adaptativo formalizado para qualquer $k$.

A natureza do critério $\rho_B$ está completamente esclarecida (Nota 26): é um critério geométrico no espaço logarítmico, implementável sem aritmética inteira via $\rho_{\text{adapt}}$, e a aritmética inteira é sua implementação ótima. A escala de validade do limiar $\rho^*$ está agora formalizada (Nota 27): seguro até $k \approx 15$ com o valor atual; adaptável para qualquer escala via $\rho^*(k) = c\,/\,(2^{k+1}(k+1)\log 2)$.

---

## Questões abertas

1. **Escala de $t_{\max}$** — para primos gêmeos, $t_{\min} \sim O(p / \log p)$ empiricamente (Nota 19, tabela até $p = 463$). A questão analítica — se existe $t_{\max}$ polinomial em $p$ que garanta separação de todos os pares — está em aberto.

2. **SNR assintótico da Etapa 2** — o SNR da Etapa 1 é estável para $p \leq 499$; o da Etapa 2 degrada. A escala exata de $t_{\max}$ necessária para manter SNR > 1 na Etapa 2 como função de $n$ está em aberto.

3. **Crivo espectral autônomo completo** — existe operador que, a partir dos picos irredutíveis de $Z_{Q(p)}$, produz o próximo primo sem aritmética inteira e sem $\zeta$? (Questão 4, Nota 19.)

4. **Prova formal do padrão de $\rho_{\min}$** — a observação de que o maior primo do bloco sempre realiza $\rho_{\min}(k)$ foi verificada empiricamente para $k \leq 11$ e sustenta a cota assintótica da Nota 27. Uma prova formal precisaria mostrar que nenhum primo interior ao bloco tem distância logarítmica menor ao reticulado que o primo do topo. Envolve propriedades da distribuição de primos no bloco que não foram formalizadas.

5. **Conexão entre escala de $\rho^*$ e escala de $t_{\max}$** — a condição $\rho^*(k) \sim 1/(q_{\max} \log q_{\max})$ e a condição espectral $t_{\max} \sim q/\log q$ têm a mesma dependência em $q/\log q$. A formalização dessa equivalência — de que resolução aritmética e resolução espectral crescem à mesma taxa — está em aberto (Nota 27, Questão 3).

6. **Ressonância espectral como detector de fatores** — pode-se detectar diretamente a existência de um fator primo comum entre dois números pela interferência de seus picos, evitando qualquer divisibilidade? (Hipótese B, Nota 20.)

---

## Conexões

- **[Motor de Herança Estrutural](https://github.com/tiagobandeira/conjectura-de-goldbach)** — série sobre Goldbach que motivou este trabalho; as sequências $L(P_n)$ (Nota 14) e classes residuais módulo primoriais (Nota 15) estão nessa série.
- **[Primalidade por Blocos Binários](https://github.com/tiagobandeira/primalidade-blocos-binarios)** — Teorema 1 (caracterização por MDC) e Proposição 2 (divisibilidade por $P(N)$), que fundamentam o classificador $\rho$ da Nota 20 e a Proposição da Nota 21.

---

## Citação

```
T. Bandeira, "Análise Espectral de Primos via Produtos de Intervalos Binários",
notas de pesquisa independente, 2026.
DOI: 10.5281/zenodo.20648983
```

---

## Licença

- Documentação e notas matemáticas: [CC BY 4.0](LICENSE.txt)
- Código-fonte: [MIT License](LICENSE-MIT.txt)