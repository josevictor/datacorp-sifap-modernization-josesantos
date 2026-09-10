package com.datacorp.sifap.payments;

import java.util.Collection;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

interface BeneficiaryRepository extends JpaRepository<Beneficiary, UUID> {

    Optional<Beneficiary> findByCpf(String cpf);

    // REQ-035 — o legado busca por NIS no descritor NUM-NIS
    // (CONSBENF.NSP:156-163), sem validar o número antes.
    Optional<Beneficiary> findByNis(long nis);

    // Usado pela carga legada para decidir idempotência em lote, evitando uma
    // consulta por registro durante a importação.
    @Query("select b.cpf from Beneficiary b where b.cpf in :cpfs")
    List<String> findExistingCpfs(@Param("cpfs") Collection<String> cpfs);

    // Só NIS preenchidos participam da unicidade: o valor 0 representa ausência
    // e pode se repetir, conforme a supressão de nulos do descritor DE,UQ,NU.
    @Query("select b.nis from Beneficiary b where b.nis > 0 and b.nis in :values")
    List<Long> findExistingNis(@Param("values") Collection<Long> values);
}
