/**
 * Contratos de resposta da API de consulta de beneficiário (REQ-034 a
 * REQ-041).
 *
 * O CPF chega sempre mascarado: o backend nunca devolve o documento completo.
 */

export interface PaymentHistoryEntry {
  readonly referencePeriod: number;
  readonly grossAmount: string;
  readonly netAmount: string;
  readonly status: string;
  readonly paymentType: string;
}

export interface Beneficiary {
  readonly id: string;
  readonly maskedCpf: string;
  readonly fullName: string;
  readonly statusCode: string;
  readonly statusDescription: string;
  readonly programCode: string;
  readonly familyIncome: string;
  readonly dependentCount: number;
  readonly regionCode: string;
  readonly nis: number;
  readonly paymentHistory: readonly PaymentHistoryEntry[];
}

export type SearchType = 'cpf' | 'nis';

/**
 * Resultado da consulta. O erro é modelado como valor, não como exceção, para
 * que a página trate "não encontrado" e "CPF inválido" como estados normais da
 * interface, e não como falha.
 */
export type BeneficiaryQueryResult =
  | { readonly kind: 'found'; readonly beneficiary: Beneficiary }
  | { readonly kind: 'not-found' }
  | { readonly kind: 'invalid-cpf' }
  | { readonly kind: 'error'; readonly message: string };
