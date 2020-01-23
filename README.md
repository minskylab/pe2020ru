# Peru 2020 Scrapper

Pero2020Scrapper es un programa que extrae tweets relacionados a las [Elecciones Congresales Extraordinarias 2020 del Peru]([https://www.wikiwand.com/es/Elecciones_congresales_extraordinarias_de_Per%C3%BA_de_2020](https://www.wikiwand.com/es/Elecciones_congresales_extraordinarias_de_Perú_de_2020)) cada 30 minutos y pone los resultados a disposición de la comunidad en las siguientes presentaciones:

1. **Dataframes como CSV** (casos de uso: pandas con python, cualquier programa que acepte CSVs)
2. **Pequeña API REST** (casos de uso: uso directo en clientes, [ejemplo](https://peru2020.minsky.cc/))

## Componentes del programa

El programa tiene dos hilos importantes, el primero se encarga de gestionar el API HTTP que esta gestionada por [Flask](https://flask.palletsprojects.com/en/1.1.x/), el segundo es el hilo encargado de ejecutar cada 30 minutos la rutina de scraping y la rutina para calcular la frecuencia de palabras del último resultado del scraping. Finalmente, el hilo principal (Main Thread) se encarga de ser el punto de inicio del programa.

Veo necesario agradecer al proyecto [Twint](https://github.com/twintproject/twint). Es gracias a este framework que se puede realizar un increíble scraping a Twetter. Tambíen destaco otros proyecto relacionados: [twitterscraper](https://github.com/taspinar/twitterscraper) de [taspinar](https://github.com/taspinar) y [twitter-scraper](https://github.com/bisguzar/twitter-scraper) de [bisguzar](https://github.com/bisguzar).



Abajo puedes ver un dibujo a mano alzada de la actual arquitectura del programa.

![diagram](schema.png)

## Uso de los dataframes



```shell
$ curl 
```