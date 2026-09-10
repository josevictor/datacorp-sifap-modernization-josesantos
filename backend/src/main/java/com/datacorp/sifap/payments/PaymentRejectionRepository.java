package com.datacorp.sifap.payments;

import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface PaymentRejectionRepository extends JpaRepository<PaymentRejection, UUID> {
}
