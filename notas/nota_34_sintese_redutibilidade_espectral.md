# Nota 34 — Síntese Experimental: Estrutura Orbital sob Eliminação Espectral

**T. Bandeira · Junho de 2026**
*Nota de síntese experimental — consolida Exp FA-LOG-1 e Exp FA-LOG-2*

---

## Resumo

Esta nota consolida uma série de experimentos exploratórios sobre o comportamento espectral de inteiros sob remoção de fatores primos, adotando a Definição de Redutibilidade Logarítmica da Nota 21 mas usando um sinal simplificado (soma direta de $2$ a $N$, sem o produto de Euler/$\zeta$) para isolar o efeito de subtrações individuais de log. O resultado central é a **lei do ganho orbital**: ao remover completamente os fatores de um conjunto de primos $\{q_1,\ldots,q_k\}$, cada inteiro livre desse conjunto se torna um atrator cujo ganho de amplitude iguala o tamanho de sua órbita, com confirmação numérica até órbitas de 19 membros e estrutura multiplicativa em até três primos simultâneos. Um artefato de medição inicialmente confundido com efeito físico (desvio sistemático em $r=11, 23$) foi isolado e explicado por completo como ruído de lotação espectral assimétrica entre sinal original e sinal removido — não como falha da lei. Um teste de controle com $q$ composto confirma que a lei se estende sem alteração, distinguindo-se apenas pela granularidade da redução. Uma fórmula fechada via soma de Parseval permite prever a norma $L^2$ de qualquer configuração de remoção sem necessidade de simulação FFT.

---

## 1. Contexto e definições

Esta nota registra a continuidade da investigação iniciada na Nota 21, que define a **Redutibilidade Logarítmica**: um inteiro $m\geq2$ é logaritmicamente redutível se $\log m = \sum_i \alpha_i \log p_i$ para primos $p_i<m$ e $\alpha_i\in\mathbb{Z}_{\geq1}$ — equivalentemente, $f_m=\sum_i\alpha_i f_{p_i}$ em frequências, com $f_x=\log(x)/2\pi$. A Proposição da Nota 21 estabelece que essa noção coincide exatamente com primalidade: irredutível $\iff$ primo.

O sinal usado aqui é uma **simplificação deliberada** do sinal formal $S_m(t)$ da Nota 21 (que usa $-\frac12\log(1-2m^{-1/2}\cos(t\log m)+m^{-1})$, com amplitude líder $\sim 2m^{-1/2}$). Nesta série, opta-se por:

$$R_{\log}(t) = \sum_{m=2}^{N} -\frac{\cos(t \cdot \log m)}{\sqrt{\log m}}$$

com amplitude $1/\sqrt{\log m}$ em vez de $\sim m^{-1/2}$, e soma direta sobre $[2,N]$ (o "fatorial") em vez do bloco binário $\mathcal{B}$ e do denominador $\zeta$ da Etapa 2. Essa troca isola o efeito de subtrações individuais de log sobre o espectro, sem o aparato de detecção de primos da Nota 21 — **não é uma tentativa de validar ou testar o Teorema de Invariância ou o Corolário (Crivo Oracle-Free)** daquela nota, que dependem de um sinal e um operador diferentes (ver Seção 12).

---

## 2. Exp FA-LOG-1 — fenômeno qualitativo

**Operação:** subtrair $k \cdot \log q$ de cada múltiplo de $q$, deslocando $\log m \to \log(m/q^{k_{\text{ef}}})$, com $k_{\text{ef}} = \min(k, v_q(m))$.

**Resultado:** ao remover completamente os fatores de $q=3$ ($k=1$), não-múltiplos de 3 ganharam ~100% de amplitude na posição original, enquanto múltiplos de 3 quase não mudaram. A leitura inicial — que isso seria simetria de "perda compensada por ganho" — estava incompleta. O experimento seguinte mostrou o mecanismo exato.

---

## 3. Exp FA-LOG-2 — estrutura orbital (um primo)

**Hipótese:** após remoção completa dos fatores de $q$, cada $m = r \cdot q^a$ (com $\gcd(r,q)=1$) converge para $f_r$. Os membros da órbita

$$\mathcal{O}_r = \{r,\, rq,\, rq^2,\, \ldots\} \cap [2,N]$$

chegam **em fase exata** em $f_r$ (são literalmente o mesmo cosseno), então o ganho de amplitude deveria ser $|\mathcal{O}_r|$.

**Resultado confirmado** com alta precisão para $q \in \{3,5,7\}$:

