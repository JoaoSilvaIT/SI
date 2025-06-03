package isel.sisinf.jpa;

import isel.sisinf.model.Dock;
import jakarta.persistence.*;

import java.util.List;

public class DockRepository {
    private EntityManagerFactory emf;

    public DockRepository(EntityManagerFactory emf) {
        this.emf = emf;
    }

    public List<Dock> getAllDocks() {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery("SELECT d FROM Dock d", Dock.class)
                    .setHint("jakarta.persistence.cache.storeMode", "REFRESH")
                    .getResultList();
        } finally {
            em.close();
        }
    }

    public List<Integer> getAllStations() {
        EntityManager em = emf.createEntityManager();
        try {
            return em.createQuery("SELECT DISTINCT d.station FROM Dock d", Integer.class).getResultList();
        } finally {
            em.close();
        }
    }

    public double getDockOccupancy(int stationId) {
        EntityManager em = emf.createEntityManager();
        try {
            Object result = em.createNativeQuery("SELECT fx_dock_occupancy(?1)")
                    .setParameter(1, stationId)
                    .getSingleResult();
            return ((java.math.BigDecimal) result).doubleValue();
        } finally {
            em.close();
        }
    }

    public Dock getDockByNumber(int number) {
        EntityManager em = emf.createEntityManager();
        try {
            return em.find(Dock.class, number);
        } finally {
            em.close();
        }
    }

    public void updateDock(Dock dock) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            em.merge(dock);
            tx.commit();
        } catch (OptimisticLockException e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }

    public void startTrip(int dockId, int clientId) {
        EntityManager em = emf.createEntityManager();
        EntityTransaction tx = em.getTransaction();
        try {
            tx.begin();
            em.createStoredProcedureQuery("startTrip")
                    .registerStoredProcedureParameter(1, Integer.class, ParameterMode.IN)
                    .registerStoredProcedureParameter(2, Integer.class, ParameterMode.IN)
                    .setParameter(1, dockId)
                    .setParameter(2, clientId)
                    .execute();
            tx.commit();
        } catch (PersistenceException e) {
            if (tx.isActive()) tx.rollback();
            throw e;
        } finally {
            em.close();
        }
    }
}
