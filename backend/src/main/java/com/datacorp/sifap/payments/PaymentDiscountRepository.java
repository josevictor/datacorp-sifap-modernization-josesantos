package com.datacorp.sifap.payments;

import java.util.List;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface PaymentDiscountRepository extends JpaRepository<PaymentDiscount, UUID> {

    List<PaymentDiscount> findByPaymentIdOrderBySequenceNumberAsc(UUID paymentId);
}
