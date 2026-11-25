/-
  Espectral.Bloco
  ===============

  Formalização dos resultados aritméticos que sustentam o artigo
  "Irredutibilidade logarítmica: o que sobrevive quando um crivo espectral
  encontra a aritmética" (T. Bandeira, 2026).

  Conteúdo:
  * `Bloco k`      -- o bloco binário A_k = [2^k, 2^(k+1) - 1]
  * `Semente k`    -- a semente S_k    = { p primo : p < 2^k }
  * `minFac_lt_dois_pow` / `existe_fator_primo_na_semente`
        -- lema do bloco (Lema 4 do artigo)
  * `bloco_primo_iff`  -- corretude do crivo por blocos (Corolário 5)
  * `logRedutivel_iff` -- irredutibilidade logarítmica (Teorema 3)
-/
import Mathlib.Data.Nat.Prime.Basic
import Mathlib.Data.Nat.Factorization.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

set_option maxHeartbeats 1000000

namespace Espectral

open Finset

/-! ## Blocos binários e sementes -/

/-- O bloco binário `A k = [2^k, 2^(k+1) - 1]`. -/
def Bloco (k : ℕ) : Finset ℕ := Icc (2 ^ k) (2 ^ (k + 1) - 1)

/-- A semente do nível `k`: os primos estritamente menores que `2^k`. -/
def Semente (k : ℕ) : Finset ℕ := (range (2 ^ k)).filter Nat.Prime

@[simp] theorem mem_Bloco {k m : ℕ} : m ∈ Bloco k ↔ 2 ^ k ≤ m ∧ m ≤ 2 ^ (k + 1) - 1 := by
  simp [Bloco]

@[simp] theorem mem_Semente {k p : ℕ} : p ∈ Semente k ↔ p.Prime ∧ p < 2 ^ k := by
  rw [Semente, Finset.mem_filter, Finset.mem_range]
  exact ⟨fun h => ⟨h.2, h.1⟩, fun h => ⟨h.2, h.1⟩⟩

/-! ## O lema do bloco -/

/-- O menor fator primo de um composto de `A k` está abaixo da base do bloco. -/
theorem minFac_lt_dois_pow (k m : ℕ) (hk : 1 ≤ k) (hlo : 2 ^ k ≤ m)
    (hhi : m < 2 ^ (k + 1)) (hc : ¬ m.Prime) : Nat.minFac m < 2 ^ k := by
  have hm0 : 0 < m := lt_of_lt_of_le (by positivity) hlo
  have hsq : Nat.minFac m ^ 2 ≤ m := Nat.minFac_sq_le_self hm0 hc
  by_contra hge
  rw [not_lt] at hge
  have h1 : (2 ^ k) ^ 2 ≤ (Nat.minFac m) ^ 2 := Nat.pow_le_pow_left hge 2
  have hpow : (2 : ℕ) ^ (2 * k) = (2 ^ k) ^ 2 := by
    rw [mul_comm 2 k, pow_mul]
  have h2 : (2 : ℕ) ^ (2 * k) ≤ m := by omega
  have h3 : (2 : ℕ) ^ (2 * k) < 2 ^ (k + 1) := lt_of_le_of_lt h2 hhi
  have h4 : 2 * k < k + 1 := by
    by_contra hle
    rw [not_lt] at hle
    have hmono : (2 : ℕ) ^ (k + 1) ≤ 2 ^ (2 * k) := Nat.pow_le_pow_right (by norm_num) hle
    omega
  omega

/-- **Lema do bloco binário.** Se `m ∈ A k` é composto, algum primo (a saber, seu
menor fator primo) divide `m` e é menor que `2^k`, isto é, pertence a `S k`. -/
theorem existe_fator_primo_na_semente (k m : ℕ) (hk : 1 ≤ k) (hlo : 2 ^ k ≤ m)
    (hhi : m < 2 ^ (k + 1)) (hc : ¬ m.Prime) :
    ∃ p, p.Prime ∧ p ∣ m ∧ p < 2 ^ k := by
  have h := minFac_lt_dois_pow k m hk hlo hhi hc
  have hm1 : m ≠ 1 := by
    intro h1
    rw [h1] at hlo
    have : (2 : ℕ) ^ k ≤ 1 := hlo
    have : 2 ≤ (2 : ℕ) ^ k := by
      calc (2 : ℕ) = 2 ^ 1 := by norm_num
        _ ≤ 2 ^ k := Nat.pow_le_pow_right (by norm_num) hk
    omega
  exact ⟨Nat.minFac m, Nat.minFac_prime hm1, Nat.minFac_dvd m, h⟩

/-- **Corretude do crivo por blocos.** Um elemento do bloco é primo se e somente
se nenhum primo abaixo da base do bloco o divide. É esta equivalência que o
algoritmo final (Nota 29) implementa. -/
theorem bloco_primo_iff (k m : ℕ) (hk : 1 ≤ k) (hlo : 2 ^ k ≤ m)
    (hhi : m < 2 ^ (k + 1)) :
    m.Prime ↔ ∀ p, p.Prime → p ∣ m → 2 ^ k ≤ p := by
  constructor
  · intro hp p hpp hpd
    rcases hp.eq_one_or_self_of_dvd p hpd with h | h
    · exact absurd h hpp.ne_one
    · omega
  · intro h
    by_contra hc
    obtain ⟨p, hpp, hpd, hplt⟩ := existe_fator_primo_na_semente k m hk hlo hhi hc
    exact absurd (h p hpp hpd) (by omega)

/-! ## Irredutibilidade logarítmica -/

