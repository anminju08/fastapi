from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
    contents : str
    is_done : bool
 #클라이언트가 보내는 json바디 검증하는 거임