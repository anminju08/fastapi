#connection.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+pymysql://root:todos@127.0.0.1:3307/todos" # docker run 3307:3306

engine = create_engine(DATABASE_URL, echo=True) #create_engine:db와 연결하는 엔진 생성/echo=True은 어떤 SQL이 실행되는 지 출력해줌
SessionFactory = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():#의존성 주입으로 쓰임
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()