| tamanho da órbita | razão medido/previsto | desvio padrão |
|---|---|---|
| 2 | 1.0008 | 0.020 |
| 3 | 1.0012 | 0.0094 |
| 4 | 1.0044 | 0.0054 |

Achados complementares:
- **Primos e compostos $q$-livres se comportam de forma idêntica** como atratores — o que importa é só o tamanho da órbita, não a estrutura aritmética interna de $r$.
- **A norma $L^2$ cresce** (não se conserva) — concentração de energia em menos picos aumenta a amplitude, efeito de soma coerente.
- **O próprio primo $q$** é caso especial: $\log(q/q)=0$, sua componente é descartada (não é atrator, é autorredutor).

---

## 4. Extensão multiplicativa — dois e três primos

**Hipótese estendida:** para um conjunto $\{q_1,\ldots,q_k\}$, a órbita de um inteiro $\{q_1,\ldots,q_k\}$-livre $r$ vira contagem de pontos de rede:

$$g_{\text{prev}}(r) = \#\Big\{(a_1,\ldots,a_k) \in \mathbb{Z}_{\geq 0}^k : r\prod_i q_i^{a_i} \leq N\Big\}$$

**Resultado — dois primos ($q=\{3,5\}$):** confirmação até órbita de 12 membros ($r=2$), razão 1.0021.

**Resultado — três primos ($q=\{3,5,7\}$):** confirmação até órbita de **19 membros** ($r=2$, a maior testada), razão **1.0021**. A lei não mostra sinal de degradação ao escalar para 3 dimensões.

**Sinergia na norma $L^2$:** o excesso sobre o produto ingênuo das razões individuais cresce com o número de primos removidos:

| configuração | excesso sobre produto ingênuo |
|---|---|
| 2 primos | +7.4% |
| 3 primos | +9.8% |

Esse comportamento agora tem **explicação fechada** (ver Seção 6).

---

## 5. Investigação do artefato metodológico (resolvida)

Dois atratores ($r=11$ e $r=23$) mostraram desvio sistemático e reprodutível em todos os experimentos — crescendo com o número de primos removidos, ao contrário do padrão geral (que melhora com órbitas maiores). Já $r=13$ mostrou desvio de **sinal oposto**.

**Hipóteses testadas e descartadas:**
1. *Vazamento do pico gigante de $r=2$.* Removido explicitamente da reconstrução — efeito medido: $\Delta \approx 10^{-4}$ (nulo). Distância espectral de $f_2$ a $f_{11}$ é de 1764 bins; decaimento de sidelobe previsto nessa distância é desprezível ($\sim 1.8\times10^{-4}$).
2. *Soma de vazamento dos vizinhos espectrais mais próximos.* Mesmo somando os 10 vizinhos mais próximos, previu apenas 14% do excesso observado. Somando **todos** os 198 outros atratores ativos: 35%. Insuficiente.

**Causa real — lotação espectral assimétrica.** Construindo o termo isolado de cada $r$ (sem nenhum outro termo no sinal) e comparando à amplitude medida no sinal original completo (299 termos ativos):

| $r$ | isolado | medido (sinal original) | delta |
|---|---|---|---|
| 11 | 1592.20 | 1557.79 | −2.16% |
| 13 | 1495.18 | 1513.49 | **+1.23%** |
| 17 | 1917.10 | 1897.77 | −1.01% |
| 19 | 1893.94 | 1879.07 | −0.79% |
| 22 | 1509.63 | 1466.97 | −2.83% |
| 23 | 1470.72 | 1434.70 | −2.45% |

O sinal de cada delta bate exatamente com o sinal do desvio de razão observado em cada $r$. O mecanismo: o sinal *original* (299 termos ativos) sofre mais interferência incoerente de fundo do que o sinal *removido* (137 ou menos termos ativos, mais esparso). Verificação quantitativa exata para $r=11$:

$$\text{razão prevista} = \frac{1 - 0.0056}{1 - 0.0216} = 1.0163 \qquad \text{vs.} \qquad \text{razão medida} = 1.0164$$

Match dentro de $10^{-4}$. Mesma verificação para $r=13$: previsto 0.99203, medido 0.9920.

**Conclusão:** o desvio de 1–3% observado em todos os experimentos é artefato de medição (ruído de lotação espectral inerente ao FFT de tempo finito com muitos termos somados), não um efeito físico sobre redutibilidade. A lei principal ($\text{ganho}=|\mathcal{O}_r|$) permanece correta; a precisão medida está subestimada pelo método atual.

