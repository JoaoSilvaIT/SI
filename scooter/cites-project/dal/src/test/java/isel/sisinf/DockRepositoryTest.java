package isel.sisinf;

import isel.sisinf.model.Dock;
import isel.sisinf.jpa.DockRepository;
import jakarta.persistence.*;
import org.junit.AfterClass;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;

import java.sql.Timestamp;
import java.util.List;

import static org.junit.Assert.*;

public class DockRepositoryTest {
    private static EntityManagerFactory emf;
    private static DockRepository dockRepo;

    @BeforeClass
    public static void setUp() {
        emf = Persistence.createEntityManagerFactory("citesPU");
        dockRepo = new DockRepository(emf);
    }

    @AfterClass
    public static void tearDown() {
        if (emf != null) emf.close();
    }

    @Before
    public void setupTestData() {
        // Ensure we have at least one free dock for testing
        EntityManager em = emf.createEntityManager();
        try {
            List<Dock> freeDocks = em.createQuery(
                            "SELECT d FROM Dock d WHERE d.state = 'free'", Dock.class)
                    .getResultList();

            if (freeDocks.isEmpty()) {
                em.getTransaction().begin();

                Dock dock = new Dock();
                dock.setStation(1); // Using existing station ID
                dock.setState("free");
                dock.setScooter(null);
                dock.setVersion(new Timestamp(System.currentTimeMillis()));

                em.persist(dock);
                em.getTransaction().commit();
            }
        } finally {
            em.close();
        }
    }

    @Test
    public void testOptimisticLockingOnDock() {
        EntityManager em = emf.createEntityManager();
        Dock freeDock = null;
        try {
            freeDock = em.createQuery(
                            "SELECT d FROM Dock d WHERE d.state = 'free'", Dock.class)
                    .setMaxResults(1)
                    .getSingleResult();
        } catch (NoResultException e) {
            fail("No free dock found for test");
        } finally {
            em.close();
        }

        EntityManager em1 = emf.createEntityManager();
        EntityManager em2 = emf.createEntityManager();

        Dock dock1 = em1.find(Dock.class, freeDock.getNumber());
        Dock dock2 = em2.find(Dock.class, freeDock.getNumber());

        em1.getTransaction().begin();
        dock1.setState("occupy");
        dock1.setScooter(1);
        em1.merge(dock1);
        em1.getTransaction().commit();
        em1.close();

        em2.getTransaction().begin();
        dock2.setState("occupy");
        dock2.setScooter(2);
        em2.merge(dock2);

        try {
            em2.getTransaction().commit();
            fail("Expected OptimisticLockException");
        } catch (RollbackException ex) {
            assertTrue("Should be caused by OptimisticLockException",
                    ex.getCause() instanceof OptimisticLockException);
        } finally {
            if (em2.getTransaction().isActive()) {
                em2.getTransaction().rollback();
            }
            em2.close();
        }
    }
}