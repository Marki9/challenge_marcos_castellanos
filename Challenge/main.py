import logging
import uvicorn
from apps.config import HOST, PORT


if __name__ == "__main__":
    try:
        uvicorn.run("apps.api:app", host=HOST, port=PORT, reload=True)
    except Exception as e:
        error = 'No se puede iniciar el sistema: %s' % e
        logging.error(error)    