**Correção recomendada para experimentos futuros:** aplicar janela de afunilamento (Hann/Hamming) na construção do sinal antes da FFT, ou normalizar as amplitudes medidas pelos valores isolados teóricos (calculáveis analiticamente, sem necessidade de medir do espectro cheio).

---

## 6. Ferramenta nova — fórmula fechada para a norma $L^2$

Para sinais compostos de cossenos com frequências bem separadas, a média quadrática no tempo aproxima-se de uma soma de Parseval:

$$\|R\|^2 \approx \frac{1}{2}\sum_{r \text{ livre}} \frac{g(r)^2}{\log r}$$

onde a soma percorre os atratores (inteiros livres do conjunto de primos removidos) e $g(r)$ é o tamanho de sua órbita. Esta fórmula **dispensa simulação FFT completa** — só exige a lista de atratores e seus tamanhos de órbita, que são puramente combinatórios.

**Verificação contra os 6 casos já medidos** (erro sempre < 0.5%):

| configuração | norma prevista | norma medida |
|---|---|---|
| original | 5.839 | 5.810 |
| $q=3$ | 9.935 | 9.917 |
| $q=5$ | 8.520 | 8.498 |
| $q=7$ | 7.834 | 7.805 |
| $q=\{3,5\}$ | 15.613 | 15.602 |
| $q=\{3,5,7\}$ | 21.415 | 21.405 |

O termo $g(r)^2$ (em vez de $g(r)$) explica analiticamente a sinergia observada na Seção 4: concentrar mais massa em menos atratores aumenta a soma de quadrados mais do que a soma simples cresceria, então a norma cresce supralinearmente conforme mais primos são removidos.

Essa fórmula permite testar rapidamente qualquer combinação de primos removidos sem rodar notebook pesado no Colab — só contagem combinatória de órbitas.

---

## 7. Glossário operacional

| termo usado nos experimentos | definição formal |
|---|---|
| atrator | inteiro $\{q_1,\ldots,q_k\}$-livre $r$; representa a classe de equivalência de $m$'s que convergem para $f_r$ |
| órbita $\mathcal{O}_r$ | $\{r\prod q_i^{a_i} \leq N\}$ — conjunto de inteiros que mapeiam para o mesmo $r$ após remoção |
| ganho ($g_{\text{prev}}$) | $|\mathcal{O}_r|$ — multiplicidade da classe; previsão para o ganho de amplitude |
| ganho medido ($g_{\text{med}}$) | razão `amp_depois / amp_antes` observada diretamente no espectro |
| razão | $g_{\text{med}}/g_{\text{prev}}$ — métrica de precisão da lei; idealmente 1.0 |
| $q$-suave | conexão com teoria de números: a contagem de órbita é equivalente à contagem de números $\{q_1,\ldots,q_k\}$-suaves (relacionada à função de Dickman-de Bruijn $\Psi(x,y)$) |

---

## 8. Status atual

| Afirmação | Status |
|---|---|
| Lei do ganho orbital ($\text{ganho}=\lvert\mathcal{O}_r\rvert$) | Confirmada numericamente, 1 a 3 primos simultâneos, até órbitas de 19 membros (Seções 3–4) |
| Estrutura multiplicativa (órbitas em múltiplos primos = produto cartesiano de potências) | Confirmada numericamente até $k=3$ (Seção 4) |
| Fórmula fechada para norma $L^2$ via soma de Parseval | Verificada contra 6 configurações medidas, erro $<0.5\%$ (Seção 6) |
| Mecanismo do artefato de medição (lotação espectral assimétrica) | Identificado e verificado quantitativamente, match $<10^{-4}$ para $r=11,13$ (Seção 5) |
| Extensão da lei para $q$ composto | Confirmada numericamente, 1 caso ($q=6$, razão $1.0016$) (Seção 9) |
| Demonstração minimalista (5 termos): colisão coerente e convergência ao Corolário | Confirmada — colisão $14{+}21\to f_7$ com razão $2.0004$ (previsto $2.0$), $f_{29}$ invariante ($\Delta<0.2\%$) ao longo de toda a remoção (Seção 10) |
| Correção via janela de Hann | Não testada |
| Fórmula assintótica contínua de contagem de pontos de rede | Testada e refutada no regime atual ($L\sim\log q_i$ não é "grande o suficiente"; ver Nota — fórmula recursiva exata) |
| Mais de três primos simultâneos | Não testado |

---

