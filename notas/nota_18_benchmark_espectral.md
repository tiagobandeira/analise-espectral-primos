# Nota 18 — Benchmark Espectral: Primorial, Fatorial e $Q(p)$ como Bases para Extração de Primos

**T. Bandeira · Junho de 2026**  
*Nota adicional motivada pela série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Comparamos sistematicamente três funções como base para extração espectral de primos via FFT de $\log|Z(\frac{1}{2}+it)|$: o primorial $P\#(p)$, o fatorial $(p-1)!$ e o produto $Q(p)$ sobre o bloco binário $[2^{n-1}, p-1]$ (Nota 17). O primorial serve como referência natural — contém exatamente os primos sem compostos — e os experimentos mostram que $Q(p)$ atinge taxa de acertos de 97,8% em média, superior ao primorial (92,0%) e ao fatorial (31,3%), com o menor tempo de cálculo médio de sinal (0,08 s) e overhead de apenas 2,2× sobre o primorial em tamanho de intervalo. O fatorial revelou-se o extrator mais fraco: perde em média 8,7 primos por caso e exige 3,3× mais elementos que o primorial. Além dos dados quantitativos, a análise visual dos espectros revela que na faixa $f \in [0.4, 0.6]$, correspondente aos primos do bloco binário de $Q(p)$, o sinal exibe picos quase periódicos de alta nitidez — estrutura ausente no primorial e fatorial. Interpretamos esse fenômeno como consequência do recorte binário, que atua como filtro natural de banda passante. A nota encerra com quatro questões sobre comportamento assintótico do método: a Questão 1 (escala de $t_{\max}$ para gaps pequenos) e a Questão 2 (colapso estrutural) permanecem em aberto; a Questão 3 (SNR assintótico) foi parcialmente respondida — Etapa 1 estável, Etapa 2 é o gargalo —; a Questão 4 ($\rho_{\min}$ e separabilidade logarítmica) foi respondida experimentalmente para $p \leq 499$.

---

## 1. Motivação

A Nota 17 validou o pipeline de dois estágios para extração espectral de primos a partir de $Z_Q(s)$. Uma questão natural que emerge é: a estrutura de $Q(p)$ é essencial para o funcionamento do método, ou qualquer produto de inteiros contendo os primos como fatores seria igualmente eficaz?

Para responder concretamente, definimos três funções geradoras e as comparamos sob as mesmas condições de amostragem e detecção:

| Função | Definição formal | Intervalo |
|--------|-----------------|-----------|
| Primorial $P\#$ | $\prod_{q < p,\, q \text{ primo}} q$ | $\{\text{primos} < p\}$ |
| Fatorial $(p-1)!$ | $\prod_{x=2}^{p-1} x$ | $[2, p-1]$ |
| $Q(p)$ | $\prod_{x=2^{n-1}}^{p-1} x$, $n = \lfloor\log_2 p\rfloor$ | $[2^{n-1}, p-1]$ |

A cada uma associa-se uma função $Z(s) = \prod_{x \in I} (1 - x^{-s})^{-1}$ e o sinal $\log|Z(\frac{1}{2}+it)|$ analisado via FFT. O primorial é a referência: seu intervalo contém exatamente os primos, sem compostos, produzindo sinal puro.

---

## 2. Metodologia

### 2.1 Função geradora e sinal espectral

Para cada conjunto de inteiros $I$, define-se:

$$Z_I(s) = \prod_{x \in I} \frac{1}{1 - x^{-s}}, \qquad s = \tfrac{1}{2} + it$$

$$\log|Z_I(\tfrac{1}{2}+it)| = -\frac{1}{2} \sum_{x \in I} \log\!\left(1 - 2x^{-1/2}\cos(t\log x) + x^{-1}\right)$$

Cada $x \in I$ contribui com uma oscilação de frequência característica $f_x = \log(x)/(2\pi)$. A FFT do sinal em $t$ decompõe essa superposição; a inversão $q = \mathrm{round}(e^{2\pi f})$ recupera os inteiros a partir dos picos.

### 2.2 Pipelines de extração

