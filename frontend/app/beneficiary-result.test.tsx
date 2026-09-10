import { render, screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import type { Beneficiary, PaymentHistoryEntry } from '@/lib/types';
import { BeneficiaryResult } from './beneficiary-result';

function payment(referencePeriod: number): PaymentHistoryEntry {
  return {
    referencePeriod,
    grossAmount: '800.00',
    netAmount: '800.00',
    status: 'G',
    paymentType: 'N',
  };
}

function beneficiary(overrides: Partial<Beneficiary> = {}): Beneficiary {
  return {
    id: '00000000-0000-0000-0000-000000000003',
    maskedCpf: '***.***.247-25',
    fullName: 'Pessoa Beneficiaria',
    statusCode: 'A',
    statusDescription: 'Ativo',
    programCode: 'P003',
    familyIncome: '800.00',
    dependentCount: 1,
    regionCode: '15',
    nis: 12345678901,
    paymentHistory: [],
    ...overrides,
  };
}

describe('BeneficiaryResult', () => {
  it('exibe o CPF apenas mascarado', () => {
    // REQ-037 / AC-037.2
    render(<BeneficiaryResult beneficiary={beneficiary()} />);

    expect(screen.getByText('***.***.247-25')).toBeInTheDocument();
    expect(screen.queryByText(/52998/)).not.toBeInTheDocument();
  });

  it('exibe o código e a descrição da situação', () => {
    // REQ-038 / AC-038.2 — a situação nunca é comunicada só por cor.
    render(
      <BeneficiaryResult
        beneficiary={beneficiary({ statusCode: 'S', statusDescription: 'Suspenso' })}
      />,
    );

    expect(screen.getByText('S — Suspenso')).toBeInTheDocument();
  });

  it('informa explicitamente a ausência de pagamentos', () => {
    // REQ-041 / AC-041.1
    render(<BeneficiaryResult beneficiary={beneficiary()} />);

    expect(screen.getByText('Nenhum pagamento encontrado.')).toBeInTheDocument();
    expect(screen.queryByRole('table')).not.toBeInTheDocument();
  });

  it('lista o histórico na ordem recebida, do mais recente ao mais antigo', () => {
    // REQ-040 / AC-040.1 — a ordenação vem do backend; a interface não pode
    // reordenar nem inverter o que recebeu.
    render(
      <BeneficiaryResult
        beneficiary={beneficiary({
          paymentHistory: [payment(202603), payment(202602), payment(202601)],
        })}
      />,
    );

    const rows = within(screen.getByRole('table')).getAllByRole('row').slice(1);
    expect(rows.map((row) => within(row).getAllByRole('cell')[0]?.textContent)).toEqual([
      '03/2026',
      '02/2026',
      '01/2026',
    ]);
  });

  it('exibe no máximo os doze pagamentos recebidos', () => {
    // REQ-039 / AC-039.1
    const periods = [
      202603, 202602, 202601, 202512, 202511, 202510, 202509, 202508, 202507, 202506,
      202505, 202504,
    ];
    render(
      <BeneficiaryResult beneficiary={beneficiary({ paymentHistory: periods.map(payment) })} />,
    );

    expect(within(screen.getByRole('table')).getAllByRole('row')).toHaveLength(13);
  });
});
