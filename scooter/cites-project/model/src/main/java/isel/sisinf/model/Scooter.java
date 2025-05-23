package isel.sisinf.model;

import jakarta.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;

@Entity
@Table(name = "SCOOTER")
public class Scooter implements Serializable {
    @Id
    @Column(name = "id")
    private int id;

    @Column(name = "weight")
    private double weight;

    @Column(name = "maxvelocity")
    private double maxVelocity;

    @Column(name = "battery")
    private int battery;

    @Column(name = "model")
    private int model;

    @Version
    @Column(name = "version")
    private Timestamp version;

    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public double getWeight() { return weight; }
    public void setWeight(double weight) { this.weight = weight; }
    public double getMaxVelocity() { return maxVelocity; }
    public void setMaxVelocity(double maxVelocity) { this.maxVelocity = maxVelocity; }
    public int getBattery() { return battery; }
    public void setBattery(int battery) { this.battery = battery; }
    public int getModel() { return model; }
    public void setModel(int model) { this.model = model; }
    public Timestamp getVersion() { return version; }
    public void setVersion(Timestamp version) { this.version = version; }
}