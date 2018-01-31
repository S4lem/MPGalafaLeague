library(DBI)
dbname="PremierLeague"
host="relational.fit.cvut.cz"
port=3306
password="relational"
user="guest"
con <- dbConnect(RMySQL::MySQL(),  dbname = dbname, user=user, password=password, host=host, port=port)


for (table in dbListTables(con)){
  print(table)
  data <- dbGetQuery(con, paste("SELECT * FROM ",table, sep=''))
  print(nrow(data))
  print(ncol(data))
  write.table(data, file = paste('Here',table,'.csv',sep=''),row.names=FALSE, na="", sep=";")
}