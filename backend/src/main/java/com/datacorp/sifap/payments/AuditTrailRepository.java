package com.datacorp.sifap.payments;

import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface AuditTrailRepository extends JpaRepository<AuditTrail, UUID> {

    long countByAffectedCpf(String affectedCpf);
}
