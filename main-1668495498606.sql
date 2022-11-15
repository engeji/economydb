
CREATE TABLE Area
(
  ID              NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  FIELD_ID        NOT NULL,
  name           ,
  sub_serfice_ID  NOT NULL,
  owner_ID        NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Area IS 'Площадь/участок, группа УКПГ';

COMMENT ON COLUMN Area.sub_serfice_ID IS 'Недропользователь';

COMMENT ON COLUMN Area.owner_ID IS 'Опаератор добычи';

CREATE TABLE AREA_FAC
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  area_ID  NOT NULL,
  fac_ID   NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE AREA_FAC IS 'Связи площадь, укпг';

CREATE TABLE Category_reserv
(
  ID    NOT NULL,
  name  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Category_reserv IS 'Катеогрии запасов';

CREATE TABLE cdks
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name    ,
  area_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE cdks IS 'центральная ДКС, в отличии от промысловой ДКС, они пренадлежит площади, а не УКПГ';

CREATE TABLE Company_name
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name  UNIQUE,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Company_name IS 'Название компании';

CREATE TABLE Complump
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  well_ID  NOT NULL,
  perf_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Complump IS 'Группа перфораций на отложение';

CREATE TABLE Deposit
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name  NOT NULL UNIQUE,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Deposit IS 'Сеноман/неоком отложение (группа объектов)';

CREATE TABLE dev_Object
(
  ID          NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name        UNIQUE,
  deposit_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE dev_Object IS 'Объект разработкиОбьект1, Обьект2, сгруппированные в отложения';

CREATE TABLE Dks
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY,
  name     NOT NULL,
  is_fact  NOT NULL,
  fac_ID   NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Dks IS 'Дожимная копрессорная станция, ДКС';

COMMENT ON COLUMN Dks.is_fact IS 'bool';

CREATE TABLE Facility
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Facility IS 'Площадка/укпг';

CREATE TABLE Field
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name  UNIQUE,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Field IS 'Месторождение';

CREATE TABLE Formation
(
  ID              NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name            NOT NULL,
  dev_ob_ID       NOT NULL,
  ID_stratigraph  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Formation IS 'пласт';

CREATE TABLE Geo_Reserves
(
  ID                   NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  value         float8 NOT NULL,
  Type_fluid_ID        NOT NULL,
  Category_ID          NOT NULL,
  in_balance           NOT NULL,
  ID_obj               NOT NULL,
  release              NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Geo_Reserves IS 'Запасы';

COMMENT ON COLUMN Geo_Reserves.in_balance IS 'bool';

COMMENT ON COLUMN Geo_Reserves.release IS 'date';

CREATE TABLE GEOMODEL
(
  ID              NOT NULL,
  release    date,
  path           ,
  memo           ,
  parrent_ID      NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE GEOMODEL IS 'Гео. модель отложения';

CREATE TABLE Group_geo
(
  ID      NOT NULL UNIQUE,
  geo_ID  NOT NULL,
  gdm_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Group_geo IS 'ГРуппы гео моделей';

CREATE TABLE HDM_reserves
(
  ID              NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  value           NOT NULL,
  type_fluids_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE HDM_reserves IS 'Зарпасы в гдм модели. Отдельная сущьность для сравнения с геологией';

CREATE TABLE HIST_HDM_model
(
  ID                   NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  path                ,
  release         date NOT NULL,
  memo                ,
  parrent_ID           NOT NULL,
  date_actual     date NOT NULL,
  date_adapt_date     ,
  HDM_res_ID           NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE HIST_HDM_model IS 'Гидродинамическая модель';

CREATE TABLE Meserment
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name ,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Meserment IS 'Размерности, м3, т. бар, паскаль';

CREATE TABLE Perforation
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY,
  top     ,
  bot     ,
  form_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Perforation IS 'Перфорация, связь между скважиной и пластом';

COMMENT ON COLUMN Perforation.top IS 'Верхняя граница';

COMMENT ON COLUMN Perforation.bot IS 'Нижняя граница';

CREATE TABLE predict_model
(
  ID             NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  parrent_ID     NOT NULL,
  hist_model_ID  NOT NULL,
  variant_id     NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE predict_model IS 'Модель, даа начала расчета которой, начинаеться с конца исторического периода';

CREATE TABLE reserve_object
(
  ID       NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name    ,
  form_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE reserve_object IS 'Объект подсчета запасов';

CREATE TABLE Stratigraph_obj
(
  ID    NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Stratigraph_obj IS 'Стратиграфическая разбивка из википедии';

CREATE TABLE Total_reserv
(
  ID      NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  geo_ID  NOT NULL,
  res_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Total_reserv IS 'Все типы запасов и флюидов';

CREATE TABLE tube
(
  ID          NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name        NOT NULL,
  parrent_ID ,
  child_ID   ,
  name       ,
  len        ,
  dia        ,
  fac_ID     ,
  well_ID     NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON COLUMN tube.len IS 'длинна';

COMMENT ON COLUMN tube.dia IS 'Диаметр';

CREATE TABLE Type_fluids
(
  ID        NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name      NOT NULL,
  meser_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE Type_fluids IS 'Тип флюидов';

CREATE TABLE WELL
(
  ID      NOT NULL GENERATED ALWAYS AS IDENTITY UNIQUE,
  name    NOT NULL,
  FAC_ID  NOT NULL,
  PRIMARY KEY (ID)
);

COMMENT ON TABLE WELL IS 'Скважины';

ALTER TABLE Complump
  ADD CONSTRAINT FK_WELL_TO_Complump
    FOREIGN KEY (well_ID)
    REFERENCES WELL (ID);

ALTER TABLE WELL
  ADD CONSTRAINT FK_Facility_TO_WELL
    FOREIGN KEY (FAC_ID)
    REFERENCES Facility (ID);

ALTER TABLE Area
  ADD CONSTRAINT FK_Field_TO_Area
    FOREIGN KEY (FIELD_ID)
    REFERENCES Field (ID);

ALTER TABLE AREA_FAC
  ADD CONSTRAINT FK_Area_TO_AREA_FAC
    FOREIGN KEY (area_ID)
    REFERENCES Area (ID);

ALTER TABLE AREA_FAC
  ADD CONSTRAINT FK_Facility_TO_AREA_FAC
    FOREIGN KEY (fac_ID)
    REFERENCES Facility (ID);

ALTER TABLE Geo_Reserves
  ADD CONSTRAINT FK_Type_fluids_TO_Geo_Reserves
    FOREIGN KEY (Type_fluid_ID)
    REFERENCES Type_fluids (ID);

ALTER TABLE Type_fluids
  ADD CONSTRAINT FK_Meserment_TO_Type_fluids
    FOREIGN KEY (meser_ID)
    REFERENCES Meserment (ID);

ALTER TABLE Group_geo
  ADD CONSTRAINT FK_GEOMODEL_TO_Group_geo
    FOREIGN KEY (geo_ID)
    REFERENCES GEOMODEL (ID);

ALTER TABLE Group_geo
  ADD CONSTRAINT FK_HIST_HDM_model_TO_Group_geo
    FOREIGN KEY (gdm_ID)
    REFERENCES HIST_HDM_model (ID);

ALTER TABLE HIST_HDM_model
  ADD CONSTRAINT FK_HIST_HDM_model_TO_HIST_HDM_model
    FOREIGN KEY (parrent_ID)
    REFERENCES HIST_HDM_model (ID);

ALTER TABLE Geo_Reserves
  ADD CONSTRAINT FK_Category_reserv_TO_Geo_Reserves
    FOREIGN KEY (Category_ID)
    REFERENCES Category_reserv (ID);

ALTER TABLE Total_reserv
  ADD CONSTRAINT FK_GEOMODEL_TO_Total_reserv
    FOREIGN KEY (geo_ID)
    REFERENCES GEOMODEL (ID);

ALTER TABLE Total_reserv
  ADD CONSTRAINT FK_Geo_Reserves_TO_Total_reserv
    FOREIGN KEY (res_ID)
    REFERENCES Geo_Reserves (ID);

ALTER TABLE GEOMODEL
  ADD CONSTRAINT FK_GEOMODEL_TO_GEOMODEL
    FOREIGN KEY (parrent_ID)
    REFERENCES GEOMODEL (ID);

ALTER TABLE Complump
  ADD CONSTRAINT FK_Perforation_TO_Complump
    FOREIGN KEY (perf_ID)
    REFERENCES Perforation (ID);

ALTER TABLE Area
  ADD CONSTRAINT FK_Company_name_TO_Area
    FOREIGN KEY (sub_serfice_ID)
    REFERENCES Company_name (ID);

ALTER TABLE Area
  ADD CONSTRAINT FK_Company_name_TO_Area1
    FOREIGN KEY (owner_ID)
    REFERENCES Company_name (ID);

ALTER TABLE Perforation
  ADD CONSTRAINT FK_Formation_TO_Perforation
    FOREIGN KEY (form_ID)
    REFERENCES Formation (ID);

ALTER TABLE dev_Object
  ADD CONSTRAINT FK_Deposit_TO_dev_Object
    FOREIGN KEY (deposit_ID)
    REFERENCES Deposit (ID);

ALTER TABLE Formation
  ADD CONSTRAINT FK_dev_Object_TO_Formation
    FOREIGN KEY (dev_ob_ID)
    REFERENCES dev_Object (ID);

ALTER TABLE Geo_Reserves
  ADD CONSTRAINT FK_reserve_object_TO_Geo_Reserves
    FOREIGN KEY (ID_obj)
    REFERENCES reserve_object (ID);

ALTER TABLE reserve_object
  ADD CONSTRAINT FK_Formation_TO_reserve_object
    FOREIGN KEY (form_ID)
    REFERENCES Formation (ID);

ALTER TABLE Formation
  ADD CONSTRAINT FK_Stratigraph_obj_TO_Formation
    FOREIGN KEY (ID_stratigraph)
    REFERENCES Stratigraph_obj (ID);

ALTER TABLE HDM_reserves
  ADD CONSTRAINT FK_Type_fluids_TO_HDM_reserves
    FOREIGN KEY (type_fluids_ID)
    REFERENCES Type_fluids (ID);

ALTER TABLE HIST_HDM_model
  ADD CONSTRAINT FK_HDM_reserves_TO_HIST_HDM_model
    FOREIGN KEY (HDM_res_ID)
    REFERENCES HDM_reserves (ID);

ALTER TABLE predict_model
  ADD CONSTRAINT FK_predict_model_TO_predict_model
    FOREIGN KEY (parrent_ID)
    REFERENCES predict_model (ID);

ALTER TABLE predict_model
  ADD CONSTRAINT FK_HIST_HDM_model_TO_predict_model
    FOREIGN KEY (hist_model_ID)
    REFERENCES HIST_HDM_model (ID);

ALTER TABLE Dks
  ADD CONSTRAINT FK_Facility_TO_Dks
    FOREIGN KEY (fac_ID)
    REFERENCES Facility (ID);

ALTER TABLE cdks
  ADD CONSTRAINT FK_Area_TO_cdks
    FOREIGN KEY (area_ID)
    REFERENCES Area (ID);

ALTER TABLE tube
  ADD CONSTRAINT FK_tube_TO_tube
    FOREIGN KEY (parrent_ID)
    REFERENCES tube (ID);

ALTER TABLE tube
  ADD CONSTRAINT FK_tube_TO_tube1
    FOREIGN KEY (child_ID)
    REFERENCES tube (ID);

ALTER TABLE tube
  ADD CONSTRAINT FK_Facility_TO_tube
    FOREIGN KEY (fac_ID)
    REFERENCES Facility (ID);

ALTER TABLE tube
  ADD CONSTRAINT FK_WELL_TO_tube
    FOREIGN KEY (well_ID)
    REFERENCES WELL (ID);
