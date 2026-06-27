# Nota 37 — Fatoração Prima Completa por Cascata de Colapso Orbital

**T. Bandeira · Junho de 2026**
*Nota experimental — complementa Nota 34, Nota 35 e Nota 36*

---

## Resumo

Esta nota demonstra que dois rounds de colapso orbital ("cascata") permitem a
**fatoração prima completa** de um lote de candidatos usando apenas FFTs, sem
nenhuma operação aritmética sobre os candidatos além da construção do sinal.

O algoritmo opera em rounds sequenciais: o Stage 1 remove a base $P_1 = \{2,3,5,7\}$
e classifica os cofatores como primos (encerrado) ou compostos (Stage 2). O Stage 2
subtrai $\log p$ **uma vez** do resíduo do Stage 1 de cada sub-grupo, revelando o
fator primo seguinte de cada cofator composto.

Aplicado a 10 candidatos com cofatores compostos $143 = 11 \cdot 13$ e $121 = 11^2$:

- **Stage 1:** quatro picos detectados com erros $< 0.003$ — dois primos diretos
  ($f_{11}$, $f_{17}$), dois compostos ($f_{143}$, $f_{121}$) enviados ao Stage 2.
- **Stage 2:** erros **exatamente 0.00000** em ambos os casos — incluindo detecção
  correta do quadrado perfeito $121 = 11^2$.
- **Total:** 10 candidatos completamente fatorados com **3 FFTs** em 2 rounds.

O resultado inesperado principal: **cada stage da cascata é mais preciso que o anterior**.
Stage 2 tem erro zero estruturalmente, porque sub-sinais com destino único eliminam
toda interferência residual. Isso inverte a intuição de métodos iterativos que acumulam
erro — aqui a precisão aumenta a cada round.

A cascata implementa o **Teorema Fundamental da Aritmética em linguagem espectral**:
cada inteiro tem uma árvore de fatores primos única, e a cascata a constrói de cima
para baixo, uma camada por FFT, até restar apenas frequências irredutíveis.

---

## 1. Contexto

O detector de fator comum (Nota 36) mostrou que quando $k$ candidatos compartilham
um cofator $q$ após remoção de $P$, a amplitude em $f_q$ cresce exatamente $k\times$.
A Nota 36 testou apenas cofatores primos (o detector identificava $q$ diretamente).

Esta nota generaliza para cofatores **compostos**: quando o pico em $f_q$ indica
$q = p \cdot r$ (composto), uma segunda aplicação do colapso orbital sobre o sub-grupo
do Stage 1 separa $p$ de $r$. O processo é repetível até que todos os cofatores
detectados sejam primos.

**Distinção crítica do Stage 2:** a operação não é substituir a base por $P_1 \cup \{p\}$
— isso removeria TODOS os fatores de $p$, incorreto para potências primas.
A operação correta é subtrair $\log p$ **uma vez** do resíduo do Stage 1:

$$\log_{\text{resid,S2}}(m) = \log_{\text{resid,S1}}(m) - \log p$$

Para $m$ com cofator $121 = 11^2$: $\log_{\text{resid,S1}} = \log(121)$,
então $\log_{\text{resid,S2}} = \log(121) - \log(11) = \log(11)$ — cofator
remanescente 11 (primo), não zero. Substituir a base daria $\log(121) - 2\log(11) = 0$ (errado).

---

## 2. Algoritmo da cascata

```
ENTRADA: candidatos C, base P1
SAÍDA: fatoração prima de cada m ∈ C

Stage 1:
  ① construir R_S1 = sinal de todos os candidatos com base P1
  ② detectar picos no espectro residual
  ③ classificar cofatores: primo → encerrado; composto → Stage 2

Stage 2 (para cada cofator composto q com grupo G_q):
  ④ para p = 11, 13, 17, ... (primos até √q):
       construir R_S2 = sinal de G_q com log(q) - log(p) como novo log
       detectar pico em f_{q/p}: se ratio ≈ |G_q| → q = p × (q/p), encerrado
  ⑤ se q/p ainda composto → Stage 3 com grupo G_q e novo cofator q/p

PARADA: todos os cofatores detectados são primos.
Rounds necessários = profundidade máxima da árvore de fatoração dos cofatores.
```

