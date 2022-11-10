from fastapi import FastAPI, Depends, HTTPException
from .auth import AuthHandler
from .schemas import AuthDetail

app = FastAPI()


auth_handler = AuthHandler()
users = []

@app.post('/register', status_code=201)
def register(auth_details: AuthDetail):
    if any(x['cpf'] == auth_details.cpf for x in users):
        raise HTTPException(status_code=400, detail='Esse cpf já possui cadastro')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'cpf': auth_details.cpf,
        'password': hashed_password
    })
    return

@app.post('/login')
def login(auth_details: AuthDetail):
    user = None
    for x in users:
        if x['cpf'] == auth_details.cpf:
            user = x
            break
    
    if(user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Senha ou cpf inválidos')
    token = auth_handler.encode_token(user['cpf'])
    return { 'token': token }

@app.get('/unprotected')
def unprotected():
    return { 'api_state' : 'online'}

@app.get('/protected')
def protected(cpf=Depends(auth_handler.auth_wrapper)):
    return { 'name' : cpf}