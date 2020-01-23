import os
import twint
import datetime

import pathlib
from os import listdir
from os.path import isfile, join
import extractor
import counter
import drawer


class StateWorker:
    def __init__(self, workspace=".", search="Elecciones Peru 2020", since="2019-10-01"):
        self.workspace = workspace
        self.pics_folder = join(self.workspace, "pics")
        self.dataframes_folder = join(self.workspace, "dataframes")

        self.search = search
        self.since = since

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

        self.freqs = []

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

        drawer.draw_word_cloud(text, with_download=True,
                               filename=draw_filename)
