import { formatAmount, formatPeriod } from '@/lib/api';
import type { Beneficiary } from '@/lib/types';

interface BeneficiaryResultProps {
  readonly beneficiary: Beneficiary;
}

/**
 * Exibe o cadastro e o histórico de pagamentos (REQ-037 a REQ-041).
 *
 * Server Component: não há interação, apenas apresentação dos dados já
 * buscados.
 */
export function BeneficiaryResult({ beneficiary }: BeneficiaryResultProps) {
  return (
    <section aria-labelledby="cadastro" className="mt-6 space-y-6">
      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 id="cadastro" className="mb-4 text-lg font-semibold">
          Dados cadastrais
        </h2>
        <dl className="grid grid-cols-1 gap-x-8 gap-y-3 sm:grid-cols-2">
          <Field label="Nome" value={beneficiary.fullName} />
          {/* REQ-037 — o CPF já chega mascarado do backend. */}
          <Field label="CPF" value={beneficiary.maskedCpf} />
          {/* REQ-038 — código e descrição juntos, nunca só cor. */}
          <Field
            label="Situação"
            value={`${beneficiary.statusCode} — ${beneficiary.statusDescription}`}
          />
          <Field label="Programa" value={beneficiary.programCode} />
          <Field label="Renda familiar" value={formatAmount(beneficiary.familyIncome)} />
          <Field label="Dependentes" value={String(beneficiary.dependentCount)} />
          <Field label="Região" value={beneficiary.regionCode} />
          <Field label="NIS" value={String(beneficiary.nis)} />
        </dl>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-6 shadow-sm">
        <h2 className="mb-4 text-lg font-semibold">Histórico de pagamentos</h2>
        {beneficiary.paymentHistory.length === 0 ? (
          // REQ-041 — ausência explícita, não uma tabela vazia.
          <p className="text-slate-600">Nenhum pagamento encontrado.</p>
        ) : (
          <>
            <table className="w-full text-left text-sm">
              <caption className="sr-only">
                Até doze pagamentos, do período mais recente para o mais antigo
              </caption>
              <thead>
                <tr className="border-b border-slate-200 text-slate-600">
                  <th scope="col" className="py-2">Período</th>
                  <th scope="col" className="py-2">Bruto</th>
                  <th scope="col" className="py-2">Líquido</th>
                  <th scope="col" className="py-2">Situação</th>
                  <th scope="col" className="py-2">Tipo</th>
                </tr>
              </thead>
              <tbody>
                {beneficiary.paymentHistory.map((payment) => (
                  <tr key={payment.referencePeriod} className="border-b border-slate-100">
                    <td className="py-2">{formatPeriod(payment.referencePeriod)}</td>
                    <td className="py-2">{formatAmount(payment.grossAmount)}</td>
                    <td className="py-2">{formatAmount(payment.netAmount)}</td>
                    <td className="py-2">{payment.status}</td>
                    <td className="py-2">{payment.paymentType}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <p className="mt-3 text-xs text-slate-500">
              Exibindo os {beneficiary.paymentHistory.length} pagamentos mais recentes, do
              período mais novo para o mais antigo.
            </p>
          </>
        )}
      </div>
    </section>
  );
}

function Field({ label, value }: { readonly label: string; readonly value: string }) {
  return (
    <div>
      <dt className="text-xs uppercase tracking-wide text-slate-500">{label}</dt>
      <dd className="text-sm font-medium">{value}</dd>
    </div>
  );
}
