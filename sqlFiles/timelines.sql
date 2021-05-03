-- timeline sql for database 

PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;  

ATTACH DATABASE 'c:\silva_proj2\userAPI\var\clients.db' as users; 
DROP TABLE IF EXISTS post; 
CREATE TABLE post(
postID INTEGER primary key AUTOINCREMENT, 
userName VARCHAR NOT NULL, 
postText TEXT, 
postTimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
UNIQUE (postID, userName)
-- CONSTRAINT fk_users FOREIGN KEY (userName) REFERENCES users(userName) ON DELETE CASCADE
); 

INSERT INTO post(postID,userName,postText,postTimestamp) VALUES(
1,'wanda vision','hello there everyone',CURRENT_TIMESTAMP); 
INSERT INTO post(postID,userName,postText,postTimestamp)VALUES(
2,'wanda vision','season 1 ending...',CURRENT_TIMESTAMP);
INSERT INTO post(postID,userName,postText,postTimestamp)VALUES(
3,'se123','first post, how am i doing?',CURRENT_TIMESTAMP);
INSERT INTO post(postID,userName,postText,postTimestamp)VALUES(4,'se123','second post, still dont know if this is right',CURRENT_TIMESTAMP);
INSERT INTO post(postID,userName,postText,postTimestamp)VALUES(
5,'bob smith','HEEEEYYYYOOOOOOO, everyone!',CURRENT_TIMESTAMP);
INSERT INTO post(postID,userName,postText,postTimestamp)VALUES(
6,'bob smith','okay im out!',CURRENT_TIMESTAMP);

COMMIT; 
