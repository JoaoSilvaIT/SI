package isel.sisinf.model;

import jakarta.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;

@Entity
@Table(name = "DOCK")
public class Dock implements Serializable {
    @Id
    @Column(name = "number")
    private int number;

    @Column(name = "station")
    private int station;

    @Column(name = "state")
    private String state;

    @Column(name = "scooter")
    private Integer scooter;

    @Version
    @Column(name = "version")
    private Timestamp version;

    // Getters and setters
    public int getNumber() { return number; }
    public void setNumber(int number) { this.number = number; }
    public int getStation() { return station; }
    public void setStation(int station) { this.station = station; }
    public String getState() { return state; }
    public void setState(String state) { this.state = state; }
    public Integer getScooter() { return scooter; }
    public void setScooter(Integer scooter) { this.scooter = scooter; }
    public Timestamp getVersion() { return version; }
    public void setVersion(Timestamp version) { this.version = version; }
}

