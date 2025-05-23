package isel.sisinf;

import isel.sisinf.jpa.DockRepository;
import isel.sisinf.jpa.RiderRepository;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import static org.junit.Assert.*;

public class AppTest {
    private EntityManagerFactory emf;
    private RiderRepository riderRepo;
    private DockRepository dockRepo;

    @Before
    public void setUp() {
        emf = Persistence.createEntityManagerFactory("citesPU");
        riderRepo = new RiderRepository(emf);
        dockRepo = new DockRepository(emf);
    }

    @After
    public void tearDown() {
        if (emf != null) emf.close();
    }

    @Test
    public void testGetDockOccupancy() {
        // Test dock occupancy function integration
        int stationId = dockRepo.getAllStations().get(0);
        double occupancy = dockRepo.getDockOccupancy(stationId);
        assertTrue("Occupancy should be between 0 and 1", occupancy >= 0.0 && occupancy <= 1.0);
    }

    @Test
    public void testRiderViewIntegration() {
        // Test that the Rider view mapping works correctly
        assertFalse("Should find at least one rider", riderRepo.getAllRiders().isEmpty());
    }
}