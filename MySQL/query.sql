/*
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

create table streamers(
id_streamer varchar(20) primary key,
nome varchar(45) not null
);

create table servidor_streamers(
id_servidor_streamer int primary key auto_increment,
fk_id_streamer varchar(20),
fk_id_servidor varchar(20),
foreign key (fk_id_streamer) references streamers(id_streamer),
foreign key (fk_id_servidor) references servidor(id_servidor)
);

create table canal_twitch(
id_canal_twitch varchar(20) primary key,
nome varchar(45) not null,
fk_id_servidor varchar(20),
foreign key (fk_id_servidor) references servidor(id_servidor)
);
*/