**Primorial:** FFT direta de $\log|Z_{P\#}|$. Não há compostos no intervalo, portanto nenhuma subtração é necessária.

**Fatorial e $Q(p)$:** pipeline de dois estágios da Nota 17. Na Etapa 1 subtraem-se os compostos da metade superior para isolar os primos grandes; na Etapa 2 usa-se $\zeta$ para revelar os primos pequenos via seus múltiplos compostos.

### 2.3 Parâmetros

Todos os experimentos usam $t_{\max} = 150$, $\Delta t = 0.05$, produzindo $N = 2998$ amostras e resolução espectral $\Delta f \approx 0.00334$. Os casos testados são $p \in \{37, 41, 53\}$.

---

## 3. Resultados quantitativos

### 3.1 Tabela completa

| $p$ | Função | $\vert I \vert$ | Taxa | FP | Perdidos | $\Delta_\text{sim}$ | $t$ (s) |
|-----|--------|-------|------|----|----------|---------------------|---------|
| 37 | Primorial | 11 | 91% | 0 | \{29\} | 9% | 0,29 |
| 37 | Fatorial | 35 | 27% | 0 | \{2,5,7,11,13,17,19,29\} | 73% | 16,20 |
| 37 | $Q(p)$ | 21 | **100%** | 0 | — | **0%** | **0,08** |
| 41 | Primorial | 12 | 92% | 0 | \{29\} | 8% | 0,04 |
| 41 | Fatorial | 39 | 33% | 0 | \{2,5,7,11,13,17,19,29\} | 67% | 0,11 |
| 41 | $Q(p)$ | 25 | **100%** | 0 | — | **0%** | **0,08** |
| 53 | Primorial | 15 | 93% | 0 | \{41\} | 7% | 0,04 |
| 53 | Fatorial | 51 | 33% | 0 | \{2,5,7,11,13,17,19,23,29,41\} | 67% | 0,08 |
| 53 | $Q(p)$ | 37 | 93% | 0 | \{41\} | 7% | 0,09 |


Parâmetros: $t_{\max}=150$, $\Delta t=0.05$. FP = falsos positivos; $\Delta_\text{sim}$ = distância simétrica normalizada.

### 3.2 Resumo por função (médias sobre $p \in \{37,41,53\}$)

| Função | Taxa média | FP médio | Perdidos médio | Tempo médio (s) | $\vert I \vert$ médio | Overhead |
|--------|-----------|----------|----------------|-----------------|-------------|----------|
| Primorial | 92,0% | 0,0 | 1,0 | 0,12 | 13 | 1,0× |
| $Q(p)$ | **97,8%** | 0,0 | **0,3** | **0,08** | 28 | 2,2× |
| Fatorial | 31,3% | 0,0 | 8,7 | 5,46 | 42 | 3,3× |

O resultado mais inesperado é que $Q(p)$ supera o primorial em taxa média — 97,8% contra 92,0% — com zero falsos positivos nos três casos. O primorial perde o primo 29 de forma consistente nos três experimentos; $Q(p)$ recupera 29 em $p \in \{37, 41\}$ e perde apenas 41 para $p = 53$ (mesmo caso do primorial). O fatorial é o extrator mais fraco por larga margem em precisão, e o mais lento para $p = 37$ (16,2 s contra 0,08 s de $Q$, diferença de 200×, devida ao cálculo de $\zeta$ no primeiro uso).

### 3.3 Eficiência: acertos por elemento do intervalo

$$\eta = \frac{|\text{primos acertados}|}{|I|}$$

| $p$ | Primorial $\eta$ | $Q(p)$ $\eta$ | Fatorial $\eta$ |
|-----|-----------------|--------------|----------------|
| 37 | 0,909 | 0,524 | 0,086 |
| 41 | 0,917 | 0,480 | 0,103 |
| 53 | 0,933 | 0,378 | 0,098 |

O primorial é intrinsecamente mais eficiente por construção. $Q(p)$ supera o fatorial em eficiência por fator de 4–6×, o que reflete o recorte do bloco binário: cada elemento de $[2^{n-1}, p-1]$ carrega informação primorial concentrada, enquanto o fatorial dilui com todos os inteiros de $[2, 2^{n-1}-1]$.

### 3.4 Padrão de primos perdidos

O primo 29 é perdido consistentemente pelo primorial e pelo fatorial para $p \in \{37, 41\}$, mas recuperado por $Q(p)$. Para $p = 53$, o primo 41 é perdido pelas três funções — recuperável aumentando $t_{\max}$ para 300, conforme documentado na Nota 17. O fatorial perde adicionalmente um bloco fixo de primos pequenos $\{2, 5, 7, 11, 13, 17, 19\}$ em todos os casos, sugerindo falha sistemática da Etapa 2 para o fatorial, não um problema de resolução.

Nenhuma função produziu falsos positivos neste experimento — diferente dos resultados da Nota 17 com parâmetros distintos. Com $t_{\max} = 150$ e $\Delta t = 0.05$ os compostos $\{4, 8, 9\}$ não foram detectados como picos, sugerindo que o limiar `altura_rel = 0.03` foi suficiente para filtrá-los.

---

## 4. Análise espectral qualitativa

### 4.1 Amplitudes nos primos reais

A tabela a seguir mostra a amplitude espectral normalizada de cada função nas frequências dos primos reais para $p = 37$:

| Primo | Primorial | Fatorial | $Q(p)$ |
|-------|-----------|----------|--------|
| 2 | 0,885 | 0,634 | 0,010 |
| 3 | **1,000** | 0,735 | 0,013 |
| 5 | 0,631 | 0,490 | 0,020 |
| 7 | 0,495 | 0,401 | 0,029 |
| 11 | 0,487 | 0,382 | 0,059 |
| 13 | 0,422 | 0,253 | 0,089 |
| 17 | 0,351 | 0,327 | 0,830 |
| 19 | 0,299 | 0,178 | 0,981 |
| 23 | 0,352 | 0,275 | **1,000** |
| 29 | 0,203 | 0,129 | 0,707 |
| 31 | 0,325 | 0,240 | 0,897 |

O contraste é imediato. No primorial e no fatorial, a amplitude decresce monotonicamente dos primos pequenos para os grandes, com máximo em $q = 3$ e valores ainda significativos em toda a faixa. Em $Q(p)$, o padrão é invertido: amplitudes próximas de zero para primos pequenos ($q \leq 13$) e amplitudes dominantes para primos do bloco ($q \geq 17$). O primo 23 é o de maior amplitude em $Q(37)$; o primo 3 domina no primorial. Esse comportamento reflete diretamente a composição dos intervalos.

### 4.2 O sinal $\log|Z|$ como função de $t$

Os três sinais exibem comportamento quasi-periódico em $t$, visualmente semelhante a um sinal de áudio multitonal. Após remoção da média no pré-processamento da FFT, o sinal apresenta aparência de quase-simetria em relação ao eixo $y = 0$. Isso é consequência da estrutura oscilatória: cada termo $-\frac{1}{2}\log(1 - 2a_x\cos(t\log x) + a_x^2)$ oscila em torno de seu valor médio, e após centralização o sinal resultante é equilibrado. A amplitude característica de cada componente decai como $x^{-1/2}$, de modo que inteiros pequenos dominam a envolvente — daí o sinal do primorial e do fatorial ter amplitude mais alta que o de $Q(p)$ nos instantes $t$ iniciais.

### 4.3 Picos quase periódicos na faixa $f \in [0.4, 0.6]$

Esta é a observação qualitativa mais interessante do experimento. A faixa $f \in [0.4, 0.6]$ corresponde a inteiros $x \approx [12, 43]$, precisamente o bloco binário de $Q(53)$: $[16, 52]$.

No espectro de $Q(p)$, essa faixa exibe picos de alta nitidez com separação limpa e nível de fundo baixo entre eles — estrutura análoga a linhas espectrais atômicas, com cada primo do bloco gerando um pico isolado. Nos espectros do primorial e do fatorial, a mesma faixa apresenta picos de altura variável com deformações entre eles, resultando numa aparência mais "ruidosa".

**Interpretação:** o recorte binário de $Q(p)$ atua como filtro de banda passante natural. Ao excluir os inteiros $[2, 2^{n-1}-1]$, excluem-se também seus primos, cujas amplitudes $a_x = x^{-1/2}$ são altas e modulam todo o sinal. No primorial, os primos pequenos estão presentes com amplitudes dominantes e interferem na região de frequências altas. No fatorial, os compostos de $[2, 15]$ adicionam ruído contínuo de baixa frequência que vaza para a faixa $[0.4, 0.6]$. Em $Q(p)$, o sinal $R_1 = \log|Z_Q/Z_\text{comp}|$ da Etapa 1 — responsável pelos picos nessa faixa — está livre dessa interferência. O resultado é um sinal quase puro de cossenos, cada um numa frequência prima bem definida.

Na faixa $f < 0.4$ o comportamento se inverte: $Q(p)$ exibe amplitudes próximas de zero (dados da Seção 4.1), enquanto primorial e fatorial têm amplitudes altas. Os primos pequenos são detectados por $Q$ apenas indiretamente via Etapa 2, com sinal mais fraco.

---

## 5. Relação hierárquica entre os três produtos

Os três produtos são hierarquicamente relacionados por divisibilidade:

$$P\#(p) \mid Q(p) \mid (p-1)!$$

O primorial divide $Q(p)$ pelo Teorema 1 da Nota sobre blocos binários: todo primo $q < p$ divide algum elemento de $[2^{n-1}, p-1]$, logo divide $Q(p)$. Por sua vez, $Q(p)$ divide $(p-1)!$ porque $[2^{n-1}, p-1] \subset [2, p-1]$.

Essa hierarquia de divisibilidade reflete diretamente a hierarquia de ruído espectral: mais compostos no intervalo implica mais frequências parasitas, maior nível de fundo e maior dificuldade de separação de picos. Os dados confirmam essa ordem: o fatorial, com mais compostos, é o mais ruidoso e perde mais primos; o primorial, sem compostos, é o mais limpo; $Q(p)$ é intermediário — e os compostos que contém são necessários para a Etapa 2 carregar a assinatura dos primos pequenos.

---

## 6. Questões abertas

**Questão 1 — Escala de $t_{\max}$.**
A separabilidade espectral de dois primos consecutivos $q_1 < q_2$ requer $t_{\max} > 2\pi/(\log q_2 - \log q_1)$. O gap médio entre primos em torno de $q$ é $\log q$ pelo teorema dos números primos, sugerindo $t_{\max} \sim O(q/\log q)$ em média. Gaps excepcionalmente pequenos — como os dos primos gêmeos $q_2 - q_1 = 2$ — forçam $t_{\max}$ muito maior. A pergunta precisa: existe $t_{\max}(p)$ polinomial em $p$ que garanta separação de todos os pares abaixo de $p$, ou gaps excepcionalmente pequenos forçam crescimento super-polinomial?

**Questão 2 — Colapso estrutural.**
Separado do problema de resolução numérica, existe uma obstrução combinatória? Ou seja, existe $p$ para o qual dois primos $q_1, q_2 < p$ produzem assinaturas espectrais idênticas em $Z_Q$ independentemente de $t_{\max}$? Isso requereria que os dois primos contribuíssem com padrões de interferência idênticos em todos os compostos do bloco — condição extremamente restritiva cuja impossibilidade não está demonstrada.

**Questão 3 — SNR assintótico e ruído proporcional** *(parcialmente respondida).*
Os experimentos do Exp 3 (`fundamentos_teoricos_v2`, $p \in [37, 499]$) forneceram resposta para as duas sub-perguntas:

- **Etapa 1 (primos do bloco):** o SNR mínimo permanece estável no intervalo $[0{,}72,\, 0{,}98]$ para $n \in \{5, 6, 7, 8\}$, sem degradação sistemática. A conjectura está confirmada: os compostos do bloco têm $x \geq 2^{n-1}$, excluindo estruturalmente os inteiros pequenos de alta amplitude que degradariam o sinal. O SNR da Etapa 1 não é um gargalo assintótico.

- **Etapa 2 (primos de $\mathcal{P}_<$ via múltiplos compostos):** o SNR mínimo cai de $\approx 3{,}8$ para $n=5$ até $\approx 0{,}22$ para $n=7$, com recuperação parcial para $n=8$. A Etapa 2 é o **gargalo identificado**: a detectabilidade dos primos pequenos via seus múltiplos compostos degrada com $p$ crescente. A solução prática é aumentar $t_{\max}$; a regra empírica $t_{\max} > 2\pi/(\log q_2 - \log q_1)$ para o par mais próximo em $\mathcal{P}_<$ é necessária e suficiente para os casos testados.

A questão em aberto passa a ser a escala exata de $t_{\max}$ necessária para manter SNR $> 1$ na Etapa 2 como função de $n$ — conectando diretamente à Questão 1 sobre gaps de primos gêmeos.

**Questão 4 — Separabilidade logarítmica e decaimento de $\rho_{\min}$** *(respondida experimentalmente).*
Experimentos sobre o classificador $\rho(m \mid \mathcal{P}_<)$ (Nota 20, Exp 4b, `fundamentos_teoricos_v2`) mediram o valor mínimo de $\rho$ entre os primos do bloco para $p \in [37, 499]$:

| $p$ | $n$ | $\rho_{\min}$ | $q$ (ρ mín) |
|-----|-----|--------------|-------------|
| 37  | 5   | 0,00925      | 31          |
| 53  | 5   | 0,00611      | 43          |
| 59  | 5   | 0,00471      | 53          |
| 97  | 6   | 0,00252      | 89          |
| 131 | 7   | 0,00162      | 127         |
| 251 | 7   | 0,00075      | 241         |
| 499 | 8   | 0,00033      | 487         |

$\rho_{\min}$ decai com $p$, mas permanece no intervalo $[3{,}3 \times 10^{-4},\, 9{,}3 \times 10^{-3}]$ — muitas ordens de grandeza acima de qualquer erro de ponto flutuante em precisão dupla ($\sim 10^{-15}$). A separação logarítmica entre primos e compostos do bloco **não colapsa** na faixa testada: compostos têm $\rho = 0$ exato (pelo Corolário do Teorema 1 da Nota MDC), e o gap mínimo observado é $\approx 3{,}3 \times 10^{-4}$. O limiar de classificação deve satisfazer $\rho^* < \rho_{\min}$; o valor $\rho^* = 10^{-6}$ é robusto para toda a faixa testada. A questão de se $\rho_{\min}$ tende a zero ou estabiliza para $p \to \infty$ permanece em aberto, mas a evidência empírica não indica colapso iminente.

---



O experimento estabelece três resultados concretos. Primeiro, $Q(p)$ é o melhor extrator entre os três: taxa média de 97,8%, zero falsos positivos, tempo médio de 0,08 s, superando inclusive o primorial em precisão nos casos $p \in \{37, 41\}$. Segundo, o fatorial é o pior extrator por larga margem — 31,3% de taxa média e perda sistemática dos primos pequenos $\{2, 5, 7, 11, 13, 17, 19\}$ — indicando que a Etapa 2 adaptada para o fatorial é menos eficaz que a original de $Q$. Terceiro, a estrutura espectral de $Q(p)$ na faixa do bloco binário é qualitativamente distinta: picos quase periódicos de alta nitidez que não aparecem no primorial nem no fatorial, resultado direto do recorte binário como filtro de banda.

Esses resultados validam que o bloco $[2^{n-1}, p-1]$ não é apenas uma escolha conveniente de intervalo, mas uma escolha matematicamente motivada com consequências espectrais mensuráveis. O Teorema 1 da Nota sobre blocos binários garante a completude informacional do bloco; o benchmark mostra que essa completude se traduz em precisão superior com custo menor.

---

## Referências

[Nota 1] T. Bandeira, *Uma caracterização de primalidade via partições binárias e MDC em intervalos reduzidos*, nota standalone (2026).  
[Nota 14] T. Bandeira, *Sequência de Sequências de Primos via Operador $W_i$ e Estrutura Primorial*, nota adicional (2026).  
[Nota 15] T. Bandeira, *Estrutura Primorial, Classes Residuais e Conexões com a Função Zeta*, nota adicional (2026).  
[Nota 16] T. Bandeira, *Conexão Espectral entre Blocos Binários e a Hierarquia Primorial*, nota adicional (2026).  
[Nota 17] T. Bandeira, *Ferramenta Espectral via $Q(p)$: Fundamentação e Validação Computacional*, nota adicional (2026).  
[Nota 19] T. Bandeira, *Detector Espectral de Primalidade: da Razão $R(k)$ à Irredutibilidade Logarítmica*, nota adicional (2026).  
[Nota 20] T. Bandeira, *Crivo Espectral sem Oráculo de Primalidade*, nota adicional (2026).  
[Exp 3/4b] T. Bandeira, `fundamentos_teoricos_v2.ipynb` — SNR como função de $p$ e estabilidade de $\rho_{\min}$, Junho de 2026.