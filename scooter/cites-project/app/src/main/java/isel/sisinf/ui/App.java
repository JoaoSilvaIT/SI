
/*
MIT License

Copyright (c) 2025, Nuno Datia, Matilde Pato, ISEL

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
package isel.sisinf.ui;

import java.util.Scanner;
import java.util.HashMap;
import isel.sisinf.model.Rider;
import isel.sisinf.jpa.RiderRepository;
import isel.sisinf.model.Dock;
import isel.sisinf.jpa.DockRepository;
import jakarta.persistence.*;
import java.sql.Timestamp;

/**
 * 
 * Didactic material to support 
 * to the curricular unit of 
 * Introduction to Information Systems 
 *
 * The examples may not be complete and/or totally correct.
 * They are made available for teaching and learning purposes and 
 * any inaccuracies are the subject of debate.
 */

interface DbWorker
{
    void doWork();
}
class UI
{
    private enum Option
    {
        // DO NOT CHANGE ANYTHING!
        Unknown,
        Exit,
        createCostumer,
        listCostumer,
        listDocks,
        startTrip,
        parkScooter,
        about
    }
    private static UI __instance = null;
  
    private HashMap<Option,DbWorker> __dbMethods;

    private EntityManagerFactory emf = Persistence.createEntityManagerFactory("citesPU");
    private RiderRepository riderRepo = new RiderRepository(emf);
    private DockRepository dockRepo = new DockRepository(emf);

    private UI()
    {
        // DO NOT CHANGE ANYTHING!
        __dbMethods = new HashMap<Option,DbWorker>();
        __dbMethods.put(Option.createCostumer, () -> UI.this.createCostumer());
        __dbMethods.put(Option.listCostumer, () -> UI.this.listCostumer()); 
        __dbMethods.put(Option.listDocks, () -> UI.this.listDocks());
        __dbMethods.put(Option.startTrip, new DbWorker() {public void doWork() {UI.this.startTrip();}});
        __dbMethods.put(Option.parkScooter, new DbWorker() {public void doWork() {UI.this.parkScooter();}});
        __dbMethods.put(Option.about, new DbWorker() {public void doWork() {UI.this.about();}});
    }

    public static UI getInstance()
    {
        // DO NOT CHANGE ANYTHING!
        if(__instance == null)
        {
            __instance = new UI();
        }
        return __instance;
    }

    private Option DisplayMenu()
    {
        Option option = Option.Unknown;
        Scanner s = new Scanner(System.in); //Scanner closes System.in if you call close(). Don't do it
        try
        {
            // DO NOT CHANGE ANYTHING!
            System.out.println("CITES Manadgement DEMO");
            System.out.println();
            System.out.println("1. Exit");
            System.out.println("2. Create Costumer");
            System.out.println("3. List Existing Costumer");
            System.out.println("4. List Docks");
            System.out.println("5. Start Trip");
            System.out.println("6. Park Scooter");
            System.out.println("8. About");
            System.out.print(">");
            int result = s.nextInt();
            option = Option.values()[result];
        }
        catch(RuntimeException ex)
        {
            //nothing to do.
        }
        
        return option;

    }
    private static void clearConsole() throws Exception
    {
        // DO NOT CHANGE ANYTHING!
        for (int y = 0; y < 25; y++) //console is 80 columns and 25 lines
            System.out.println("\n");
    }

    public void Run() throws Exception
    {
        // DO NOT CHANGE ANYTHING!
        Option userInput;
        do
        {
            clearConsole();
            userInput = DisplayMenu();
            clearConsole();
            try
            {
                __dbMethods.get(userInput).doWork();
                System.in.read();
            }
            catch(NullPointerException ex)
            {
                //Nothing to do. The option was not a valid one. Read another.
            }

        }while(userInput!=Option.Exit);
    }

    /**
    To implement from this point forward. 
    -------------------------------------------------------------------------------------     
        IMPORTANT:
    --- DO NOT MESS WITH THE CODE ABOVE. YOU JUST HAVE TO IMPLEMENT THE METHODS BELOW ---
    --- Other Methods and properties can be added to support implementation. 
    ---- Do that also below                                                         -----
    -------------------------------------------------------------------------------------
    
    */

    private static final int TAB_SIZE = 24;

