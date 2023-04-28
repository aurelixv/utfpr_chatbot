CREATE TABLE INTERNSHIP_TEXT (
    INTERNSHIP_INFO_ID INT,
    INTERNSHIP_TYPE_ID INT,
    UPDATE_TIMESTAMP TIMESTAMP,
    INFO_TEXT VARCHAR(500),
    PRIMARY KEY (INTERNSHIP_INFO_ID, INTERNSHIP_TYPE_ID, UPDATE_TIMESTAMP),
    FOREIGN KEY (INTERNSHIP_INFO_ID) REFERENCES INTERNSHIP_INFO (INTERNSHIP_INFO_ID),
    FOREIGN KEY (INTERNSHIP_TYPE_ID) REFERENCES INTERNSHIP_TYPE (INTERNSHIP_TYPE_ID)
);