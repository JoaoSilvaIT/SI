package isel.sisinf;

import isel.sisinf.model.Rider;
import isel.sisinf.model.Dock;
import isel.sisinf.jpa.RiderRepository;
import isel.sisinf.jpa.DockRepository;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import jakarta.persistence.OptimisticLockException;
import jakarta.persistence.RollbackException;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.sql.Timestamp;
import java.util.List;

import static org.junit.Assert.*;

public class AppTest {
    private static EntityManagerFactory emf;
    private static RiderRepository riderRepo;
    private static DockRepository dockRepo;

    @BeforeClass
    public static void setUp() {
        emf = Persistence.createEntityManagerFactory("citesPU");
        riderRepo = new RiderRepository(emf);
        dockRepo = new DockRepository(emf);
    }

    @AfterClass
    public static void tearDown() {
        if (emf != null) emf.close();
    }

    @Test
    public void testCreateAndFindRider() {
        Rider rider = new Rider();
        rider.setName("Integration Test User");
        rider.setEmail("integrationtest@email.com");
        rider.setTaxNumber(123123123);
        rider.setDtRegister(Timestamp.valueOf("2025-05-22 12:00:00"));
        rider.setCredit(20.0);
        rider.setTypeOfCard("resident");
        try {
            riderRepo.createRider(rider);
        } catch (Exception e) {
            // Ignore if already exists
        }
        List<Rider> riders = riderRepo.getAllRiders();
        boolean found = riders.stream().anyMatch(r -> r.getEmail().equals("integrationtest@email.com"));
        assertTrue("Created rider should be found in the list", found);
    }

    @Test
    public void testDockOccupancyFunction() {
        List<Integer> stations = dockRepo.getAllStations();
        assertFalse("There should be at least one station", stations.isEmpty());
        int stationId = stations.get(0);
        double occupancy = dockRepo.getDockOccupancy(stationId);
        assertTrue("Occupancy should be between 0 and 1", occupancy >= 0.0 && occupancy <= 1.0);
    }

    @Test
    public void testOptimisticLockingOnDock() {
        int dockNumber = dockRepo.getAllDocks().stream()
            .filter(d -> "free".equalsIgnoreCase(d.getState()))
            .map(Dock::getNumber)
            .findFirst()
            .orElseThrow(() -> new RuntimeException("No free dock found for test"));

        var em1 = emf.createEntityManager();
        var em2 = emf.createEntityManager();
        Dock dock1 = em1.find(Dock.class, dockNumber);
        Dock dock2 = em2.find(Dock.class, dockNumber);

        em1.getTransaction().begin();
        dock1.setState("occupy");
        dock1.setScooter(1); // Use a valid scooter id
        em1.merge(dock1);
        em1.getTransaction().commit();
        em1.close();

        em2.getTransaction().begin();
        dock2.setState("occupy");
        dock2.setScooter(2); // Use a different valid scooter id
        em2.merge(dock2);
        try {
            em2.getTransaction().commit();
            fail("Expected OptimisticLockException");
        } catch (RollbackException ex) {
            assertNotNull(ex.getCause());
            assertTrue(ex.getCause() instanceof OptimisticLockException);
        } finally {
            em2.close();
        }
    }
}