    private void createCostumer() {
        Scanner scanner = new Scanner(System.in);
        System.out.println("Enter name:");
        String name = scanner.nextLine();
        System.out.println("Enter email:");
        String email = scanner.nextLine();
        System.out.println("Enter tax number:");
        int taxNumber = Integer.parseInt(scanner.nextLine());
        System.out.println("Enter registration date (yyyy-mm-dd hh:mm:ss):");
        String dtRegisterStr = scanner.nextLine();
        System.out.println("Enter card credit:");
        double credit = Double.parseDouble(scanner.nextLine());
        System.out.println("Enter card type (resident/tourist):");
        String typeOfCard = scanner.nextLine();
        Rider rider = new Rider();
        rider.setName(name);
        rider.setEmail(email);
        rider.setTaxNumber(taxNumber);
        rider.setDtRegister(Timestamp.valueOf(dtRegisterStr));
        rider.setCredit(credit);
        rider.setTypeOfCard(typeOfCard);
        try {
            riderRepo.createRider(rider);
            System.out.println("Customer created successfully.");
        } catch (Exception e) {
            System.out.println("Error creating customer: " + e.getMessage());
        }
    }
  
    private void listCostumer()
    {
        try {
            for (Rider rider : riderRepo.getAllRiders()) {
                System.out.printf("ID: %d, Name: %s, Email: %s, Tax: %d, Card: %s, Credit: %.2f\n",
                    rider.getId(), rider.getName(), rider.getEmail(), rider.getTaxNumber(), rider.getTypeOfCard(), rider.getCredit());
            }
        } catch (Exception e) {
            System.out.println("Error listing customers: " + e.getMessage());
        }
    }

    private void listDocks()
    {
        try {
            for (Integer stationId : dockRepo.getAllStations()) {
                double occupancy = dockRepo.getDockOccupancy(stationId);
                System.out.printf("Station %d - Occupancy: %.2f%%\n", stationId, occupancy * 100);
                for (Dock dock : dockRepo.getAllDocks()) {
                    if (dock.getStation() == stationId) {
                        System.out.printf("  Dock %d: State=%s, Scooter=%s\n", dock.getNumber(), dock.getState(), dock.getScooter() == null ? "None" : dock.getScooter().toString());
                    }
                }
            }
        } catch (Exception e) {
            System.out.println("Error listing docks: " + e.getMessage());
        }
    }

    private void startTrip() {
        Scanner scanner = new Scanner(System.in);
        try {
            System.out.println("Enter dock number:");
            int dockId = Integer.parseInt(scanner.nextLine());
            System.out.println("Enter client ID:");
            int clientId = Integer.parseInt(scanner.nextLine());
            dockRepo.startTrip(dockId, clientId);
            System.out.println("Trip started successfully.");
        } catch (PersistenceException e) {
            System.out.println("Error starting trip: " + e.getCause().getMessage());
        } catch (Exception e) {
            System.out.println("Error: " + e.getMessage());
        }
    }

    private void parkScooter()
    {
        Scanner scanner = new Scanner(System.in);
        try {
            System.out.println("Enter dock number:");
            int dockNumber = Integer.parseInt(scanner.nextLine());
            System.out.println("Enter scooter ID:");
            int scooterId = Integer.parseInt(scanner.nextLine());
            Dock dock = dockRepo.getDockByNumber(dockNumber);
            if (dock == null) {
                System.out.println("Dock not found.");
                return;
            }
            if (!"free".equalsIgnoreCase(dock.getState())) {
                System.out.println("Dock is not free. Current state: " + dock.getState());
                return;
            }
            dock.setState("occupy");
            dock.setScooter(scooterId);
            try {
                dockRepo.updateDock(dock);
                System.out.println("Scooter parked successfully.");
            } catch (OptimisticLockException e) {
                System.out.println("Error: The dock was modified by another transaction. Please try again.");
            }
        } catch (Exception e) {
            System.out.println("Error parking scooter: " + e.getMessage());
        }
    }

    private void about()
    {
        System.out.println("DAL version:"+ isel.sisinf.jpa.Dal.version());
        System.out.println("Core version:"+ isel.sisinf.model.Core.version());
        System.out.println("Group: G70T44D");
        System.out.println("Members: Pedro Silva - 47183, Gonçalo Pontes - 51642, João Silva - 51682");
        
    }
}

public class App{
    public static void main(String[] args) throws Exception{
        UI.getInstance().Run();
    }
}

