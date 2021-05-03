-- $ sqlite3 clients.db < clients.sql
PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS users;
CREATE TABLE users(
userID INTEGER primary key AUTOINCREMENT,
userName VARCHAR NOT NULL,
email VARCHAR,
pswd VARCHAR
-- primary key (userID, userName)
);

DROP TABLE IF EXISTS userFollows;
CREATE TABLE userFollows(
userName VARCHAR NOT NULL, -- user_name of user
follows VARCHAR NOT NULL, -- user_name of follower
PRIMARY KEY (userName, follows)
-- FOREIGN KEY (userName) REFERENCES users(userName)
);



INSERT INTO users(userName,email,pswd) VALUES(
'elizabeth warren','warren123@gmail.com','392');
INSERT INTO users(userName,email,pswd) VALUES(
'bob smith','smith@yahoo.com','381kknr-');
INSERT INTO users(userName,email,pswd) VALUES(
'wanda vision','vision@gmail.com','vision23is!alive');
INSERT INTO users(userName,email,pswd) VALUES(
'chavezQuinto','chavez@gmail.com','pswdEasy');
INSERT INTO users(userName,email,pswd) VALUES(
'rebeccaHaunt','hauntyHung@gmail.com','notPswd');
INSERT INTO users(userName,email,pswd) VALUES(
'se123','sanchez@hotmail.com','dontKn23');


INSERT INTO userFollows(userName,follows) VALUES(
'se123','wanda vision');
INSERT INTO userFollows(userName,follows) VALUES(
'rebeccaHaunt', 'chavezQuinto');
INSERT INTO userFollows(userName,follows) VALUES(
'se123','rebeccaHaunt');
INSERT INTO userFollows(userName,follows) VALUES(
'se123', 'bob smith');
INSERT INTO userFollows(userName,follows) VALUES(
'bob smith', 'se123');
INSERT INTO userFollows(userName, follows) VALUES(
'elizabeth warren','bob smith');
INSERT INTO userFollows(userName, follows) VALUES(
'bob smith', 'wanda vision');
INSERT INTO userFollows(userName, follows) VALUES(
'elizabeth warren', 'wanda vision');

COMMIT; 