/-- `m` é logaritmicamente redutível: `log m` é combinação linear inteira de
logaritmos de primos **menores** que `m`. -/
def LogRedutivel (m : ℕ) : Prop :=
  ∃ (s : Finset ℕ) (e : ℕ → ℕ), (∀ p ∈ s, p.Prime) ∧ (∀ p ∈ s, p < m) ∧
    (∀ p ∈ s, 0 < e p) ∧ Real.log m = ∑ p ∈ s, (e p : ℝ) * Real.log p

/-- O logaritmo do produto das potências é a soma ponderada dos logaritmos. -/
theorem log_prod_pow {s : Finset ℕ} {e : ℕ → ℕ} (hpos : ∀ p ∈ s, 0 < p) :
    Real.log (∏ p ∈ s, (p : ℝ) ^ (e p)) = ∑ p ∈ s, (e p : ℝ) * Real.log p := by
  rw [Real.log_prod (fun p hp => by
    have hp' : (0 : ℝ) < (p : ℝ) := by exact_mod_cast hpos p hp
    exact pow_ne_zero _ hp'.ne')]
  exact Finset.sum_congr rfl fun p hp => by rw [Real.log_pow]

/-- Se a decomposição logarítmica existe, então `m` é aquele produto. -/
theorem eq_prod_of_log_eq {m : ℕ} {s : Finset ℕ} {e : ℕ → ℕ} (hm : 0 < m)
    (hpos : ∀ p ∈ s, 0 < p) (h : Real.log m = ∑ p ∈ s, (e p : ℝ) * Real.log p) :
    m = ∏ p ∈ s, p ^ (e p) := by
  have hcast : ((∏ p ∈ s, p ^ (e p) : ℕ) : ℝ) = ∏ p ∈ s, (p : ℝ) ^ (e p) := by
    push_cast
    rfl
  have hlogN : Real.log (∏ p ∈ s, (p : ℝ) ^ (e p)) =
      ∑ p ∈ s, (e p : ℝ) * Real.log p := log_prod_pow hpos
  have hlog : Real.log (m : ℝ) = Real.log ((∏ p ∈ s, p ^ (e p) : ℕ) : ℝ) := by
    rw [hcast, hlogN]
    exact h
  have hposN : (0 : ℝ) < ((∏ p ∈ s, p ^ (e p) : ℕ) : ℝ) := by
    have hnn : 0 < ∏ p ∈ s, p ^ (e p) :=
      Finset.prod_pos fun p hp => pow_pos (hpos p hp) _
    exact_mod_cast hnn
  have hmR : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  have hinj := Real.log_injOn_pos (show (m : ℝ) ∈ Set.Ioi 0 from hmR)
    (show ((∏ p ∈ s, p ^ (e p) : ℕ) : ℝ) ∈ Set.Ioi 0 from hposN) hlog
  exact_mod_cast hinj

/-- **Teorema 3** (irredutibilidade logarítmica). Para `m ≥ 2`, `log m` é
combinação linear inteira de logs de primos menores que `m` se e somente se `m`
é composto. -/
theorem logRedutivel_iff (m : ℕ) (hm : 2 ≤ m) : LogRedutivel m ↔ ¬ m.Prime := by
  constructor
  · rintro ⟨s, e, hprime, hlt, he, hlog⟩
    intro hmp
    have hm0 : 0 < m := by omega
    have hsne : s.Nonempty := by
      rcases Finset.eq_empty_or_nonempty s with rfl | h
      · rw [Finset.sum_empty] at hlog
        have hlog0 : Real.log (m : ℝ) = 0 := hlog
        have hpos' : (0 : ℝ) < Real.log (m : ℝ) :=
          Real.log_pos (by exact_mod_cast (by omega : 1 < m))
        linarith
      · exact h
    obtain ⟨p0, hp0⟩ := hsne
    have hprod := eq_prod_of_log_eq hm0 (fun p hp => (hprime p hp).pos) hlog
    have hdvd : p0 ∣ m := by
      rw [hprod]
      have h1 : p0 ^ 1 ∣ p0 ^ (e p0) := pow_dvd_pow p0 (he p0 hp0)
      have h2 : p0 ^ (e p0) ∣ ∏ p ∈ s, p ^ (e p) :=
        Finset.dvd_prod_of_mem (fun p => p ^ (e p)) hp0
      simpa using dvd_trans h1 h2
    rcases hmp.eq_one_or_self_of_dvd p0 hdvd with h | h
    · exact absurd h (hprime p0 hp0).ne_one
    · have hp0lt : p0 < m := hlt p0 hp0
      omega
  · intro hc
    have hm0 : m ≠ 0 := by omega
    have hlt : ∀ p ∈ m.primeFactors, p < m := by
      intro p hp
      have hpne : p ≠ m := by
        intro h
        exact hc (h ▸ Nat.prime_of_mem_primeFactors hp)
      exact lt_of_le_of_ne (Nat.le_of_dvd (by omega) (Nat.dvd_of_mem_primeFactors hp)) hpne
    refine ⟨m.primeFactors, m.factorization, ?_, hlt, ?_, ?_⟩
    · intro p hp
      exact Nat.prime_of_mem_primeFactors hp
    · intro p hp
      exact (Nat.prime_of_mem_primeFactors hp).factorization_pos_of_dvd hm0
        (Nat.dvd_of_mem_primeFactors hp)
    · calc Real.log (m : ℝ)
          = Real.log ((∏ p ∈ m.primeFactors, p ^ m.factorization p : ℕ) : ℝ) := by
            conv_lhs => rw [Nat.prod_primeFactors_pow_factorization hm0]
        _ = ∑ p ∈ m.primeFactors, (m.factorization p : ℝ) * Real.log p := by
            push_cast
            exact log_prod_pow (s := m.primeFactors) (e := m.factorization)
              (fun p hp => (Nat.prime_of_mem_primeFactors hp).pos)

end Espectral
