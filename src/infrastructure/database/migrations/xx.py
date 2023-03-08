# gender = postgresql.ENUM('MALE', 'FEMALE', 'OTHER', name='gender')
# life_status = postgresql.ENUM('ALIVE', 'DEAD', name='lifestatus')
# try:
#     gender.drop(conn)
#     life_status.drop(conn)
# except DependentObjectsStillExistError:
#     pass