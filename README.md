# Scraper Agenda Motor
Ejemplo de scraper para obtener las quedadas de Agenda Motor, saltandose Cloudflare

### Dependencias
```
pip install cfscrape
pip install bs4
```

### Lanzar script
```
python3 RUTA/scraper-agendamotor.py **RUTA**
```

### Ejemplo de json
```
[
  {
    "title": "KDD Club Cupra en Barcelona",
    "date": "2021-11-1",
    "site": "Circuito de Parcmotor Castelloli,  Crta. Nacional A-2, Km 560  Castelloli, Barcelona 08719 Espana",
    "address": {
      "street": "Crta. Nacional A-2, Km 560",
      "locality": "Castelloli",
      "region": ""
    },
    "image": "https://agendamotor.es/wp-content/uploads/kdd-club-cupra-en-circuito-castelloli-240x300.jpg",
    "state": false
  }
]
```

### Ejecutarlo desde NodeJS
```
import { PythonShell } from 'python-shell';

export class ScraperService {
  private path = 'RUTA';
  getEventsFromAgendaMotor = () => {
    return new Promise((resolve, reject) => {
      const path = `${this.path}/scripts/python/`;
      console.log(path);
      let options = {
        scriptPath: path,
        args: [path],
      };
      PythonShell.run('scraper-agendamotor.py', options, (err, result) => {
        if (err) {
          reject({ message: 'Error' });
        }
        resolve(result[0]);
      });
    });
  };
}

```
