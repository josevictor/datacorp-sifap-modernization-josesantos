package com.datacorp.sifap.payments;

import java.util.Optional;
import java.util.UUID;
import org.springframework.data.jpa.repository.JpaRepository;

interface SocialProgramRepository extends JpaRepository<SocialProgram, UUID> {

    Optional<SocialProgram> findByCode(String code);
}
