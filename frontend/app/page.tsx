import { findBeneficiary } from '@/lib/api';
import type { BeneficiaryQueryResult, SearchType } from '@/lib/types';
import { BeneficiaryResult } from './beneficiary-result';
import { BeneficiarySearchForm } from './beneficiary-search-form';

interface PageProps {
  readonly searchParams: Promise<{ tipo?: string; termo?: string }>;
}

/**
 * Página de consulta de beneficiário (REQ-034 a REQ-042).
 *
 * Server Component: a busca acontece no servidor, então o endereço da API e a
 * resposta completa nunca passam pelo navegador.
 */
export default async function Page({ searchParams }: PageProps) {
  const params = await searchParams;
  const searchType: SearchType = params.tipo === 'nis' ? 'nis' : 'cpf';
  const term = params.termo?.trim() ?? '';

  const result: BeneficiaryQueryResult | null =
    term === '' ? null : await findBeneficiary(searchType, term);

  return (
    <main>
      <h1 className="mb-6 text-2xl font-bold">Consulta de beneficiário</h1>

      <BeneficiarySearchForm initialSearchType={searchType} initialTerm={term} />

      {result !== null && <Result result={result} />}
    </main>
  );
}

function Result({ result }: { readonly result: BeneficiaryQueryResult }) {
  if (result.kind === 'found') {
    return <BeneficiaryResult beneficiary={result.beneficiary} />;
  }

  const message =
    result.kind === 'not-found'
      ? 'Beneficiário não encontrado.'
      : result.kind === 'invalid-cpf'
        ? 'CPF inválido. Verifique os dígitos informados.'
        : result.message;

  return (
    <p role="status" className="mt-6 rounded-md border border-amber-200 bg-amber-50 p-4">
      {message}
    </p>
  );
}
