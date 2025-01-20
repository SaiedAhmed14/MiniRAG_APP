from fastapi import FastAPI
app=FastAPI()
@app.get("/Saied_Ahmed")
def name ():
    return{
        'message':'Saied Ahmed'
    }
