-- To populate the remote DB (the normal db_population.py took too long to complete on the remote DB)
-- Insert just the necessary data
INSERT INTO modules VALUES ('CS3235');
INSERT INTO modules VALUES ('CS4243');
INSERT INTO modules VALUES ('CS4236');
INSERT INTO modules VALUES ('CP4101');
INSERT INTO modules VALUES ('CS5231');
INSERT INTO modules VALUES ('CS2220');
INSERT INTO modules VALUES ('CS1020');

INSERT INTO rooms VALUES('1');
INSERT INTO rooms VALUES('2');
INSERT INTO room_accesses VALUES ('CS3235', '1');