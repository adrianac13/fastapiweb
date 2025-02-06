from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from data.dao.dao_usuario import DaoUsuario
from data.database import database


app = FastAPI()
dao_usuario = DaoUsuario()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

NAV_ITEMS = [
    {"name": "Inicio", "url": "/"},
    {"name": "Destacados", "url": "/destacados"},
    {"name": "Formulario", "url": "/formulario"},
    {"name": "Calculadora", "url": "/calculadora"}
]

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/destacados", response_class=HTMLResponse)
async def destacados(request: Request):
    return templates.TemplateResponse("destacados.html", {"request": request})

@app.get("/calculadora", response_class=HTMLResponse)
async def presupuesto(request: Request):
    return templates.TemplateResponse("calculadora.html", {"request": request})

@app.post("/calculadora", response_class=HTMLResponse)
async def calcular_presupuesto(
    request: Request, 
    personas: int = Form(...), 
    dias: int = Form(...), 
    destino: str = Form(...),
    calidad: str = Form(...)
):
    costo_por_persona_por_dia = {
        "Paris": 150, 
        "Roma": 120, 
        "Tokio": 200,
        "Nueva York": 180,
        "Londres": 140,
        "Sídney": 220,
        "Dubái": 190,
        "El Cairo": 100,
        "Rio de Janeiro": 130,
        "Bangkok": 110
    }
    ajuste_calidad = {
        "Básica": 0.9,    
        "Estándar": 1.0,  
        "Lujo": 1.5      
    }
    if destino in costo_por_persona_por_dia and calidad in ajuste_calidad:
        costo_base = costo_por_persona_por_dia[destino]
        ajuste = ajuste_calidad[calidad]
        presupuesto = personas * dias * costo_base * ajuste
    else:
        presupuesto = 0  
    return templates.TemplateResponse("calculadora.html", {
        "request": request,
        "personas": personas,
        "dias": dias,
        "destino": destino,
        "calidad": calidad,
        "presupuesto": round(presupuesto, 2)  
    })

@app.get("/reservas", response_class=HTMLResponse)
def get_reservas(request: Request):
    reservas = dao_usuario.get_all(database)
    return templates.TemplateResponse(
        "index.html", {"request": request, "reservas": reservas}
    )

@app.get("/formulario", response_class=HTMLResponse)
async def get_formulario(request: Request):
    reservas = dao_usuario.get_all(database)
    return templates.TemplateResponse("formulario.html", {"request": request, "reservas": reservas})

@app.post("/usuario/addreserva")
async def add_reserva(request: Request, nombre_reserva: str = Form(...), destino: str = Form(...), duracion: str = Form(...), presupuesto: float = Form(...), fecha_reserva: str = Form(...)):
    dao_usuario.insert(database, nombre_reserva, destino, duracion, presupuesto, fecha_reserva)
    return RedirectResponse(url="/formulario", status_code=303)

@app.post("/usuario/updatereserva/")
async def update_reserva(
    request: Request,
    id: int = Form(...),
    nombre_reserva: str = Form(...),
    destino: str = Form(...),
    duracion: str = Form(...),
    presupuesto: float = Form(...),
    fecha_reserva: str = Form(...),
):
    dao_usuario.update(database, id, nombre_reserva, destino, duracion, presupuesto, fecha_reserva)
    return RedirectResponse(url="/formulario", status_code=303)

@app.post("/usuario/deletereserva/")
async def delete_reserva(request: Request, id: int = Form(...)):
    dao_usuario.delete(database, id)
    return RedirectResponse(url="/formulario", status_code=303)
