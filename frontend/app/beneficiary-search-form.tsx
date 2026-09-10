'use client';

import { useState } from 'react';
import type { SearchType } from '@/lib/types';

interface BeneficiarySearchFormProps {
  readonly initialSearchType: SearchType;
  readonly initialTerm: string;
}

/**
 * Formulário de busca (REQ-034 e REQ-035).
 *
 * É o único componente cliente da página: precisa de estado para alternar
 * entre CPF e NIS. O envio usa GET, então o resultado fica endereçável pela
 * URL e a página permanece um Server Component.
 */
export function BeneficiarySearchForm({
  initialSearchType,
  initialTerm,
}: BeneficiarySearchFormProps) {
  const [searchType, setSearchType] = useState<SearchType>(initialSearchType);

  return (
    <form method="get" className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
      <fieldset className="mb-4">
        <legend className="mb-2 text-sm font-medium text-slate-700">Buscar por</legend>
        <div className="flex gap-4">
          {(['cpf', 'nis'] as const).map((option) => (
            <label key={option} className="flex items-center gap-2 text-sm">
              <input
                type="radio"
                name="tipo"
                value={option}
                checked={searchType === option}
                onChange={() => setSearchType(option)}
                className="h-4 w-4"
              />
              {option.toUpperCase()}
            </label>
          ))}
        </div>
      </fieldset>

      <div className="flex flex-col gap-2 sm:flex-row sm:items-end">
        <div className="flex-1">
          <label htmlFor="termo" className="mb-1 block text-sm font-medium text-slate-700">
            {searchType === 'cpf' ? 'CPF (11 dígitos)' : 'NIS'}
          </label>
          <input
            id="termo"
            name="termo"
            type="text"
            inputMode="numeric"
            defaultValue={initialTerm}
            required
            className="w-full rounded-md border border-slate-300 px-3 py-2"
          />
        </div>
        <button
          type="submit"
          className="rounded-md bg-slate-900 px-4 py-2 font-medium text-white hover:bg-slate-700"
        >
          Consultar
        </button>
      </div>
    </form>
  );
}
