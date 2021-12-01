create database messenger_db;
use messenger_db;

create table accounts(
	id integer primary key,
    login varchar(20)
);

create table messages(
	id integer primary key,
    src integer,
    dst integer,
    message varchar(20)
);

create user 'appaccount'@'%' identified by 'csci2052021';

grant select, insert on messenger_db.* to 'appaccount'@'%';

insert into accounts values (1, 'adam'),
			    (2, 'autumn'),
                            (3, 'geo'),
                            (4, 'howard'),
                            (5, 'garegin'),
			    (6, 'noah');                            

-- initialization fix
insert into messages values (0, 0, 0, '0');