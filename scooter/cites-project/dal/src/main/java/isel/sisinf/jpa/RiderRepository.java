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
            Long count = em.createQuery("SELECT COUNT(p) FROM Person p WHERE p.taxnumber = :taxnumber", Long.class)
                    .setParameter("taxnumber", rider.getTaxNumber())
                    .getSingleResult();
            if (count != null && count > 0) {
                throw new IllegalArgumentException("A customer with this tax number already exists.");
            }
            // Use native query to insert into the RIDER view, which will trigger the INSTEAD OF INSERT trigger
            em.persist(rider);
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
            return em.createQuery("SELECT r FROM Rider r", Rider.class)
                    .getResultList();
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

