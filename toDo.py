from fastapi import FastAPI
from typing import List
from typing import Optional
from pydantic import BaseModel
from uuid import uuid4
from fastapi.middleware import Middleware
from fastapi.middleware.cors import CORSMiddleware

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
]

app = FastAPI(middleware=middleware)

class Task(BaseModel):
	id: Optional[str]
	name: str
	isDone: bool = False


banco: List[Task] = []

# GETS
@app.get("/")
def check():
    return {'mensagem': 'Olá, seja bem-vindo ao FastAPI'}


# Adicionando uma nova tarefa
@app.post("/tasks")
def create_task(task: Task):
    for tasks in banco:
        # Não permitir tarefas com o mesmo nome
        if tasks.name == task.name:
            return {'erro': 'Tarefa já cadastrada'}
    task.id = str(uuid4())
    banco.append(task)
    return task


# Listando todas as tarefas
@app.get("/tasks")
def get_tasks():
    return banco


# Mostrar o progresso de conclusão das tarefas
@app.get("/tasks/done")
def get_done_tasks():
    done_tasks = []
    for task in banco:
        if task.isDone:
            done_tasks.append(task)
    return {"done_tasks": done_tasks, "total": len(done_tasks)}
 

# Removendo uma tarefa da listagem
@app.delete("/tasks/{task_id}")
def remove_task(TaskId: str):
    for task in banco:
        if task.id == TaskId:
            banco.remove(task)
            return {'mensagem': 'Tarefa removida com sucesso'}      
    return {'erro': 'Tarefa não localizada'}
    
    
# Atualizando o status de uma tarefa (marcar e desmarcar como concluída)
@app.patch("/tasks/{task_id}")
def update_task(TaskId: str):
    for task in banco:
        if task.id == TaskId:
            if task.isDone:
                task.isDone = False
            else:
                task.isDone = True
            # return {'mensagem': 'Tarefa atualizada'}
            return task
    return {'erro': 'Tarefa não localizada'}
