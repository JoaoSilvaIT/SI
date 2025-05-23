package isel.sisinf.jpa;

import isel.sisinf.model.Rider;
import jakarta.persistence.*;
import java.util.List;

public class RiderRepository {
    private EntityManagerFactory emf;

    public RiderRepository(EntityManagerFactory emf) {
        this.emf = emf;
    }

    public void createRider(Rider rider) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            // Check if a rider with the same tax number already exists
            Long count = (Long) em.createNativeQuery("SELECT COUNT(*) FROM PERSON WHERE taxnumber = ?1")
                .setParameter(1, rider.getTaxNumber())
                .getSingleResult();
            if (count != null && count > 0) {
                throw new IllegalArgumentException("A customer with this tax number already exists.");
            }
            // Use native query to insert into the RIDER view, which will trigger the INSTEAD OF INSERT trigger
            em.createNativeQuery(
                "INSERT INTO RIDER (email, taxnumber, name, dtregister, credit, typeofcard) VALUES (?1, ?2, ?3, ?4, ?5, ?6)")
                .setParameter(1, rider.getEmail())
                .setParameter(2, rider.getTaxNumber())
                .setParameter(3, rider.getName())
                .setParameter(4, rider.getDtRegister())
                .setParameter(5, rider.getCredit())
                .setParameter(6, rider.getTypeOfCard())
                .executeUpdate();
            tx.commit();
        } catch (Exception e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    public List<Rider> getAllRiders() {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createNativeQuery("SELECT id, email, taxnumber, name, dtregister, cardid, credit, typeofcard FROM RIDER", Rider.class).getResultList();
        } finally {
            em.close();
        }
    }

    public Rider getRiderById(int id) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.find(Rider.class, id);
        } finally {
            em.close();
        }
    }
}