## 9. Controle com $q$ composto — resultado

**Correção sobre a formulação original do teste:** $v_q(m) = \max\{v : q^v \mid m\}$ é perfeitamente bem definida para qualquer $q \geq 2$, primo ou composto — não há ambiguidade. O código de remoção de um primo (`orbitas_q`, `construir_R_removido`) funciona sem nenhuma alteração para $q$ composto. A pergunta certa não era "a lei quebra?", mas **"remover $q=6$ como unidade produz a mesma redistribuição que remover $q=\{2,3\}$ como primos separados?"**

A diferença prevista: sob $q=2$ (primo), a componente de $m=2$ desaparece ($\log(2/2)=0$). Sob $q=6$ (composto), $m=2$ **não é múltiplo de 6** — sobrevive como atrator próprio, com órbita $\{2, 12, 72\}$ (multiplicando por 6 a cada passo).

**Resultado medido** ($N=300$):

```
Inteiros 6-livres: 249
  r=2  |orbita|=3  [2, 12, 72]
  r=3  |orbita|=3  [3, 18, 108]
  r=4  |orbita|=3  [4, 24, 144]
  ...

amp em f_2:  original=3876.46  |  removido q=6: 11648.53  (orbita prevista=3)
```

$$\text{razão} = \frac{11648.53/3876.46}{3} = 1.0016 \quad (+0.16\%)$$

Confirma a previsão dentro do nível de ruído de lotação espectral já caracterizado na Seção 5 (assim como os demais casos de órbita de tamanho 3 medidos anteriormente). **A lei se estende sem modificação para $q$ composto** — $r=2$ sobrevive e ganha amplitude sob $q=6$, em vez de desaparecer como acontece sob remoção de $q=2$ sozinho. O composto não invalida a lei; ele apenas opera numa granularidade mais grossa, exigindo que todos os fatores primos do composto apareçam simultaneamente para que a redução ocorra.

---

## 10. Demonstração minimalista — compostos vs. primo de controle

Para isolar o mecanismo de redutibilidade de forma mais direta que os experimentos de $N=300$, montou-se um sinal com apenas 5 termos: quatro compostos escolhidos por sua decomposição em fatores pequenos — $12=2^2\cdot3$, $14=2\cdot7$, $21=3\cdot7$, $25=5^2$ — e um primo de controle, $29$, que não compartilha nenhum fator com os demais.

**Procedimento:** remover progressivamente $2, 3, 5, 7$ (cumulativamente) via $\log_{\text{novo}}(m) = \log m - \sum_q v_q(m)\log q$, e observar a posição de cada termo e a amplitude em $f_{29}$ a cada estágio.

| estágio (removidos) | posições ativas | amp em $f_{29}$ |
|---|---|---|
| $\{\}$ | 5 picos distintos: $f_{12}, f_{14}, f_{21}, f_{25}, f_{29}$ | 1260.06 |
| $\{2\}$ | $12\to f_3$, $14\to f_7$; $21,25,29$ inalterados | 1260.19 |
| $\{2,3\}$ | $12$ descartado; **$14$ e $21$ colidem em $f_7$** | 1262.60 |
| $\{2,3,5\}$ | $25$ também descartado; $14{+}21$ seguem juntos em $f_7$ | 1262.76 |
| $\{2,3,5,7\}$ | **todos os compostos descartados** — só $f_{29}$ sobrevive | 1262.78 |

A amplitude em $f_{29}$ varia menos de $0.2\%$ do início ao fim — dentro do ruído residual caracterizado na Seção 5, não um efeito real. Confirma-se também a previsão exata de soma coerente na colisão: com apenas $14$ presente em $f_7$, a amplitude medida é $2326.52$; com $14$ e $21$ sobrepostos, $4653.90$ — razão $2.0004$ (previsto: $2.0000$).

**Interpretação.** O estágio final — só $f_{29}$ sobrevivendo após remover todos os fatores primos dos compostos escolhidos — é uma réplica em miniatura controlada do Corolário da Nota 21 (Crivo Oracle-Free): após eliminar as contribuições redutíveis, restam exatamente os elementos logaritmicamente irredutíveis. A colisão $14+21\to f_7$ no meio do caminho ilustra de forma mais direta que os experimentos anteriores o que significa "redutível" nesta linguagem: $\log 14$ e $\log 21$ não são só *afetados* pela remoção de $3$ — eles são, literalmente, $\log 2+\log 7$ e $\log 3+\log 7$, construções de outras frequências que coincidem assim que a parte que os distingue é removida.

