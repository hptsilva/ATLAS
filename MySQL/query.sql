create database bot_discord;

create table servidor(
id_servidor varchar(20) primary key,
nome varchar(45) not null,
autorizacao_dm enum('Sim','Não') not null,
status_servidor enum('quarentena','liberado') not null
);

create table canal_de_boas_vindas(
id_canal_boas_vindas varchar(20) primary key,
nome varchar(45) not null,
fk_id_servidor varchar(20) unique,
foreign key (fk_id_servidor) references servidor(id_servidor)
);
