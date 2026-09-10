import { afterEach, describe, expect, it, vi } from 'vitest';
import { findBeneficiary, formatPeriod } from './api';

function jsonResponse(status: number, body: unknown): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'content-type': 'application/json' },
  });
}

afterEach(() => {
  vi.unstubAllGlobals();
});

describe('findBeneficiary', () => {
  it('envia o CPF como critério de busca', async () => {
    // REQ-034 / AC-034.1
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, { maskedCpf: '***.***.247-25' }));
    vi.stubGlobal('fetch', fetchMock);

    const result = await findBeneficiary('cpf', '52998224725');

    expect(fetchMock.mock.calls[0]?.[0]).toContain('cpf=52998224725');
    expect(result.kind).toBe('found');
  });

  it('envia o NIS como critério de busca', async () => {
    // REQ-035 / AC-035.1
    const fetchMock = vi.fn().mockResolvedValue(jsonResponse(200, { nis: 700100200 }));
    vi.stubGlobal('fetch', fetchMock);

    await findBeneficiary('nis', '700100200');

    expect(fetchMock.mock.calls[0]?.[0]).toContain('nis=700100200');
  });

  it('distingue beneficiário não encontrado de CPF inválido', async () => {
    // REQ-034 / AC-034.2 e REQ-036 / AC-036.1 — são causas diferentes: uma é
    // ausência de cadastro, a outra é erro de digitação. Colapsá-las em uma
    // única mensagem esconderia do usuário o que ele precisa corrigir.
    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse(404, {})));
    expect((await findBeneficiary('cpf', '11144477735')).kind).toBe('not-found');

    vi.stubGlobal('fetch', vi.fn().mockResolvedValue(jsonResponse(422, {})));
    expect((await findBeneficiary('cpf', '52998224724')).kind).toBe('invalid-cpf');
  });

  it('trata falha de rede como erro, sem lançar exceção', async () => {
    // REQ-034 — a indisponibilidade do serviço não pode derrubar a página.
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('offline')));

    const result = await findBeneficiary('cpf', '52998224725');

    expect(result.kind).toBe('error');
  });
});

describe('formatPeriod', () => {
  it('formata o período AAAAMM como MM/AAAA', () => {
    // REQ-039
    expect(formatPeriod(202603)).toBe('03/2026');
  });
});
