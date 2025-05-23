package isel.sisinf;

import isel.sisinf.model.Rider;
import isel.sisinf.jpa.RiderRepository;
import jakarta.persistence.EntityManagerFactory;
import jakarta.persistence.Persistence;
import org.junit.AfterClass;
import org.junit.BeforeClass;
import org.junit.Test;

import java.sql.Timestamp;
import java.util.List;

import static org.junit.Assert.*;

public class RiderRepositoryTest {
    private static EntityManagerFactory emf;
    private static RiderRepository repo;

    @BeforeClass
    public static void setUp() {
        emf = Persistence.createEntityManagerFactory("citesPU");
        repo = new RiderRepository(emf);
    }

    @AfterClass
    public static void tearDown() {
        if (emf != null) emf.close();
    }

    @Test
    public void testCreateAndFindRider() {
        Rider rider = new Rider();
        rider.setName("Test User");
        rider.setEmail("testuser@email.com");
        rider.setTaxNumber(111222333);
        rider.setDtRegister(Timestamp.valueOf("2025-05-22 10:00:00"));
        rider.setCredit(10.0);
        rider.setTypeOfCard("resident");
        try {
            repo.createRider(rider);
        } catch (Exception e) {
        }
        List<Rider> riders = repo.getAllRiders();
        boolean found = riders.stream().anyMatch(r -> r.getEmail().equals("testuser@email.com"));
        assertTrue("Created rider should be found in the list", found);
    }
}

