package com.datacorp.sifap.payments;

import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface PaymentRepository extends JpaRepository<Payment, UUID> {

    boolean existsByCpfAndReferencePeriod(String cpf, int referencePeriod);
}
