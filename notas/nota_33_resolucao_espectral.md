# Nota 33 — Resolução Espectral de $R_{\text{primo}}$ em Pares $(p, p+2)$: Calibração de $T_{\max}$

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

O Exp BB e o Exp CC investigaram a amplitude normalizada em $f_{p+2}$:

$$\hat{a}_{p+2} = \frac{|\mathcal{F}[R_{\text{primo}}](f_{p+2})|}
{T_{\max}/(2\sqrt{p+2})}$$

no sinal $R_{\text{primo}}$ construído com conhecimento prévio de todos
os primos $\leq N$. O experimento é, por construção, **internamente
consistente mas não um crivo independente**: quando $p+2$ é primo, o
termo $S_{p+2}$ foi incluído em $R_{\text{primo}}$ na construção do
sinal; quando $p+2$ é composto, não foi. A separação observada entre
os dois casos confirma o mecanismo teórico previsto — não detecta
primalidade de forma independente.

O resultado substantivo é sobre **resolução espectral**: com
$T_{\max} = 1500$ fixo, a dicotomia prevista pela Nota 21 colapsa
para $p > 80$ ($\hat{a}_{p+2}$ torna-se estatisticamente indistinguível
entre os dois casos, Mann-Whitney $p = 0.418$). Com $T_{\max} = 6500$,
a dicotomia é robusta em toda a faixa $p \leq 299$ (Mann-Whitney
$p < 10^{-10}$, separação em mediana de $\approx 20\times$).

Em outras palavras: $T_{\max} = 6500$ é suficiente como piso operacional
para que a estrutura espectral de $R_{\text{primo}}$ reflita fielmente
a dicotomia pico-direto vs. intermodulação prevista pela Nota 21 para
$N = 300$. Isso abre a possibilidade de usar $R_{\text{primo}}$ com
$T_{\max} = 6500$ em experimentos subsequentes que analisem a estrutura
dos pares dentro da faixa $p \leq 299$, desde que a primalidade dos
elementos seja conhecida a priori.

---

## 1. Configuração e pressuposto

Sinais $R_{\text{primo}}$ e $R_{\text{comp}}$ da Nota 30 com $N = 300$,
construídos com conhecimento explícito de todos os primos $\leq N$ via
`isprime`. O sinal $R_{\text{primo}}$ contém $S_m$ se e somente se $m$
é primo — a partição é feita a priori, não inferida espectralmente.

Para cada primo $p \leq 299$, analisa-se o par $(p, p+2)$ em dois casos:

- **Gêmeo:** $p+2$ primo — $S_{p+2}$ foi incluído em $R_{\text{primo}}$
  na construção
- **Misto:** $p+2$ composto — $S_{p+2}$ foi excluído de $R_{\text{primo}}$
  na construção

A separação espectral observada é, portanto, consequência direta dessa
partição: o experimento verifica se o espectro com resolução $T_{\max}$
reflete a estrutura imposta, não se consegue inferir a estrutura
independentemente.

---

## 2. Mecanismo e verificação de consistência

### 2.1 Par gêmeo

$p+2$ é primo, logo $\log(p+2)$ é logaritmicamente irredutível (Nota 21)
e $S_{p+2}$ foi incluído em $R_{\text{primo}}$. Esse termo contribui
diretamente com amplitude $\approx T_{\max}/(2\sqrt{p+2})$ na frequência
$f_{p+2}$. Por ortogonalidade assintótica, os demais primos contribuem
com $O(T_{\max}^{-1})$ — desprezível para $T_{\max}$ suficientemente
grande. Portanto, a teoria prevê:

$$\hat{a}_{p+2}^{\text{gêmeo}} \approx 1$$

O experimento verifica se $T_{\max}$ é grande o suficiente para que essa
previsão seja numericamente observável — não infere a primalidade de $p+2$.

### 2.2 Par misto

$p+2$ é composto, logo $S_{p+2}$ foi excluído de $R_{\text{primo}}$.
O pico em $f_{p+2}$ vem apenas de intermodulações entre primos $q < p+2$
na forma $\sum e_i \log q_i = \log(p+2)$. Essas intermodulações são
ressonantes (a igualdade é exata), mas cada termo individual é
$O(1/(\sqrt{q}\,T_{\max}))$, e a soma é $O(T_{\max}^{-1})$:

$$\hat{a}_{p+2}^{\text{misto}} = O\!\left(\frac{1}{T_{\max}}\right) \ll 1$$

O experimento verifica se $T_{\max}$ é grande o suficiente para que o
piso de intermodulação seja distinguível do pico direto.

### 2.3 Ablação direta (Exp BB-4)

Remover $S_{p+2}$ de $R_{\text{primo}}$ para pares gêmeos reduz o pico
em $f_{p+2}$ por fator de 10–250. Isso confirma que o pico observado é
dominado pelo termo direto — consistente com a teoria — e não é artefato
de intermodulações entre os demais primos.

---

## 3. Resultados do Exp CC

### 3.1 Acurácia com $T_{\max} = 6500$ (Exp CC, $N = 300$)

| Regime | Acurácia | FP | FN | Mann-Whitney $p$ |
|---|---|---|---|---|
| Adaptativo ($T_{\max}=6500$) | **100%** (62/62) | 0 | 0 | $< 10^{-10}$ |
| Fixo ($T_{\max}=1500$) | 51.6% (32/62) | 30 | 0 | 0.418 |

