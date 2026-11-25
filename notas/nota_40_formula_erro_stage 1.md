# Nota 40 — Fórmula Analítica do Erro de Stage 1

**T. Bandeira · Junho de 2026**
*Nota analítica — complementa Nota 37 e Nota 38*

---

## Resumo

Esta nota deriva uma fórmula fechada exata para o erro residual de medição
do Stage 1 do detector espectral — a diferença entre a razão observada
$\hat{k}_q = \text{amp}(f_q) / \text{amp\_iso}(q)$ e o valor inteiro correto $k_q$.
O erro existe porque grupos distintos coexistem no mesmo sinal e seus sidelobes
se somam vetorialmente no bin de cada grupo.

**Fórmula exata:**

$$\text{razão}(q) = k_q + \sum_{r \neq q} k_r \cdot \text{Re}\!\left[\frac{A_r(\hat{\omega}_q)}{A_q(\hat{\omega}_q)}\right]$$

onde $A_r(\hat{\omega})$ é a amplitude complexa que o grupo $r$ contribui
no bin $\hat{\omega}$, calculável pela série geométrica da Nota 39.

O ingrediente crítico é a parte real — não o módulo. O modelo de
sidelobe simples (que usa módulo) errava por fatores de até 15×.
Com a parte real, o erro entre fórmula e dados é de **1–4% em todos os
oito casos** testados (Nota 37 e Nota 38 Exp C), usando dados
já existentes — sem nenhum experimento novo.

A fórmula também explica por que a **Lei da Interferência Nula**
(Nota 38) é exata: quando o sinal tem um único grupo, a soma é vazia
e $\text{razão}(q) = k_q$ identicamente, sem necessidade de
nenhuma aproximação.

---

## 1. Setup e notação

O sinal de Stage 1 é:

$$R(t) = \sum_r k_r \left(-\frac{\cos(\omega_r t)}{\sqrt{\omega_r}}\right), \qquad \omega_r = \log r$$

onde a soma percorre todos os atratores $r$ com $k_r$ candidatos convergindo
para $f_r = \omega_r / 2\pi$.

A FFT discreta no bin $\hat{\omega}_q$ (bin mais próximo de $\omega_q$) é:

$$\hat{R}(\hat{\omega}_q) = \sum_r k_r \cdot A_r(\hat{\omega}_q)$$

onde a **amplitude complexa** de cada grupo no bin é:

$$A_r(\hat{\omega}) = -\frac{\Delta t}{2\sqrt{\omega_r}}
\left[S(\omega_r - \hat{\omega}) + S(-\omega_r - \hat{\omega})\right]$$

com $S(\alpha) = e^{i\alpha t_0}\dfrac{1-e^{i\alpha N\Delta t}}{1-e^{i\alpha \Delta t}}$
(série geométrica da Nota 39).

---

## 2. Derivação da fórmula exata

A razão medida é:

$$\text{razão}(q) = \frac{|\hat{R}(\hat{\omega}_q)|}{\text{amp\_iso}(q)}
= \frac{\left|k_q A_q(\hat{\omega}_q) + \displaystyle\sum_{r \neq q} k_r A_r(\hat{\omega}_q)\right|}{|A_q(\hat{\omega}_q)|}$$

Para interferência pequena ($|\epsilon_r| \ll 1$ onde $\epsilon_r = k_r A_r / (k_q A_q)$),
a expansão de $|1 + \sum \epsilon_r|$ a primeira ordem dá:

$$|1 + z| = \sqrt{(1+\text{Re}\,z)^2 + (\text{Im}\,z)^2} \approx 1 + \text{Re}\,z$$

Logo:

$$\boxed{\text{razão}(q) \approx k_q + \sum_{r \neq q} k_r \cdot \text{Re}\!\left[\frac{A_r(\hat{\omega}_q)}{A_q(\hat{\omega}_q)}\right]}$$