---

## 11. Próximos passos sugeridos

1. **Reexecutar com janela de Hann** para eliminar o artefato de lotação espectral identificado na Seção 5, e comparar a precisão da razão antes/depois da correção.

2. **Testar a fórmula fechada da Seção 6** contra combinações maiores de primos (4, 5 primos) sem precisar rodar FFT — só contagem combinatória — para mapear rapidamente como a sinergia na norma evolui.

3. **Investigar a transição entre regime discreto e regime assintótico contínuo** na contagem de órbitas, aumentando $N$ até a fórmula de volume contínuo ($L^k/(k!\prod\log q_i)$) começar a convergir com a contagem exata recursiva.

4. **Comparar $q$ composto com múltiplos fatores primos repetidos** (ex: $q=12=2^2\cdot3$) para verificar se a granularidade de redução escala com a multiplicidade dos fatores primos do composto, e não só com o conjunto de primos distintos que o compõem.

5. **Generalizar a demonstração minimalista da Seção 10** com mais de um primo de controle simultaneamente, e com compostos que compartilham fatores parcialmente (ex: $14$ e $35=5\cdot7$, que colidem em $f_5$ ou $f_7$ dependendo da ordem de remoção) — mapearia sistematicamente quais sequências de colisão são possíveis dado um conjunto inicial de compostos.

---

## 12. Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026). Define a Redutibilidade Logarítmica, a Proposição de equivalência com primalidade, e o operador de eliminação $\mathcal{R}_m$ via Teorema de Invariância.

**Relação com esta nota.** Os experimentos FA-LOG adotam a Definição de Redutibilidade Logarítmica da Nota 21 (Seção 2 daquela nota), mas operam sobre um sinal e um operador estruturalmente diferentes:

- *Sinal.* A Nota 21 usa $S_m(t)$ (amplitude $\sim m^{-1/2}$, via expansão de $-\frac12\log(1-2m^{-1/2}\cos(t\log m)+m^{-1})$); esta nota usa $-\cos(t\log m)/\sqrt{\log m}$ (amplitude $\sim 1/\sqrt{\log m}$), simplificação adotada para isolar o efeito de subtrações individuais.
- *Operador.* O $\mathcal{R}_m$ da Nota 21 subtrai $S_m$ por inteiro, eliminando um termo e deixando os demais intocados (Teorema de Invariância, ortogonalidade no limite $T\to\infty$). A operação desta nota desloca $\log m \to \log(m/q^{k})$ — não elimina, **realoca** o termo, frequentemente sobrepondo-o a outro termo já existente na nova frequência. É essa realocação coerente, não a eliminação, que produz a estrutura orbital descrita nas Seções 3–4.

Esta nota não testa nem depende do Teorema de Invariância, do Corolário (Crivo Oracle-Free), ou do uso de $\zeta$ via produto de Euler descritos na Nota 21 — o objetivo aqui é puramente experimental, sobre a perturbação espectral de subtrações individuais de log num sinal simplificado.

---

## 13. Notebooks e arquivos

| arquivo | conteúdo |
|---|---|
| `exp_fat_log__1_.ipynb` | Exp FA-LOG-1 — deslocamento de $k\log q$, fenômeno qualitativo de redistribuição (Seção 2) |
| `exp_fat_log2.ipynb` (executado como `exp_fat_log2__1_.ipynb`) | Exp FA-LOG-2 — estrutura orbital com um primo (Seção 3). Recebeu, em células coladas na mesma sessão, as extensões para dois primos, três primos (Seção 4), o controle com $q$ composto (Seção 9) e a demonstração minimalista compostos vs. primo de controle (Seção 10) |
| `fat_log2_ganho_destino.csv` | tabela de ganho previsto vs. medido, um primo, $q\in\{3,5,7\}$ |
| `fat_log2_scatter_ganho.png`, `fat_log2_zoom_orbitas.png`, `fat_log2_espectro_completo.png` | figuras do experimento de um primo |
| `fat_log2_ganho_2primos.png`, `fat_log2_ganho_3primos.png` | figuras das extensões multiplicativas |
| `fat_log2_demo_minimalista.png` | figura da demonstração minimalista (Seção 10) |
| `espectros_log2.pkl` | espectros serializados ($F_{\log}$, espectros removidos por $q\in\{3,5,7\}$, freqs) para reanálise sem precisar reexecutar a FFT |
| `exp_fat_log2_resultados.zip` | pacote consolidado dos itens acima |