### 3.2 Separação por faixa de $p$

| Faixa de $p$ | sep. adaptativo | sep. fixo |
|---|---|---|
| $[2, 30)$ | 0.993 | 0.893 |
| $[30, 60)$ | 0.902 | 0.848 |
| $[60, 100)$ | 0.693 | 0.242 |
| $[100, 150)$ | 0.797 | 0.055 |
| $[150, 200)$ | 0.895 | **$-0.012$** |

(Separação = mediana$_{\text{gêmeo}}$ $-$ mediana$_{\text{misto}}$ de $\hat{a}_{p+2}$)

Com $T_{\max}$ fixo, a separação colapsa para $p > 150$ e torna-se negativa
— mistos aparecem acima dos gêmeos. Com $T_{\max} = 6500$, a separação
permanece robusta em todas as faixas.

### 3.3 Distribuições

| Tipo | Mediana $\hat{a}_{p+2}$ | Média |
|---|---|---|
| Gêmeo | 0.942 | 0.885 |
| Misto | 0.026 | 0.046 |

A separação é de aproximadamente **20×** em mediana — sem sobreposição
entre as duas distribuições para os 62 pares testados.

---

## 4. A lei de escala de $T_{\max}$

Com $T_{\max} = \pi p$ (proporcional ao primo individual), a acurácia
foi baixa. O valor $T_{\max} = 6500$ que produziu separação completa
para $p_{\max} = 299$ corresponde a $\approx 21.7 \times p_{\max}$ —
sugerindo que o $T_{\max}$ necessário cresce mais rápido que $p$,
possivelmente como $O(p^2/\log p)$ ou compatível com o crescimento
exponencial em $\log N$ estabelecido na Nota 28 para o critério de
Rayleigh aplicado ao sinal coletivo.

A lei de escala exata de $T_{\max}$ como função de $p_{\max}$ e $N$
permanece em aberto e é objeto de investigação futura (Exp DD proposto).

---

## 5. Conexão com as notas anteriores

- **Nota 21:** a irredutibilidade logarítmica de $\log(p+2)$ para $p+2$
  primo é o fundamento do mecanismo — sem ela, não haveria separação.
- **Nota 28:** o critério de Rayleigh determina o $T_{\max}$ mínimo para
  resolução espectral suficiente — a lei de escala de $T_{\max}$ nesta
  nota é uma instância local desse critério.
- **Nota 30:** a razão dicotômica $\mathcal{R}(f_{p+2})$ também separa
  os dois tipos (Mann-Whitney $p = 0.0035$ no Exp BB), mas com menor
  potência que $\hat{a}_{p+2}$ com $T_{\max}$ adaptativo.
- **Nota 31:** $\hat{a}_{p+2} \approx 1$ para gêmeos confirma a lei de
  escala do numerador localmente em $f_{p+2}$.

---

## 6. Questões em aberto

**Questão 1 — Lei de escala de $T_{\max}$.** Por que $T_{\max} = \pi p$
não é suficiente mas $T_{\max} = 6500$ para $p \leq 299$ funciona? A lei
de crescimento de $T_{\max}$ como função de $p_{\max}$ e $N$ precisa ser
caracterizada — varrer sistematicamente $T_{\max} \in \{1000, 2000, 3000,
4000, 5000, 6000, 6500\}$ para diferentes $N$ (Exp DD proposto).

**Questão 2 — Mistos grandes.** Para $p+2$ composto grande, a amplitude
residual de intermodulação depende da estrutura de $p+2$? Compostos com
fatores pequenos (potências de 2, múltiplos de 6) têm mais modos de
intermodulação ressonante e deveriam ter $\hat{a}_{p+2}$ maior — potencial
fonte de falsos positivos para $T_{\max}$ insuficiente.

**Questão 3 — Explicação da resolução.** Por que a separação existe apenas
estudando os sinais locais dos pares? A análise do sinal do par isolado
$(S_p + S_{p+2})$ já contém a informação sobre primalidade de $p+2$
via $\hat{a}_{p+2}$ — um resultado que conecta a irredutibilidade
logarítmica com a resolução espectral local e merece formalização
independente.

**Questão 4 — Escalas maiores.** Pares gêmeos foram verificados
computacionalmente para valores muito grandes de $p$. Se a separação
persiste para esses valores com $T_{\max}$ adequado, o critério espectral
funciona universalmente — o que flertar com questões sobre a infinitude
de pares gêmeos, embora essa conexão permaneça especulativa até que o
comportamento dos mistos nessa escala seja caracterizado.

---

## Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026).  
[Nota 28] T. Bandeira, *Escala de $t_{\max}$ para a Etapa 2* (2026).  
[Nota 30] T. Bandeira, *Dicotomia Espectral entre Primos e Compostos* (2026).  
[Nota 31] T. Bandeira, *Lei de Escala da Razão Espectral* (2026).  
[Exp BB] T. Bandeira, `exp_bb_gemeo_vs_misto.ipynb` (2026).  
[Exp CC] T. Bandeira, `exp_cc_adaptativo_tmax_6500.ipynb` (2026).

---

*Esta nota é parte da série Motor de Herança Estrutural e está licenciada para uso acadêmico livre.*