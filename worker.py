import os
import twint
import datetime

import pathlib
from os import listdir
from os.path import isfile, join
import extractor
import counter
import drawer

import threading

import time

import asyncio


class GovernmentWorker(threading.Thread):
    def __init__(self, event, loop, workspace=".", search="Elecciones2020", since="2019-10-01", interval_s=30*60):
        threading.Thread.__init__(self)

        self.loop = loop
        self.stopped = event
        self.workspace = workspace
        self.pics_folder = join(self.workspace, "pics")
        self.dataframes_folder = join(self.workspace, "dataframes")

        self.search = search
        self.since = since

        self.interval_time = interval_s
        self.freqs = []

        pathlib.Path(self.pics_folder).mkdir(exist_ok=True)
        pathlib.Path(self.dataframes_folder).mkdir(exist_ok=True)

        onlyfiles = [f for f in listdir(self.dataframes_folder) if isfile(
            join(self.dataframes_folder, f))]

        if len(onlyfiles) > 0:
            times = [datetime.datetime.strptime(file, "%d-%m-%Y_%H:%M.csv")
                     for file in onlyfiles]
            times.sort(reverse=True)
            self.last_dataframe = times[0].strftime("%d-%m-%Y_%H:%M.csv")
        else:
            self.save_new_snapshot()

        print(self.last_dataframe)
        self.perform_generators()

    def save_new_snapshot(self):
        c = twint.Config()
        c.Search = self.search
        c.Since = self.since
        c.Store_csv = True
        c.Output = join(self.dataframes_folder, "temp.csv")

        twint.run.Search(c)

        name = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M.csv")

        os.rename(c.Output, join(self.dataframes_folder, name))

        self.last_dataframe = name

    def perform_generators(self):
        dataframe_filename = join(self.dataframes_folder, self.last_dataframe)
        draw_filename = join(
            self.pics_folder, self.last_dataframe.replace(".csv", ".png"))

        text = extractor.extract_tweets_from_csv(dataframe_filename)

        self.freqs = counter.freq_str(text, minimal_counts=2)

        drawer.draw_word_cloud(text, filename=draw_filename)

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.save_new_snapshot()
        while not self.stopped.wait(self.interval_time):
            print("executing snapshot")
            self.save_new_snapshot()
            self.perform_generators()
