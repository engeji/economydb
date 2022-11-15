
CREATE TABLE CDKS_operation_type
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'тип операций с ДКС';

ALTER TABLE CDKS_operation_type
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE dks_operation_type
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Тип операций с ДКС';

ALTER TABLE dks_operation_type
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE list_operation_cdks
(
  ID                 NOT NULL AUTO_INCREMENT,
  cdks_operation_ID  NOT NULL,
  variant_ID         NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE list_operation_cdks
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE list_operation_dks
(
  ID                   NOT NULL AUTO_INCREMENT,
  dks_operation_ID INT NOT NULL,
  varisnt_ID           NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'список мероприятий с дкс';

ALTER TABLE list_operation_dks
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE list_operation_tube
(
  ID                 NOT NULL AUTO_INCREMENT,
  tube_operation_ID  NOT NULL,
  variant_ID         NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE list_operation_tube
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE list_operation_well
(
  ID                 NOT NULL AUTO_INCREMENT,
  well_operation_ID  NOT NULL,
  variant_ID         NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE list_operation_well
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE operation_cdks
(
  ID       NOT NULL AUTO_INCREMENT,
  cdks_id  NOT NULL,
  type_ID  NOT NULL,
  date     NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE operation_cdks
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE operation_dks
(
  ID      INT NULL     AUTO_INCREMENT,
  dks_id      NOT NULL,
  type_ID     NOT NULL,
  date        NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE operation_dks
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE operation_tube
(
  ID       NOT NULL AUTO_INCREMENT,
  type_ID  NOT NULL,
  tube_id  NOT NULL,
  date     NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE operation_tube
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE operation_well
(
  ID       NOT NULL AUTO_INCREMENT,
  well_id  NOT NULL,
  type_ID  NOT NULL,
  date     NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE operation_well
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE tube_operation_type
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Тип операций с шлейфами';

ALTER TABLE tube_operation_type
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE variant
(
  ID   NOT NULL AUTO_INCREMENT,
  tag  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'сценарный вариант';

ALTER TABLE variant
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE well_operation_type
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Тип операций смио скважина';

ALTER TABLE well_operation_type
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

ALTER TABLE operation_dks
  ADD CONSTRAINT FK_dks_operation_type_TO_operation_dks
    FOREIGN KEY (type_ID)
    REFERENCES dks_operation_type (ID);

ALTER TABLE list_operation_dks
  ADD CONSTRAINT FK_operation_dks_TO_list_operation_dks
    FOREIGN KEY (dks_operation_ID)
    REFERENCES operation_dks (ID);

ALTER TABLE list_operation_dks
  ADD CONSTRAINT FK_variant_TO_list_operation_dks
    FOREIGN KEY (varisnt_ID)
    REFERENCES variant (ID);

ALTER TABLE operation_well
  ADD CONSTRAINT FK_well_operation_type_TO_operation_well
    FOREIGN KEY (type_ID)
    REFERENCES well_operation_type (ID);

ALTER TABLE operation_tube
  ADD CONSTRAINT FK_tube_operation_type_TO_operation_tube
    FOREIGN KEY (type_ID)
    REFERENCES tube_operation_type (ID);

ALTER TABLE list_operation_tube
  ADD CONSTRAINT FK_operation_tube_TO_list_operation_tube
    FOREIGN KEY (tube_operation_ID)
    REFERENCES operation_tube (ID);

ALTER TABLE list_operation_tube
  ADD CONSTRAINT FK_variant_TO_list_operation_tube
    FOREIGN KEY (variant_ID)
    REFERENCES variant (ID);

ALTER TABLE list_operation_well
  ADD CONSTRAINT FK_variant_TO_list_operation_well
    FOREIGN KEY (variant_ID)
    REFERENCES variant (ID);

ALTER TABLE list_operation_well
  ADD CONSTRAINT FK_operation_well_TO_list_operation_well
    FOREIGN KEY (well_operation_ID)
    REFERENCES operation_well (ID);

ALTER TABLE list_operation_cdks
  ADD CONSTRAINT FK_variant_TO_list_operation_cdks
    FOREIGN KEY (variant_ID)
    REFERENCES variant (ID);

ALTER TABLE operation_cdks
  ADD CONSTRAINT FK_CDKS_operation_type_TO_operation_cdks
    FOREIGN KEY (type_ID)
    REFERENCES CDKS_operation_type (ID);

ALTER TABLE list_operation_cdks
  ADD CONSTRAINT FK_operation_cdks_TO_list_operation_cdks
    FOREIGN KEY (cdks_operation_ID)
    REFERENCES operation_cdks (ID);
