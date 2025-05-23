/*
 *   ISEL-DEETC-SisInf
 *   ND 2022-2025
 *
 *   
 *   Information Systems Project - Active Databases
 *   
 */

/* ### DO NOT REMOVE THE QUESTION MARKERS ### */


-- region Question 1.a 
CREATE OR REPLACE FUNCTION trg_check_scooter_in_dock() RETURNS trigger AS $$
BEGIN
    -- Check if the scooter is in a dock and the dock is occupied
    IF NOT EXISTS (
        SELECT 1 FROM DOCK d
        WHERE d.scooter = NEW.scooter AND d.state = 'occupy'
    ) THEN
        RAISE EXCEPTION 'Scooter % is not in an occupied dock.', NEW.scooter;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_scooter_in_dock
BEFORE INSERT ON TRAVEL
FOR EACH ROW
EXECUTE FUNCTION trg_check_scooter_in_dock();
-- endregion

-- region Question 1.b
CREATE OR REPLACE FUNCTION trg_check_one_ongoing_trip() RETURNS trigger AS $$
BEGIN
    -- Check if the scooter is already in an ongoing trip
    IF EXISTS (
        SELECT 1 FROM TRAVEL t
        WHERE t.scooter = NEW.scooter AND t.dfinal IS NULL
    ) THEN
        RAISE EXCEPTION 'Scooter % is already in an ongoing trip.', NEW.scooter;
    END IF;
    -- Check if the client is already in an ongoing trip
    IF EXISTS (
        SELECT 1 FROM TRAVEL t
        WHERE t.client = NEW.client AND t.dfinal IS NULL
    ) THEN
        RAISE EXCEPTION 'Client % is already in an ongoing trip.', NEW.client;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER check_one_ongoing_trip
BEFORE INSERT ON TRAVEL
FOR EACH ROW
EXECUTE FUNCTION trg_check_one_ongoing_trip();
-- endregion

-- region Question 2
DROP FUNCTION IF EXISTS fx_dock_occupancy(integer);
CREATE OR REPLACE FUNCTION fx_dock_occupancy(stationid integer) RETURNS numeric AS $$
DECLARE
    total_docks integer;
    occupied_docks integer;
BEGIN
    SELECT COUNT(*) INTO total_docks FROM DOCK WHERE station = stationid;
    IF total_docks = 0 THEN
        RETURN 0;
    END IF;
    SELECT COUNT(*) INTO occupied_docks FROM DOCK WHERE station = stationid AND state = 'occupy';
    RETURN occupied_docks::numeric / total_docks;
END;
$$ LANGUAGE plpgsql;
 
-- region Question 3
CREATE OR REPLACE VIEW RIDER
AS
SELECT p.*,c.dtregister,cd.id AS cardid,cd.credit,cd.typeofcard
FROM CLIENT c INNER JOIN PERSON p ON (c.person=p.id)
    INNER JOIN CARD cd ON (cd.client = c.person);

-- Make RIDER view updatable (INSERT/UPDATE)
-- INSTEAD OF INSERT trigger
CREATE OR REPLACE FUNCTION rider_view_insert() RETURNS trigger AS $$
BEGIN
    -- Check if a PERSON with the given taxnumber already exists
    SELECT id INTO NEW.id FROM PERSON WHERE taxnumber = NEW.taxnumber;

    -- If not found, insert into PERSON
    IF NOT FOUND THEN
        INSERT INTO PERSON (email, taxnumber, name)
        VALUES (NEW.email, NEW.taxnumber, NEW.name)
        RETURNING id INTO NEW.id;
    END IF;

    -- Check if CLIENT already exists for the person
    IF NOT EXISTS (SELECT 1 FROM CLIENT WHERE person = NEW.id) THEN
        INSERT INTO CLIENT (person, dtregister)
        VALUES (NEW.id, NEW.dtregister);
    END IF;

    -- Insert into CARD
    INSERT INTO CARD (credit, typeofcard, client)
    VALUES (NEW.credit, NEW.typeofcard, NEW.id)
    RETURNING id INTO NEW.cardid;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER rider_view_insert_trg
INSTEAD OF INSERT ON RIDER
FOR EACH ROW
EXECUTE FUNCTION rider_view_insert();

-- INSTEAD OF UPDATE trigger
CREATE OR REPLACE FUNCTION rider_view_update() RETURNS trigger AS $$
BEGIN
    -- Update PERSON
    UPDATE PERSON SET email = NEW.email, taxnumber = NEW.taxnumber, name = NEW.name
    WHERE id = OLD.id;
    -- Update CLIENT
    UPDATE CLIENT SET dtregister = NEW.dtregister
    WHERE person = OLD.id;
    -- Update CARD
    UPDATE CARD SET credit = NEW.credit, typeofcard = NEW.typeofcard
    WHERE id = OLD.cardid;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER rider_view_update_trg
INSTEAD OF UPDATE ON RIDER
FOR EACH ROW
EXECUTE FUNCTION rider_view_update();
-- endregion

-- region Question 4
DROP PROCEDURE IF EXISTS startTrip(integer, integer);
CREATE OR REPLACE PROCEDURE startTrip(dockid integer, clientid integer)
LANGUAGE plpgsql
AS $$
DECLARE
    scooter_id integer;
    now_time timestamp := now();
BEGIN
    -- Check dock is occupied and get scooter
    SELECT scooter INTO scooter_id FROM DOCK WHERE number = dockid AND state = 'occupy';
    IF scooter_id IS NULL THEN
        RAISE EXCEPTION 'Dock % is not occupied or does not exist.', dockid;
    END IF;
    -- Insert new trip
    INSERT INTO TRAVEL (dinitial, comment, evaluation, dfinal, client, scooter, stinitial, stfinal)
    VALUES (now_time, NULL, NULL, NULL, clientid, scooter_id, (SELECT station FROM DOCK WHERE number = dockid), NULL);
    -- Update dock to free
    UPDATE DOCK SET state = 'free', scooter = NULL WHERE number = dockid;
END;
$$;
-- endregion

