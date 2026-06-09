"""
Experimento Espectral Corrigido — Notas 14/15/16
T. Bandeira · Junho de 2026

Recupera todos os primos < p via análise espectral de Z_Q(s),
usando um pipeline de dois estágios que resolve o problema de
cancelamento da versão original (Z_Q / zeta).

Bugs corrigidos em relação aos códigos originais:
  1. Sinal de log|Z_Q|: -0.5*sum(log(...)) em vez de +0.5
  2. Método 1 (matching por tabela) substituído por q = round(exp(2*pi*f))
  3. Divisão por zeta substituída por pipeline de dois estágios

Pipeline:
  Etapa 1: R1(t) = log|Z_Q / Z_compostos|
           → detecta primos DENTRO do intervalo [2^(n-1), p-1]
           (compostos cancelados; primos grandes ficam limpos)

  Etapa 2: R2(t) = log|Z_Q / (zeta * Z_primos_dentro)|
           → detecta primos FORA do intervalo (< 2^(n-1))
           (primos grandes removidos manualmente com resultado da Etapa 1)

  União: todos os primos < p
"""

import numpy as np
from scipy.signal import find_peaks
from mpmath import mp
import math

mp.dps = 20


# ── Utilidades ──────────────────────────────────────────────────────────────

def is_prime(n):
    if n < 2: return False
    if n == 2: return True
    if n % 2 == 0: return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0: return False
    return True

def log_modZ(xs, t_vals):
    """
    log|Z(0.5+it)| onde Z(s) = prod_{x in xs} (1 - x^{-s})^{-1}

    Fórmula: log|Z| = -0.5 * sum_x log(1 - 2*x^{-0.5}*cos(t*log x) + x^{-1})
    """
    if len(xs) == 0:
        return np.zeros(len(t_vals))
    xs = np.asarray(xs, dtype=float)
    logx = np.log(xs)
    a    = np.exp(-0.5 * logx)
    res  = np.empty(len(t_vals))
    for i, t in enumerate(t_vals):
        theta = t * logx
        term  = np.maximum(1 - 2*a*np.cos(theta) + a*a, 1e-300)
        res[i] = -0.5 * np.sum(np.log(term))   # sinal CORRETO
    return res

def log_abs_zeta(t_vals):
    """log|zeta(0.5 + it)| calculado via mpmath."""
    res = []
    for t in t_vals:
        z = mp.zeta(mp.mpc(0.5, t))
        res.append(float(mp.log(abs(z))) if abs(z) > 1e-8 else 0.0)
    return np.array(res)

def fft_picos(sinal, t_step, f_min, f_max, altura_rel=0.03):
    """
    FFT do sinal, detecta picos em [f_min, f_max] e converte para inteiros
    via q = round(exp(2*pi*f)).
    """
    sinal = sinal - np.mean(sinal)
    fft   = np.fft.rfft(sinal)
    freq  = np.fft.rfftfreq(len(sinal), d=t_step)
    amp   = np.abs(fft)

    mask  = (freq > f_min) & (freq < f_max)
    if mask.sum() == 0:
        return []

    amp_filt  = amp[mask]
    freq_filt = freq[mask]
    peaks, _  = find_peaks(amp_filt,
                           height=np.max(amp_filt) * altura_rel,
                           distance=2)
    return sorted({int(round(math.exp(2 * math.pi * freq_filt[pk])))
                   for pk in peaks})


# ── Pipeline de dois estágios ────────────────────────────────────────────────

def recuperar_primos(p, t_max=300, t_step=0.02, altura_rel=0.03, verbose=False):
    """
    Recupera espectralmente todos os primos < p.

    Parâmetros
    ----------
    p          : primo alvo (o intervalo Q(p) = [2^(n-1), p-1] é usado)
    t_max      : limite superior de t na amostragem (padrão 300)
    t_step     : passo de amostragem em t (padrão 0.02, resolução 1/(N*dt))
    altura_rel : fração do pico máximo como limiar de detecção (padrão 0.03)

    Retorna
    -------
    lista ordenada de primos estimados < p
    """
    n     = p.bit_length() - 1
    start = 1 << (n - 1)

    xs          = np.arange(start, p)
    xs_compostos = np.array([x for x in xs if not is_prime(int(x))])

    t_vals = np.arange(0.1, t_max, t_step)
    res_fft = 1.0 / (len(t_vals) * t_step)
    if verbose:
        print(f"  Q({p}) = [{start}, {p-1}], |intervalo| = {len(xs)}")
        print(f"  Amostras: {len(t_vals)}, resolução FFT = {res_fft:.5f}")

    # Pré-computar os três sinais base
    logZQ    = log_modZ(xs, t_vals)
    logZc    = log_modZ(xs_compostos, t_vals)
    logzeta  = log_abs_zeta(t_vals)

    # ── Etapa 1: primos DENTRO do intervalo [start, p-1] ──
    R1 = logZQ - logZc
    candidatos1 = fft_picos(R1, t_step,
                            f_min=math.log(start) / (2*math.pi) - 0.02,
                            f_max=math.log(p)     / (2*math.pi) + 0.05,
                            altura_rel=altura_rel)
    primos_dentro = [q for q in candidatos1 if start <= q < p and is_prime(q)]
    if verbose:
        print(f"  Etapa 1 → primos dentro [{start},{p-1}]: {primos_dentro}")

    # ── Etapa 2: primos FORA do intervalo (< start) ──
    logZ_pd = log_modZ(np.array(primos_dentro, dtype=float), t_vals)
    R2 = logZQ - logzeta - logZ_pd
    candidatos2 = fft_picos(R2, t_step,
                            f_min=math.log(2)     / (2*math.pi) - 0.02,
                            f_max=math.log(start) / (2*math.pi) + 0.02,
                            altura_rel=altura_rel)
    primos_fora = [q for q in candidatos2 if 2 <= q < start and is_prime(q)]
    if verbose:
        print(f"  Etapa 2 → primos fora  [2,{start-1}]:   {primos_fora}")

    return sorted(set(primos_dentro + primos_fora))


# ── Testes ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    casos = [37, 41, 53]

    print("=" * 60)
    print("Recuperação espectral de primos < p (pipeline 2 estágios)")
    print("=" * 60)

    for p in casos:
        reais = [q for q in range(2, p) if is_prime(q)]
        print(f"\np = {p}")
        estimados = recuperar_primos(p, verbose=True)
        acertos = sorted(set(estimados) & set(reais))
        falsos  = sorted(set(estimados) - set(reais))
        missing = sorted(set(reais)     - set(estimados))
        print(f"  Resultado : {estimados}")
        print(f"  Reais     : {reais}")
        print(f"  Acertos   : {len(acertos)}/{len(reais)}")
        if falsos:  print(f"  Falsos+   : {falsos}")
        if missing: print(f"  Faltando  : {missing}")

        # Primorial
        if not falsos and not missing:
            d = math.prod(estimados)
            d_real = math.prod(reais)
            print(f"  Primorial : {d} {'✓' if d == d_real else '✗ (esperado '+str(d_real)+')'}")