O número de FFTs é $1 + \sum_i d_i$, onde $d_i$ é a profundidade da árvore
do $i$-ésimo cofator composto. Para cofatores com dois fatores primos: $1 + k_c$
FFTs, com $k_c$ = número de grupos compostos no Stage 1.

---

## 3. Candidatos e estrutura esperada

| grupo | candidatos | cofator Stage 1 | estrutura esperada |
|---|---|---|---|
| Grupo 1 | 286, 429, 572, 715, 1001 | **143 = 11·13** (composto, 5×) | 2·11·13, 3·11·13, 4·11·13, 5·11·13, 7·11·13 |
| Grupo 2 | 242, 363, 484 | **121 = 11²** (composto, 3×) | 2·11², 3·11², 4·11² |
| Controle | 22, 34 | **11, 17** (primos, 1× cada) | 2·11, 2·17 |

**Resolução espectral:** para $T_{\max}=6500$, a separação $f_{143}$ vs $f_{142}$
é de 7.3 bins (acima do mínimo de 6 bins para $W=5$). A Nota 35 previu exatamente
esse limite; aqui verificamos que 7.3 bins é suficiente na prática.

---

## 4. Stage 1 — resultados

| cofator | primo | amp | razão | erro | status |
|---|---|---|---|---|---|
| 143 | Não | 7285.74 | 4.99717 | 0.00283 | COMPOSTO → S2 |
| 121 | Não | 4156.35 | 3.00036 | 0.00036 | COMPOSTO → S2 |
| 11  | Sim | 1592.03 | 0.99989 | 0.00011 | PRIMO ✓ |
| 17  | Sim | 1918.07 | 1.00051 | 0.00051 | PRIMO ✓ |

Primos detectados diretamente: $\{11, 17\}$.
Compostos a resolver: $\{143, 121\}$.

**Padrão de erros no Stage 1:** o maior erro é em $f_{143}$ (0.00283), que é o pico
mais próximo de $f_{121}$ (distância espectral 0.0266). O pico de $f_{143}$ tem
amplitude 5× e gera um sidelobe não nulo na posição de $f_{121}$, levemente
inflando a medição de $f_{143}$ a partir da interferência destrutiva parcial de $f_{121}$.
Todos os erros são $< 0.3\%$, suficientes para classificação correta com threshold de 1.8.

---

## 5. Stage 2 — resultados

### 5.1 Crack do cofator 143 = 11 × 13

**Operação:** subtrair $\log(11)$ uma vez do resíduo do Stage 1 de cada candidato do Grupo 1.

$$\log_{\text{resid,S2}}(286) = \log(143) - \log(11) = \log(13) \quad \forall m \in \text{Grupo 1}$$

Todos os 5 candidatos convergem para $f_{13}$:

| resultado | valor |
|---|---|
| amp em $f_{13}$ | 7475.88 |
| razão | **5.00000** |
| erro | **0.00000** |
| conclusão | $143 = 11 \times 13$ ✓ |

### 5.2 Crack do cofator 121 = 11²

**Operação:** subtrair $\log(11)$ uma vez (não duas!) do resíduo do Stage 1 de cada candidato do Grupo 2.

$$\log_{\text{resid,S2}}(242) = \log(121) - \log(11) = \log(11) \quad \forall m \in \text{Grupo 2}$$

O cofator remanescente é $11$ (primo), confirmando $121 = 11 \times 11$:

| resultado | valor |
|---|---|
| amp em $f_{11}$ | 4776.60 |
| razão | **3.00000** |
| erro | **0.00000** |
| conclusão | $121 = 11 \times 11 = 11^2$ ✓ |

### 5.3 Fatoração prima completa recuperada

| $m$ | fatoração recuperada pela cascata | correta |
|---|---|---|
| 286 | $2 \cdot 11 \cdot 13$ | ✓ |
| 429 | $3 \cdot 11 \cdot 13$ | ✓ |
| 572 | $2^2 \cdot 11 \cdot 13$ | ✓ |
| 715 | $5 \cdot 11 \cdot 13$ | ✓ |
| 1001 | $7 \cdot 11 \cdot 13$ | ✓ |
| 242 | $2 \cdot 11^2$ | ✓ |
| 363 | $3 \cdot 11^2$ | ✓ |
| 484 | $2^2 \cdot 11^2$ | ✓ |
| 22 | $2 \cdot 11$ | ✓ |
| 34 | $2 \cdot 17$ | ✓ |

