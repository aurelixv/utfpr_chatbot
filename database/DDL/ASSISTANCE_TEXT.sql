CREATE TABLE ASSISTANCE_TEXT (
    ASSISTANCE_INFO_ID INT,
    ASSISTANCE_TYPE_ID INT,
    UPDATE_TIMESTAMP TIMESTAMP,
    INFO_TEXT TEXT,
    PRIMARY KEY (ASSISTANCE_INFO_ID, ASSISTANCE_TYPE_ID, UPDATE_TIMESTAMP),
    FOREIGN KEY (ASSISTANCE_INFO_ID) REFERENCES ASSISTANCE_INFO (ASSISTANCE_INFO_ID),
    FOREIGN KEY (ASSISTANCE_TYPE_ID) REFERENCES ASSISTANCE_TYPE (ASSISTANCE_TYPE_ID)
);
