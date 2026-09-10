package com.datacorp.sifap.payments;

import java.util.Collection;
import java.util.List;
import java.util.UUID;
import org.springframework.data.domain.Limit;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

interface PaymentRepository extends JpaRepository<Payment, UUID> {

    boolean existsByCpfAndReferencePeriod(String cpf, int referencePeriod);

    /**
     * Histórico de pagamentos do período mais recente para o mais antigo
     * (REQ-039 e REQ-040).
     *
     * <p>O legado rotula o bloco como {@code LAST 12} mas executa
     * {@code READ PAYMENT-V BY NUM-CPF} (CONSBENF.NSP:270-284), que percorre
     * pelo descritor de CPF e corta na décima segunda ocorrência sem ordenar
     * por período. Com mais de doze pagamentos, ele pode exibir os mais
     * antigos sob um rótulo que promete os mais recentes.
     *
     * <p>A ordenação explícita é a correção deliberada de REQ-040.
     */
    List<Payment> findByCpfOrderByReferencePeriodDesc(String cpf, Limit limit);

    /**
     * Chaves {@code (cpf, período)} já gravadas para os CPFs informados.
     *
     * <p>Usada pela carga legada para decidir idempotência em lote, evitando
     * uma consulta por pagamento durante a importação.
     */
    @Query("select concat(p.cpf, '#', p.referencePeriod) from Payment p where p.cpf in :cpfs")
    List<String> findExistingKeys(@Param("cpfs") Collection<String> cpfs);
}