**10/10 candidatos completamente fatorados. 3 FFTs. 2 rounds.**

---

## 6. O resultado não previsto: Stage 2 é mais preciso que Stage 1

| Stage | operação | erro |
|---|---|---|
| Stage 1 | detectar $f_{143}$ | 0.00283 |
| Stage 1 | detectar $f_{121}$ | 0.00036 |
| Stage 1 | detectar $f_{11}$ | 0.00011 |
| Stage 1 | detectar $f_{17}$ | 0.00051 |
| **Stage 2** | **crack cofator 143** | **0.00000** |
| **Stage 2** | **crack cofator 121** | **0.00000** |

Stage 2 tem erro zero porque seus sub-sinais têm **um único destino**.
Quando todos os termos de um sinal convergem para o mesmo $f_q$, a soma
é perfeitamente coerente: $k$ cópias idênticas do cosseno $-\cos(t\log q)/\sqrt{\log q}$,
sem nenhuma interferência cruzada possível. O resultado é estruturalmente exato,
não apenas aproximado.

No Stage 1, os quatro grupos coexistem no mesmo sinal. Os sidelobes do pico
de $f_{143}$ (amplitude $5 \times$) vazam levemente na posição de $f_{121}$
(distância 0.0266, separação 173 bins — pequena o suficiente para sidelobe residual).
Esse vazamento de ~0.003 explica o maior erro do Stage 1.

**Hipótese geral:** o erro de medição na cascata é proporcional à amplitude
dos vizinhos espectrais mais próximos dividida pela distância espectral.
Quando o sub-sinal tem um único destino (todos os termos coerentes), não há
vizinhos e o erro é zero. Isso prevê que **stages mais avançados da cascata
são sempre mais precisos** — propriedade oposta à de métodos iterativos
clássicos que acumulam erro.

---

## 7. Quadrados perfeitos e generalização

A detecção de $121 = 11^2$ demonstra que a cascata lida corretamente com
potências primas. A generalização:

- Para $q = p^k$: Stage 2 subtrai $\log p$ uma vez → cofator remanescente $p^{k-1}$.
  - Se $k-1 = 1$: primo, encerrado em Stage 2.
  - Se $k-1 > 1$: Stage 3 subtrai $\log p$ mais uma vez → cofator $p^{k-2}$. E assim por diante.
- Número de rounds para fatorar $p^k$: exatamente $k-1$ stages após o Stage 1.
- Para $q = p \cdot r$ ($p \neq r$, ambos primos): Stage 2 revela $r$ ao subtrair $\log p$.
  O algoritmo testa $p$ em ordem crescente — o primeiro $p$ que "encaixa" (ratio = $|\mathcal{G}_q|$)
  é o menor fator primo de $q$.

A cascata é, portanto, uma implementação espectral da **fatoração por divisão experimental**,
com duas diferenças qualitativas: (1) todos os candidatos de um grupo são processados
em paralelo em uma FFT, e (2) a confirmação do fator correto vem da razão de amplitude,
não de um teste de divisibilidade.

---

## 8. Conexão com o Teorema Fundamental da Aritmética

O Teorema Fundamental da Aritmética estabelece que todo inteiro $n > 1$ tem uma única
fatoração em primos. A cascata de colapso orbital implementa este teorema espectralmente:

| aspecto aritmético | realização espectral |
|---|---|
| Cada $n$ tem fatores primos | Cada candidato tem cofatores irredutíveis |
| Os fatores primos são únicos | Cada candidato pertence a uma única órbita em cada stage |
| Fatoração = decomposição em irredutíveis | Cascata = descascamento de camadas até $f_q$ primo |
| A fatoração termina | A cascata para quando todos os picos são primos |

A unicidade das órbitas (cada candidato pertence a exatamente uma por stage)
é a analogia direta da unicidade da fatoração. O "descascamento" de fatores
primos pela cascata é uma tradução do algoritmo de divisão repetida pelo menor
fator primo — mas operando em lote sobre todos os candidatos de um grupo
simultaneamente, em vez de candidato por candidato.

Uma observação adicional: os primos detectados ao longo da cascata são exatamente
as **frequências irredutíveis** da Nota 21 — posições espectrais que não se
deslocam sob nenhum colapso orbital. A cascata converge para eles porque são
os únicos pontos fixos do processo de remoção de fatores.

---

## 9. Status atual