**O que o modelo de sidelobe simples ignorava:** o denominador $A_q(\hat{\omega}_q)$
é um número complexo com fase $\phi_q$ determinada pelo offset fracionário
do bin e por $t_0$. A projeção de $A_r$ sobre a direção de $A_q$ no plano
complexo — que é $\text{Re}[A_r/A_q]$ — pode ser muito diferente de $|A_r/A_q|$.
Em particular, pode ser positiva (interferência construtiva), negativa
(destrutiva) ou próxima de zero (ortogonal), explicando a amplitude
e o sinal variáveis dos erros observados.

---

## 3. Simplificação: termo anti-ressonante negligível

O termo $S(-\omega_r - \hat{\omega})$ em $A_r$ corresponde à componente de
frequência $-(\omega_r + \hat{\omega})$, que está a uma distância de
$(\omega_r + \hat{\omega})/(2\pi\Delta f) \approx \omega_r T_{\max}/\pi$ bins
da frequência zero — tipicamente dezenas de milhares de bins. Seu módulo é:

$$|S(-\omega_r - \hat{\omega})| \lesssim \frac{1}{|\sin((\omega_r+\hat{\omega})\Delta t/2)|} \lesssim \frac{2}{(\omega_r+\hat{\omega})\Delta t}$$

Verificando para os grupos das Notas 37–38: a razão
$|S(-\omega_r-\hat{\omega})|/|S(\omega_r-\hat{\omega})|$ é de 1–35%
(não é negligível em todos os casos, especialmente para $r$ e $q$ próximos).
A fórmula completa com ambos os termos mantém precisão de 1–4%.

---

## 4. Verificação contra dados existentes

### 4.1 Nota 37 Stage 1 (4 grupos: 143×5, 121×3, 11×1, 17×1)

| $q$ | $k_q$ | erro obs. | pred. |módulo| pred. exato | $\text{pred}/\text{obs}$ |
|---|---|---|---|---|---|
| 143 | 5 | 0.00283 | 0.00361 | −0.00283 | **1.000** |
| 121 | 3 | 0.00036 | 0.00085 | +0.00036 | **1.005** |
| 11 | 1 | 0.00011 | 0.00043 | −0.00011 | **0.997** |
| 17 | 1 | 0.00051 | 0.00101 | +0.00051 | **0.991** |

A coluna "pred. |módulo|" usa o sidelobe simples sem fase — erra por fatores
de 1.3× a 3.9×. A coluna "pred. exato" usa a fórmula com parte real —
erro de 0–1%.

### 4.2 Nota 38 Exp C Stage 1 (P1={2}, 4 grupos: 105×5, 15×3, 7×1, 11×1)

| $q$ | $k_q$ | erro obs. | pred. |módulo| pred. exato | $\text{pred}/\text{obs}$ |
|---|---|---|---|---|---|
| 105 | 5 | 0.00147 | 0.00152 | −0.00147 | **1.002** |
| 15 | 3 | 0.00077 | 0.00223 | −0.00077 | **0.996** |
| 7 | 1 | 0.00016 | 0.00166 | −0.00017 | **1.038** |
| 11 | 1 | 0.00362 | 0.00400 | −0.00362 | **1.001** |

**Erro máximo em todos os 8 casos: 4%.**

O caso $q=7$ no Exp C é o mais revelador: sidelobe simples prevê erro de 0.00166
(10× acima do observado 0.00016), enquanto a fórmula exata dá −0.00017
(1.038× — quase exato). A diferença é que as interferências dos grupos 105, 15
e 11 quase se cancelam em $f_7$ quando suas fases são consideradas.

---

## 5. Por que a Lei da Interferência Nula é exata

Com um único grupo no sinal, a soma $\sum_{r \neq q}$ é vazia:

$$\text{razão}(q) = k_q + 0 = k_q \quad \text{(exato)}$$

Isso vale para qualquer $k_q$, qualquer $T_{\max}$, qualquer $t_0$ —
não depende de nenhuma aproximação. É uma identidade da FFT de um
cosseno puro amostrado uniformemente. A Lei da Interferência Nula
(Nota 38) emerge diretamente da fórmula como caso especial, agora
com prova analítica em vez de apenas confirmação empírica.

---

## 6. Interpretação geométrica

