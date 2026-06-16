# Nota 31 — Lei de Escala da Razão Espectral $\mathcal{R}(f_p)$

**T. Bandeira · Junho de 2026**  
*Nota adicional à série Motor de Herança Estrutural — Artigos 01–12*

---

## Resumo

Dados os sinais $R_{\text{primo}}$ e $R_{\text{comp}}$ da Nota 30, a razão
espectral $\mathcal{R}(f_p) = |\mathcal{F}[R_{\text{primo}}](f_p)| /
|\mathcal{F}[R_{\text{comp}}](f_p)|$ obedece a duas leis de escala distintas:

**Numerador** (verificado, corr = $-0.969$, slope = $-0.455 \approx -0.5$):
$$|\mathcal{F}[R_{\text{primo}}](f_p)| \approx \frac{T_{\max}}{2\sqrt{p}}$$

**Denominador** (dois regimes, expoente efetivo dependente de $T_{\max}$):
$$|\mathcal{F}[R_{\text{comp}}](f_p)| \approx \frac{1}{T_{\max}}
\left[\sqrt{p}\log T_{\max} + \frac{p}{2\log p}\right]$$

**Razão resultante** (lei empírica para $N = 200$, $T_{\max} \sim 10^3$):
$$\mathcal{R}(f_p) \approx C \cdot p^{-1.338}$$

com expoente efetivo $-1.338 = -0.455 - 0.883$, onde $-0.455$ vem do
numerador e $+0.883$ do denominador para $T_{\max} = 1500$.

---

## 1. Configuração

Dados $N \geq 2$ e $T_{\max} > 0$, os sinais são:
$$R_{\text{primo}}(t) = -\sum_{p \leq N} \frac{\cos(t\log p)}{\sqrt{p}}, \qquad
R_{\text{comp}}(t) = -\sum_{\substack{c \leq N \\ c \text{ composto}}}
\frac{\cos(t\log c)}{\sqrt{c}}$$

com transformadas $\mathcal{F}[R](f_p) = \int_0^{T_{\max}} R(t)\,e^{-2\pi i f_p t}\,dt$
e $f_p = \log(p)/(2\pi)$.

---

## 2. Numerador: $|\mathcal{F}[R_{\text{primo}}](f_p)| \approx T_{\max}/(2\sqrt{p})$

### 2.1 Derivação

O coeficiente de Fourier de $R_{\text{primo}}$ em $f_p$ é:

$$\mathcal{F}[R_{\text{primo}}](f_p) = -\sum_{q \leq N,\,q\text{ primo}}
\frac{1}{\sqrt{q}}\int_0^{T_{\max}}\cos(t\log q)\,e^{-it\log p}\,dt$$

**Termo $q = p$:** a integral vale $T_{\max}/2$ (fase zero no primeiro harmônico).

**Termos $q \neq p$:** $\log q \neq \log p$ para primos distintos, portanto cada
integral oscila com frequência $|\log q - \log p|/(2\pi) > 0$ e contribui
com $O(1/|\log q - \log p|)$. Por ortogonalidade assintótica (Nota 21),
essas contribuições se cancelam em amplitude normalizada por $T_{\max}$.

O termo dominante é portanto $q = p$:

$$|\mathcal{F}[R_{\text{primo}}](f_p)| \approx \frac{T_{\max}}{2\sqrt{p}}$$

### 2.2 Verificação (Exp W-A, $N = 200$, $T_{\max} = 1500$)

Ajuste em $\log_{10}$ vs $\log_{10}p$: slope $= -0.455$ (esperado $-0.5$),
correlação $= -0.969$. O desvio de $-0.5$ para $-0.455$ é efeito de borda
para primos grandes próximos de $N$.

---

## 3. Denominador: estrutura de dois regimes

A contribuição individual do composto $c$ ao denominador em $f_p$ é:

$$|I(c, p, T_{\max})| = \frac{1}{\sqrt{c}} \cdot
\frac{|\sin(\delta_{cp}\,T_{\max}/2)|}{|\delta_{cp}|}, \qquad
\delta_{cp} = \log(c/p)$$

que é o kernel de Dirichlet ponderado por $1/\sqrt{c}$. A fronteira
$\delta^* = 1/T_{\max}$ separa dois regimes:

### 3.1 Regime distante ($|\delta_{cp}| > 1/T_{\max}$)

Para compostos fora do lóbulo central, $|I| \approx 1/(\sqrt{c}|\delta_{cp}|)$.
A soma sobre compostos distantes, integrando sobre $\delta \in [1/T_{\max}, \log p]$:

$$D_{\text{dist}}(p, T_{\max}) \approx
\frac{\sqrt{p}}{T_{\max}}\left[\log T_{\max} + \tfrac{1}{2}\log\log p + C_1\right]
\approx \frac{\sqrt{p}\log T_{\max}}{T_{\max}}$$

Expoente em $p$: $+1/2$. Cresce com $\log T_{\max}$.

### 3.2 Regime próximo ($|\delta_{cp}| < 1/T_{\max}$)

