
CREATE TABLE depreciation_period_defalut_value
(
  ID                          NOT NULL AUTO_INCREMENT,
  prize_depr_value            NOT NULL,
  prize_depr_value_measer_id  NOT NULL COMMENT 'проценты',
  tax_period                  NOT NULL,
  accaunting_period           NOT NULL,
  period_measer_id            NOT NULL COMMENT 'года',
  event_ID                    NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Срок амартизации';

ALTER TABLE depreciation_period_defalut_value
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE event
(
  ID          NOT NULL AUTO_INCREMENT,
  name        NOT NULL,
  expense_ID  NOT NULL,
  params      NULL     COMMENT 'TODO',
  PRIMARY KEY (ID)
);

ALTER TABLE event
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE expense
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
);

ALTER TABLE expense
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE fact_capacity
(
  ID              NOT NULL AUTO_INCREMENT,
  owner_id        NOT NULL,
  deposit_id      NOT NULL,
  capacity_vlaue  NOT NULL,
  measers_id      NOT NULL,
  mults_id        NOT NULL COMMENT 'множитель для тысяч',
  fact_date       NOT NULL,
  path_source     NULL     COMMENT 'Ссылка на файл источник',
  memo            NULL    ,
  event_ID        NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'стоимость ГТМ';

ALTER TABLE fact_capacity
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE fliud_cost_price
(
  id             NOT NULL AUTO_INCREMENT,
  value          NOT NULL,
  fluid_type_id  NOT NULL,
  fluid_type_id  NOT NULL COMMENT 'год',
  deposit_id     NOT NULL,
  PRIMARY KEY (id)
) COMMENT 'Себестоимость флюида';

ALTER TABLE fliud_cost_price
  ADD CONSTRAINT UQ_id UNIQUE (id);

CREATE TABLE fluid_sale_price
(
  ID             NOT NULL AUTO_INCREMENT,
  value          NOT NULL,
  fluid_type_id  NOT NULL,
  date           NOT NULL COMMENT 'год',
  deposit_id     NOT NULL,
  condition_ID   NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Цена реализации флюида';

ALTER TABLE fluid_sale_price
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE fluid_sale_price_condition
(
  ID    NOT NULL AUTO_INCREMENT,
  name  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Условия расчета цен реализации продукции';

ALTER TABLE fluid_sale_price_condition
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE MET
(
  ID             NOT NULL AUTO_INCREMENT,
  value          NOT NULL,
  fluid_type_id  NOT NULL,
  date           NOT NULL COMMENT 'год',
  deposit_id     NOT NULL,
  condition_ID   NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'mineral extraction tax (НДПИ)';

ALTER TABLE MET
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE Tax_default_value
(
  ID           NOT NULL,
  Tax_value    NOT NULL,
  tax_type_ID  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Ставки налога на имущество и прибыль';

ALTER TABLE Tax_default_value
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE Tax_type
(
  ID         NOT NULL AUTO_INCREMENT,
  name       NOT NULL,
  measer_id  NOT NULL COMMENT 'тут в процентах( надо дополнить справочник)',
  PRIMARY KEY (ID)
);

ALTER TABLE Tax_type
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

CREATE TABLE wgpt
(
  ID                 NOT NULL AUTO_INCREMENT,
  well_id            NOT NULL,
  value              NOT NULL,
  date               NOT NULL,
  variant_ID         NOT NULL,
  fluid_type_id      NOT NULL,
  event_ID_for_well  NOT NULL,
  PRIMARY KEY (ID)
) COMMENT 'Показатели накопленная добычадобычи по скважинам для КРСов';

ALTER TABLE wgpt
  ADD CONSTRAINT UQ_ID UNIQUE (ID);

ALTER TABLE Tax_default_value
  ADD CONSTRAINT FK_Tax_type_TO_Tax_default_value
    FOREIGN KEY (tax_type_ID)
    REFERENCES Tax_type (ID);

ALTER TABLE fact_capacity
  ADD CONSTRAINT FK_event_TO_fact_capacity
    FOREIGN KEY (event_ID)
    REFERENCES event (ID);

ALTER TABLE event
  ADD CONSTRAINT FK_expense_TO_event
    FOREIGN KEY (expense_ID)
    REFERENCES expense (ID);

ALTER TABLE depreciation_period_defalut_value
  ADD CONSTRAINT FK_event_TO_depreciation_period_defalut_value
    FOREIGN KEY (event_ID)
    REFERENCES event (ID);

ALTER TABLE wgpt
  ADD CONSTRAINT FK_event_TO_wgpt
    FOREIGN KEY (event_ID_for_well)
    REFERENCES event (ID);

ALTER TABLE fluid_sale_price
  ADD CONSTRAINT FK_fluid_sale_price_condition_TO_fluid_sale_price
    FOREIGN KEY (condition_ID)
    REFERENCES fluid_sale_price_condition (ID);

ALTER TABLE MET
  ADD CONSTRAINT FK_fluid_sale_price_condition_TO_MET
    FOREIGN KEY (condition_ID)
    REFERENCES fluid_sale_price_condition (ID);