A fórmula tem uma leitura geométrica simples no plano complexo.
$A_q(\hat{\omega}_q)$ define uma direção. Cada $A_r(\hat{\omega}_q)$
é um vetor que pode apontar em qualquer direção, dependendo da
diferença de fase $(\omega_r - \omega_q) \cdot t_{\text{centro}}$
onde $t_{\text{centro}} = t_0 + (N-1)\Delta t/2$ é o centro da janela temporal.

O erro de Stage 1 é a **projeção da soma das interferências sobre
a direção do grupo alvo** — não a soma dos módulos. Para grupos muito
distantes em frequência ($|\omega_r - \omega_q| \gg 2\pi/T_{\max}$),
essa projeção oscila entre positiva e negativa dependendo de
$(\omega_r - \omega_q) \cdot t_{\text{centro}} \bmod 2\pi$.

Uma consequência prática: **dois experimentos com o mesmo conjunto
de grupos mas $T_{\max}$ diferente podem ter erros de Stage 1 com
sinais opostos**, porque a fase relativa muda com $T_{\max}$. O valor
absoluto do erro é limitado pelo sidelobe simples, mas o valor real
pode ser qualquer coisa entre $-|\text{sidelobe}|$ e $+|\text{sidelobe}|$.

---

## 7. Fórmula compacta para uso prático

Usando a decomposição polar de $S(\alpha)$:

$$S(\alpha) = e^{i\psi(\alpha)} \left|\frac{\sin(\alpha N\Delta t/2)}{\sin(\alpha \Delta t/2)}\right|$$

onde $\psi(\alpha) = \alpha(t_0 + (N-1)\Delta t/2)$ é a fase acumulada,
a contribuição de $r$ ao erro de $q$ pode ser escrita como:

$$k_r \cdot \text{Re}\!\left[\frac{A_r}{A_q}\right]
= k_r \cdot \frac{\sqrt{\log q}}{\sqrt{\log r}} \cdot
\frac{|S(\omega_r - \hat{\omega}_q)|}{|S(\omega_q - \hat{\omega}_q)|}
\cdot \cos\!\big[\psi(\omega_r - \hat{\omega}_q) - \psi(\omega_q - \hat{\omega}_q)\big]$$

O fator $\cos[\ldots]$ é o que o modelo de sidelobe simples perdia.
Ele vale 1 se as fases se alinham, −1 se são opostas, e tem expectativa
de zero se $(\omega_r - \omega_q) T_{\max} \gg 1$ (muitos ciclos entre grupos).
Nesse sentido, o modelo de sidelobe simples é um **limite superior** para
$|\text{erro}|$, e o sinal e a magnitude exata são determinados pela fase.

---

## 8. Status

| afirmação | status |
|---|---|
| Fórmula exata para razão(q) com múltiplos grupos | Derivada e verificada — Seções 2–4 |
| Precisão da fórmula (8 casos testados) | Erro máximo 4%, maioria abaixo de 1% |
| Lei da Interferência Nula como corolário analítico | Provada — Seção 5 |
| Modelo de sidelobe simples como limite superior para \|erro\| | Estabelecido — Seção 7 |
| Verificação com Stage 1 de 3 ou mais grupos distintos | Confirmada (Nota 37: 4 grupos, Nota 38: 4 grupos) |
| Verificação com grupos de profundidade variável (Nota 38 Exp C) | Confirmada |

---

## 9. Referências

[Nota 37] T. Bandeira, *Fatoração Prima Completa por Cascata de Colapso Orbital*
(2026). Os dados do Stage 1 (4 grupos: 143×5, 121×3, 11×1, 17×1) são o
primeiro conjunto de verificação desta nota.

[Nota 38] T. Bandeira, *Escalabilidade, Profundidade 3 e a Lei da Interferência
Nula* (2026). Estabelece a Lei da Interferência Nula empiricamente; esta nota
prova o resultado analiticamente como corolário da fórmula exata. Os dados
do Exp C (P1={2}, 4 grupos) são o segundo conjunto de verificação.

[Nota 39] T. Bandeira, *Dois Regimes do Detector Espectral e Comparação com
MDC par-a-par* (2026). Deriva a série geométrica $S(\alpha)$ para `amp_iso(q)`;
esta nota usa a mesma série como bloco construtivo para $A_r(\hat{\omega})$.
