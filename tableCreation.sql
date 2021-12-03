DROP
	TABLE IF EXISTS ACCOUNTS;
DROP 
	TABLE IF EXISTS DIRECT_MESSAGE;
DROP
	TABLE IF EXISTS CHANNELS;
DROP
	TABLE IF EXISTS CHANNEL_MESSAGES;
DROP 
	TABLE IF EXISTS CHANNEL_MEMBERS;

create table accounts (
id INTEGER unique auto_increment,
time_created integer,
username varchar(30) unique,
password varchar(40),
primary key (id));

create table direct_messages(
id Integer unique auto_increment,
sender_id integer,
recipient_id integer,
content varchar(2048),
unread boolean,
primary key (id),
foreign key (sender_id) references accounts (id),
foreign key (recipient_id) references accounts (id));

create table channels(
channel_id integer unique auto_increment,
channel_name varchar(20),
primary key (channel_id));

create table channel_messages(
message_id integer unique auto_increment,
sender_id integer,
content varchar(2048),
primary key (message_id));

create table channel_members(
channel_id integer,
member_id integer,
primary key (channel_id, member_id),
foreign key (channel_id) references channels (channel_id),
 foreign key (member_id) references accounts (id));