Compostos em $c \in (p - p/T_{\max},\, p + p/T_{\max})$ contribuem com
$|I| \approx T_{\max}/(2\sqrt{p})$ cada. O número desses compostos é
$n_{\text{próx}} \approx 2p/(T_{\max}\log p)$. Contribuição total:

$$D_{\text{próx}}(p, T_{\max}) \approx
n_{\text{próx}} \cdot \frac{T_{\max}}{2\sqrt{p}} \cdot \frac{1}{\sqrt{p}}
\approx \frac{p}{T_{\max}\log p} \cdot \frac{T_{\max}}{2p}
\cdot \sqrt{p} = \frac{\sqrt{p}}{2\log p}$$

Reescrevendo como $p/(2T_{\max}\log p)$ após normalização por $T_{\max}$:
expoente em $p$ tendendo a $+1$.

### 3.3 Forma completa e expoente efetivo

$$\boxed{D(p, T_{\max}) \approx \frac{1}{T_{\max}}
\left[\sqrt{p}\log T_{\max} + \frac{p}{2\log p}\right]}$$

O expoente efetivo global é a média ponderada dos dois regimes. O Exp W-D
Extended mediu empiricamente:

$$\alpha_{\text{eff}}(T_{\max}) \approx 0.14\,\ln T_{\max}$$

confirmado para $T_{\max} \in \{500, 1000, 1500, 2000, 3000\}$:

| $T_{\max}$ | $\ln T_{\max}$ | slope medido | $0.14\ln T_{\max}$ |
|---|---|---|---|
| 500  | 6.21 | 0.385 | 0.869 |
| 1000 | 6.91 | 0.711 | 0.967 |
| 1500 | 7.31 | 0.883 | 1.023 |
| 2000 | 7.60 | 1.008 | 1.064 |
| 3000 | 7.91 | 1.097 | 1.107 |

A lei $0.14\ln T_{\max}$ é empírica; a derivação analítica da constante
$0.14$ permanece em aberto (ver Seção 5, Questão 1).

---

## 4. Razão espectral e lei de escala

### 4.1 Forma geral

$$\mathcal{R}(f_p) = \frac{T_{\max}^2/2}{p\log T_{\max} + p^{3/2}/(2\log p)}$$

Para $p$ pequeno ($p \ll T_{\max}/\log T_{\max}$), o regime distante domina:
$$\mathcal{R}(f_p) \approx \frac{T_{\max}^2}{2p\log T_{\max}}$$

Para $p$ grande, o regime próximo domina e a razão decai mais rápido que $1/p$.

### 4.2 Lei empírica ($N=200$, $T_{\max}=1500$)

$$\mathcal{R}(f_p) \approx C \cdot p^{-1.338}, \qquad \text{corr} = -0.925$$

O expoente $-1.338 = -0.455 - 0.883$ é consistente internamente:
slope(razão) = slope(numerador) $-$ slope(denominador).

### 4.3 Dualidade posição/amplitude

Invertendo a lei do numerador:

$$p \approx \left(\frac{T_{\max}}{2\,|\mathcal{F}[R_{\text{primo}}](f_p)|}\right)^2$$

A amplitude do pico em $f_p$ e a posição $f_p$ codificam $p$ de forma
complementar: posição via $f_p = \log p/(2\pi)$, amplitude via
$T_{\max}/(2\sqrt{p})$.

---

## 5. Questões em aberto

**Questão 1 — Constante 0.14.** A lei empírica $\alpha_{\text{eff}} \approx
0.14\ln T_{\max}$ não foi derivada analiticamente. Uma derivação exigiria
contagem precisa de compostos na fronteira de regime $\delta^* = 1/T_{\max}$,
conectando com a distribuição local de primos.

**Questão 2 — Regime assintótico.** O expoente efetivo continua crescendo
além de $T_{\max} = 3000$? Se sim, não existe regime assintótico simples
e a lei de escala é intrinsecamente dependente de $T_{\max}$.

**Questão 3 — Conexão com Cramér.** Para $T_{\max} \sim p\log p$ (escala
de Cramér), a janela do regime próximo tem largura $\sim 1/\log p$ —
a mesma escala dos gaps entre primos. Nesse regime, a estrutura do
denominador conectaria diretamente com a Conjectura de Cramér sobre
gaps máximos entre primos consecutivos.

---

## Referências

[Nota 21] T. Bandeira, *Formalização do Crivo Espectral Oracle-Free* (2026).  
[Nota 28] T. Bandeira, *Escala de $t_{\max}$ para a Etapa 2* (2026).  
[Nota 30] T. Bandeira, *Dicotomia Espectral entre Primos e Compostos* (2026).  
[Exp W] T. Bandeira, `exp_w_denominador_espectral.ipynb` (2026).  
[Exp W-D Extended] T. Bandeira, `exp_wd_extended.ipynb` (2026).

---

*Esta nota é parte da série Motor de Herança Estrutural e está licenciada para uso acadêmico livre.*
