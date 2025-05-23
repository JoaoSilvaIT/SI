package isel.sisinf.model;

import jakarta.persistence.*;
import java.io.Serializable;
import java.sql.Timestamp;

@Entity
@Table(name = "RIDER", schema = "public", catalog = "postgres")
public class Rider implements Serializable {
    @Id
    @Column(name = "id")
    private int id;

    @Column(name = "email")
    private String email;

    @Column(name = "taxnumber")
    private int taxNumber;

    @Column(name = "name")
    private String name;

    @Column(name = "dtregister")
    private Timestamp dtRegister;

    @Column(name = "cardid")
    private int cardId;

    @Column(name = "credit")
    private double credit;

    @Column(name = "typeofcard")
    private String typeOfCard;

    // Getters and setters
    public int getId() { return id; }
    public void setId(int id) { this.id = id; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public int getTaxNumber() { return taxNumber; }
    public void setTaxNumber(int taxNumber) { this.taxNumber = taxNumber; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public Timestamp getDtRegister() { return dtRegister; }
    public void setDtRegister(Timestamp dtRegister) { this.dtRegister = dtRegister; }
    public int getCardId() { return cardId; }
    public void setCardId(int cardId) { this.cardId = cardId; }
    public double getCredit() { return credit; }
    public void setCredit(double credit) { this.credit = credit; }
    public String getTypeOfCard() { return typeOfCard; }
    public void setTypeOfCard(String typeOfCard) { this.typeOfCard = typeOfCard; }
}

