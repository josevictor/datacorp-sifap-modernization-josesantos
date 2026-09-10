import type { Beneficiary, BeneficiaryQueryResult, SearchType } from './types';

/**
 * Endereço do backend. É variável de servidor, sem o prefixo NEXT_PUBLIC_,
 * para que o endereço interno da API não seja embutido no pacote enviado ao
 * navegador.
 */
const API_URL = process.env.API_URL ?? 'http://localhost:8080';

/**
 * Consulta um beneficiário por CPF ou NIS (REQ-034 e REQ-035).
 *
 * O critério é o parâmetro enviado, substituindo o campo de tela
 * `#TYPE-SEARCH` do programa legado.
 */
export async function findBeneficiary(
  searchType: SearchType,
  term: string,
): Promise<BeneficiaryQueryResult> {
  const query = new URLSearchParams({ [searchType]: term });

  let response: Response;
  try {
    response = await fetch(`${API_URL}/api/v1/beneficiaries?${query}`, {
      cache: 'no-store',
    });
  } catch {
    return { kind: 'error', message: 'Não foi possível contatar o serviço de consulta.' };
  }

  if (response.status === 404) {
    return { kind: 'not-found' };
  }

  // REQ-036 — o backend rejeita o CPF inválido sem acessar o cadastro. A
  // interface distingue esse caso de "não encontrado": um é erro de digitação,
  // o outro é ausência de cadastro.
  if (response.status === 422) {
    return { kind: 'invalid-cpf' };
  }

  if (!response.ok) {
    return { kind: 'error', message: 'A consulta falhou.' };
  }

  const beneficiary = (await response.json()) as Beneficiary;
  return { kind: 'found', beneficiary };
}

/** Formata o período `AAAAMM` como `MM/AAAA`. */
export function formatPeriod(period: number): string {
  const text = String(period);
  return `${text.slice(4, 6)}/${text.slice(0, 4)}`;
}

/** Formata um valor decimal recebido como texto na moeda local. */
export function formatAmount(amount: string): string {
  return new Intl.NumberFormat('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  }).format(Number(amount));
}