| Afirmação | Status |
|---|---|
| Stage 1 classifica primos vs compostos com erro $< 0.003$ | Confirmado — 4 picos, 2 primos, 2 compostos (Seção 4) |
| Stage 2 crack de cofator semiprímo ($p \cdot r$): erro 0.00000 | Confirmado — $143 = 11 \times 13$ (Seção 5.1) |
| Stage 2 crack de quadrado perfeito ($p^2$): erro 0.00000 | Confirmado — $121 = 11^2$ (Seção 5.2) |
| Precisão crescente a cada stage (Stage 2 > Stage 1) | Confirmado e explicado por sub-sinal de destino único (Seção 6) |
| Generalização para $p^k$ com $k > 2$ (Stage 3+) | Não testado — previsto pela estrutura do algoritmo |
| Escalabilidade com $|\mathcal{C}| \gg 10$ candidatos | Não testado |
| Cofatores compostos com mais de 2 fatores primos distintos | Não testado (requer Stage 3) |
| Cofatores $> 200$ com $T_{\max}$ pela fórmula da Nota 35 | Não testado |

---

## 10. Próximos passos sugeridos

1. **Escalabilidade com $k$ grande:** testar $|\mathcal{G}_q| = 20, 50, 100$ candidatos
   compartilhando o mesmo cofator composto. A previsão é que o SNR cresce linearmente
   com $k$ (sinal = $k\times$, ruído de Stage 1 constante), tornando o detector
   mais robusto com mais candidatos — propriedade oposta ao MDC par-a-par.

2. **Stage 3 — cofatores com 3 fatores primos:** incluir candidatos com cofator
   $p \cdot r \cdot s$ (ex: $11 \cdot 13 \cdot 17 = 2431$, mas verificar resolução pela
   fórmula de $T_{\max}$ da Nota 35 antes). Stage 3 subtrai $\log r$ do resíduo do Stage 2.
   Verificar se o erro continua zero no Stage 3.

3. **Cofatores maiores com $T_{\max}$ calculado:** usar cofatores em $[100, 200]$
   e calcular $T_{\max}$ mínimo pela fórmula $(2W+1) \cdot 2\pi / \Delta f_{\min}$,
   validando que a cascata funciona sem usar o valor empírico 6500.

4. **Comparação formal com trial division em lote:** para $k$ candidatos com
   cofator $q = p \cdot r$, trial division requer $k$ divisões por $p$;
   a cascata requer 1 FFT de $k$ termos. Para $k$ grande, a FFT amortiza.
   Derivar o ponto de cruzamento em função de $k$, $T_{\max}/\Delta t$ e $|p|$.

---

## 11. Referências

[Nota 34] T. Bandeira, *Síntese Experimental: Estrutura Orbital sob Eliminação
Espectral* (2026). Estabelece a Lei do Ganho Orbital e o mecanismo de
colapso em órbitas. Esta nota usa a lei como motor de cada stage da cascata.

[Nota 35] T. Bandeira, *Verificação Espectral por Colapso Orbital* (2026).
Deriva a fórmula de $T_{\max}$ e demonstra a verificação em lote.
A escolha de candidatos e resolução espectral desta nota segue a fórmula da Nota 35.

[Nota 36] T. Bandeira, *Detector Espectral de Fator Comum em Lote* (2026).
Demonstra que a amplitude em $f_q$ identifica fatores primos compartilhados
diretamente. Esta nota estende o detector para cofatores compostos via cascata.

**Posição na série:** a sequência Nota 34 → 35 → 36 → 37 constitui uma progressão
de complexidade crescente: lei orbital → verificação → detecção → fatoração.
A cada nota, um novo nível de estrutura aritmética é revelado pela mesma operação
fundamental de colapso orbital.

---

## 12. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_cascata_colapso_orbital.ipynb` | Implementação completa: Stage 1 (classificação), Stage 2 (crack dos compostos), árvore de fatoração, resumo quantitativo |
| `cascata_stage1.png` | Stage 1: espectro com 4 picos + barras de razão (compostos vs primos) |
| `cascata_stage2.png` | Stage 2: espectro antes/depois de subtrair $\log(11)$ para cada grupo composto |
| `cascata_arvore.png` | Árvore de fatoração visual: dois rounds de colapso orbital como "descascamento" de camadas |
| `cascata_resultados.zip` | Pacote consolidado das figuras |
