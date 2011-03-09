import cx_Oracle
import os, sys

if len(sys.argv) < 5:
   print 'Please use argument, [user] [password] [sid] [object type] [output directory]'
   sys.exit(1)


usr = sys[1]
passwd = sys[2]
sid = sys[3]
objType = sys[4]
dirName = sys[5]

pkg_list = """
SELECT object_name
FROM user_objects
WHERE object_type = :OBJ_TYPE
ORDER BY object_name
"""

pkg_ddl = """
SELECT DBMS_METADATA.GET_DDL('SEQUENCE', object_name)
FROM user_objects
WHERE object_type = :OBJ_TYPE
AND object_name = :OBJ_NAME
"""

conn = cx_Oracle.connect('%s/%s@%s' % (usr, passwd, sid))
cur = conn.cursor()
binSel = {'OBJ_TYPE': objType}
res = cur.execute(pkg_list, binSel)
for row in res.fetchall():
   pkgName = row[0]
   binSel = {'OBJ_TYPE': objType, 'OBJ_NAME':pkgName}
   res_ddl = cur.execute(pkg_ddl, binSel)
   for data in res_ddl.fetchall():
      fileName = dirName + os.path.sep + 'DDL_%s.sql' % pkgName
      f = open(fileName, 'w')
      for line in data:         
         f.write(str(line))
      f.close()

