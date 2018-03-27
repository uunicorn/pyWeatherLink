
create table if not exists raw (
    timestamp                   INTEGER,
    
    WindSpeed                   FLOAT,
    AverageWindSpeed            FLOAT,
    WindDirection               FLOAT, 
    IndoorTemperature           FLOAT,
    IndoorRelativeHumidity      FLOAT,
    OutdoorTemperature          FLOAT,
    OutdoorRelativeHumidity     FLOAT,
    QFE                         FLOAT,
    QFETrend                    FLOAT,
    Forecast                    FLOAT,
    
    RainRate                    FLOAT,
    RainDay                     FLOAT,
    
    OutdoorDewpoint             FLOAT
);

create index if not exists timestamp on raw (timestamp);
