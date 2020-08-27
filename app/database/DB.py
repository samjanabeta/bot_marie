import pymysql


class DB(object):
    def __init__(self, host, user, password, dbName, charset):
        self.sql = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=dbName,
            charset=charset,
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__migrate()

    def __migrate(self):
        try:
            with self.sql.cursor() as cursor:
                if not self.checkTable('resume'):
                    resumeSql = 'CREATE TABLE `resume` (`file_id` varchar(255) NOT NULL,`user_id` bigint NOT NULL, `file_url` text NOT NULL, `file_name` varchar(255) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                    cursor.execute(resumeSql)

                    indexesSql = 'ALTER TABLE `resume` ADD PRIMARY KEY (`file_id`), ADD UNIQUE KEY `unique_user_id` (`user_id`);'
                    cursor.execute(indexesSql)

                if not self.checkTable('users'):
                    usersSql = 'CREATE TABLE `users` (`id` bigint NOT NULL, `first_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL, `last_name` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL, `username` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL, `started_ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP) ENGINE=InnoDB DEFAULT CHARSET=utf8;'
                    cursor.execute(usersSql)

                    primaryKeySql = 'ALTER TABLE `users` ADD PRIMARY KEY (`id`);'
                    cursor.execute(primaryKeySql)
            self.sql.commit()
        finally:
            print('Migration finished')

    def checkTable(self, table_name):
        table_exists = False
        try:
            with self.sql.cursor() as cursor:
                sql = f'SHOW TABLES LIKE \'{table_name}\''
                result = cursor.execute(sql)
                table_exists = result > 0
        finally:
            print()

        return table_exists

    def saveUser(self, user):
        try:
            with self.sql.cursor() as cursor:
                sql = 'INSERT INTO users SET id=%s, first_name=%s, last_name=%s, username=%s'
                cursor.execute(sql, (user.id, user.first_name, user.last_name, user.username))
            self.sql.commit()
        finally:
            print("USER SAVE CALLED")

    def saveResume(self, user_id, file_id, file_url, file_name):
        try:
            with self.sql.cursor() as cursor:
                sql = 'REPLACE INTO resume SET file_id=%s, user_id=%s, file_url=%s, file_name=%s'
                cursor.execute(sql, (file_id, user_id, file_url, file_name))
            self.sql.commit()
        finally:
            print("RESUME SAVED")

    def deleteResume(self, user_id):
        """
                :param user_id: User identifier to get info about
                :return: Boolean is returned
                :rtype: :obj:`Boolean`
                """
        resume_deleted = False
        try:
            with self.sql.cursor() as cursor:
                sql = 'DELETE FROM resume WHERE user_id=%s'
                deleted = cursor.execute(sql, user_id)
                resume_deleted = deleted > 0
            self.sql.commit()
        finally:
            print("RESUME DELETED")

        return resume_deleted