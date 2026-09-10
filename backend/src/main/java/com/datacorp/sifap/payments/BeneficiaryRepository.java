package com.datacorp.sifap.payments;

import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface BeneficiaryRepository extends JpaRepository<Beneficiary, UUID> {

    Optional<Beneficiary> findByCpf(String cpf);

    // REQ-035 — o legado busca por NIS no descritor NUM-NIS
    // (CONSBENF.NSP:156-163), sem validar o número antes.
    Optional<Beneficiary> findByNis(long nis);
}
