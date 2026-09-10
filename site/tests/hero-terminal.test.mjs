import assert from "node:assert/strict";
import test from "node:test";
import { t } from "../src/lib/i18n.ts";
import { localeCodes } from "../src/lib/model.ts";

test("should localize the legacy terminal and identify it as a visual simulation", () => {
  // REQ-PORTAL-002, REQ-PORTAL-006
  const expected = {
    en: {
      terminalTitle: "Beneficiary query",
      terminalSearchType: "Search type",
      terminalReady: "Awaiting query",
      terminalSubmit: "Query",
      terminalExit: "Exit",
      terminalSimulation: "Visual simulation",
      terminalEmpty: "Empty field",
      terminalNotice: "Demonstration only. No connection to real data.",
    },
    es: {
      terminalTitle: "Consulta de beneficiarios",
      terminalSearchType: "Tipo de búsqueda",
      terminalReady: "Esperando consulta",
      terminalSubmit: "Consultar",
      terminalExit: "Salir",
      terminalSimulation: "Simulación visual",
      terminalEmpty: "Campo vacío",
      terminalNotice: "Solo demostración. Sin conexión a datos reales.",
    },
    "pt-br": {
      terminalTitle: "Consulta de beneficiários",
      terminalSearchType: "Tipo de pesquisa",
      terminalReady: "Aguardando consulta",
      terminalSubmit: "Consultar",
      terminalExit: "Sair",
      terminalSimulation: "Simulação visual",
      terminalEmpty: "Campo vazio",
      terminalNotice: "Apenas demonstração. Sem conexão com dados reais.",
    },
  };

  assert.deepEqual(Object.keys(expected), [...localeCodes]);
  for (const locale of localeCodes) {
    const words = t(locale);
    for (const [key, value] of Object.entries(expected[locale])) {
      assert.equal(words[key], value, `${locale}: ${key}`);
    }
    assert.match(words.terminalLabel, /SIFAP/);
    assert.match(words.terminalLabel, /3270/);
    assert.match(words.terminalCaption, /SIFAP/);
  }
  for (const key of ["terminalLabel", "terminalCaption", "terminalNotice"]) {
    assert.equal(new Set(localeCodes.map((locale) => t(locale)[key])).size, localeCodes.length, key);
  }
});
