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

