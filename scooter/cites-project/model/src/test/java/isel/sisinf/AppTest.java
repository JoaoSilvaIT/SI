package isel.sisinf;

import junit.framework.Test;
import junit.framework.TestCase;
import junit.framework.TestSuite;

/**
 * Unit test for simple App.
 */
public class AppTest 
    extends TestCase
{
    /**
     * Create the test case
     *
     * @param testName name of the test case
     */
    public AppTest( String testName )
    {
        super( testName );
    }

    /**
     * @return the suite of tests being tested
     */
    public static Test suite()
    {
        return new TestSuite( AppTest.class );
    }

    /**
     * Rigourous Test :-)
     */
    public void testApp()
    {
        assertTrue( true );
    }

    public void testRiderModel() {
        isel.sisinf.model.Rider rider = new isel.sisinf.model.Rider();
        rider.setId(1);
        rider.setEmail("test@email.com");
        rider.setTaxNumber(123456789);
        rider.setName("Test Rider");
        java.sql.Timestamp now = new java.sql.Timestamp(System.currentTimeMillis());
        rider.setDtRegister(now);
        rider.setCardId(10);
        rider.setCredit(15.5);
        rider.setTypeOfCard("resident");
        assertEquals(1, rider.getId());
        assertEquals("test@email.com", rider.getEmail());
        assertEquals(123456789, rider.getTaxNumber());
        assertEquals("Test Rider", rider.getName());
        assertEquals(now, rider.getDtRegister());
        assertEquals(10, rider.getCardId());
        assertEquals(15.5, rider.getCredit());
        assertEquals("resident", rider.getTypeOfCard());
    }

    public void testDockModel() {
        isel.sisinf.model.Dock dock = new isel.sisinf.model.Dock();
        dock.setNumber(5);
        dock.setStation(2);
        dock.setState("free");
        dock.setScooter(null);
        java.sql.Timestamp now = new java.sql.Timestamp(System.currentTimeMillis());
        dock.setVersion(now);
        assertEquals(5, dock.getNumber());
        assertEquals(2, dock.getStation());
        assertEquals("free", dock.getState());
        assertNull(dock.getScooter());
        assertEquals(now, dock.getVersion());
    }

    public void testScooterModel() {
        isel.sisinf.model.Scooter scooter = new isel.sisinf.model.Scooter();
        scooter.setId(7);
        scooter.setWeight(12.5);
        scooter.setMaxVelocity(25.0);
        scooter.setBattery(80);
        scooter.setModel(3);
        java.sql.Timestamp now = new java.sql.Timestamp(System.currentTimeMillis());
        scooter.setVersion(now);
        assertEquals(7, scooter.getId());
        assertEquals(12.5, scooter.getWeight());
        assertEquals(25.0, scooter.getMaxVelocity());
        assertEquals(80, scooter.getBattery());
        assertEquals(3, scooter.getModel());
        assertEquals(now, scooter.getVersion());
    }
}
